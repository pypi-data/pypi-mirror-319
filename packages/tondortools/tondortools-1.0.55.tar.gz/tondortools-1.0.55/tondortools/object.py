import os
from pathlib import Path
from typing import Optional
try:
    import ogr, osr
except:
    from osgeo import ogr, osr
from tondortools.tool import read_raster_info
from osgeo import gdal
import math
import subprocess
import logging
import shutil
import time
from copy import copy
import numpy as np
from multiprocessing import Pool
import geopandas as gpd
from shapely.ops import unary_union
import pandas as pd
from osgeo.gdalconst import GDT_Int16, GDT_Float32, GDT_Byte, GDT_Int16

from .tiling import do_split_save_gpkg
from .tool import raster2array, create_maskedraster, read_raster_info, calculate_time
from .logging_config import init_logging, get_console_handler


import logging


init_logging()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(get_console_handler())  # Add the common handler
log.propagate = False



USE_PARALLEL = True
CPU_COUNT = 7

def do_gpkg_reprojection(source_gpkg, target_gpkg, template_epsg):

    epsg =get_gpkg_epsg(template_epsg)

    if not Path(target_gpkg).exists():
        reproject_gpkg = ["ogr2ogr", "-f", "gpkg", "-t_srs", f"epsg:{epsg}", str(target_gpkg),
                          str(source_gpkg)]
        cmd_output = subprocess.run(reproject_gpkg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("exit code {} --> {}".format(cmd_output.returncode, reproject_gpkg))

    return target_gpkg



def get_gpkg_epsg(gpkg_path):
    source = ogr.Open(str(gpkg_path), update=False)
    layer = source.GetLayer()
    epsg = layer.GetSpatialRef().GetAuthorityCode(None)
    source = None
    layer = None
    return epsg

def get_layer_name(gpkg_path):
    source = ogr.Open(str(gpkg_path), update=False)
    layer = source.GetLayer()
    layer_name = layer.GetName()
    return layer_name

def create_raster_bounds(raster, sourceSR, output_tiff):
    (xmin, ymax, RasterXSize, RasterYSize, pixel_width, _, epsg, _, _, raster_bbox) = read_raster_info(raster)

    # Define the input GeoPackage and output GeoTIFF
    mem_driver = gdal.GetDriverByName('Gtiff')
    mem_raster = mem_driver.Create(str(output_tiff), RasterXSize, RasterYSize,
                                   1, gdal.GDT_Byte)
    # Set the geotransform
    mem_raster.SetGeoTransform((xmin, pixel_width, 0, ymax, 0, -pixel_width))
    mem_raster.SetProjection(sourceSR.ExportToWkt())
    mem_band = mem_raster.GetRasterBand(1)
    mem_band.Fill(0)
    mem_raster = None

def get_parcel_positions(output_tiff, raster):
    ds_output = gdal.Open(str(output_tiff))
    outputarray = ds_output.GetRasterBand(1).ReadAsArray()
    outputarray = outputarray.astype(np.float32)
    arraymask = outputarray == 1
    positions = np.argwhere(arraymask == True)
    return positions

def create_parcelgpkg(sourceSR, feature, output_gpkg, raster=None):
    # Read parcel geometry
    feature_geom = feature.GetGeometryRef()
    if raster is not None:
        # Open data
        raster_ds = gdal.Open(str(raster))
        # Reproject vector geometry to same projection as raster
        targetSR = osr.SpatialReference()
        targetSR.ImportFromWkt(raster_ds.GetProjectionRef())
        coordTrans = osr.CoordinateTransformation(sourceSR, targetSR)
        feature_geom.Transform(coordTrans)

    # Create a memory layer from the feature
    mem_driver = ogr.GetDriverByName("GPKG")
    mem_ds = mem_driver.CreateDataSource(str(output_gpkg))

    if (feature_geom.GetGeometryName() == 'MULTIPOLYGON'):
        mem_layer = mem_ds.CreateLayer("parcel", sourceSR, ogr.wkbMultiPolygon)
    if (feature_geom.GetGeometryName() == 'POLYGON'):
        mem_layer = mem_ds.CreateLayer("parcel", sourceSR, ogr.wkbPolygon)
    new_field = ogr.FieldDefn('ID', ogr.OFTString)
    new_field.SetWidth(100)
    mem_layer.CreateField(new_field)

    mem_feature = ogr.Feature(mem_layer.GetLayerDefn())
    mem_feature.SetGeometry(feature.GetGeometryRef())
    mem_feature.SetField('ID', str(1))
    mem_layer.CreateFeature(mem_feature)

    feature_bbox = mem_feature.GetGeometryRef().GetEnvelope()
    mem_ds = None
    return feature_bbox

def get_parcel_locations(feature, sourceSR, raster, touch_status, work_dir):

    feature_fid= feature.GetFID()
    output_gpkg = Path(work_dir).joinpath(f"parcel_{feature_fid}.gpkg")
    output_tiff = Path(work_dir).joinpath(f"parcel_{feature_fid}.tif")

    if output_tiff.exists():
        output_tiff.unlink()

    if output_gpkg.exists():
        output_gpkg.unlink()

    feature_bbox = create_parcelgpkg(sourceSR, feature, output_gpkg, raster)

    create_raster_bounds(raster, sourceSR, output_tiff)
    create_maskedraster(output_gpkg, output_tiff, touch_status)
    parcel_position = get_parcel_positions(output_tiff, raster)

    if output_tiff.exists():
        output_tiff.unlink()

    if output_gpkg.exists():
        output_gpkg.unlink()
    return parcel_position

def parcelids_indices(object_path, raster, touch_status, work_dir, parcel_column=None):
    source = ogr.Open(str(object_path), update=False)
    layer = source.GetLayer()
    sourceSR = layer.GetSpatialRef()

    parcel_location_dict = {}

    for parcel in layer:
        parcel_locations = get_parcel_locations(parcel, sourceSR, raster, touch_status, Path(work_dir))
        if parcel_column is not None:
            parcel_location_dict[str(parcel.GetField(parcel_column))] = parcel_locations
        else:
            parcel_location_dict[str(parcel.GetFID())] = parcel_locations

    return parcel_location_dict

def update_object_count(object_path, parcel_location_dict, column_name = "count", parcel_column=None):
    source = ogr.Open(str(object_path), update=True)
    layer = source.GetLayer()
    sourceSR = layer.GetSpatialRef()

    ## set pixel count
    new_field = ogr.FieldDefn(column_name, ogr.OFTReal)
    new_field.SetWidth(5)
    layer.CreateField(new_field)

    for parcel in layer:
        if parcel_column is not None:
            parcel_name = str(parcel.GetField(parcel_column))
        else:
            parcel_name = str(parcel.GetFID())

        parcel_locations = parcel_location_dict[parcel_name]
        parcel_count = parcel_locations.shape[0]
        parcel.SetField(column_name, parcel_count)
        layer.SetFeature(parcel)
    source = None
    layer = None
    log.debug(f" --- {object_path} done ---")

##########################
def create_work_dirs(gpkg_paths, work_dir):

    gpkg_workdir_tuple_list = []
    for gpkg_path_item in gpkg_paths:
        gpkg_path_item_name = Path(gpkg_path_item).stem
        gpkg_work_dir = work_dir.joinpath(gpkg_path_item_name)
        os.makedirs(gpkg_work_dir, exist_ok=True)
        gpkg_workdir_tuple_list.append((str(gpkg_path_item), str(gpkg_work_dir)))
    return gpkg_workdir_tuple_list


def count_pixel_subgpkg(input_data):
    gpkg_path = Path(input_data[0])
    template_raster = Path(input_data[1])
    touch_status = input_data[2]
    work_dir = input_data[3]
    parcel_column = input_data[4]
    column_name = input_data[5]
    if "_NODATA.txt" in gpkg_path.name:
        return

    parcel_location_dict = parcelids_indices(gpkg_path, template_raster, touch_status, work_dir, parcel_column)
    update_object_count(gpkg_path, parcel_location_dict, column_name, parcel_column=parcel_column)

##########################

class ObjectLayer:
    def __init__(self, config):
        self.config = config
        self.touch_status = None
        self.pixel_size = Optional[int]

        self.origin = None
        self.target_epsg = None

        self.parse_config(self.config)
        self.setup_origin(self.config.get("origin", None))

        self.object_layer = None
        self.parcel_column = None
        self.local_path = None
        self.local_path_status = False
        
        self.parcel_location_dict = None

    @property
    def parcel_ids(self):
        if self.parcel_location_dict is None:
            raise Exception("call set_parcelids_indices function before calling this function")
        return self.parcel_location_dict.keys()

    @property
    def object_path(self):
        if self.local_path is not None:
            return self.local_path

        if self.object_layer is not None:
            return self.object_layer

        raise Exception(f"object layer not set.")

    def set_object_layer(self, gpkg_filepath):
        if not Path(gpkg_filepath).exists():
            raise Exception(f"{gpkg_filepath} does not exists.")
        self.object_layer = gpkg_filepath

    def set_check_parcel_column(self, column_name):
        CLASS_ATTRIBUTE = column_name
        source = ogr.Open(str(self.object_layer), update=False)
        layer = source.GetLayer()
        layer_defn = layer.GetLayerDefn()
        field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]
        if CLASS_ATTRIBUTE not in field_names:
            msg = "File {:s} does not have expected attribute {:s}".format(str(self.object_layer), CLASS_ATTRIBUTE)
            raise Exception(msg)
        else:
            self.parcel_column = column_name
            return True

    def set_rasternodata_value(self, nodata_value):
        self.nodata_value = nodata_value

    def copy_totmp(self, tmp_dir):
        self.local_path = Path(tmp_dir).joinpath(Path(self.object_layer).name)
        shutil.copy(self.object_layer, self.local_path)
        self.local_path_status = True

    def set_local_path(self):
        self.local_path = self.object_path
        self.local_path_status = True
        
    def reproject(self):
        if self.local_path_status == False: raise Exception(f"copy to local path first")
        source = ogr.Open(str(self.local_path), update=False)
        layer = source.GetLayer()
        input_gpkg_epsg = layer.GetSpatialRef().GetAuthorityCode(None)
        if int(input_gpkg_epsg) != int(self.target_epsg):
            gpkg_copy = Path(self.local_path).parent.joinpath(str(self.local_path.name).replace('.gpkg', '_copy.gpkg'))
            shutil.copy(self.local_path, gpkg_copy)
            self.local_path.unlink()
            reproject_gpkg = ["ogr2ogr", "-f", "gpkg", "-t_srs", f"epsg:{self.target_epsg}", str(self.local_path), str(gpkg_copy)]
            cmd_output = subprocess.run(reproject_gpkg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log.info("exit code {} --> {}".format(cmd_output.returncode, reproject_gpkg))
            gpkg_copy.unlink()

    def parse_config(self, config):
        all_in_status = config.get("touch_status", "all_on")
        if not all_in_status in ["all_in", "all_touch", "all_on"]:
            raise Exception(f"touch status can be only all_in, all_touch, all_on.")

        self.touch_status = all_in_status

        pixel_size = config.get("pixel_size", 10)
        self.pixel_size = int(pixel_size)

    def setup_origin(self, origin=None, raster=None):
        if origin is not None:
            self.origin = origin["coordinates"]
            self.target_epsg = origin["epsg"]

        if raster is not None:
            (xmin, ymax, _, _, _, _, epsg, _, _, _) = read_raster_info(
                raster)
            self.origin = (xmin, ymax)
            self.target_epsg = epsg

    def check_origin(self, raster=None):
        if raster == None and self.origin == None:
            raise Exception(f"Origin is not set. Extraction will not be correct")

        if raster is not None:
            (xmin, ymax, _, _, _, _, epsg, _, _, _) = read_raster_info(
                raster)
            self.origin = (xmin, ymax)
            self.target_epsg = epsg

    def setup_raster_extent(self, feature_bbox, output_gpkg):
        pass

    ########################################
    ########################################
    ########################################
    def find_nearest_vertex(self, point, pixel_size, position):
        # define origin and pixel size
        origin = self.origin  # example origin, replace with your own values

        if position == 'upperleft':

            # calculate the row and column of the pixel
            row = math.ceil((point[1] - origin[1]) / pixel_size) + 1
            col = math.ceil((point[0] - origin[0]) / pixel_size) - 1

            # calculate the nearest top left vertex of the pixel
            vertex_x = origin[0] + col * pixel_size
            vertex_y = origin[1] + row * pixel_size

        elif position == 'bottomright':
            row = math.floor((point[1] - origin[1]) / pixel_size) - 1
            col = math.floor((point[0] - origin[0]) / pixel_size) + 1

            # calculate the nearest bottom right vertex of the pixel
            vertex_x = origin[0] + (col + 1) * pixel_size
            vertex_y = origin[1] + (row + 1) * pixel_size

        return (vertex_x, vertex_y)

    def create_raster_parcelbounds(self, pixel_size, feature_bbox, sourceSR, output_tiff):

        featurexmin = feature_bbox[0]
        featurexmax = feature_bbox[1]
        featureymin = feature_bbox[2]
        featureymax = feature_bbox[3]

        point = (featurexmin, featureymax)
        (xmin, ymax) = self.find_nearest_vertex(point, pixel_size, position='upperleft')
        point = (featurexmax, featureymin)
        (xmax, ymin) = self.find_nearest_vertex(point, pixel_size, position='bottomright')

        xOrigin = self.origin[0]
        yOrigin = self.origin[1]
        # Specify offset and rows and columns to read
        xoff = int((xmin - xOrigin) / pixel_size)
        yoff = int((yOrigin - ymax) / pixel_size)
        xcount = int((xmax - xmin) / pixel_size) + 1
        ycount = int((ymax - ymin) / pixel_size) + 1

        # Define the input GeoPackage and output GeoTIFF
        mem_driver = gdal.GetDriverByName('Gtiff')
        mem_raster = mem_driver.Create(str(output_tiff), xcount, ycount,
                                       1, gdal.GDT_Byte)
        # Set the geotransform
        mem_raster.SetGeoTransform((xmin, pixel_size, 0, ymax, 0, -pixel_size))
        mem_raster.SetProjection(sourceSR.ExportToWkt())
        mem_band = mem_raster.GetRasterBand(1)
        mem_band.Fill(0)
        mem_raster = None
        offset = (xoff, yoff)
        return output_tiff, offset

    def get_raster_values(self, output_tiff, raster, offset):
        ds_output = gdal.Open(str(output_tiff))
        outputarray = ds_output.GetRasterBand(1).ReadAsArray()
        outputarray = outputarray.astype(np.float32)
        arraymask = outputarray == 1

        # Read raster as arrays
        (_, _, RasterXSize, RasterYSize, _, _, _, _, _, _) = read_raster_info(output_tiff)
        raster_ds = gdal.Open(str(raster))
        banddataraster = raster_ds.GetRasterBand(1)
        dataraster = banddataraster.ReadAsArray(offset[0], offset[1], RasterXSize, RasterYSize).astype(np.float32)
        return dataraster[arraymask]

    def aggregate_raster_parcel(self, feature, pixel_size, sourceSR, config, raster=None, work_dir=None):

        feature_fid= feature.GetFID()
        output_gpkg = Path(work_dir).joinpath(f"parcel_{feature_fid}.gpkg")
        output_tiff = Path(work_dir).joinpath(f"parcel_{feature_fid}.tif")

        if output_gpkg.exists():
            output_gpkg.unlink()
        if output_tiff.exists():
            output_tiff.unlink()

        self.check_origin(raster)
        feature_bbox = create_parcelgpkg(sourceSR, feature, output_gpkg, raster)

        output_tiff, offset = self.create_raster_parcelbounds(pixel_size, feature_bbox, sourceSR, output_tiff)

        create_maskedraster(output_gpkg, output_tiff, self.touch_status)
        raster_values = self.get_raster_values(output_tiff, raster, offset)

        if output_tiff.exists():
            output_tiff.unlink()
        if output_gpkg.exists():
            output_gpkg.unlink()

        return raster_values

    ########################################
    ### functionalities ###########
    ########################################

    def set_parcelids_indices(self, work_dir, raster):
        parcel_location_dict = parcelids_indices(self.object_path, raster, self.touch_status, work_dir, self.parcel_column)
        self.parcel_location_dict = parcel_location_dict

    def set_pixel_count(self):
        if self.parcel_location_dict is None:
            raise Exception("call set_parcelids_indices function before calling this function")
        update_object_count(self.object_path, self.parcel_location_dict, self.parcel_column)

    def get_parcelids(self):
        if self.parcel_location_dict is None:
            raise Exception("call set_parcelids_indices function before calling this function")
        return self.parcel_location_dict.keys()

    def get_raster_parcel_values(self, parcel_id, input_array):
        mask_index = self.get_parcel_indices(parcel_id)

        if isinstance(input_array, np.ndarray):
            parcel_values = input_array[mask_index[:, 0], mask_index[:, 1]]
            return parcel_values

        if isinstance(input_array, Path):
            raster = gdal.Open(str(input_array))
            nodata_value = raster.GetRasterBand(1).GetNoDataValue()

            raster_array = raster2array(str(input_array))
            raster_array[raster_array == nodata_value] = np.nan
            parcel_values = raster_array[mask_index[:, 0], mask_index[:, 1]]
            return parcel_values

        raise Exception(f"neither array nor path")

    def get_parcel_indices(self, parcel_id):
        return self.parcel_location_dict[parcel_id]

    ########################################
    ##### parallel pixel count ########
    ########################################

    def count_pixels_parallel(self, work_dir, raster_template, column_name= "count"):
        layer_name = get_layer_name(self.local_path)
        gpkg_paths = do_split_save_gpkg(self.local_path, self.local_path.name, work_dir, subtiles_count=14)
        gpkg_workdir = create_work_dirs(gpkg_paths, work_dir)

        subtasks = []
        for gpkg_workdir_item in gpkg_workdir:
            args = [gpkg_workdir_item[0], raster_template, self.touch_status, gpkg_workdir_item[1], self.parcel_column, column_name]
            subtasks.append(args)

        p = Pool(CPU_COUNT)
        p.map(count_pixel_subgpkg, tuple(subtasks), chunksize=1)


        self.local_path.unlink()
        for gpkg_workdir_item in gpkg_workdir:
            tile_gpkg_path = gpkg_workdir_item[0]
            org_cmd = ["ogr2ogr", "-f", "gpkg", "-append", "-nln", layer_name,
                       str(self.local_path), str(tile_gpkg_path)]
            cmd_output = subprocess.run(org_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log.info("exit code {} --> {}".format(cmd_output.returncode, org_cmd))
        log.info(f"{self.local_path} created after pixel count")

    def process_gpkg(self, column_name = "L1_code"):
        source_gpkg = self.local_path
        result_gpkg = self.local_path.parent.joinpath(f"{self.local_path.stem}_merged.gpkg")
        process_gpkg(source_gpkg, result_gpkg, column_name=column_name)

    def remove_overlap(self):
        if self.local_path_status == False: raise Exception(f"copy to local path first")
        shutil.copy(self.local_path, self.local_path.parent.joinpath(self.local_path.name.replace(".gpkg", "_ori.gpkg")))
        gdf = gpd.read_file(self.local_path)

        invalid_mask = ~gdf.geometry.is_valid
        gdf.loc[invalid_mask, 'geometry'] = gdf.loc[invalid_mask, 'geometry'].buffer(0)

        # Iterate through each polygon and subtract it from the rest to remove overlaps
        non_overlapping_gdf = gpd.GeoDataFrame(columns=gdf.columns)
    
        for index, row in gdf.iterrows():
    
            neighbors = gdf.drop(index)[gdf.touches(row['geometry']) | gdf.intersects(row['geometry'].buffer(1))]
            if len(neighbors) ==0:
                non_overlapping_gdf = gpd.GeoDataFrame(pd.concat([non_overlapping_gdf, gpd.GeoDataFrame([row])], ignore_index=True))
                continue
            polygon = row.geometry
            other_polygons = neighbors.geometry.unary_union
            non_overlapping_polygon = polygon.difference(other_polygons)
            if not non_overlapping_polygon.is_empty:
                new_row = row.copy()
                new_row.geometry = non_overlapping_polygon
                non_overlapping_gdf = gpd.GeoDataFrame(pd.concat([non_overlapping_gdf, gpd.GeoDataFrame([new_row])], ignore_index=True))
            gdf.drop(index, inplace=True)
    
        non_overlapping_gdf.set_crs(gdf.crs, inplace=True)
        self.local_path.unlink()
        non_overlapping_gdf.to_file(self.local_path, driver="GPKG")


def recode_gpkg_column(gpkg_path, conversion_table_path,
                       conversion_table_original_column, conversion_table_target_column,
                       gpkg_column):

    # Read the GeoPackage file
    gdf = gpd.read_file(gpkg_path)

    # Read the conversion table CSV
    conversion_df = pd.read_csv(conversion_table_path, encoding_errors='ignore')

    gdf[f"{gpkg_column}_str"] = gdf[f"{gpkg_column}"].astype(str)
    conversion_dict = dict(
        zip(conversion_df[conversion_table_original_column].astype(str), conversion_df[conversion_table_target_column]))
    # Apply the conversion to the specified column in the GeoDataFrame
    gdf[conversion_table_target_column] = gdf[f"{gpkg_column}_str"].map(conversion_dict)
    gdf.drop(columns=[f"{gpkg_column}_str"], inplace=True)

    gpkg_path.unlink()
    # Save the modified GeoDataFrame to a new GeoPackage file
    gdf.to_file(gpkg_path, driver="GPKG")

    log.info(f"Recode completed: {gpkg_path}. {gpkg_column} --> {conversion_table_target_column}")


def group_polygons_assigngroupid(gdf_input):
    gdf = copy(gdf_input)

    invalid_mask = ~gdf.geometry.is_valid
    gdf.loc[invalid_mask, 'geometry'] = gdf.loc[invalid_mask, 'geometry'].buffer(0)

    # Create a new column to store the group ID for each polygon
    gdf['group_id'] = -1

    group_id = 0
    # Iterate over each row in the GeoDataFrame
    for idx, row in gdf.iterrows():

        # Get the group ID of the current row
        if row['group_id'] != -1:
            row_group_id = row['group_id']
        else:
            row_group_id = group_id
            group_id += 1

        # Find all polygons that touch or intersect the current row's geometry
        neighbors = gdf[gdf.touches(row['geometry']) | gdf.intersects(row['geometry'].buffer(1))]

        # Check if any neighbors have a different group ID
        neighbor_group_ids = neighbors.loc[neighbors['group_id'] != -1, 'group_id']
        if not neighbor_group_ids.empty:
            # Get the unique group IDs of the neighbors
            unique_group_ids = neighbor_group_ids.unique()

            # Assign the current row's group ID to the neighbors with different group IDs
            gdf.loc[neighbors.index, 'group_id'] = row_group_id

            # Update the group ID for all polygons with the unique group IDs
            gdf.loc[gdf['group_id'].isin(unique_group_ids), 'group_id'] = row_group_id

        else:
            # Assign the current row's group ID to the neighbors with the default group ID
            gdf.loc[neighbors.index, 'group_id'] = row_group_id

    grouped_geoms = []
    for unique_group_id in gdf.group_id.unique():
        gdf_group_id = gdf.loc[gdf.group_id == unique_group_id]
        touching_geoms = []
        for idx, row in gdf_group_id.iterrows():
            touching_geoms.append(row)
        grouped_geoms.append(touching_geoms)
    return grouped_geoms

def convert_list_gdf(merged_geoms_list):
    df= pd.DataFrame(merged_geoms_list)
    if len(df) > 0:
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
    else:
        gdf = gpd.GeoDataFrame()
    return gdf

def merge_geoms(grouped_geoms):
    merged_attribute_list = []
    for group_geom in grouped_geoms:
        if len(group_geom) > 1:
            merged_geom = unary_union([geom_item.geometry for geom_item in group_geom])
            tol = 3
            corrected_geom = merged_geom.buffer(tol).buffer(-tol)

            merged_attribute = copy(group_geom[0])
            merged_attribute.geometry = corrected_geom
            merged_attribute_list.append(merged_attribute)
        else:
            merged_attribute = copy(group_geom[0])
            merged_attribute_list.append(merged_attribute)

    return  merged_attribute_list

def perform_parcel_merge_subgpkg(input_data):
    gpkg_path = Path(input_data[0])
    gpkg_merged_path = Path(input_data[1])

    gdf = gpd.read_file(gpkg_path)

    group_withid = group_polygons_assigngroupid(gdf)
    merged_geoms_list_group_id = merge_geoms(group_withid)
    gdf_group_id = convert_list_gdf(merged_geoms_list_group_id)
    gdf_group_id.to_file(gpkg_merged_path, driver="GPKG")

def process_gpkg(source_gpkg, result_gpkg, column_name = "SAMAS"):
    master_df = gpd.read_file(source_gpkg)
    group_df = gpd.GeoDataFrame(columns=master_df.columns)
    group_df_groupid = gpd.GeoDataFrame(columns=master_df.columns)

    subtasks = []
    files_to_merge = []
    for value in master_df[column_name].unique():
        group = master_df.loc[master_df[column_name] == value]
        group_gpkg_path = source_gpkg.parent.joinpath(f"{source_gpkg.stem}_{str(value)}{source_gpkg.suffix}")
        group_gpkg_merged_path = source_gpkg.parent.joinpath(f"{source_gpkg.stem}_{str(value)}_merged{source_gpkg.suffix}")
        group.to_file(str(group_gpkg_path), driver="GPKG")
        #perform_parcel_merge_subgpkg([group_gpkg_path, group_gpkg_merged_path])

        args = [str(group_gpkg_path), str(group_gpkg_merged_path)]
        subtasks.append(args)

    p = Pool(CPU_COUNT)
    p.map(perform_parcel_merge_subgpkg, tuple(subtasks), chunksize=1)


    for gpkg_workdir_item in gpkg_workdir:
        args = [gpkg_workdir_item[0], raster_template, self.touch_status, gpkg_workdir_item[1], self.parcel_column,
                column_name]
        subtasks.append(args)
    
    ori_gdf = gpd.read_file(source_gpkg)  # specify the layer name if necessary

    gdf = ori_gdf.dissolve(by=column_name)
    
    # Find unique attributes and initialize an empty GeoDataFrame for results
    unique_attrs = gdf[column_name].unique()
    result_gdf = gpd.GeoDataFrame(columns=gdf.columns, crs=gdf.crs)

    for attr in unique_attrs:
        # Filter polygons with the current attribute
        current_polygons = gdf[gdf[column_name] == attr]

        # Dissolve into a single polygon if possible
        dissolved = current_polygons.dissolve()

        # Subtract overlaps with different attributes
        other_polygons = gdf[gdf[attribute] != attr]
        for _, other_row in other_polygons.iterrows():
            dissolved['geometry'] = dissolved['geometry'].apply(lambda x: x.difference(other_row['geometry']))

        result_gdf = result_gdf.append(dissolved.reset_index(), ignore_index=True)
    
    result_gdf.to_file(str(result_gpkg), driver='GPKG')
    return result_gdf


def inner_buffer(geometry, buffer_distance):
    return geometry.buffer(-buffer_distance)

def create_gdf_inner_buffer(input_gdf, buffer_factor):
    pixel_size = 1
    buffer_distance = buffer_factor*pixel_size
    input_gdf["geometry"] = input_gdf["geometry"].apply(lambda geom: inner_buffer(geom, buffer_distance))
    return input_gdf

def create_gpkg_inner_buffer(input_gpkg, output_gpkg, buffer_factor):
    gdf = gpd.read_file(input_gpkg)

    output_gdf = create_gdf_inner_buffer(gdf, buffer_factor)
    
    output_gdf.to_file(str(output_gpkg), driver="GPKG")
    log.debug(f"Inner buffer applied and saved {output_gpkg}")
    
    
def count_vector_pixel(gpkg_path, template_raster, work_dir, touch_status ="all_in", field_name = 'pixel_count', data_type = GDT_Int16):
    (xmin, ymax, RasterXSize, RasterYSize, pixel_width, _, epsg, _, _, _) = read_raster_info(
        template_raster)

    raster_parcel_config = {"touch_status": touch_status, "pixel_size": pixel_width}
    ObjectLayer_instance = ObjectLayer(raster_parcel_config)
    ObjectLayer_instance.set_object_layer(gpkg_path)
    ObjectLayer_instance.set_local_path()
    ObjectLayer_instance.setup_origin(raster=template_raster)
    ObjectLayer_instance.reproject()

    source = ogr.Open(str(gpkg_path), update=True)
    layer = source.GetLayer()
    sourceSR = layer.GetSpatialRef()

    new_field = ogr.FieldDefn(field_name, ogr.OFTReal)
    new_field.SetWidth(5)
    layer.CreateField(new_field)

    raster_ds = gdal.Open(str(template_raster))
    banddataraster = raster_ds.GetRasterBand(1)
    banddataarray = banddataraster.ReadAsArray()
    banddataarray = banddataarray.astype(np.float32)
    raster_allinpixel_values = np.zeros_like(banddataarray)

    log.debug(f"-- Getting pixels for {layer.GetFeatureCount()} parcels--")
    start_time = time.time()
    ObjectLayer_instance.set_parcelids_indices(work_dir, template_raster)
    calculate_time(start_time)

    for parcel in layer:
        if ObjectLayer_instance.parcel_column is None:
            parcel_name = str(parcel.GetFID())
        else:
            parcel_name = str(parcel.GetField(ObjectLayer_instance.parcel_column))

        parcel_locations = ObjectLayer_instance.get_parcel_indices(parcel_name)
        parcel_count = parcel_locations.shape[0]
        parcel.SetField(field_name, parcel_count)
        layer.SetFeature(parcel)

    source = None    
    layer = None
    raster_ds = None
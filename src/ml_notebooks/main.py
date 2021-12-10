# Import python packages
import pystac
import os
import json
import requests
import urllib.request
import rasterio
from tempfile import TemporaryDirectory
from pathlib import Path
import typing
from typing import Dict, List, Tuple
from logging import DEBUG, Logger
from rasterio.warp import calculate_default_transform
from shapely.geometry import Polygon, mapping
from datetime import datetime
from itertools import islice

logger = Logger(__name__, level=DEBUG)
ASSET_DIR = 'assets/'

def main() -> None:

    catalog = pystac.Catalog(id='overstory-stac', description='Overstory STAC Catalog.')
    # print(list(catalog.get_all_items()))
    # print(list(catalog.get_children()))

    # Define item id's saved in `./assets/` dir
    item_ids = [
        '20210425_100412_ssc3_u0001',
        '20210425_100412_ssc3_u0002',
        '20210528_131522_ssc9_u0001',
        '20210710_133141_ssc8_u0001',
        '20210922_100732_ssc12_u0001',
        '20210922_100732_ssc12_u0002',
    ]

    # Loop through each item
    for item_id in item_ids:
        
        metadata_file = os.path.join(ASSET_DIR, 'metadata', f'{item_id}_metadata.json') 
        metadata_data = dict(_load_from_json(metadata_file))
        
        # print(metadata_data['id'])
        # print(metadata_data['properties'])
        # print(metadata_data['properties']["acquired"][:-1])


    stac_items = create_STAC_Items(item_ids=item_ids)

    for _, item in enumerate(stac_items):
        catalog.add_item(item[0])
        print(json.dumps(item[0].to_dict(), indent=4))


def _load_from_json(file):
    # Helper function to read .json files
    with open(file, "r") as f:
        data = json.load(f)
        return data

def create_STAC_Item(tiff_path: str, metadata_json: Dict) -> Tuple[List[str], Tuple]:
    """Creates a STAC item.
    
    Args:
        tiff_path (str): path to the .tif file
        metadata_json (Dict): dict content of metadata.json file
        
    Returns:
        List of STAC items.
    """

    with rasterio.open(tiff_path) as sample_cog:
        
        bounds = sample_cog.bounds
        src_crs = sample_cog.crs
        dst_crs = 'EPSG:4326'  # EPSG identifier for WGS84 coordinate system used by the geojson format
        
        left, bottom, right, top = rasterio.warp.transform_bounds(sample_cog.crs, dst_crs, *bounds)
        bbox = [left, bottom, right, top]
        
        # Create geojson feature
        geom = mapping(Polygon([
          [left, bottom],
           [left, top],
           [right, top],
           [right, bottom]
        ]))
        
        time_acquired = datetime.strptime(metadata_json["properties"]["acquired"][:-1], '%Y-%m-%dT%H:%M:%S.%f')
        
        # Instantiate pystac item
        item = pystac.Item(id=metadata_json["id"],
                 geometry=geom,
                 bbox=bbox,
                 datetime = time_acquired,
                 properties={
                 })

        # Use Planet metadata.json to add some common metadata to the STAC item
        metadata_properties = metadata_json["properties"]
        
        for key, value in islice(metadata_properties.items(), 1, None):

            # Add some common metadata for the item not included in the core item specification
            if(key == 'gsd'):
                item.common_metadata.gsd = value
        

        # Tuple containing spatial and temporal extent information to use later in this tutorial
        item_extent_info =  (bbox, geom, time_acquired)
     
    # Returns a list containing the PySTAC Item object and a tuple 
    # holding the bounding box, geojson polygon, and date the item was acquired
    return item, (item_extent_info)


def create_STAC_Items(
    item_ids: List[str],
) -> List[Tuple]:
    """ Create STAC Items.
    
    Args:
        item_ids (List[str]): 
        item_type (str):  
    
    Returns:
        stac_items (List[Tuple]): list of STAC items
    """

    # Define metadata files
    metadata_files = []
    metadata_files = sorted(['assets/metadata/' + item_id + '_metadata.json' for item_id in item_ids], reverse=True)

    # Define urls TODO fix
    urls = []
    urls = sorted([os.path.join('assets', item_id, 'files', 'SkySatCollect', item_id, 'pansharpened_udm2', f'{item_id}_pansharpened_udm.tif') for item_id in item_ids], reverse=True)

    # empty list to store STAC items
    stac_items = []
    
    for asset_url, item_metadata in zip(urls, metadata_files):
        metadata_json = _load_from_json(item_metadata)

        # Create STAC Items
        item, extent = create_STAC_Item(
            tiff_path=asset_url, 
            metadata_json=metadata_json
        )

        # Add asset to STAC items list
        item.add_asset(
              key='analytic',
              asset=pystac.Asset(
                  href=asset_url,
                  title= "4-Band Analytic",
                  
                  # indicate it is a cloud optimized geotiff
                  media_type=pystac.MediaType.COG,
                  roles=([
                    "analytic"
                  ])
              )
        ) 
        stac_items.append((item, extent))
    return stac_items


if __name__ == "__main__":
    main()
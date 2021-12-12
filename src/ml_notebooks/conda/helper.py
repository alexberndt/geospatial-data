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

# Define core repository directories
ROOT_DIR = Path(os.getcwd()).parents[2]
ASSETS_DIR = os.path.join(ROOT_DIR, "assets/")
ASSETS_DIR_TEST = os.path.join(ROOT_DIR, "assets_test/")

# Helper function to read .json files
def read_json(file: str) -> Dict:
    with open(file, "r") as f:
        data = json.load(f)
        return data
    
    
def get_metadata_path(item_id: str) -> str:
    """ Returns the metadata file path.
    
    Based on the file structure in assets/
    
    Args:
        item_id (str): file item ID to be read.
    """
    return os.path.join(ASSETS_DIR, item_id, 'metadata', f'{item_id}_metadata.json')


def get_udm_file_path(item_id: str) -> str:
    """ Returns the udm.tif file path.
    
    Based on the file structure in assets/
    
    Args:
        item_id (str): file item ID to be read.
    """
    return os.path.join(ASSETS_DIR, _get_skysat_path(item_id), f'{item_id}_pansharpened_udm.tif')


def get_udm2_file_path(item_id: str) -> str:
    """ Returns the udm2.tif file path.
    
    Based on the file structure in assets/
    
    Args:
        item_id (str): file item ID to be read.
    """
    return os.path.join(ASSETS_DIR, _get_skysat_path(item_id), f'{item_id}_pansharpened_udm2.tif')


def get_tif_file_path(item_id: str) -> str:
    """ Returns the pansharpened.tif file path.
    
    Based on the file structure in assets/
    
    Args:
        item_id (str): file item ID to be read.
    """
    return os.path.join(ASSETS_DIR, _get_skysat_path(item_id), f'{item_id}_pansharpened.tif')


def get_COG_file_path(item_id: str) -> str:
    """ Returns the pansharpened.tif file path.
    
    Based on the file structure in assets/
    
    Args:
        item_id (str): file item ID to be read.
    """
    return os.path.join(ASSETS_DIR, item_id, 'files', f'{item_id}_pansharpened_cog_rgb.tif')


def _get_skysat_path(item_id: str) -> str:
    return os.path.join(item_id, 'files', 'SkySatCollect', item_id, 'pansharpened_udm2')
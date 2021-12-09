# Define helper function to get STAC item
def create_STAC_Item(tiff_path, metadata_json):
    """Creates a STAC item.
    
    Args:
        tiff_path (str): path to the .tif file
        metadata_json (str): 
        
    Returns:
        
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

        # Enable item extensions
        item.ext.enable('eo')
        item.ext.enable('view') 
        item.ext.enable('projection')
        
        for key, value in islice(metadata_properties.items(), 1, None):

            # Add some common metadata for the item not included in the core item specification
            if(key == 'gsd'):
                item.common_metadata.gsd = value
            
            # View Geometry Extension 
            if (key == 'sun_azimuth'):
                item.ext.view.sun_azimuth = value
            if (key == 'sun_elevation'):
                item.ext.view.sun_elevation = value
            
            # Electro Optical Extension - 
            if(key == 'cloud_cover'):
                item.ext.eo.cloud_cover = value
           
           # Projection Extension
            if(key == 'epsg_code'):
                item.ext.projection.epsg = value

        # Tuple containing spatial and temporal extent information to use later in this tutorial
        item_extent_info =  (bbox, geom, time_acquired)
     
    # Returns a list containing the PySTAC Item object and a tuple 
    # holding the bounding box, geojson polygon, and date the item was acquired
    return item, (item_extent_info)


def create_STAC_Items(metadata_folder_name, planet_order_id, item_type, item_ids, storage_bucket_name):
    """ Create STAC Items.
    
    Args:
        metadata_folder_name:
        planet_order_id:
        item_type:
        item_ids:
        storage_bucket_name: 
    
    Returns:
        
    """

    # Store metadata 
    store_item_metadata(order_id, metadata_folder_name, item_type , item_ids)
    metadata_directory = metadata_folder_name + '/' + order_id + '/' + item_type
    metadata_files = sorted(Path(metadata_directory).glob('*'), reverse=True)

    urls = []
    urls = sorted([storage_bucket_name + item_id + '_pansharpened_udm.tif' for item_id in item_ids], reverse=True)

    # empty list to store STAC items
    stac_items = []
    
    for asset_url, item_metadata in zip(urls, metadata_files):
        m = load_item_metadata(item_metadata)

        item, extent = create_STAC_Item(asset_url, m)
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
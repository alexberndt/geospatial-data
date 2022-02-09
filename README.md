# Introduction to Geospatial Data

This repository serves as a brief introduction into the field of geo-spatial data. The objective is to play around with various solutions proposed by the geo-spatial and GIS communities. 

Specifically, this repository covers

1. Spatio-Temporal Asset Catalog (STAC) creation and querying using `pystac` and `pystac_client`.
2. Creating monthly mosaics of satellite data using `Dask`.
3. Cloud Optimized GeoTIFFs (COGs) and the use of tilers using `titiler`.

## Get Started

```bash
git clone git@github.com:alexberndt/geospatial-data
cd geospatial-data
poetry install
```

Get started with a jupyter notebook by running

```bash
poetry run jupyter-lab
```

## Notebooks

This repository consists of

1. STAC Registry and Querying
   
   1. `src/ml_notebooks/stac/stac.ipynb`
   2. `src/ml_notebooks/stac/read_stac_api.ipynb`

   with helper functions written in a separate file `src/ml_notebooks/stac/helper.py` to aide with code readability.

   > Although `catalog.validate()` passed all checks, I was struggling to query data using the `pystac_client` tool. Any idea as to what I was doing wrong?

   To avoid being blocked by this, I used a publicly available STAC catalog to test STAC queries with (see `read_stac_api.ipynb` notebook).

2. Exploration of Provided Satellite Data

   1. `src/ml_notebooks/stac/explore_data.ipynb`

3. Monthly Mosaic

   1. `src/ml_notebooks/conda/monthly_mosaic.ipynb`

   > As mentioned above, I was struggling getting the STAC queries to work without error, so ended up testing the _coiled_-based cloud cluster using the example STAC provided by Planetary Computer. The results are documented in this notebook:

   1. `src/ml_notebooks/conda/median_mosaic.ipynb`
   
4. COG Visualization

   1. `src/ml_notebooks/cog/cog_visualizations.ipynb`

## Assets Folder

The assets are saved as follows

![file structure diagram](.github/markdown/assets.png "File Structure")

## Technologies

Here follows a list of technologies commonly used to solve ML-related problems in the geo-spatial industry:

1. [Dask](https://dask.org/)
2. [Xarray](https://xarray.pydata.org/en/stable/)
3. [Coiled](https://coiled.io/)
4. [Dagster](https://dagster.io/)
5. [PySTAC](https://pystac.readthedocs.io/en/1.0/#)

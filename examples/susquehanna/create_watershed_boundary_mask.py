import os, sys

from pyearth.system.define_global_variables import *
from pyearth.toolbox.data.ocean.define_land_ocean_mask import create_land_ocean_vector_mask, convert_land_ocean_mask_to_raster


sFilename_geojson_out = '/qfs/people/liao313/data/hexwatershed/susquehanna/vector/hydrology/boundary_wgs.geojson'
sFilename_tif_out = '/compyfs/liao313/04model/pyflowline/watershed_boundary_mask.tif'

#define resolution as 1km as the equator, which is
dResolution_x_in = 30 /3600.0
dResolution_y_in = 30 /3600.0


#covnert to raster

convert_land_ocean_mask_to_raster(sFilename_geojson_out, sFilename_tif_out, dResolution_x_in, dResolution_y_in)

print('finished creating land ocean mask in raster.')
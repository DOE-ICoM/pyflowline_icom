import numpy as np
from pyearth.gis.gdal.read.raster.gdal_read_geotiff_file import gdal_read_geotiff_file
dResolution_coastline = 3
#use natural earth coastline data
#read land-ocean mask
sFilename_land_oceam_mask = '/compyfs/liao313/04model/pyflowline/land_ocean_mask.tif'
#read the geotiff using gdal
dummy = gdal_read_geotiff_file(sFilename_land_oceam_mask)
aData = dummy['dataOut']
nrow = aData.shape[0]
ncol = aData.shape[1]
pixelHeight = dummy['pixelHeight'] #30/3600.0
pixelWidth = dummy['pixelWidth']
#get the index where the coast is located
dummy_index = np.where(aData == 1)
# Convert the index from one matrix to another
irows, icols = dummy_index
# Get lat and lon using vectorized operations
dLon = -180.0 + icols * pixelWidth
dLat = 90.0 + irows * pixelHeight
# Convert to the new matrix index using vectorized operations
iX =(dLon + 180).astype(int)
iY = (90.0 - dLat).astype(int)
# Convert 2D indices to 1D indices
flat_indices = iY * 180 + iX
print(iY, iX)
print(flat_indices)
import numpy as np
import jigsawpy
from osgeo import gdal #read geotiff file

def compute_mask(aData, value, pixelWidth, pixelHeight, nspace_column, nspace_row):
    #computer a mask for a 2D arary from one size to another
    dummy_index = np.where(aData == value)
    irows, icols = dummy_index
    dLon = -180.0 + icols * pixelWidth
    dLat = 90.0 + irows * pixelHeight
    iX = ((dLon + 180.0) / (360.0 / nspace_column)).astype(int)
    iY = ((dLat + 90) / (180.0 / nspace_row)).astype(int)
    iX = np.clip(iX, 0, nspace_column - 1)
    iY = np.clip(iY, 0, nspace_row - 1)
    mask = np.full((nspace_row, nspace_column), False, dtype=bool)
    mask[iY, iX] = True
    return mask

if (__name__ == "__main__"):
    opts = jigsawpy.jigsaw_jig_t()  # user-defined options
    geom = jigsawpy.jigsaw_msh_t()  # geometry to be meshed
    spac = jigsawpy.jigsaw_msh_t()  # mesh spacing function h(x)
    mesh = jigsawpy.jigsaw_msh_t()  # mesh object

#-- geometry = sphere
    geom.mshID = "ellipsoid-mesh"
    geom.radii = 6371.220 * np.ones(3)  # [km] so spacing also [km]

#-- mesh spacing grid
    ncolumn = 43200 #360
    nrow = 21600 #180
    spac.mshID = "ellipsoid-grid"  # 'grid' = structured matrix
    spac.xgrid = np.linspace(-1. * np.pi, +1. * np.pi, ncolumn)
    spac.ygrid = np.linspace(-.5 * np.pi, +.5 * np.pi, nrow)

    # uniform spacing
    spac.value = 200. * np.ones((spac.ygrid.size, spac.xgrid.size))

    # smaller in mask
    xmat, ymat = np.meshgrid(spac.xgrid, spac.ygrid)
    mask = np.logical_and.reduce((  # lon-lat box
        xmat > 30. * np.pi / 180., xmat < 60. * np.pi / 180.,
        ymat > 20. * np.pi / 180., ymat < 40. * np.pi / 180.
        ) )
    #spac.value[mask] = 5.

    #use a geotiff file
    sFilename_land_ocean_mask= 'land_ocean_mask.tif'
    sDriverName='GTiff'
    pDriver = gdal.GetDriverByName(sDriverName)
    pDataset = gdal.Open(sFilename_land_ocean_mask, gdal.GA_ReadOnly)
    ncolumn_raster = pDataset.RasterXSize
    nrow_raster = pDataset.RasterYSize
    pBand = pDataset.GetRasterBand(1)
    aLand_ocean_mask = pBand.ReadAsArray(0, 0, ncolumn_raster, nrow_raster)
    pGeotransform = pDataset.GetGeoTransform()
    dPixelWidth = pGeotransform[1]
    dPixelHeight = pGeotransform[5]
    aCoast_mask = compute_mask(aLand_ocean_mask, 1, dPixelWidth, dPixelHeight, ncolumn, nrow)
    spac.value[aCoast_mask] =  5.0

#-- a minimal set of user-opts for jigsaw
    opts.geom_file = "geom.msh"  # files for each object
    opts.hfun_file = "spac.msh"
    opts.mesh_file = "mesh.msh"
    opts.jcfg_file = "opts.jig"

    opts.hfun_scal = "absolute"  # h(x) in [km]
    opts.hfun_hmin = 0.  # no min. bound
    opts.hfun_hmax = 1000.  # arbitrary big max. bound
    opts.verbosity = 1  # print more log output

    jigsawpy.savemsh(opts.geom_file, geom)
    jigsawpy.savemsh(opts.hfun_file, spac)

    jigsawpy.cmd.jigsaw(opts, mesh)  # generate the mesh

#-- if you'd like to viz. in paraview
    jigsawpy.savevtk("spac.vtk", spac)
    jigsawpy.savevtk("mesh.vtk", mesh)
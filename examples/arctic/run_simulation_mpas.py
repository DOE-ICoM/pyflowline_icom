import os, sys, stat
from pathlib import Path
from os.path import realpath
import cartopy.crs as ccrs
from pyflowline.configuration.read_configuration_file import pyflowline_read_configuration_file
from pyflowline.configuration.change_json_key_value import change_json_key_value

#===================================
#set up workspace path
#===================================
sPath_parent = str(Path(__file__).parents[2]) # data is located two dir's up
sPath_data = realpath( sPath_parent +  '/data/arctic' )
sWorkspace_input =  str(Path(sPath_data)  /  'input')
sWorkspace_output = '/compyfs/liao313/04model/pyflowline/arctic'
if not os.path.exists(sWorkspace_output):
    os.makedirs(sWorkspace_output)

#===================================
#you need to update this file based on your own case study
#===================================
sFilename_configuration_in = realpath( sPath_parent +  '/data/arctic/input/pyflowline_arctic_mpas_icom2.json' )
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )

#===================================
#setup case information
#===================================
iFlag_create_job = 0
iFlag_visualization = 1
iCase_index = 3
sMesh_type = 'mpas'
sDate='20240601'

#===================================
#setup output and HPC job
#===================================


if iFlag_create_job ==1:
    sSlurm = 'short'
    sFilename_job = sWorkspace_output + '/' + sMesh_type + '.bash'
    ofs = open(sFilename_job, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

#===================================
#visualization spatial extent
#===================================
change_json_key_value(sFilename_configuration_in, 'sWorkspace_output', sWorkspace_output)
oPyflowline = pyflowline_read_configuration_file(sFilename_configuration_in,
    iCase_index_in=iCase_index, sDate_in=sDate)

#oPyflowline.aBasin[0].dLatitude_outlet_degree=39.462000
#oPyflowline.aBasin[0].dLongitude_outlet_degree=-76.009300
if iFlag_create_job ==1:
    oPyflowline._pyflowline_create_hpc_job(sSlurm_in = sSlurm )

    sLine  = 'cd ' + oPyflowline.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)


if iFlag_visualization == 1:

    pProjection_map = ccrs.Orthographic(central_longitude=0,  central_latitude=90, globe=None)
    pProjection_data = ccrs.Geodetic()

    sFilename = os.path.join(  oPyflowline.sWorkspace_output, 'mesh.ps' )

    oPyflowline.plot(sFilename_output_in = sFilename,
                      iFlag_title_in=0 ,
                      iDPI_in = 300,
                      sVariable_in='mesh',
                      pProjection_map_in = pProjection_map,
                        pProjection_data_in=pProjection_data)


    pass

if iFlag_create_job ==1:
    ofs.close()
    os.chmod(sFilename_job, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)
print('Finished')
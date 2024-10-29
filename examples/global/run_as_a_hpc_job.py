
from pyflowline.mesh.dggrid.create_dggrid_mesh import dggrid_find_resolution_by_index
from pyflowline.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file
import os
import stat

from pathlib import Path
from os.path import realpath

import numpy as np
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyflowline simulation started.')


sMesh_type = 'dggrid'
sSlurm = 'slurm'
iCase_index = 1
dResolution_meter = 5000
iFlag_create_job = 1
iFlag_visualization = 0
aExtent_full = None

pProjection_map = None
sDate = '20231201'
sPath = str(Path().resolve())
iFlag_option = 1
sWorkspace_data = realpath(sPath + '/data/global')
sWorkspace_input = str(Path(sWorkspace_data) / 'input')
sWorkspace_output = '/compyfs/liao313/04model/pyhexwatershed/global'

iMesh_type = 5

# set up dggrid resolution level

sDggrid_type = 'ISEA3H'
# generate a bash job script
if iFlag_create_job == 1:
    sFilename_job = sWorkspace_output + '/' + sDate + 'submit.bash'
    ofs = open(sFilename_job, 'w')
    sLine = '#!/bin/bash' + '\n'
    ofs.write(sLine)

sFilename_configuration_in = os.path.join(
    sWorkspace_input, 'pyflowline_global_dggrid.json')


if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This configuration file does not exist: ', sFilename_configuration_in)
    exit()

# mpas mesh only has one resolution
iFlag_stream_burning_topology = 1
iFlag_use_mesh_dem = 0
iFlag_elevation_profile = 0

aExtent = [-60.6, -59.2, -3.6, -2.5]
# aExtent = None

iResolution_index = 3

dResolution = dggrid_find_resolution_by_index(sDggrid_type, iResolution_index)
print(dResolution)

oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in,
                                                           iCase_index_in=iCase_index, 
                                                            iResolution_index_in = iResolution_index, 
                                                              sDate_in=sDate, sMesh_type_in=sMesh_type)

oPyflowline._pyflowline_create_hpc_job(sSlurm_in=sSlurm)


if iFlag_create_job == 1:
    ofs.close()
    os.chmod(sFilename_job, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)

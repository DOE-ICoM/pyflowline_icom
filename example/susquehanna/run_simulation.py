import os, sys, stat
from pathlib import Path
from os.path import realpath
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time Pyflowline simulation started.')

from pyflowline.classes.pycase import flowlinecase
from pyflowline.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file
from pyflowline.pyflowline_create_template_configuration_file import pyflowline_create_template_configuration_file



#example


sDate='20220630'


dataPath = str(Path(__file__).parents[2]) # data is located two dir's up
iFlag_option = 1
sWorkspace_data = realpath( dataPath +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  str(Path(sWorkspace_data)  /  'output')
sWorkspace_output=  '/compyfs/liao313/04model/pyflowline/susquehanna'
#an example configuration file is provided with the repository, but you need to update this file based on your own case study
aMesh_type = ['hexagon', 'square','latlon','mpas']
aResolution_meter = [5000, 10000, 50000]
iCase_index = 1



sPath = str( Path().resolve() )
sSlurm = 'short'

sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
ofs = open(sFilename, 'w')
sLine  = '#!/bin/bash' + '\n'
ofs.write(sLine)
for iMesh_type in range(1, 5):
    sMesh_type = aMesh_type[iMesh_type-1]
    if sMesh_type=='hexagon':
        sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyflowline_susquehanna_hexagon.json' )
    else:
        if sMesh_type=='square':
            sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyflowline_susquehanna_square.json' )
        else:
            if sMesh_type=='latlon':
                sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyflowline_susquehanna_latlon.json' )
            else:
                sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyflowline_susquehanna_mpas.json' )

    
        
    

    if os.path.isfile(sFilename_configuration_in):
        pass
    else:
        print('This configuration does not exist: ', sFilename_configuration_in )
    
    if iMesh_type != 4:
        for iResolution in range(1, 4):    
            dResolution_meter = aResolution_meter[iResolution-1]

            oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in, \
            iCase_index_in=iCase_index, dResolution_meter_in=dResolution_meter, sDate_in=sDate)

            oPyflowline.create_hpc_job(sSlurm_in =sSlurm )  
            print(iCase_index)

            sLine  = 'cd ' + oPyflowline.sWorkspace_output + '\n'
            ofs.write(sLine)
            sLine  = 'sbatch submit.job' + '\n'
            ofs.write(sLine)
            iCase_index= iCase_index+1
           
    else:
        oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in, \
            iCase_index_in=iCase_index, dResolution_meter_in=dResolution_meter, sDate_in=sDate)

        oPyflowline.create_hpc_job(sSlurm_in =sSlurm )   
        print(iCase_index)

        sLine  = 'cd ' + oPyflowline.sWorkspace_output + '\n'
        ofs.write(sLine)
        sLine  = 'sbatch submit.job' + '\n'
        ofs.write(sLine)
        pass

ofs.close()
os.chmod(sFilename, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)   

print('Finished')

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time Pyflowline simulation finished.')

    


import os, sys
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

sDate='20220630'

dataPath = str(Path(__file__).parents[2]) # data is located two dir's up

sWorkspace_data = realpath( dataPath +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')


#an examples configuration file is provided with the repository, but you need to update this file based on your own case study
sMesh = 'latlon'
aResolution_meter = [5000, 10000, 50000]
iCase_index = 1
sPath = str( Path().resolve() )

sFilename_configuration_in = realpath( sPath +  '/examples/susquehanna/pyflowline_susquehanna_latlon.json' )
       
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )



sSlurm = 'short'
sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
ofs = open(sFilename, 'w')
sLine  = '#!/bin/bash' + '\n'
ofs.write(sLine)
for iResolution in range(1, 4):    
    dResolution_meter = aResolution_meter[iResolution-1]
    oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in, \
    iCase_index_in=iCase_index, dResolution_meter_in=dResolution_meter, sDate_in=sDate)
    oPyflowline.aBasin[0].dLatitude_outlet_degree=39.462000
    oPyflowline.aBasin[0].dLongitude_outlet_degree=-76.009300
    oPyflowline.create_hpc_job(sSlurm_in =sSlurm )  
    
    sLine  = 'cd ' + oPyflowline.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)        
    iCase_index= iCase_index+1
           
print('Finished')

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time Pyflowline simulation finished.')

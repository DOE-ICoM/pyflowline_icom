import os, sys
from pathlib import Path
from os.path import realpath
import argparse
import logging
from typing import NoReturn
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time Pyflowline simulation started.')

from pyflowline.classes.pycase import flowlinecase
from pyflowline.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file



#set up input
dataPath = str(Path(__file__).parents[2]) # data is located two dir's up

sWorkspace_data = realpath( dataPath +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')

#setup output and HPC job 
sSlurm = 'short'
sWorkspace_output = '/compyfs/liao313/04model/pyflowline/susquehanna'
sFilename = sWorkspace_output + '/' + 'hexagon.bash'
ofs = open(sFilename, 'w')
sLine  = '#!/bin/bash' + '\n'
ofs.write(sLine)

#set up configuration file
#you may need to update this file based on your own case study
sPath = str( Path().resolve() )    
sFilename_configuration_in = realpath( sPath +  '/examples/susquehanna/pyflowline_susquehanna_hexagon.json' )

if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )


#set up cases information
iFlag_visualization=0
iCase_index = 1
sDate='20220905'
sMesh = 'hexagon'
aResolution_meter = [5000, 10000, 50000]
nResolution = len(aResolution_meter)
for iResolution in range(1, nResolution + 1):    
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

    sFilename =  'filtered_flowline.png'
    #oPyflowline.plot(sFilename, sVariable_in = 'flowline_filter'aExtent_in =aExtent_full  )
    sFilename =  'conceptual_flowline_with_mesh.png'
    if iFlag_visualization == 1:
        #oPyflowline.plot(sFilename,  iFlag_title=1 ,sVariable_in='overlap',    aExtent_in =aExtent_full )  
            #pass
        #sFilename =  'meander.png'
        #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in='overlap',     aExtent_in =aExtent_meander )       
        #sFilename =  'braided.png'
        #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in='overlap',     aExtent_in =aExtent_braided )    
        #sFilename =  'confluence.png'
        #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in='overlap',     aExtent_in =aExtent_confluence )    
        #sFilename =  'outlet.png'
        #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in='overlap',     aExtent_in =aExtent_outlet )         
        sFilename =  'area_of_difference.png'
        #oPyflowline.plot( sFilename,sVariable_in = 'aof',  aExtent_in=aExtent_full)
        pass
    
    iCase_index= iCase_index+1

           
print('Finished')

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time Pyflowline simulation finished.')

import os, sys
from pathlib import Path
from os.path import realpath

from pyflowline.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file

#===================================
#set up workspace path
#===================================
sPath_parent = str(Path(__file__).parents[2]) # data is located two dir's up
sPath_data = realpath( sPath_parent +  '/data/great_lakes' )
sWorkspace_input =  str(Path(sPath_data)  /  'input')
sWorkspace_output = '/compyfs/liao313/04model/pyflowline/great_lakes'

if not os.path.exists(sWorkspace_output):
    os.makedirs(sWorkspace_output)


#===================================
#you need to update this file based on your own case study
#=================================== 
sFilename_configuration_in = realpath( sPath_parent +  '/examples/great_lakes/pyflowline_great_lakes_latlon.json' )
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )

#===================================
#setup case information
#===================================
iCase_index = 4
iFlag_visualization=1
sDate='20230701'
sMesh = 'latlon'
aResolution_meter = [5000, 10000, 50000]
aResolution_degree = [0.05, 0.5, 1]
aResolution_degree = [ 2]
nResolution = len(aResolution_meter)


#===================================
#setup output and HPC job 
#===================================
sSlurm = 'short'
sFilename = sWorkspace_output + '/' + sMesh + '.bash'
ofs = open(sFilename, 'w')
sLine  = '#!/bin/bash' + '\n'
ofs.write(sLine)


#===================================
#visualization spatial extent
#===================================
aExtent_full = [-78.5,-75.5, 39.2,42.5]
aExtent_meander = [-76.5,-76.2, 41.6,41.9] #meander
aExtent_braided = [-77.3,-76.5, 40.2,41.0] #braided
aExtent_confluence = [-77.3,-76.5, 40.2,41.0] #confluence
aExtent_outlet = [-76.0,-76.5, 39.5,40.0] #outlet
aExtent_dam = [-75.75,-76.15, 42.1,42.5] #dam  

for iResolution in range(1, nResolution + 1):  
    #dResolution_meter = aResolution_meter[iResolution-1]
    dResolution_meter = None
    dResolution_degree = aResolution_degree[iResolution-1]
    oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in, 
    iCase_index_in=iCase_index, 
    dResolution_meter_in=dResolution_meter,
    dResolution_degree_in = dResolution_degree,
      sDate_in=sDate)
   
    oPyflowline.mesh_generation()
    
    sWorkspace_output_basin = oPyflowline.sWorkspace_output

    if iFlag_visualization == 1:
        sFilename = os.path.join(  sWorkspace_output_basin, 'mesh.png' )     
        oPyflowline.plot(sVariable_in = 'mesh', sFilename_output_in = sFilename)
        
        
        pass

    iCase_index= iCase_index+1
           
ofs.close() 
print('Finished')



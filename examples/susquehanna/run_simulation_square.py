import os, sys
from pathlib import Path
from os.path import realpath

from pyflowline.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file
#===================================
#set up workspace path
#===================================
sPath_parent = str(Path(__file__).parents[2]) # data is located two dir's up
sPath_data = realpath( sPath_parent +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sPath_data)  /  'input')
sWorkspace_output = '/compyfs/liao313/04model/pyflowline/susquehanna'


#===================================
#you need to update this file based on your own case study
#=================================== 
sFilename_configuration_in = realpath( sPath_parent +  '/examples/susquehanna/pyflowline_susquehanna_square.json' )
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )

#===================================
#setup case information
#===================================
iCase_index = 1
iFlag_visualization=0
sDate='20220905'
sMesh = 'square'
aResolution_meter = [5000, 10000, 50000]
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
    dResolution_meter = aResolution_meter[iResolution-1]
    oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in, \
    iCase_index_in=iCase_index, dResolution_meter_in=dResolution_meter, sDate_in=sDate)
    oPyflowline.aBasin[0].dLatitude_outlet_degree=39.462000
    oPyflowline.aBasin[0].dLongitude_outlet_degree=-76.009300
    oPyflowline._create_hpc_job(sSlurm_in =sSlurm )  
    
    sLine  = 'cd ' + oPyflowline.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)        

    
    if iFlag_visualization == 1:
        sFilename =  'filtered_flowline.png'
        oPyflowline._plot(sFilename, sVariable_in = 'flowline_filter', aExtent_in = aExtent_full  )
        
        sFilename =  'conceptual_flowline_with_mesh.png'
        oPyflowline._plot(sFilename,  iFlag_title=1 ,sVariable_in='overlap',    aExtent_in =aExtent_full )  
        
        sFilename =  'meander.png'
        oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',     aExtent_in =aExtent_meander )       

        sFilename =  'braided.png'
        oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',     aExtent_in =aExtent_braided )    

        sFilename =  'confluence.png'
        oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',     aExtent_in =aExtent_confluence )    

        sFilename =  'outlet.png'
        oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',     aExtent_in =aExtent_outlet )         

        sFilename =  'area_of_difference.png'
        oPyflowline._plot( sFilename,sVariable_in = 'aof',  aExtent_in=aExtent_full)
        pass
    
    iCase_index= iCase_index+1

ofs.close()           
print('Finished')


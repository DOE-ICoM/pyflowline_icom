import os, sys
from pathlib import Path
from os.path import realpath
import importlib.util
from shutil import copy2
from pyflowline.configuration.read_configuration_file import pyflowline_read_configuration_file
from pyflowline.configuration.change_json_key_value import change_json_key_value

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
sFilename_configuration_in = realpath( sPath_parent +  '/data/susquehanna/input/pyflowline_susquehanna_mpas.json' )
sFilename_basins_in = realpath( sWorkspace_input +  '/pyflowline_susquehanna_basins.json' )
sFilename_jigsaw_in = realpath( sWorkspace_input +  '/pyflowline_jigsaw.json' )
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )

#===================================
#setup case information
#===================================
iFlag_create_job = 1
iFlag_visualization = 0
iCase_index = 29
sMesh_type = 'mpas'
sDate='20240901'

#===================================
#setup output and HPC job
#===================================
sSlurm = 'short'
sSlurm = 'slurm'
sFilename = sWorkspace_output + '/' + sMesh_type + '.bash'
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

oPyflowline = pyflowline_read_configuration_file(sFilename_configuration_in, \
    iCase_index_in=iCase_index, sDate_in=sDate)

# Set the basin outlet coordinates
dLongitude_outlet_degree = -76.009300
dLatitude_outlet_degree = 39.462000

sWorkspace_output = oPyflowline.sWorkspace_output

#we want to copy the example configuration file to the output directory
sFilename_configuration_copy= os.path.join( sWorkspace_output, 'pyhexwatershed_configuration_copy.json' )
copy2(sFilename_configuration_in, sFilename_configuration_copy)

#copy the basin configuration file to the output directory as well
sFilename_configuration_basins_copy = os.path.join( sWorkspace_output, 'pyhexwatershed_configuration_basins_copy.json' )
copy2(sFilename_basins_in, sFilename_configuration_basins_copy)

sFilename_jigsaw_configuration_copy = os.path.join( sWorkspace_output, 'jigsaw_configuration_copy.json' )
copy2(sFilename_jigsaw_in, sFilename_jigsaw_configuration_copy)

#now switch to the copied configuration file for modification
sFilename_configuration = sFilename_configuration_copy
sFilename_basins = sFilename_configuration_basins_copy
sFilename_jigsaw = sFilename_jigsaw_configuration_copy

#change_json_key_value(sFilename_configuration, 'sWorkspace_output', sWorkspace_output) #output folder
change_json_key_value(sFilename_configuration, 'sFilename_basins', sFilename_basins) #basin configuration file
change_json_key_value(sFilename_configuration, 'sFilename_jigsaw_configuration', sFilename_jigsaw) #basin configuration file
#change the boundary file
#sFilename_mesh_boundary = realpath(os.path.join(sWorkspace_input, 'boundary.geojson'))
#change_json_key_value(sFilename_configuration, 'sFilename_mesh_boundary', sFilename_mesh_boundary)
#change the dem file

oPyflowline = pyflowline_read_configuration_file(sFilename_configuration,
                    iCase_index_in=iCase_index,
                    sDate_in= sDate, sMesh_type_in = sMesh_type)

oPyflowline.iFlag_flowline = 0
oPyflowline.iFlag_simplification = 0

if iFlag_create_job ==1:
    oPyflowline._pyflowline_create_hpc_job(sSlurm_in = sSlurm )
    print(iCase_index)
    sLine  = 'cd ' + oPyflowline.sWorkspace_output + '\n'
    ofs.write(sLine)
    sLine  = 'sbatch submit.job' + '\n'
    ofs.write(sLine)
else:
    oPyflowline.iFlag_user_provided_binary = 0 # set = 1 if setting the path to the binary
    oPyflowline.pyflowline_setup()
    oPyflowline.pyflowline_flowline_simplification()
    oPyflowline.iFlag_mesh_boundary = 1
    aCell = oPyflowline.pyflowline_mesh_generation()
    oPyflowline.pyflowline_reconstruct_topological_relationship()
    oPyflowline.pyflowline_export()


if iFlag_visualization == 1:
    sFilename =  'filtered_flowline.png'
    oPyflowline._plot(sFilename, sVariable_in = 'flowline_filter', aExtent_in =aExtent_full  )

    sFilename =  'conceptual_flowline_with_mesh.png'
    oPyflowline._plot(sFilename,  iFlag_title=1 ,sVariable_in='overlap',   aExtent_in =aExtent_full )

    sFilename =  'meander.png'
    oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',    aExtent_in =aExtent_meander )

    sFilename =  'braided.png'
    oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',    aExtent_in =aExtent_braided )

    sFilename =  'confluence.png'
    oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',    aExtent_in =aExtent_confluence )

    sFilename =  'outlet.png'
    oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',    aExtent_in =aExtent_outlet )

    sFilename =  'area_of_difference.png'
    oPyflowline._plot( sFilename,sVariable_in = 'aof',  aExtent_in=aExtent_full)
    pass

ofs.close()
print('Finished')
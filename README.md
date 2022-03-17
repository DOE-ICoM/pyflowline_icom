# Overview 
This repository is a tutorial to demonstrate the capability and workflow of the PyFlowline model. In this demo, we will use the Model for Prediction Across Scales (MPAS) mesh (see below) as an example.

# Pyflowline
The Pyflowline model is a Python package to generate conceptual river networks for hydrologic models. PyFlowline is mesh independent, meaning you can apply it to almost any mesh system including the tradition rectangle mesh, Triangulated Irregular Network (TIN) mesh and MPAS mesh.


# Installation
The full deployment of PyFlowline is still under development. It can be installed through either Pythin PyPI or the Conda system, which is recommended because of the dependency packages.

As of right now, you can install PyFlowline using the following steps:

1. install the dependency packages through Conda 


2. install PyFlowline through the PyPI:
    pip3 install pyflowline

3. (Optional) Install the visualization package through Conda:
    conda install -c conda-forge

4. (Optional) Install the Python JupyterNote to run this tutorial.


# Usage
We use the notebook.py example file under the tests/example/ directory to showcase the model workflow.
An additional Python package is required for the visualization purpose. Also see requirements.txt.

The follow steps are recommended:  

1. Open the terminal or use your preferred Conda application to create a new Conda environment:

    `conda create --name pyflowline python=3.8`

2. Activate the newly crated conda environment

    `conda activate pyflowline`

3. Install dependency packages using conda  

    `conda install -c conda-forge numpy shapely netCDF4 gdal`

4. Install PyFlowline  

    `pip3 install pyflowline`

5. Install and setup the Python Jupyter Notebook

6. Clone this repository and set this environment as the workspace environment

7. Navigate to the notebook and run it in your preferred Python IDE.

8. Visulize the results with QGIS


If using pyenv-virtualenv rather than Conda, the following steps are recommended (assumes a working installation of pyenv-virtualenvwrapper):  

1. cd to your preferred directory and clone this repo.

2. Open the terminal or use your preferred application to create a new virtualenv:    

    `mkvirtualenv -p python3.8 -a /path/to/local/copy/of/this/repo pyflowline`
	
3. activate the environment if it isn't automatically:
	
	`workon pyflowline`
	
4. Install pyflowline:
	
	`pip3 install pyflowline`

5. Make sure the dependencies listed above (numpy, shapely, netcdf4, gdal) are installed:

    `lssitepackages`
	
6. Open notebooks/pyflowline.ipynb in your preferred IDE
	- Note: If running in vscode, ensure the kernel is set to your activated environment and install ipykernel when prompted

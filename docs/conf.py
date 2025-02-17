# Configuration file for the Sphinx documentation builder.                                                                                                                 
#                                                                                                                                                                          
# This file only contains a selection of the most common options. For a full                                                                                               
# list see the documentation:                                                                                                                                              
# http://www.sphinx-doc.org/en/master/config                                                                                                                               

# -- Path setup --------------------------------------------------------------                                                                                             

# If extensions (or modules to document with autodoc) are in another directory,                                                                                            
# add these directories to sys.path here. If the directory is relative to the                                                                                              
# documentation root, use os.path.abspath to make it absolute, like shown here.                                                                                            
#
import json
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
print(sys.path)

# -- Project information -----------------------------------------------------                                                                                             

with open("../recipe/meta.json", "r", encoding="utf-8") as f:
    version = json.loads(f.read())["version"]

project = 'Unified Workflow'
author = ''
author_list = 'Holt, C., E. Carpenter, J. Derrico, V. Hagerty, F. Gabelmann, R. Mahajan, B. Cash, O. Adejumo, J. Prestopnik'
verinfo = version
release = f'{version}'
release_date = '2023-05-01'
release_year = release_date.split("-")[0]
release_month = release_date.split("-")[1]
release_day = release_date.split("-")[2]
copyright = f'{release_year}, {author_list}'

# -- General configuration ---------------------------------------------------                                                                                             

# Add any Sphinx extension module names here, as strings. They can be                                                                                                      
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom                                                                                                      
# ones.                                                                                                                                                                    
extensions = ['sphinx.ext.autodoc','sphinx.ext.intersphinx',]

# Add any paths that contain templates here, relative to this directory.                                                                                                   
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and                                                                                                     
# directories to ignore when looking for source files.                                                                                                                     
# This pattern also affects html_static_path and html_extra_path.                                                                                                          
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'Flowchart' ]

# Suppress certain warning messages                                                                                                                                        
suppress_warnings = ['ref.citation']

# -- Options for HTML output -------------------------------------------------                                                                                             

# The theme to use for HTML and HTML Help pages.  See the documentation for                                                                                                
# a list of builtin themes.                                                                                                                                                
#                                                                                                                                                                          
html_theme = 'sphinx_rtd_theme'
html_theme_path = ["_themes", ]
html_css_files = ['theme_override.css']

# Add any paths that contain custom static files (such as style sheets) here,                                                                                              
# relative to this directory. They are copied after the builtin static files,                                                                                              
# so a file named "default.css" will overwrite the builtin "default.css".                                                                                                  
html_static_path = ['_static']

# The name of an image file (relative to this directory) to place at the top                                                                                               
# of the sidebar.                                                                                                                                                          
html_logo = os.path.join('_static','UFS_image.png')

# -- Intersphinx control -----------------------------------------------------                                                                                             
intersphinx_mapping = {'numpy':("https://docs.scipy.org/doc/numpy/", None)}

numfig = True

numfig_format = {
    'figure': 'Figure %s',
}

# -- Export variables --------------------------------------------------------                                                                                             

rst_epilog = f"""                                                                                                                                                          
.. |copyright|    replace:: {copyright}                                                                                                                                    
.. |author_list|  replace:: {author_list}                                                                                                                                  
.. |release_date| replace:: {release_date}                                                                                                                                 
.. |release_year| replace:: {release_year}                                                                                                                                 
"""


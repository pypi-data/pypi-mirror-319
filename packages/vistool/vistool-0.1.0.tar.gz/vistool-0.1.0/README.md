[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KaysHaydock/VisTool.git/HEAD)

# VisTool: A Python Package for Visualising Health Datasets

## Overview
VisTool is a Python package designed to provide high-level visualisation tools for analysing health datasets. This toolkit enables users to visualise and interrogate the end users data with ease, facilitating better insights and decision-making.

## Project Structure
The repository is organised as follows:  

1. **`vistool/`**  
   Contains the core Python modules and functions, split into four main areas:  
   - **`combine.py`**: Tools for merging and combining datasets.  
   - **`download.py`**: Utilities for downloading and preprocessing data.  
   - **`visualize.py`**: Functions to generate various visualisations.  
   - **`wrangle.py`**: Methods for cleaning and preparing datasets for analysis.  

2. **`binder/`**  
   Includes the `environment.yml` file, which can be used to recreate the Python software environment required to run VisTool.  

3. **`notebooks/`**  
   - **`example_usage.ipynb`**: Demonstrates how to interact with the package's functions and provides examples of analyses and visualisations.  
   - **`documentation.ipynb`**: This is an additional notebook serving as documentation, including a user guide and a tutorial for using the package.
   -  **`advanced_example_usage.ipynb`**: This is an additional/optional notebook to read if you wish to see a few more advanced way of interacting with the packages functions.
   -  **`interactive_usage_in_dev.ipynb`**: This is an additional notebook still in the development stages which could be extended, it is for interactive features, showcasing the next milestone of the package.
4. **`tests/`**  
   - **`test_combine.py`, `test_download.py`, `test_visualize.py`, `test_wrangle.py`** - Four Python files containing Pytest-based unit tests for the core modules.  
   - An Excel file, **`functional_testing.xlsx`**, documenting functional tests with input-output examples.  

5. **`Instructions_readme/`**  
   A separate file providing detailed instructions on installing and running the package.  

6. **`LICENSE`**  
   The project is licensed under the MIT Licence.  

7. **`pyproject.toml`**  
   Contains metadata and configurations for building the package.  

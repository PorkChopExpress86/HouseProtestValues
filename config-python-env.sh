#!/bin/bash

# Config python3.13
# sudo add-apt-repository ppa:deadsnakes/ppa -y

# sudo apt install python3.13-full

# python3.13 -m ensurepip --upgrade
# python3.13 -m pip install --upgrade pip

# Create environment
python3.13 -m venv .venv

# Activate environment
source .venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install required packages
pip install pandas geopandas chardet numpy selenium webdriver-manager


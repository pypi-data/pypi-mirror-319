#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting build and publish process...${NC}"

# Check and install required packages
echo -e "${GREEN}Checking and installing required packages...${NC}"
pip install --upgrade pip build twine

# Clean previous builds
echo -e "${GREEN}Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info

# Build the package
echo -e "${GREEN}Building package...${NC}"
python -m build

# Upload to PyPI
echo -e "${GREEN}Uploading to PyPI...${NC}"
python -m twine upload dist/*

echo -e "${GREEN}Build and publish completed successfully!${NC}" 
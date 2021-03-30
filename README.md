# UWP-container-converter

This program aims to make it possible to easily convert Astroneer UWP file systems into a normal file system and back

## Requirement
-   Python 3.9

## Usage
use `python converter.py -d` to decode the microsoft saves to `%localappdata%\Packages\SystemEraSoftworks.29415440E1269_ftk5pbg2rayv2\SystemAppData-decode` and `python converter.py -e` to convert the folder back to microsoft. (when converting back the original one will be overwritten)

Note: this may not work with saves over 16MB

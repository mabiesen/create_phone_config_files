# Script to assist with the creation of phone configuration files

## Inputs:

1. CSV file - headers are representative of fields in configuration file
2. Dummy configuration file - file to be loaded into memory and altered to suit
3. Name of output directory (to be located in project directory), supplied at runtime.
4. Type of delimiter to the file (i.e. are params separated by =?)
5. Name of copy directory (should we copy to tftpboot? ultimately that is the question), supplied at run time


## Outputs:

1. Files named with MAC address, containing appropriate configuration


## TODO:

1.  Currently only works for text:  need to make available for xml

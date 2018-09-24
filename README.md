# Script to assist with the creation of phone configuration files

NOTE:  THIS IS FOR HISTORICAL REFERENCE ONLY.  Project moved to Percipia repo

## Inputs:

1. CSV file - headers are representative of fields in configuration file
2. Dummy configuration file - file to be loaded into memory and altered to suit
3. JSON file containing parameters.  See bleow for detail.
4. Name of output directory (to be located in project directory), supplied at runtime.
5. Name of copy directory (should we copy to tftpboot? ultimately that is the question), supplied at run time


#### JSON explained
1. textOrXML - tell program if text based or xml based string replacement
2. text_delimiter - if text file, tell program to separate keys and vals based on this parameter.
3. text_delimiter_override - Some config files do not have merely empty values, Bittel for instance outputs a file with parameters that are not delimited AND have no value.  The override signifies:  IF delimiter does not exist, THEN add delimiter and value to key.
4. configfile_extension - extension used to find the config file and write out new config files.  MUST contain a period as first character.
5. filename_field - name of the field which contains detail to name the file, USUALLY mac address related
6. filename_to_upper_bool - true or false, should letters in filename be capitalize?
7. filename_prefix_or_none - some config files need a prefix, for example "SEP" for cisco.

```
{
  "textOrXML": "XML",
  "text_delimiter": "\t",
  "text_delimiter_override": "true",
  "filename_extension": ".xml",
  "filename_field": "MAC_ADDRESS",
  "filename_to_upper_bool": "true",
  "filename_prefix_or_none": "SEP"
}
```

## Outputs:

1. Files named with MAC address, containing appropriate configuration


## TODO:

1.  Add option to script to create a mock csv input file with appropriate csv headers

# !/bin/bash
import util_csv
import util_text
import util_dir
import json
import sys
import re

#---Reading files ------------------------------------------
# function to put starter phone cfg into variable

def read_config_file():
    print("looking for config file")
    filepath = get_filepath_with_extension(".cfg")
    print("reading config file")
    try:
        config_lines = util_text.readToArray(filepath)
        return config_lines
    except:
        print("We were unable to read the configuration.")
        print(sys.exc_info()[0])
        program_exit()

# function to put csv file into variables
def read_csv():
    print("looking for csv file")
    filepath = get_filepath_with_extension(".csv")
    print("reading csv file")
    try:
        csv_lines = util_csv.csv_reader(filepath)
        return csv_lines
    except:
        print("There was an error loading csv data")
        print(sys.exc_info()[0])
        program_exit()

# should output dict
def read_json_file():
    print("looking for map file")
    filepath = get_filepath_with_extension(".json")
    print("reading parameters file")
    try:
        parameters_dict = {}
        with open(filepath, 'r') as f:
            parameters_dict = json.load(f)
        return parameters_dict
    except:
        print("There was an error loading the parameters json file")
        print(sys.exc_info()[0])
        program_exit()


def get_filepath_with_extension(extension):
    print("Looking for a file with extension %s" %(extension))
    # should validate one and only one file of kind, else error and exit
    current_dir = util_dir.get_current_dir()
    num_filetype = util_dir.get_num_of_filetype(extension,current_dir)
    if num_filetype > 1:
        print("There are %d of %s files in the directory: \n%s" %(num_filetype,extension,current_dir))
        print("This is not acceptable, keep clean!")
        program_exit()

    # get the full file path
    filename = util_dir.get_file_with_extension(extension, current_dir)
    filepath = util_dir.construct_filepath(current_dir,filename)

    # should validate file not blank or non-existent
    if not util_dir.is_file_empty(filepath):
        print("The file at %s is empty" %(filepath))
        print("This is not acceptable, all files must be present.")
        program_exit()

    # should return full file path
    return filepath



# --Writing Files-------------------------------------------

# function to write final values to file
def write_to_file(filepath, lines):
    print("Writing file: \n%s\n to directory" %(filepath))
    try:
        util_text.writeLineByLine(filepath, lines)
    except:
        print("An error writing %s file occurred" %(filename))
        print(sys.exc_info()[0])
        program_exit()

#-- Directory work -------------------------------------------

# function to move file to appropriate location
def create_or_clear_dir(directory_of_output):
    print("Creating dir if does not exist, else clearing the directory")
    try:
        util_dir.make_or_clear_dir(directory_of_output)
    except:
        print("Failed creating output directory")
        program_exit()


def create_output_directory():
    print("We need to create a new directory for output")
    name_of_dir = raw_input("Please enter a name for the new directory: ")
    directory_of_output =  util_dir.filepath_from_script_dir(name_of_dir)
    print("Your files will be output to: " + directory_of_output)
    create_or_clear_dir(directory_of_output)
    return directory_of_output

#-- String Manipulation/Comparison ---------------------------------------


def replace_after_char(origstring, addstring, thischar="="):
    print("Replacing line in config file")
    if thischar in origstring:
        return origstring.split(thischar, 1)[0] + thischar + addstring
    else:
        print("You have set a bad delimiter!!! it is not present in the string")
        print("delimiter: %s" %(thischar))
        print("origstring: %s" %(origstring))
        print("The data should not be trusted; you should review your config file")
        program_exit()


#-- Prompts ---------------------------------------------------------
# begginning prompt
def introduction():
    print("This program is intended to assist with phone configuration file creation")
    print("Before you begin, place one configuration file template into the project directory.")
    print("Additionally, provide a csv file that contains the following headers: ")
    print("Csv file should be comma delimited")
    print("And finally, you must have a json file containing your parameters.")


def mapping_option():
    print("")
    print("Values can be mapped from common origin to reduce redundancy.")
    print("Or if you prefer verbose and illegible-because-their-so-damn-similar variables, you can forego the json file and merely use csv.")
    print("")
    x = raw_input("Would you like to map out specific parameters, represented through csv headers, to device values?")


def program_exit():
    print("exiting program")
    sys.exit()


#-- Array manip ----------------------------------------------------------------
# function to loop over all values in csv lines
# NEEDS TO BE FIXED!!!!! uses dict
def config_search_and_replace(config_lines,key,value):
    for line_id,line in enumerate(config_lines):
        if key in line:
            print("key found")
            mod_line = replace_after_char(line,value,"\t")
            print(mod_line)
            config_lines[line_id] = mod_line
            return config_lines
    return config_lines

def remove_newline_from_array(myarray):
    print("removing newlines from array items")
    for xid,x in enumerate(myarray):
        myarray[xid] = util_text.strip_newline_char(x)
    return myarray


# function to obtain destination from user
# DESTINATION COULD BE LOCAL OR NON LOCAL

#--------MAIN-------------------MAIN--------------MAIN--------------------------
def main():
    introduction()
    print("startingp program")
    print("setting variables")
    directory_of_output = create_output_directory()
    csv_lines = read_csv()
    print(csv_lines)
    config_lines = read_config_file()
    json_data = read_json_file()

    # Keep header row csv
    csv_header = csv_lines[0]

# -------Direct CSV MAP-----------------
    for line_id,line in enumerate(csv_lines):
        #skip first line
        if line_id == 0:
            continue
        for field_id,field in enumerate(csv_header):
            print("Looking for field: %s" %field)
            print("replacing")
            config_lines = config_search_and_replace(config_lines, re.sub(' +','',field),line[field_id])

        config_lines = remove_newline_from_array(config_lines)
        print(config_lines)
        print("Writing configfile to %s" %(directory_of_output))
        write_to_file(directory_of_output +"/" + line[0] + ".cfg",config_lines)
main()
# ------MAPPING OPTION ---------------

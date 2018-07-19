# !/bin/bash
#m ain data structures
from util_xml_file import *
from util_text_file import *

# helper functions
import util_dir
import util_csv

# standard lib
import json
import sys
import re

#---Reading files ------------------------------------------

# should output list of lists
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
    filepath = get_filepath_with_extension(".json")
    print("reading parameters file")
    try:
        parameters_dict = {}
        with open(filepath, 'r') as f:
            parameters_dict = json.load(f)
        return parameters_dict
    except:
        print("There was an error loading the parameters json file")
        print("It is possible that you forgot a comma separator")
        print(sys.exc_info()[0])
        program_exit()

# search current directory, retrieve file with extension
# used to get csv/json/config files
def get_filepath_with_extension(extension):
    print("Looking for a file with extension %s" %(extension))
    # should validate one and only one file of kind, else error and exit
    current_dir = util_dir.get_current_dir()
    num_filetype = util_dir.get_num_of_filetype(extension,current_dir)
    if num_filetype != 1:
        print("There are %d of %s files in the directory: \n%s" %(num_filetype,extension,current_dir))
        print("This is not acceptable, must have 1 and only 1 %s file" %(extension))
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


#-- Directory work -------------------------------------------

# function to move file to appropriate location
def create_or_clear_dir(directory_of_output):
    print("Creating dir if does not exist, else clearing the directory")
    try:
        util_dir.make_or_clear_dir(directory_of_output)
    except:
        print("Failed creating output directory")
        program_exit()


#-- Prompts ---------------------------------------------------------
# begginning prompt
def introduction():
    print("This program is intended to assist with phone configuration file creation")
    print("")
    print("Before you begin, place one configuration file template into the project directory.")
    print("")
    print("Additionally, provide a csv file that contains parameters as headers")
    print("Csv file should be comma delimited")
    print("NOTE:  YOU MUST PUT THE MAC ADDRESS IN FIRST COLUMN!!! MANDATORY.")
    print("")
    print("And finally, include a json file containing some phone specific detail")
    print("see the example file")

# create the local output directory
def create_output_directory():
    print("We need to create a new directory for output")
    name_of_dir = raw_input("Please enter a name for the new, project-local directory: ")
    directory_of_output =  util_dir.filepath_from_script_dir(name_of_dir)
    print("Your files will be output to: " + directory_of_output)
    create_or_clear_dir(directory_of_output)
    return directory_of_output

# copy the files to a different, final directory
# this is meant to be used to move files to tftpboot
def copy_files_to_directory(directory_of_output):
    answer = raw_input("If you would like to copy files to an existing directory, enter directory path.  Else, enter 'n': ")
    if answer == 'n':
        print("you chose not to move files")
    else:
        print("Validating the chosen directory")
        validation = util_dir.check_for_dir(answer)
        if validation == False:
            print("That was not an acceptable directory")
            print("Files will not be copied")
            program_exit()
        else:
            print("Copying files...")
            try:
                util_dir.copy_files_to_directory(directory_of_output,answer)
            except:
                print("There was an error copying files to the selected directory")
                program_exit()


# exit the program gracefully
def program_exit():
    print("exiting program")
    sys.exit()
#-------------------------------------------------------------------------------


# Check to see if the replacement was truly successful
# Check should involve evaluation of number of replacements
def replacement_check(status_tuple):
    success, ctr, key = status_tuple
    if success == True:
        if ctr == 0:
            print("Oh no! we couldn't find the parameter %s" %(key))
            print("Please insure that the parameter is spelled correctly and retry")
            program_exit()
        if ctr > 1:
            print("Oh no! we found multiple matches for parameter %s" %(key))
            print("Perhaps the parameter string exists as part of another parameter?")
            print("Please look into this and try again")
            program_exit()

    if success == False:
        print("There was an issue. Please correct root cause and try again")
        program_exit()

# function to obtain destination from user
# DESTINATION COULD BE LOCAL OR NON LOCAL

#--------MAIN-------------------MAIN--------------MAIN--------------------------
def main():
    introduction()
    print("starting program")
    print("setting variables")

    # get user-provided directory for output - to be in project dir
    directory_of_output = create_output_directory()

    # CSV data
    csv_lines = read_csv()
    print("Collecting csv header")
    csv_header = csv_lines[0]

    # JSON data
    json_data = read_json_file()
    data_type = json_data["textOrXML"]
    extension = json_data['configfile_extension']

    # get the config file
    filepath = get_filepath_with_extension(extension)

    # determine whether we should evaluate as a text file or xml
    if data_type == "text":
        try:
            file_class = TextFile(filepath, json_data)
        except Exception as e:
            print("Error creating text fileclass")
            print(e)
            program_exit()
    elif data_type == "XML":
        try:
            file_class = XMLFile(filepath, json_data)
        except Exception as e:
            print("Error creating xml file class")
            print(e)
            program_exit()
    else:
        print("An invalid config file type was supplied in the json file")
        print("This is not acceptable.  Please configure the")
        print("textOrXML field to say either 'text' or 'XML' accordingly")
        program_exit()

#------ Iterate over CSV data and replace
    for line_id,line in enumerate(csv_lines):
        # skip first line, contains header!
        if line_id == 0:
            continue
        for field_id,field in enumerate(csv_header):
            print("Looking for field: %s" %field)
            field_no_white = re.sub(' +','',field)
            replacement_check(file_class.replace_a_string(field_no_white, line[field_id]))

        print("Writing configfile to %s" %(directory_of_output))

        # prep the filename
        filename = line[0]
        if json_data["filename_to_upper_bool"].upper() == "TRUE":
            filename = filename.upper()
        if json_data["filename_prefix_or_none"].upper() != "NONE":
            filename = json_data["filename_prefix_or_none"] + filename

        final_file_path = directory_of_output +"/" + filename + extension

        # write the file
        write_success = file_class.write_to_file(final_file_path)
        if write_success == False:
            print("There was an error writing data to file")
            program_exit()

    # offer the option to copy files to tftpboot
    copy_files_to_directory(directory_of_output)
    print("Program complete!")

main()

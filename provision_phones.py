# !/bin/bash
import util_csv
import util_text_file
import util_dir
import util_xml_file
import json
import sys
import re

#---Reading files ------------------------------------------
# function to put starter phone cfg into variable

def read_config_file(extension):
    print("looking for config file")
    filepath = get_filepath_with_extension(extension)
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
        print("It is possible that you forgot a comma separator")
        print(sys.exc_info()[0])
        program_exit()


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
    name_of_dir = raw_input("Please enter a name for the new, project-local directory: ")
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
    print("")
    print("Before you begin, place one configuration file template into the project directory.")
    print("")
    print("Additionally, provide a csv file that contains parameters as headers")
    print("Csv file should be comma delimited")
    print("NOTE:  YOU MUST PUT THE MAC ADDRESS IN FIRST COLUMN!!! MANDATORY.")
    print("")
    print("And finally, include a json file containing some phone specific detail")
    print("see the example file")


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



def program_exit():
    print("exiting program")
    sys.exit()


#-- Array manip ----------------------------------------------------------------
# function to loop over all values in csv lines
def string_config_search_and_replace(config_lines,key,value,delimiter):
    ctr = 0
    for line_id,line in enumerate(config_lines):
        if key in line:
            ctr = ctr + 1
            print("key found")
            mod_line = replace_after_char(line,value,delimiter)
            print(mod_line)
            config_lines[line_id] = mod_line
            return config_lines
    if ctr == 0:
        print("Oh no! we couldn't find the parameter %s" %(key))
        print("Please insure that the parameter is spelled correctly and retry")
        program_exit()
    if ctr > 1:
        print("Oh no! we found multiple matches for parameter %s" %(key))
        print("Perhaps the parameter string exists as part of another parameter?")
        print("Please look into this and try again")
        program_exit()
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
    print("starting program")
    print("setting variables")
    directory_of_output = create_output_directory()
    csv_lines = read_csv()
    print(csv_lines)
    json_data = read_json_file()

    # Keep header row csv
    print("Collecting csv header")
    csv_header = csv_lines[0]

# -------Direct CSV MAP-----------------

#----- Set the config file ----
    data_type = json_data["textOrXML"]
    extension = json_data['extension']

    if data_type == "text":
        config_lines = read_config_file(extension)
    elif data_type == "XML":
        xml_obj = util_xml_file.XMLFile(get_filepath_with_extension(extension))
    else:
        print("An invalid config file type was supplied in the json file")
        print("This is not acceptable.  Please configure the")
        print("textOrXML field to say either 'text' or 'XML' accordingly")
        program_exit()

#------ Iterate over CSV data and replace
    for line_id,line in enumerate(csv_lines):
        #skip first line
        if line_id == 0:
            continue
        for field_id,field in enumerate(csv_header):
            print("Looking for field: %s" %field)
            field_no_white = re.sub(' +','',field)
            if data_type == "text":
                config_lines = string_config_search_and_replace(config_lines,field_no_white,line[field_id],json_data["delimiter"])
            if data_type == "XML":
                xml_obj.replace_tag_text(field_no_white,line[field_id])

        print("Writing configfile to %s" %(directory_of_output))

        # cleanup newlines if text
        if data_type == "text":
            config_lines = remove_newline_from_array(config_lines)

        # prep the filename
        filename = line[0]
        if json_data["nameToUpper"].upper() == "TRUE":
            filename = filename.upper()
        if json_data["namePrefix"].upper() != "NONE":
            filename = json_data["namePrefix"] + filename

        final_file_path = directory_of_output +"/" + filename + extension

        # write the file
        if data_type == "text":
            write_to_file(final_file_path,config_lines)
        if data_type == "XML":
            xml_obj.write_to_file(final_file_path)


    # offer the option to copy files to tftpboot
    copy_files_to_directory(directory_of_output)
    print("Program complete!")

main()

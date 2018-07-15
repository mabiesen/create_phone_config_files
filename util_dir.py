import os

def make_or_clear_dir(dirpath):
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    else:
        delete_dir_files(dirpath)

def delete_dir_files(dirpath):
    map( os.unlink, (os.path.join(dirpath,f) for f in os.listdir(dirpath)) )

def check_for_dir(dirpath):
    if not os.path.isdir(dirpath):
        return False
    return True

def get_num_of_filetype(extension, dir):
    return len([f for f in os.listdir(dir)
         if f.endswith(extension) and os.path.isfile(os.path.join(dir, f))])

def get_file_with_extension(extension,dir):
    for f in os.listdir(dir):
        if f.endswith(extension):
            return f

def check_only_one_of_filetype(directory, extension):
    if get_num_of_filetype(extension,directory) > 1:
        return False
    return True

def construct_filepath(mypath, filename):
    return os.path.join(mypath, filename)

def filepath_from_script_dir(filename):
    scriptdir = get_current_dir()
    return construct_filepath(scriptdir, filename)

def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))

def is_file_empty(filepath):
    return os.path.isfile(filepath) and os.path.getsize(filepath) > 0

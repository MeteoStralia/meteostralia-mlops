import os

def create_folder_if_necessary(output_folderpath):
    # Create folder if necessary
    if not os.path.exists(output_folderpath):
        os.makedirs(output_folderpath)
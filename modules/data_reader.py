import os
import sys
import shutil

def read_file(filename=f'{sys.path[1]}/data/database.csv'):
    f = open(filename, "r")
    return f.read().splitlines()

def add_entry_to_file(entry, src=f'{sys.path[1]}/data/database.csv', bkp_dest=f'{sys.path[1]}/data/database_bkp.csv', is_backup_needed=True):
    if is_backup_needed:
        shutil.copyfile(src, bkp_dest)
    f = open(src, "a+")
    f.write(entry)

def get_available_image(index):
    try:
        f = open(f'{sys.path[1]}/img/{index}.png', "r")
        return f'{sys.path[1]}/img/{index}.png'
    except Exception as err:
        return f'{sys.path[1]}//img/{index}.jpg'


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def convert_binary_to_img(data, filename):
    with open(filename, "wb") as fh:
        fh.write(data)
    return filename


def remove_file(filename):
    os.remove(filename)

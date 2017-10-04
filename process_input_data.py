import json
import random
import logging
import math
import re
import platform
import os


input_files_list = 'input_files.json'
number_of_slaves = 4
remote_machine_name_pattern = 'cpp-test(\\d{2})'
base_dir = os.path.dirname(__file__) + "/"

class ProcessInputData(object):

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

    def main(self):
        logging.info("STARTED PROCESSING INPUT TEST DATA")
        with open(input_files_list) as input_files:
            files_to_process = json.load(input_files)
        for filename in files_to_process['files_to_shuffle']:
            file_path = base_dir  + filename
            shuffle_lines_in_file(file_path)
        for filename in files_to_process['files_to_split']:
            file_path = base_dir  + filename
            process_file_for_part_extraction(file_path)

def shuffle_lines_in_file(filename):
    try:
        archive_file(filename)
        lines = open(filename).readlines()
        random.shuffle(lines)
        open(filename, 'wb').writelines(lines)
        logging.info("Lines in {0} file has been randomly shuffled".format(filename))
    except IOError:
        logging.warning("Could not open {0} file".format(filename))

def process_file_for_part_extraction(filename):
    part_number_to_extract = get_remote_machine_index()
    if part_number_to_extract:
        try:
            archive_file(filename)
            extract_part_from_file(part_number_to_extract, filename)
        except IOError:
            logging.warning("Could not open {0} file".format(filename))
    else:
        logging.warning("File split process for {0} not started".format(filename));


def extract_part_from_file(part_number, filename):
    file_part_size = int(math.ceil(file_len(filename) / float(number_of_slaves)))

    input_file = open(filename, 'r')

    counter = 0
    current_file_part = 1
    output_file = None
    for line in input_file:
        if counter % file_part_size == 0:
            if output_file:
                output_file.close()
                output_file = None
            if current_file_part == part_number:
                output_file = open(filename, 'wb')
            current_file_part += 1
        if output_file: output_file.write(line)
        counter += 1
    logging.info("Extracted part number {0} of {1} file".format(int(part_number), filename))


def get_remote_machine_index():
    machine_name = platform.node()
    pattern = remote_machine_name_pattern
    m = re.search(pattern, machine_name)
    if m:
        found = m.group(1)
        logging.info("Identified remote machine number:{0}".format(found))
        return int(found)
    else:
        logging.warning("Could not identify remote machine number from given hostname: {} ".format(machine_name))
    return None


def archive_file(filename):
    with open(filename) as loaded_file:
        lines = loaded_file.read()
        index = filename.find(".")
        original_filename = filename[:index] + '_original' + filename[index:]
        with open(original_filename, 'wb') as output_file:
            output_file.writelines(lines)
        logging.info("Original file {0} was saved in {1}".format(filename , original_filename))

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if __name__ == '__main__':
    ProcessInputData().main()
#!/usr/bin/python

import os
import re

files_in_dir = []
experiments = {}


def list_directories():
    # list all files in directories
    for root, dirs, files in os.walk("./results"):
        for file in files:
            if file.endswith(".log"):
                files_in_dir.append(os.path.join(root, file))


def classication_by_experiment(file_names_array):
    for file_name in file_names_array:
        in_file = open(file_name, 'rt')
        contents = tail(in_file, 2)
        contents.replace(r"\r", r"\n")
        in_file.close()
        # filter log results
        re_match = re.search(
            "init_time=([0-9]*\.?[0-9]{6}); stall_count=([0-9]*); stall_time=([0-9]*\.?[0-9]{6})", contents)
        if re_match:
            init_time = re_match.group(0)
            stall_count = re_match.group(1)
            stall_time = re_match.group(2)
            log_data = [init_time, stall_count, stall_time]
            # get staX name
            sta_name = re.search('log_(sta[0-9]{1})', file_name).group(1)

            # Group experiments by name, date and time
            re_match = re.search('_rep([0-9]{8})\_([0-9]{6})\_(.+?)\.', file_name)
            exp_name = re_match.group(3)
            exp_date = re_match.group(1)
            exp_time = re_match.group(2)
            if exp_name not in experiments.keys():
                experiments[exp_name] = {}
            if exp_date not in experiments[exp_name].keys():
                experiments[exp_name][exp_date] = {}
            if exp_time not in experiments[exp_name][exp_date].keys():
                experiments[exp_name][exp_date][exp_time] = {sta_name: log_data}
        else:
            init_time = 0.00
            stall_count = 0
            stall_time = 0.00
            print "Error processing file: \n {0:s}".format(file_name)
            print "No AppQoE data."


def tail(f, lines=20):
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number * BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0, 0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])


def main():
    list_directories()
    classication_by_experiment(files_in_dir)
    print experiments


if __name__ == '__main__':
    main()

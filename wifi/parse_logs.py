#!/usr/bin/python

from __future__ import print_function
import os
import re
import locale

files_in_dir = []
experiments = {}
experiments_a = []


def list_directories():
    # list all files in directories
    for root, dirs, files in os.walk("./results_10"):
        for file in files:
            if file.endswith(".log"):
                files_in_dir.append(os.path.join(root, file))


def classication_by_experiment(file_names_array):
    for file_name in file_names_array:
        in_file = open(file_name, 'rt')
        contents = tail(in_file, 2)
        contents.replace(r"\r", r"\n")
        in_file.close()
        # initializing variables
        init_time = 0.00
        stall_count = 0
        stall_time = 0.00
        # filter log results
        re_match = re.search(
            "init_time=([0-9]*\.?[0-9]{6}); stall_count=([0-9]*); stall_time=([0-9]*\.?[0-9]{6})", contents)
        if re_match:
            init_time = re_match.group(1)
            stall_count = re_match.group(2)
            stall_time = re_match.group(3)
            log_data = []
            log_data.append(init_time)
            log_data.append(stall_count)
            log_data.append(stall_time)
            # get staX name
            sta_name = re.search('log_(sta[0-9]{1})', file_name).group(1)

            # Group experiments by name, date and time
            re_match = re.search(
                '_rep([0-9]{8})\_([0-9]{6})\_(.+?)\.', file_name)
            exp_name = re_match.group(3)
            exp_date = re_match.group(1)
            exp_time = re_match.group(2)
            if exp_name not in experiments.keys():
                experiments[exp_name] = {}
            if exp_date not in experiments[exp_name].keys():
                experiments[exp_name][exp_date] = {}
            if exp_time not in experiments[exp_name][exp_date].keys():
                experiments[exp_name][exp_date][exp_time] = []
            sta_log = {}
            sta_log[sta_name] = log_data
            experiments[exp_name][exp_date][exp_time].append(sta_log)
            exp_row = []
            exp_row.append(exp_name)
            exp_row.append(exp_date)
            exp_row.append(exp_time)
            exp_row.append(sta_name)
            exp_row.append(init_time)
            exp_row.append(stall_count)
            exp_row.append(stall_time)
            experiments_a.append(exp_row)
        else:
            print ("Error processing file: \n {0:s}".format(file_name))
            print ("No AppQoE data.")


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


def print_data(exp_array):
    # for exp_name, exp_values in exp_array.iteritems():
    #     print '*************** {0:10s}****************'.format(exp_name)
    #     for exp_date_name, exp_date_values in exp_values.iteritems():
    #         print exp_date_name
    #         print exp_date_values
    experiments_s = sorted(experiments_a, key=lambda row: (
        row[0], row[1], row[2], row[3]))
    exp_name = ''
    exp_time = ''
    for exp_data in experiments_s:
        if exp_name != exp_data[0]:
            print ("\n")
            print ('**************************************************')
            print ('{0:s}'.format(exp_data[0]))
            print ('**************************************************')
            exp_name = exp_data[0]

        if(exp_time != exp_data[2]):
            exp_time = exp_data[2]
            print("\r")

        #    [0]        [1]        [2]      [3]       [4]        [5]      [6]
        # ['EIGHT', '20161007', '143443', 'sta8', '1234.488037', '4', '277.575989']
        print ('{0:s};{1:f};{2:d};{3:f};'.format(
            exp_data[2],
            float(exp_data[4]),
            int(exp_data[5]),
            float(exp_data[6])).replace(".", ","),
            end="")

    print("\n")


def main():
    list_directories()
    classication_by_experiment(files_in_dir)
    print_data(experiments)


if __name__ == '__main__':
    main()

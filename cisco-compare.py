#!/usr/bin/env python
# -*- coding:utf-8 -*-

try:
    import optparse
    import os
    import sys
    import difflib
    import shutil


except Exception as err:
    print '[!] ' + str(err)
    sys.exit(0)


def find_item(item, file_name):
    item_value = []
    item_line = []
    line_number = 0
    f = open(file_name, 'rt')
    for line in f.readlines():
        line = line.strip()
        line_number = line_number + 1
        if line.startswith(item):
            item_value.append(line)
            item_line.append(line_number)
    f.close()
    return item_value, item_line


def find_section(start_char, end_char, file_name):
    item_value = []
    item_line = []
    inRecordingMode = False
    line_number = 0
    f = open(file_name, 'rt')
    for line in f.readlines():
        line = line.strip()
        line_number = line_number + 1
        if line.startswith(start_char):
            inRecordingMode = True
            item_value.append(line)
            item_line.append(line_number)
        elif inRecordingMode:
            if line.startswith(end_char):
                inRecordingMode = False
                item_value.append(line)
                item_line.append(line_number)
            elif line.startswith('access-list'):
                inRecordingMode = False
            else:
                item_value.append(line)
                item_line.append(line_number)
    f.close()
    return item_line, item_value


def compare_lists(list_a, list_b, name):
    working_dir = os.path.dirname(os.path.abspath(__file__)) + '/debug'
    if os.path.exists(working_dir):
        shutil.rmtree(working_dir)
    os.makedirs(working_dir)
    file_a = working_dir + '/file_a_' + name
    file_b = working_dir + '/file_b_' + name
    file_dif = working_dir + '/file_dif_' + name
    f = open(file_a, 'wt')
    for element in list_a:
        f.write(element)
        f.write('\n')
    f.close()
    f = open(file_b, 'wt')
    for element in list_b:
        f.write(element)
        f.write('\n')
    f.close()
    f = open(file_dif, 'wt')
    with open(file_b, 'r') as file_0:
        with open(file_a, 'r') as file_1:
            diff = difflib.unified_diff(
                file_0.readlines(),
                file_1.readlines(),
                fromfile='file_0',
                tofile='file_1',
            )
            for line in diff:
                f.write(line)
                sys.stdout.write(line)
    file_0.close()
    file_1.close()
    f.close()


def test_file(file_name):
    if not os.path.isfile(file_name):
        print 'file ' + '<' + file_name + '>' + ' not found'
        sys.exit(0)


def start():
    pars = optparse.OptionParser(description=' add later')
    pars.add_option('--acl', type='string', dest='acl', help='Default enabled needs to be set to 0 if acl should not be compared', default='1')
    pars.add_option('--int', type='string', dest='int', help='Default enabled needs to be set to 0 if int should not be compared', default='1')
    pars.add_option('--obj', type='string', dest='obj', help='Default enabled needs to be set to 0 if obj should not be compared', default='1')
    pars.add_option('-c', type='string', dest='current', help='The current configuration file there are working', default='None')
    pars.add_option('-n', type='string', dest='new', help='The new configuration there needs to be compared to the current', default='None')
    pars.add_option('--debug', type='string', dest='debug', help='enable to keep the debug file', default='0')
    opts, args = pars.parse_args()
    test_file(opts.current)
    test_file(opts.new)

    if opts.acl is '1':
        print '-*- Access-List compare -*-'
        name = 'acl'
        item_value1, item_line1 = find_item('access-list', opts.current)
        item_value2, item_line2 = find_item('access-list', opts.new)
        compare_lists(item_value1, item_value2, name)

    if opts.int is '1':
        print '-*- Interface compare -*-'
        start_char = 'interface'
        end_char = '!'
        name = 'int'
        int_current_line, int_current_value = find_section(start_char,end_char, opts.current)
        int_new_line, int_new_value = find_section(start_char, end_char, opts.new)
        compare_lists(int_current_value, int_new_value, name)

    if opts.obj is '1':
        print '-*- Object-group compare -*-'
        start_char = 'object-group'
        end_char = 'object-group'
        name = 'obj'
        obj_current_line, obj_current_value = find_section(start_char,end_char, opts.current)
        obj_new_line, obj_new_value = find_section(start_char, end_char, opts.new)
        compare_lists(obj_current_value, obj_new_value, name)

    if opts.debug is '0':
        working_dir = os.path.dirname(os.path.abspath(__file__)) + '/debug'
        print '-*- Debug files are being deleted -*-'
        shutil.rmtree(working_dir)

if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt as err:
        print '\n[!] why :-)'
        sys.exit(0)

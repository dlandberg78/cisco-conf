#!/usr/bin/env python
# -*- coding:utf-8 -*-

try:
    import optparse
    import os
    import sys

except Exception as err:
    print '[!] ' + str(err)
    sys.exit(0)


def find_item(item, file_name):
    item_value = []
    item_line = []
    line_number = 0
    f = open(file_name, 'rt')
    for line in f.readlines():
        line_number = line_number + 1
        if line.startswith(item):
            item_value.append(line)
            item_line.append(line_number)
    f.close()
    return item_value, item_line

def find_section(start, end, file_name):
    item_value = []
    item_line = []
    inRecordingMode = False
    line_number = 0
    f = open(file_name, 'rt')
    for line in f.readlines():
        line_number = line_number + 1
        if line.startswith(start):
            inRecordingMode = True
            item_value.append(line)
            item_line.append(line_number)
        elif inRecordingMode:
            if line.startswith(end):
                inRecordingMode = False
                item_value.append(line)
                item_line.append(line_number)
            else:
                item_value.append(line)
                item_line.append(line_number)
    f.close()
    return item_line, item_value

def compare_lists(list_a, list_b, line_b):
    for a, b in zip(list_a, list_b):
        if not a == b:
            if a not in list_b:
                for i in (i for i, x in enumerate(list_a) if x == a):
                    print 'Line: ' + str(line_b[i]) + ' are missing in new conf: ' + a


def test_file(file_name):
    if not os.path.isfile(file_name):
        print 'file ' + file_name + ' not found'
        sys.exit(0)


def start():
    pars = optparse.OptionParser(description=' add later')
    pars.add_option('--acl', type='string', dest='acl', help='add later', default=1)
    pars.add_option('--int', type='string', dest='int', help='add later', default=1)
    pars.add_option('--obj', type='string', dest='obj', help='add later', default=1)
    pars.add_option('-c', type='string', dest='current', help='add later', default='None')
    pars.add_option('-n', type='string', dest='new', help='add later', default='None')
    opts, args = pars.parse_args()
    test_file(opts.current)
    test_file(opts.new)

    if opts.acl is '1':
        print '-*- Access-List compare: -*-'
        item_value1, item_line1 = find_item('access-list', opts.current)
        item_value2, item_line2 = find_item('access-list', opts.new)
        compare_lists(item_value1, item_value2, item_line2)

    if opts.int is '1':
        print '-*- Interface compare: -*-'
        start_char = 'interface'
        end_char = '!'
        int_current_line, int_current_value = find_section(start_char,end_char, opts.current)
        int_new_line, int_new_value = find_section(start_char, end_char, opts.new)
        compare_lists(int_current_value, int_new_value, int_new_line)

    if opts.obj is '1':
        print '-*- Interface compare: -*-'
        start_char = ''
        end_char = '!'
        obj_current_line, obj_current_value = find_section(start_char,end_char, opts.current)
        obj_new_line, obj_new_value = find_section(start_char, end_char, opts.new)
        compare_lists(obj_current_value, obj_new_value, obj_new_line)
if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt as err:
        print '\n[!] why :-)'
        sys.exit(0)

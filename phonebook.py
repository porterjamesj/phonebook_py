#!/usr/bin/env python
import sys
import re
import os


def pb_parse_input_row(row):
    """parse one row from file input"""
    row = row.rstrip("\n")  # remove trailing newline
    name = [c for c in row if not c.isdigit()]  # remove digits
    number = [c for c in row if c.isdigit()]  # remove non-digits
    return name, number


def pb_parse_output_row(name, number):
    """parse output string from name & number"""
    return name + ' ' + number + '\n'


def print_results(rows):
    """parse all results (accepts list of key-value pairs)"""
    if len(rows) > 0:
        for name, number in rows.iteritems():
            print name + ' ' + number
    else:
        print 'No results'


def pb_load(filename):
    """load phonebook from file"""
    pb = {}
    with open(filename, 'r') as f:
        for line in f:
            name, number = pb_parse_input_row(line)
            pb[name] = number
    return pb


def pb_save(filename, pb):
    """save phonebook to a file"""
    with open(filename, 'w') as f:
        for name, number in pb.iteritems():
            f.write(pb_parse_output_row(name, number))


def pb_create(filename):
    if not os.path.isfile(filename):
        # sadly there is no os.touch method, I'm not aware of a better
        # way to do it than this
        file_obj = open(filename, 'w')
        file_obj.close()
        print('Created phonebook %s in current directory' % (filename))
    else:
        print('Error: file %s already exists!' % (filename))
        return False


def pb_lookup(name_lookup, pb):
    """find by text partial match to name string"""
    results = {}
    search_name = name_lookup.lower()
    for name, num in pb.iteritems():
        if search_name in name.lower():
            results[name] = num
    return results


def pb_reverse_lookup(number, pb):
    """find by phone number (exact match)"""
    results = {}
    num = re.sub('\D', '', number)
    for name, num in pb.iteritems():
        if num == number:
            results[name] = num
    return results


def pb_add(name, number, pb):
    """check if row exists. Return false if already exists"""
    if name in pb:
        return False
    pb[name] = number
    return True


def pb_change(name, number, pb):
    print(name, number, pb)
    if name in pb:
        pb[name] = number
        return True
    else:
        return False


def pb_remove(name, pb):
    """phonebook remove 'John Michael' hsphonebook.pb # error message on
    not exist"""
    if (name in pb):
        pb.pop(name, None)
        return True
    else:
        return False


def parse_arguments(args):
    accepted_commands = ['create', 'add', 'change', 'remove',
                         'lookup', 'reverse-lookup']
    filename = None
    name = None
    number = None
    search_term = None

    command = args[0]
    if command not in accepted_commands:
        print 'Command not recognized'
        return False

    filename = args.pop()
    if command in ['lookup', 'reverse-lookup']:
        search_term = args[1]
    elif command in ['add', 'change']:
        name = args[1]
        number = args[2]
    elif command == 'remove':
        name = args[1]
    return filename, name, number, search_term


def handle_lookup(filename, search_term, phonebook):
    results = pb_lookup(search_term, phonebook)
    if len(results) > 0:
        print_results(results)
    else:
        print('No search results for %s' % (search_term))


def handle_add(name, number, filename, phonebook):
    if pb_add(name, number, phonebook):
        print('Added "%s %s to phonebook %s' % (name, number, filename))
        pb_save(filename, phonebook)
    else:
        print('A person called %s already in phonebook %s. Changes ignored.' %
              (name, filename))


def handle_change(name, number, filename, phonebook):
    if pb_change(name, number, phonebook):
        print('Change number for "%s" to "%s" in phonebook %s' %
              (name, number, filename))
        pb_save(filename, phonebook)
    else:
        print('No person called %s in phonebook %s. Changes ignored.' %
              (name, filename))


def handle_remove(name, filename, phonebook):
    if pb_remove(name, phonebook):
        print('Removed "%s" from phonebook %s' % (name, filename))
        pb_save(filename, phonebook)
    else:
        print('No person called %s in phonebook %s. Changes ignored.' %
              (name, filename))


def main():
    # get argumets, make sure the py file is not the first one.
    arguments = sys.argv
    if arguments[0] == 'phonebook.py':
        arguments.pop(0)
    command = arguments[0]
    filename, name, number, search_term = parse_arguments(arguments)

    if command == 'create':
        # create new phonebook file
        pb_create(filename)
    else:
        phonebook = pb_load(filename)
        if command == 'lookup':
            # phonebook lookup Sarah hsphonebook.pb
            # error message on no such phonebook
            handle_lookup(filename, search_term, phonebook)
        elif command == 'reverse-lookup':
            # phonebook reverse-lookup '312 432 5432' hsphonebook.pb
            print_results(pb_reverse_lookup(search_term, phonebook))
        elif command == 'add':
            handle_add(name, number, filename, phonebook)
        elif command == 'change':
            # phonebook change 'John Michael' '234 521 2332' hsphonebook.pb
            # error message on not exist
            handle_change(name, number, filename, phonebook)
        elif command == 'remove':
            # phonebook remove 'John Michael' hsphonebook.pb
            # error message on not exist
            handle_remove(name, filename, phonebook)


if __name__ == "__main__":
    main()

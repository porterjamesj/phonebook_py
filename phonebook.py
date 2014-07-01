#!/usr/bin/env python
import sys
import argparse
import os


def pb_parse_input_row(row):
    """parse one row from file input"""
    row = row.rstrip("\n")  # remove trailing newline
    name = "".join([c for c in row if not c.isdigit()]).strip()  # remove digits
    number = "".join([c for c in row if c.isdigit()])  # remove non-digits
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


def pb_lookup(query, pb):
    """find by text partial match to name string"""
    results = {}
    lowered_query = query.lower()
    for contact in pb:
        if lowered_query in contact.lower():
            results[contact] = pb[contact]
    return results


def pb_reverse_lookup(number, pb):
    """find by phone number (exact match)"""
    results = {}
    cannonical_num = "".join([c for c in number if c.isdigit()])
    for name, num in pb.iteritems():
        if num == cannonical_num:
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
    if name in pb:
        pb.pop(name)
        return True
    else:
        return False


parser = argparse.ArgumentParser(description="Manage those phonebooks.")
subparsers = parser.add_subparsers(dest="command")

create_parser = subparsers.add_parser("create", help="Create a new phonebook.")
create_parser.add_argument("name", help="name of the phonebook to create.")

lookup_parser = subparsers.add_parser("lookup",
                                      help="Lookup a person in a phonebook.")
lookup_parser.add_argument("name", help="name of person to lookup.")
lookup_parser.add_argument("phonebook", help="phonebook to look up in.")

add_parser = subparsers.add_parser("add",
                                   help="Add a new person to phonebook.")
add_parser.add_argument("name", help="name of person to add")
add_parser.add_argument("number", help="their number")
add_parser.add_argument("phonebook", help="phonebook to look up in.")

change_parser = subparsers.add_parser("change",
                                      help="Change someone's phone number.")
change_parser.add_argument("name", help="name of person whose number to change.")
change_parser.add_argument("number", help="new number")
change_parser.add_argument("phonebook", help="phonebook to change in.")

remove_parser = subparsers.add_parser("remove",
                                      help="Remove someone.")
remove_parser.add_argument("name", help="name of person to remove.")
remove_parser.add_argument("phonebook", help="phonebook to remove them from.")

rev_lookup_parser = subparsers.add_parser("reverse-lookup",
                                          help="Look someone up by number.")
rev_lookup_parser.add_argument("number", help="number of person to look up.")
rev_lookup_parser.add_argument("phonebook", help="phonebook to lookup in.")


def handle_lookup(search_term, phonebook):
    results = pb_lookup(search_term, phonebook)
    if results:
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
    args = parser.parse_args()  # uses sys.argv internally

    if args.command == 'create':
        # create new phonebook file
        pb_create(args.name)
    else:
        phonebook = pb_load(args.phonebook)
        if args.command == 'lookup':
            # phonebook lookup Sarah hsphonebook.pb
            # error message on no such phonebook
            handle_lookup(args.name, phonebook)
        elif args.command == 'reverse-lookup':
            # phonebook reverse-lookup '312 432 5432' hsphonebook.pb
            print_results(pb_reverse_lookup(args.number, phonebook))
        elif args.command == 'add':
            handle_add(args.name, args.number, args.phonebook, phonebook)
        elif args.command == 'change':
            # phonebook change 'John Michael' '234 521 2332' hsphonebook.pb
            # error message on not exist
            handle_change(args.name, args.number, args.phonebook, phonebook)
        elif args.command == 'remove':
            # phonebook remove 'John Michael' hsphonebook.pb
            # error message on not exist
            handle_remove(args.name, args.phonebook, phonebook)


if __name__ == "__main__":
    main()

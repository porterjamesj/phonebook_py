#!/usr/bin/env python
import argparse
import os

"""General Comments

There are a few more things here that I would do, but I think it's better
for you to do them for learning purposes :)

You're right that it would probably be good for all the pb_ functions
to be factored into a Phonebook class. Something else to pay attention
to here: Notice how the pb_ functions don't know anything about the
fact that they're being called from a command line client? They deal
only with manipulating the phonebook itself and don't know anything
about the frontend. They could just easily be used for a web frontend,
GUI app, etc. This is a good thing. Whenever I write a command line
application I try to pay attention to where this boundary falls and
make sure that I write a interface-agnostic core (in your case this
would be the Phonebook class) and then write a thin command line
wrapper around this (in your case this is the handle_*
functions). Often I actually pull these two halves out into separate
modules (files) just to make sure I don't cross that boundary and
couple the two.

Another thing: notice how there's a similar structure to many of the
handle_* functions? They do something, check if it worked, and then
maybe save the phonebook and print an appropriate message? There's
probably a way those could be factored out to avoid that duplication.
"""

# internal phonebook manipulation functions


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


# command line handler functions

def handle_rev_lookup(args):
    print_results(pb_reverse_lookup(args.number, args.phonebook))


def handle_lookup(args):
    results = pb_lookup(args.name, args.phonebook)
    if results:
        print_results(results)
    else:
        print('No search results for %s' % (args.name))


def handle_add(args):
    if pb_add(args.name, args.number, args.phonebook):
        print('Added "%s %s to phonebook %s' %
              (args.name, args.number, args.phone_file))
        pb_save(args.phone_file, args.phonebook)
    else:
        print('A person called %s already in phonebook %s. Changes ignored.' %
              (args.name, args.phone_file))


def handle_change(args):
    if pb_change(args.name, args.number, args.phonebook):
        print('Change number for "%s" to "%s" in phonebook %s' %
              (args.name, args.number, args.phone_file))
        pb_save(args.phone_file, args.phonebook)
    else:
        print('No person called %s in phonebook %s. Changes ignored.' %
              (args.name, args.phone_file))


def handle_remove(args):
    if pb_remove(args.name, args.phonebook):
        print('Removed "%s" from phonebook %s' % (args.name, args.phone_file))
        pb_save(args.phone_file, args.phonebook)
    else:
        print('No person called %s in phonebook %s. Changes ignored.' %
              (args.name, args.phone_file))


def handle_create(args):
    pb_create(args.name)


parser = argparse.ArgumentParser(description="Manage those phonebooks.")
subparsers = parser.add_subparsers(dest="command")

create_parser = subparsers.add_parser("create", help="Create a new phonebook.")
create_parser.add_argument("name", help="name of the phonebook to create.")
create_parser.set_defaults(func=handle_create)

lookup_parser = subparsers.add_parser("lookup",
                                      help="Lookup a person in a phonebook.")
lookup_parser.add_argument("name", help="name of person to lookup.")
lookup_parser.add_argument("phone_file", help="phonebook to look up in.")
lookup_parser.set_defaults(func=handle_lookup)

add_parser = subparsers.add_parser("add",
                                   help="Add a new person to phonebook.")
add_parser.add_argument("name", help="name of person to add")
add_parser.add_argument("number", help="their number")
add_parser.add_argument("phone_file", help="phonebook to look up in.")
add_parser.set_defaults(func=handle_add)

change_parser = subparsers.add_parser("change",
                                      help="Change someone's phone number.")
change_parser.add_argument("name", help="name of person whose number to change.")
change_parser.add_argument("number", help="new number")
change_parser.add_argument("phone_file", help="phonebook to change in.")
change_parser.set_defaults(func=handle_change)

remove_parser = subparsers.add_parser("remove",
                                      help="Remove someone.")
remove_parser.add_argument("name", help="name of person to remove.")
remove_parser.add_argument("phone_file", help="phonebook to remove them from.")
remove_parser.set_defaults(func=handle_remove)

rev_lookup_parser = subparsers.add_parser("reverse-lookup",
                                          help="Look someone up by number.")
rev_lookup_parser.add_argument("number", help="number of person to look up.")
rev_lookup_parser.add_argument("phone_file", help="phonebook to lookup in.")
rev_lookup_parser.set_defaults(func=handle_rev_lookup)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.command != "create":
        args.phonebook = pb_load(args.phone_file)
    args.func(args)

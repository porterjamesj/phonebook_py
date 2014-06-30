import sys
import re

# parse one row from file input
def pb_parse_input_row(row):
    name = re.sub('\d', '', row)    # remove digits
    name = name.replace('\n', '')
    number = re.sub('\D', '', row)  # remove non-digits
    return name.strip(), number

# parse output string from name & number
def pb_parse_output_row(name, number):
    return name + ' ' + number + '\n'

# parse all results (accepts list of key-value pairs)
def print_results(rows):
    for name, number in rows.iteritems():
        print pb_parse_output_row(name, number)

# load phonebook from file
def pb_load(filename):
    pb = {}
    file_obj = open(filename, 'r')
    for line in file_obj:
        name, number = pb_parse_input_row(line)
        pb[name] = number
    file_obj.close()
    return pb

# save phonebook to a file
def pb_save(filename, pb):
    file_obj = open(filename, 'w')
    for name, number in pb.iteritems():
        file_obj.write(pb_parse_output_row(name, number))
    file_obj.close()

# find by text partial match to name string
def pb_lookup(name_lookup, pb):
    results = {};
    search_name = name_lookup.lower()
    for name, num in pb.iteritems():
        if search_name in name.lower():
            results[name] = num
    return results

# find by phone number (exact match)
def pb_reverse_lookup(number, pb):
    results = {}
    num = re.sub('\D', '', number)
    for name, num in pb.iteritems():
        if num == number:
            results[name] = num
    return results

# check if row exists. Return false if already exists
def pb_add(name, number, pb):
    if name in pb: return False
    pb[name] = number
    return True

def pb_change(name, number, pb):
    if name in pb:
        pb[name] = number
        return True
    else:
        return False

# phonebook remove 'John Michael' hsphonebook.pb # error message on not exist
def pb_remove(name, pb):
    if (name in pb):
        pb.pop(name, None)
        return True
    else:
        return False


def main():
    phonebook = {}

    # get argumets, make sure the py file is not the first one.
    arguments = sys.argv
    if arguments[0] == 'phonebook.py': arguments.pop(0)
    cmd = arguments[0]

    if cmd == 'create':
        # create new phonebook file
        filename = arguments[1]
        pb_save(filename, {})
        print 'Created phonebook ' + filename + 'in current directory'
    elif cmd == 'lookup':
        # phonebook lookup Sarah hsphonebook.pb # error message on no such phonebook
        search_term = arguments[1]
        filename = arguments[2]
        phonebook = pb_load(filename)
        results = pb_lookup(search_term, phonebook)
        if results.length > 0:
            print_results(results)
        else:
            print 'No search results for ' + search_term
    elif cmd == 'reverse-lookup':
        # phonebook reverse-lookup '312 432 5432' hsphonebook.pb
        search_term = arguments[1]
        filename = arguments[2]
        phonebook = pb_load(filename)
        print_results(pb_reverse_lookup(search_term, phonebook))
    elif cmd == 'add':
        # add 'John Michael' '123 456 4323' hsphonebook.pb # error message on duplicate name
        name = arguments[1]
        number = arguments[2]
        filename = arguments[3]
        phonebook = pb_load(filename)
        if pb_add(name, number, phonebook) == True:
            print 'Added "' + name + ' ' + number + '" to phonebook ' + filename
            pb_save(filename, phonebook)
        else:
            print 'A person called ' + name + ' already in phonebook ' + filename + '. Changes ignored.'
    elif cmd == 'change':
        # phonebook change 'John Michael' '234 521 2332' hsphonebook.pb # error message on not exist
        name = arguments[1]
        number = arguments[2]
        filename = arguments[3]
        phonebook = pb_load(filename)
        if pb_change(name, number, phonebook) == True:
            print 'Change number for "' + name + '" to "' + number + '" in phonebook ' + filename
            pb_save(filename, phonebook)
        else:
            print 'No person called ' + name + ' in phonebook ' + filename + '. Changes ignored.'
    elif cmd == 'remove':
        name = arguments[1]
        filename = arguments[2]
        phonebook = pb_load(filename)
        if pb_remove(name, phonebook) == True:
            print 'Removed "' + name + '" from phonebook ' + filename
            pb_save(filename, phonebook)
        else:
            print 'No person called ' + name + ' in phonebook ' + filename + '. Changes ignored.'

        # phonebook remove 'John Michael' hsphonebook.pb # error message on not exist
    else:
        print 'Command not recognized'

main()
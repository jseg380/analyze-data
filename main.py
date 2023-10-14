from sys import argv
from os.path import isfile
import time
import unicodedata

def write_log(message):
    with open('analyze-data.log', 'a') as log:
        log.write(f'{message}\n')


def get_elements(line, separator):
    # If there are no strings then string.split works fine
    if '"' not in line:
        return line.split(separator)
    
    elements = []
    for part in line.split('"'):
        # The part is not a quoted string
        if part[0] == separator:
            elements.extend(part.split(separator)[1:])
        elif part[-1] == separator:
            elements.extend(part.split(separator)[:-1])
        else:
            elements.append(part)

    return elements


def read_file(file):
    customer_list = []
    separator = ','
    required_fields = ['street', 'zip', 'city', 
                       'last check-in date', 'company']

    with open(file, 'r') as f:
        # Read the header which contains the fields
        fields = f.readline().replace('\n', '').lower().split(separator)

        line = f.readline().replace('\n', '')
        while line != '':
            if line == separator * (len(fields) - 1):
                # Line is "empty", log it and continue processing the file
                write_log(f'Empty line: "{line}"')
                line = f.readline().replace('\n', '')
                continue

            elements = get_elements(line, separator)
            
            if len(elements) < len(fields):
                # The row contains less fields than it should, log it and continue
                write_log(f'Line with less fields than the header: "{line}"')
            else:
                customer = {}
                for i, value in enumerate(elements):
                    # If a required field is empty log it and continue processing
                    if fields[i].lower() in required_fields and value == '':
                        write_log(f'Required field {fields[i]} is empty in line: "{line}"')
                        break
                    customer[fields[i].lower()] = value

                if (len(customer) == len(fields)):
                    customer_list.append(customer)
            
            # Finally
            line = f.readline().replace('\n', '')

        return (fields, customer_list)

def sort_ascendent_date(customer_list):
    return sorted(
            customer_list, 
            key=lambda d: time.strptime(d['last check-in date'], '%d/%m/%Y'))

def sort_customer_names_list(customer_list):
    names_list = map(
            lambda d: d['first name'] + ' ' + d['last name'],
            customer_list)

    return sorted(
            names_list, 
            key=lambda w: ''.join(c for c in unicodedata.normalize('NFD', w)
                                  if unicodedata.category(c) != 'Mn'))

def sort_companies_jobs_list(customer_list):
    jobs_list = map(
            lambda d: d['job'],
            customer_list)

    return sorted(set(jobs_list))

def main():
    # The program accepts one file either passed as an argument or by inputing
    # when the program is started (in case it is called without arguments)
    input_file = None

    if len(argv) == 1:
        input_file = input('Name of the file with the data: ')
    else:
        input_file = argv[1]

    if not isfile(input_file):
        write_log(f'Could not open file "{input_file}"')
        raise FileNotFoundError()

    fields, customer_list = read_file(input_file)
    
    sorted_customer_list = sort_ascendent_date(customer_list)
    print(f'Customer with the earliest check in date: {sorted_customer_list[0]}')
    print(f'Customer with the latest check in date: {sorted_customer_list[-1]}')
    sorted_names_list = sort_customer_names_list(customer_list)
    print(f'List of customer\'s full names ordered alphabetically:')
    for i in sorted_names_list:
        print(i)
    sorted_jobs_list = sort_companies_jobs_list(customer_list)
    print(f'List of companies user\'s jobs ordered alphabetically:')
    for i in sorted_jobs_list:
        print(i)

if __name__ == '__main__':
    main()
else:
    write_log('Invalid call of analyze-data')

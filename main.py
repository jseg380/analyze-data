from sys import argv
from os.path import isfile

# The program accepts one file either passed as an argument or by inputing
# when the program is started (in case it is called without arguments)
input_file = None

if len(argv) == 1:
    input_file = input('Name of the file with the data: ')
else:
    input_file = argv[1]

if not isfile(input_file):
    raise FileNotFoundError()

import re
import sys

import numpy as np


def readTrodesExtractedDataFile(filename):
    '''Read extracted trodes binary.

    Parameters
    ----------
    filename : str

    Returns
    -------
    data_file : dict

    '''
    with open(filename, 'rb') as file:
        # Check if first line is start of settings block
        if file.readline().decode().strip() != '<Start settings>':
            raise Exception("Settings format not supported")
        fieldsText = dict()
        for line in file:
            # Read through block of settings
            line = line.decode().strip()
            # filling in fields dict
            if line != '<End settings>':
                settings_name, setting = line.split(': ')
                fieldsText[settings_name] = setting
            # End of settings block, signal end of fields
            else:
                break
        # Reads rest of file at once, using dtype format generated by parse_dtype()
        fieldsText['data'] = np.fromfile(
            file, dtype=parse_dtype(fieldsText['Fields']))
        return fieldsText


def parse_dtype(fieldstr):
    '''Parses last fields parameter (<time uint32><...>) as a single string
    Assumes it is formatted as <name number * type> or <name type>
    Returns: np.dtype
    '''
    # Returns np.dtype from field string
    sep = re.split('\s', re.sub(r"\>\<|\>|\<", ' ', fieldstr).strip())
    typearr = []

    # Every two elemets is fieldname followed by datatype
    for i in range(0, len(sep), 2):
        fieldname = sep[i]
        repeats = 1
        ftype = 'uint32'
        # Finds if a <num>* is included in datatype
        if '*' in sep[i + 1]:
            temptypes = re.split('\*', sep[i + 1])
            # Results in the correct assignment, whether str is num*dtype or dtype*num
            ftype = temptypes[temptypes[0].isdigit()]
            repeats = int(temptypes[temptypes[1].isdigit()])
        else:
            ftype = sep[i + 1]
        try:
            fieldtype = getattr(np, ftype)
        except AttributeError:
            print(ftype + " is not a valid field type.\n")
            sys.exit(1)
        else:
            typearr.append((str(fieldname), fieldtype, repeats))

    return np.dtype(typearr)


def write_trodes_extracted_datafile(filename, data_file):
    """Takes the dictionary created by `readTrodesExtractedDataFile` and writes
    it to a new binary file.

    Parameters
    ----------
    data_file : dict
    filename : str

    """
    with open(filename, 'wb') as file:
        file.write('<Start settings>\n'.encode())
        for key, value in data_file.items():
            if key != 'data':
                line = f'{key}: {value}\n'.encode()
                file.write(line)
        file.write('<End settings>\n'.encode())
        file.write(data_file['data'].tobytes())

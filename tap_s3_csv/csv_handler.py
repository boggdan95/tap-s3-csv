import codecs
import csv
import re

from tap_s3_csv.logger import LOGGER as logger

def generator_wrapper(reader):
    to_return = {}

    for row in reader:
        for key, value in row.items():
            if key is None:
                key = '_s3_extra'

            formatted_key = key

            # remove non-word, non-whitespace characters
            formatted_key = re.sub(r"[^\w\s]", ' ', formatted_key)

            # replace whitespace with underscores
            formatted_key = re.sub(r"\s+", ' ', formatted_key)

            to_return[formatted_key] = value

        yield to_return


def get_row_iterator(table_spec, file_handle):
    # we use a protected member of the s3 object, _raw_stream, here to create
    # a generator for data from the s3 file.
    # pylint: disable=protected-access
    if 'encoding' in table_spec:
        encoding = table_spec['encoding']
    else:
        encoding = 'utf-8'


    file_stream = codecs.iterdecode(
        file_handle._raw_stream, encoding=encoding)

    field_names = None
    delimiter = None

    if 'field_names' in table_spec:
        field_names = table_spec['field_names']
    if 'delimiter' in table_spec:
        delimiter = table_spec['delimiter']

    reader = csv.DictReader(file_stream, fieldnames=field_names, delimiter=delimiter)    
    
    doublequote = None
    quotechar = None
    quoting = None

    if 'doublequote' in table_spec:
        doublequote = table_spec['doublequote']
    if 'quotechar' in table_spec:
        quotechar = table_spec['quotechar']
    if 'quoting' in table_spec:
        quoting = table_spec['quoting']

    if doublequote != None and quotechar != None and quoting != None:
        if quoting == 'csv.QUOTE_NONE':
            reader = csv.DictReader(file_stream, fieldnames=field_names, delimiter=delimiter, doublequote=doublequote, quotechar=quotechar, quoting=csv.QUOTE_NONE)
        if quoting == 'csv.QUOTE_MINIMAL':
            reader = csv.DictReader(file_stream, fieldnames=field_names, delimiter=delimiter, doublequote=doublequote, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
        if quoting == 'csv.QUOTE_ALL':
            reader = csv.DictReader(file_stream, fieldnames=field_names, delimiter=delimiter, doublequote=doublequote, quotechar=quotechar, quoting=csv.QUOTE_ALL)
        if quoting == 'csv.QUOTE_NONNUMERIC':
            reader = csv.DictReader(file_stream, fieldnames=field_names, delimiter=delimiter, doublequote=doublequote, quotechar=quotechar, quoting=csv.QUOTE_NONNUMERIC)


    return generator_wrapper(reader)

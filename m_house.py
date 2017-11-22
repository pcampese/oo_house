#!/usr/bin/env python

# Import modules
import logging
import csv
import string
import locale   # For currency display


# Configure Logging
logger = logging.getLogger(__name__)

# Set the locale
locale.setlocale( locale.LC_ALL, '' )


class House:

    def __init__(self, raw_data=None):
        self.raw_data = raw_data    # Raw CSV data
        self.address = None     # The full address (i.e. 1 Main St, Town, MA, 12345)
        self.address_obj = Address()     # The full address (i.e. 1 Main St, Town, MA, 12345)
        self.sales = {}
        self.date = None
        self.price = None
        logger.debug('Initializing House')
        if (self.raw_data):
            self.validate_raw_data()
            self.parse_raw_data()

    def set_address(self, address):
        logger.debug('set_address: <{}>'.format(address))
        self.address = address

    def get_address(self):
        logger.debug('get_address: <{}>'.format(self.address))
        return self.address

    def set_address_obj(self, address_text):
        logger.debug('set_address_obj: <{}>'.format(address_text))
        # Would need to create functions for splitting up the text and putting
        # it into the Address object
        pass

    def set_date(self, date):
        logger.debug('set_date: <{}>'.format(date))
        self.date = date

    def get_date(self):
        logger.debug('get_date: <{}>'.format(self.date))
        return self.date

    def set_price(self, price):
        logger.debug('set_price: <{}>'.format(price))
        self.price = int(price)

    def get_price(self):
        logger.debug('get_price: <{}>'.format(self.price))
        return self.price

    def set_raw_data(self, raw_data):
        logger.debug('set_raw_data: <{}>'.format(raw_data))
        self.raw_data = raw_data

    def get_raw_data(self):
        logger.debug('get_raw_data: <{}>'.format(self.raw_data))
        return self.raw_data

    def get_all(self, formatting=True):
        all_data = []

        all_data.append(self.get_address())
        all_data.append(self.get_date())
        all_data.append(
            locale.currency(self.get_price(), grouping=True ))

        logger.debug('get_all: <{}>'.format(all_data))
        return all_data

    def validate_raw_data(self):
        logger.debug('validate_raw_data: START')

        # Is the data valid
        is_valid = True

        # Get the raw_data
        raw_data = self.get_raw_data()
        logger.debug('raw_data = <{}>'.format(raw_data))

        # There should be exactly 2 rows of data
        # row1 = header = [label1, label2, etc.]
        # row2 = data = [value1, value2, etc.]
        try:
            if len(raw_data) != 2:
                logger.error(
                    'The data provided needs exactly 2 rows:'' 1) Header 2) Data.')
                is_valid = False
        except:
            logger.error('The data provided is not a list.')

        # Check the header row
        try:
            if len(raw_data[0]) < 1:
                logger.error(
                    'The header row doesnt have enough entries')
                is_valid = False
        except:
            logger.error('The header row is not a list.')
            is_valid = False

        # Check the data row
        try:
            if len(raw_data[1]) < 1:
                logger.error(
                    'The data row doesnt have enough entries')
                is_valid = False
        except:
            logger.error('The data row is not a list.')
            is_valid = False

        logger.debug('validation result = <{}>'.format(is_valid))

        logger.debug('validate_raw_data: END')
        return is_valid


    def parse_raw_data(self):
        # Get the data
        (header, data) = self.get_raw_data()

        # Address
        street = string.capwords(data[header.index('ADDRESS')])
        city = string.capwords(data[header.index('CITY')])
        state = data[header.index('STATE')]
        zipcode = data[header.index('ZIP')]
        full_address = '{}, {}, {}, {}'.format(street, city, state, zipcode)
        self.set_address(full_address)

        # Sale Info
        self.set_date(data[header.index('SOLD DATE')])
        self.set_price(data[header.index('PRICE')])

        logger.debug('full_address = <{}>'.format(full_address))

class Address:

    def __init__(self):
        self.number = None
        self.street_name = None
        self.street_suffix = None
        self.unit = None
        self.city = None
        self.state = None
        self.zipcode = None
        self.county = None
        self.country = None
        logger.debug('Initializing Address')

    def set_number(self, number):
        logger.debug('set_number: <{}>'.format(number))
        self.number = number

    def get_number(self):
        logger.debug('get_number: <{}>'.format(self.number))
        return self.number


class CsvParser:

    def __init__(self, filename):
        self.filename = filename
        self.delimiter = ','
        self.csv_file_object = None
        self.csv_reader_object = None
        logger.debug('Initializing self with: filename = <{}>'.format(
            self.filename))

    def set_filename(self, filename):
        logger.debug('set_filename: <{}>'.format(filename))
        self.filename = filename

    def get_filename(self):
        logger.debug('get_filename: <{}>'.format(self.filename))
        return self.filename

    def set_delimiter(self, delimiter):
        logger.debug('set_delimiter: <{}>'.format(delimiter))
        self.delimiter = delimiter

    def get_delimiter(self):
        logger.debug('get_delimiter: <{}>'.format(self.delimiter))
        return self.delimiter

    def set_csv_file_object(self, csv_file_object):
        logger.debug('set_csv_file_object: <{}>'.format(csv_file_object))
        self.csv_file_object = csv_file_object

    def get_csv_file_object(self):
        logger.debug('get_csv_file_object: <{}>'.format(self.csv_file_object))
        return self.csv_file_object

    def set_csv_reader_object(self, csv_reader_object):
        logger.debug('set_csv_reader_object: <{}>'.format(csv_reader_object))
        self.csv_reader_object = csv_reader_object

    def get_csv_reader_object(self):
        logger.debug('get_csv_reader_object: <{}>'.format(self.csv_reader_object))
        return self.csv_reader_object

    # Open the csv file
    def open_csv(self):
        logger.debug('open_csv: START')

        f = self.get_filename()
        logger.debug('open_csv: filename=<{}>'.format(f))

        # Open the file, only if it's not already open
        if not self.get_csv_file_object():
            try:
                logger.debug('open_csv: opening <{}>'.format(f))
                csvfile = open(f, 'rb')
                self.set_csv_file_object(csvfile)
            except IOError as e:
                logger.error("IO Error({0}): {1}".format(e.errno, e.strerror))
        else:
            logger.debug('open_csv: "{}" is already open'.format(f))

        logger.debug('open_csv: END')


    # Close the csv file
    def close_csv(self):
        logger.debug('close_csv: START')

        f = self.get_filename()
        f_obj = self.get_csv_file_object()

        # Close it, if it's a file object
        if f_obj:
            logger.debug('close_csv: closing <{}>'.format(f))
            try:
                f_obj.close()
                self.set_csv_file_object(None)
            except IOError as e:
                logger.error("close_csv: IO Error({0}): {1}".format(
                    e.errno, e.strerror))
        else:
            logger.debug('close_csv: "{}" is already closed'.format(f))

        logger.debug('close_csv: END')


    # Print the entire csv file
    def read_csv(self):
        logger.debug('read_csv: START')

        # Make sure the file is open
        self.open_csv()

        # Get the File object
        f_obj = self.get_csv_file_object()

        # Create the CSV Reader object
        logger.debug('Opening CSV for reading')
        csv_reader = csv.reader(f_obj, delimiter=',')
        self.set_csv_reader_object(csv_reader)

        logger.debug('read_csv: END')


    # Print the entire csv file
    def print_csv(self):
        logger.debug('print_csv: START')

        # Open the file for reading
        self.read_csv()

        # Get the CSV Reader Object
        csv_reader = self.get_csv_reader_object()
        for row in csv_reader:
            print ', '.join(row)

        # Close the file
        self.close_csv()

        logger.debug('print_csv: END')


    # Convert to a list of 1-line csv's
    def split(self):
        logger.debug('split: START')

        # Open the file for reading
        self.read_csv()

        # Get the CSV Reader Object
        csv_reader = self.csv_reader_object

        # Get the header
        header = csv_reader.next()

        # Generate the mini-csvs
        mini_csv_list = []
        for row in csv_reader:
            mini_csv_list.append([header, row])

        # Close the file
        self.close_csv()

        logger.debug('split: END')
        return mini_csv_list
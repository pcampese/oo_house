#!/usr/bin/env python

# Import modules
import logging
import csv
import string
import collections

# Configure Logging
logger = logging.getLogger(__name__)


class House:

    def __init__(self, id=None):
        self.id = id    # instance variable unique to each instance
        self.address = None     # The full address (i.e. 1 Main St, Town, MA, 12345)
        self.address_obj = Address()     # The full address (i.e. 1 Main St, Town, MA, 12345)
        self.sales = {}
        self.sales_date = None
        self.sales_price = None
        logger.debug('Initializing self with: id = <{}>'.format(self.id))

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

    def set_sales_date(self, sales_date):
        logger.debug('set_sales_date: <{}>'.format(sales_date))
        self.sales_date = sales_date

    def get_sales_date(self):
        logger.debug('get_sales_date: <{}>'.format(self.sales_date))
        return self.sales_date

    def set_sales_price(self, sales_date):
        logger.debug('set_sales_price: <{}>'.format(sales_price))
        self.sales_price = sales_price

    def get_sales_price(self):
        logger.debug('get_sales_price: <{}>'.format(self.sales_price))
        return self.sales_price

    def get_all(self):
        all_data = []

        all_data.append(self.get_address())
        all_data.append(self.get_sales_date())
        all_data.append(self.get_sales_price())

        logger.debug('get_all: <{}>'.format(all_data))
        return all_data


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
        logger.debug('Initializing self')

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
        self.houses = []
        self.csv_file_object = None
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

    def set_houses(self, houses):
        logger.debug('set_houses: <{}>'.format(houses))
        self.houses = houses

    def get_houses(self):
        logger.debug('get_houses: <{}>'.format(self.houses))
        return self.houses

    def set_csv_file_object(self, csv_file_object):
        logger.debug('set_csv_file_object: <{}>'.format(csv_file_object))
        self.csv_file_object = csv_file_object

    def get_csv_file_object(self):
        logger.debug('get_csv_file_object: <{}>'.format(self.csv_file_object))
        return self.csv_file_object

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
    def print_csv(self):
        logger.debug('print_csv: START')

        # Make sure the file is open
        self.open_csv()

        # Get the File object
        f_obj = self.get_csv_file_object()

        logger.debug('print_csv...')
        csv_reader = csv.reader(f_obj, delimiter=',')
        for row in csv_reader:
            print ', '.join(row)

        # Close the file
        self.close_csv()

        logger.debug('print_csv: END')



def process_csv(csv_file_object):
    logger.debug('process_csv: START')
    # list = process_header()
    #    return a list:
    #    index 0 == row 0 title,
    #    index 1 == row 1 title,
    #    etc.}
    # for row in csv_file:
    #    create

    # Determine the dialect
    dialect = get_dialect(csv_file_object)

    # Create a csv reader object
    csv_reader = csv.reader(csv_file_object)

    # Process the header row
    header_list = process_header(csv_reader)
    address_index = header_list.index('ADDRESS')

    # Create a list of houses
    houses = []

    # Create a house for each object
    for row in csv_reader:
        logger.debug('row = <{}>'.format(row))
        h = House()
        h.set_address(row[address_index])
        houses.append(h)
    logger.debug('process_csv: END')

    return houses


def process_header(csv_file_object):
    logger.debug('process_header: START')

    # Read the first line of the csv file
    header_list = csv_file_object.next()

    logger.debug('header_list = <{}>'.format(header_list))

    logger.debug('process_header: END')
    return header_list

# Determine the dialect.
# This does not work with redfin CSV data.  It sets delimiter=':'
def get_dialect(csv_file_object):
    logger.debug('get_dialect: START')
    # Create Sniffer object
    sniffer = csv.Sniffer()

    # Read in some data
    data_sample = csv_file_object.read(1024)

    # Determine the dialect
    dialect = sniffer.sniff(data_sample)

    # Rewind the file
    csv_file_object.seek(0)

    logger.debug('dialect.delimiter = <{}>'.format(dialect.delimiter))

    logger.debug('get_dialect: END')
    return dialect
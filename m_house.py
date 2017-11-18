#!/usr/bin/env python

# Import modules
import logging
import csv
import string
import collections

# Configure Logging
logger = logging.getLogger(__name__)


class House:

    def __init__(self, id):
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

    def set_number(self, number):
        logger.debug('set_number: <{}>'.format(number))
        self.number = number

    def get_number(self):
        logger.debug('get_number: <{}>'.format(self.number))
        return self.number


# Read in a csv file
def read_csv(filename):
    logger.debug('read_csv: <{}>'.format(filename))
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            print ', '.join(row)

# Read in a csv file
def read_csv2(filename):
    logger.debug('read_csv: <{}>'.format(filename))
    with open(filename, 'rb') as csvfile:
        process_csv(csvfile)

def process_csv(csv_file_object):
    # list = process_header()
    #    return a list:
    #    index 0 == row 0 title,
    #    index 1 == row 1 title,
    #    etc.}
    # for row in csv_file:
    #    create

    header_list = process_header2(csv_file_object)
    header_list = process_header2(csv_file_object)



def process_header(csv_file_object):
    # Return the header_list
    header_list = None      # Default value

    # Read the first line of the csv file
    first_line = csv_file_object.readline()

    # Go back to the beginning of the file
    # csv_file_object.seek(0)

    # If if the first line is a header, then make it a list
    if (csv.Sniffer().has_header(first_line)):
        logging.debug('csv file has a header')
        header_list = string.split(first_line, ',')
    else:
        logging.debug('csv file does not have header')

    logging.debug('header_list = <{}>'.format(header_list))

    return header_list

def process_header2(csv_file_object):
    # Return the header_list
    header_list = None      # Default value

    # Read the first line of the csv file
    first_line = csv_file_object.read(1024)

    # Go back to the beginning of the file
    # csv_file_object.seek(0)

    # If if the first line is a header, then make it a list
    if (csv.Sniffer().has_header(first_line)):
        logging.debug('csv file has a header')
        header_list = string.split(first_line, ',')
    else:
        logging.debug('csv file does not have header')

    logging.debug('header_list = <{}>'.format(header_list))

    return header_list
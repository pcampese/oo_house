#!/usr/bin/env python

# Import modules
import logging
import csv
import string
import locale   # For currency display
import numpy    # For math
from scipy import stats    # For science!
from datetime import date
from time import strptime

# Configure Logging
logger = logging.getLogger(__name__)

# Set the locale
locale.setlocale( locale.LC_ALL, '' )

class Redfin:

    def __init__(self, city='natick'):
        self.city = city
        self.max_homes = 999999
        self.region_id = {
            'arlington':    29773,
            'natick':       29757,
            'newton':       11619,}

    def generate_url(self):
        logger.debug('generate_link')

        url = ('https://www.redfin.com/stingray/api/gis-csv?al=3&'
                    'market=boston&'
                    'num_homes={}&'
                    'ord=dollars-per-sq-ft-asc&'
                    'page_number=1&'
                    'region_id={}&'
                    'region_type=6&'
                    'sold_within_days=36500&'
                    'sp=true&status=9&'
                    'uipt=1,2,3,4,5,6&'
                    'v=8'.format(
                        self.max_homes,
                        self.region_id[string.lower(self.city)]))

        return url


class Analysis:

    def __init__(self, dataset_dict):
        self.dataset_dict = dataset_dict
        self.validate()
        self.selection = self.dataset_dict.keys()

    def validate(self):
        logger.debug('validate')
        if self.dataset_dict:
            try:
                for (key, value) in self.dataset_dict.iteritems():
                    logger.debug('key: <{}> | value = <{}>'.format(key, value))
            except:
                logger.error('argument must be a dictionary')

    def history_chart(self, start_year=None, end_year=None):
        logger.debug('history_chart')

        for name in self.selection:
            title1 = string.capwords(name)
            title2 = '{} to {}'.format(start_year, end_year)
            logger.info('| {:-^42} |'.format('-'))
            logger.info('| {:^42} |'.format(title1))
            logger.info('| {:^42} |'.format(title2))
            logger.info('| {:-^42} |'.format('-'))
            logger.info('| {:^6} | {:^15} | {:^15} |'.format('Year', 'Average', 'Median'))
            logger.info('| {:-^6} | {:-^15} | {:-^15} |'.format('-', '-', '-'))
            for year in range(start_year,end_year+1):
                self.dataset_dict[name].filters['year'] = year
                self.dataset_dict[name].apply_filters()
                logger.info('| {:<6} | {:<15} | {:<15} |'.format(
                    year,
                    locale.currency(self.dataset_dict[name].average_price(), grouping=True),
                    locale.currency(self.dataset_dict[name].median_price(), grouping=True)))

                # Clear the time filter
                self.dataset_dict[name].filters['year'] = None
            logger.info('| {:-^6} | {:-^15} | {:-^15} |'.format('-', '-', '-'))

    def time_chart(self, units, start, end):
        logger.debug('time_chart')

        # Generate list of valid time units
        #   self.selection[0] == 1st key from dataset_dict
        #   self.dataset_dict[...] == the dataset indicated by that 1st key
        #   .filters.keys() == List of filter keys for that dataset
        valid_units = self.dataset_dict[self.selection[0]].filters.keys()
        if units not in valid_units:
            logger.error('{} not valid.  Should be one of {}'.format(
                units, valid_units))

        units_cap = string.capwords(units)

        for name in self.selection:
            title1 = string.capwords(name)
            title2 = '{} to {}'.format(start, end)
            logger.info('| {:-^42} |'.format('-'))
            logger.info('| {:^42} |'.format(title1))
            logger.info('| {:^42} |'.format(title2))
            logger.info('| {:-^42} |'.format('-'))
            logger.info('| {:^6} | {:^15} | {:^15} |'.format(
                units_cap, 'Average', 'Median'))
            logger.info('| {:-^6} | {:-^15} | {:-^15} |'.format('-', '-', '-'))
            for time in range(start,end+1):
                self.dataset_dict[name].filters[units] = time
                self.dataset_dict[name].apply_filters()
                logger.info('| {:<6} | {:<15} | {:<15} |'.format(
                    time,
                    locale.currency(self.dataset_dict[name].average_price(),
                                    grouping=True),
                    locale.currency(self.dataset_dict[name].median_price(),
                                    grouping=True)))

                # Clear the time filter
                self.dataset_dict[name].filters[units] = None
            logger.info('| {:-^6} | {:-^15} | {:-^15} |'.format('-', '-', '-'))

    def time_chart_percentile(self, units, start, end):
        logger.debug('time_chart_percentile')

        # Generate list of valid time units
        #   self.selection[0] == 1st key from dataset_dict
        #   self.dataset_dict[...] == the dataset indicated by that 1st key
        #   .filters.keys() == List of filter keys for that dataset
        valid_units = self.dataset_dict[self.selection[0]].filters.keys()
        if units not in valid_units:
            logger.error('{} not valid.  Should be one of {}'.format(
                units, valid_units))

        units_cap = string.capwords(units)

        percentiles = [5, 10, 20, 25, 50, 75, 80]

        for name in self.selection:
            # Format the calculated data
            formatted_data = []
            column_width = 0

            for time in range(start,end+1):
                self.dataset_dict[name].filters[units] = time
                self.dataset_dict[name].apply_filters()

                # Dynamic width based on the percentiles provided
                formatted_row = '| {:<6} |'.format(time)
                for p in percentiles:
                    price, count = self.dataset_dict[name].percentile_price(p)

                    # Count number of homes that are within this percentile
                    self.dataset_dict[name].save_filters()
                    self.dataset_dict[name].filters['max_price'] = price
                    self.dataset_dict[name].apply_filters()
                    count = len(self.dataset_dict[name].get_prices())
                    self.dataset_dict[name].restore_filters()
                    self.dataset_dict[name].apply_filters()

                    column = (' {:<15} ({:3}) |'.format(
                        locale.currency(price,
                                        grouping=True),
                        count))
                    column_width = len(column)-3    # Get column width
                    formatted_row += column
                formatted_data.append(formatted_row)

            # Format the minor headings
            formatted_minor = '| {:^6} |'.format(units_cap)
            formatted_divider = '| {:-^6} |'.format('-')
            for p in percentiles:
                formatted_p = '{}%'.format(p)
                formatted_minor += ' {:^{}} |'.format(formatted_p, column_width)

                formatted_divider += ' {:-^{}} |'.format('-', column_width)

            # Get the row width
            row_width = len(formatted_data[0])-4

            # Format and print the major headings
            title1 = string.capwords(name)
            title2 = '{} to {}'.format(start, end)
            title3 = 'Percentile'
            logger.info('| {:-^{}} |'.format('-', row_width))
            logger.info('| {:^{}} |'.format(title1, row_width))
            logger.info('| {:^{}} |'.format(title2, row_width))
            logger.info('| {:^{}} |'.format(title3, row_width))
            logger.info('| {:-^{}} |'.format('-', row_width))

            # Print the minor headings
            logger.info(formatted_minor)
            logger.info(formatted_divider)

            # Print the data
            for row in formatted_data:
                logger.info(row)

            logger.info(formatted_divider)

            # Clear the time filter
            self.dataset_dict[name].filters[units] = None


class Dataset:

    def __init__(self, house_list=None):
        self.house_list = house_list
        self.house_list_filtered = house_list
        self.filters = None
        self.filters_default = {    # We can filter by this
            'min_price': 0,
            'max_price': 999999999,
            'beds': None,
            'baths': None,
            'month': None,
            'year': None,}
        self.filters_stack = []
        self.clear_filters()    # Assign the default filters

    def save_filters(self):
        self.filters_stack.append(self.filters.copy())

    def restore_filters(self):
        self.filters = self.filters_stack.pop()

    def clear_filters(self):
        logger.debug('clear_filters')
        self.filters = self.filters_default.copy()

    def apply_filters(self):
        logger.debug('apply_filters')
        logger.debug('Filters: <{}>'.format(self.filters))

        # Clear the filtered list
        self.house_list_filtered = []

        # Apply the filters and populate the filtered list
        for house in self.house_list:
            logger.debug('Filtering against this address now: <{}>'.format(
                house.address))
            logger.debug('House Price: <{}>'.format(house.price))

            # Price
            if (house.price >= self.filters['min_price'] and
                house.price <= self.filters['max_price']):
                logger.debug('Included: Price')
            else:
                logger.debug('Excluded: Price')
                continue

            # Year
            logger.debug('Date = <{}>'.format(house.date_obj))
            if self.filters['year']:
                if house.date_obj:
                    if (house.date_obj.year == self.filters['year']):
                        logger.debug('Included: Year')
                    else:
                        logger.debug('Excluded: Year')
                        continue
                else:
                    logger.debug('Excluded: No Date')
                    continue

            # Month
            logger.debug('Date = <{}>'.format(house.date_obj))
            if self.filters['month']:
                if house.date_obj:
                    if (house.date_obj.month == self.filters['month']):
                        logger.debug('Included: Year')
                    else:
                        logger.debug('Excluded: Year')
                        continue
                else:
                    logger.debug('Excluded: No Date')
                    continue

            # Beds
            logger.debug('Beds = <{}>'.format(house.beds))
            if self.filters['beds']:
                if house.beds:
                    if (house.beds >= self.filters['beds']):
                        logger.debug('Included: Beds')
                    else:
                        logger.debug('Excluded: Beds')
                        continue
                else:
                    logger.debug('Excluded: No Beds')
                    continue

            # Baths
            logger.debug('Baths = <{}>'.format(house.baths))
            if self.filters['baths']:
                if house.baths:
                    if (house.baths >= self.filters['baths']):
                        logger.debug('Included: Baths')
                    else:
                        logger.debug('Excluded: Baths')
                        continue
                else:
                    logger.debug('Excluded: No Baths')
                    continue

            # It passed all filters, so add it to the list
            logger.debug('Add to filtered list')
            self.house_list_filtered.append(house)
            logger.debug('len(house_list_filtered)=<{}>'.format(
                len(self.house_list_filtered)))

    def std_deviation(self, conf=0.68):
        logger.debug('std_deviation')
        logger.debug('list=<{}>, conf=<{}>'.format(self.get_prices(), conf))
        mean = numpy.mean(self.get_prices())
        logger.debug('mean=<{}>'.format(mean))

        sigma = numpy.std(self.get_prices())
        logger.debug('sigma=<{}>'.format(sigma))

        return stats.norm.interval(conf, loc=mean, scale=sigma)

    def print_average_price(self):
        logger.info('Average Price: {}'.format(
            locale.currency(self.average_price(), grouping=True)))

    def print_median_price(self):
        logger.info('Median Price: {}'.format(
            locale.currency(self.median_price(), grouping=True)))

    def print_percentile_price(self):
        percentiles = [25, 50, 75]

        for p in percentiles:
            logger.info('Percentile Price ({}%): {}'.format(
                p,
                locale.currency(self.percentile_price(p),
                                grouping=True)))

    def average_price(self):
        logger.debug('average_price')

        average = 0
        price_list = self.get_prices()
        if len(self.get_prices()) > 0:
            average = numpy.average(price_list)

        price_list_count = len(price_list)

        return (average, price_list_count)

    def median_price(self):
        logger.debug('median_price')

        median = 0
        price_list = self.get_prices()
        if len(self.get_prices()) > 0:
            median = numpy.median(price_list)

        price_list_count = len(price_list)

        return (median, price_list_count)

    def percentile_price(self, percentile=None):
        logger.debug('percentile_price')

        if not percentile:
            percentile = 50      # The default percentile
        percentiles_results = 0
        price_list = self.get_prices()

        if len(self.get_prices()) > 0:
            percentiles_results = numpy.percentile(price_list, percentile)

        price_list_count = len(price_list)

        return (percentiles_results, price_list_count)

    def get_prices(self):
        price_list = []

        for house in self.house_list_filtered:
            price_list.append(house.price)

        return price_list

    def print_all(self):
        for house in self.house_list_filtered:
            logger.info('house_details = <{}>'.format(house.get_all()))


class House:

    def __init__(self, raw_data=None):
        self.raw_data = raw_data    # Raw CSV data
        self.address = None     # The full address (i.e. 1 Main St, Town, MA, 12345)
        self.address_obj = Address()     # The full address (i.e. 1 Main St, Town, MA, 12345)
        self.sales = {}
        self.sale_date = None
        self.date_obj = None
        self.price = None
        self.beds = None
        self.baths = None
        logger.debug('Initializing House')
        if (self.raw_data):
            self.validate_raw_data()
            self.parse_raw_data()
        if self.sale_date:
            self.set_date()

    def set_date(self):
        month_name, day, year = self.sale_date.split('-')
        month_num = strptime(
            month_name,
            '%B').tm_mon

        self.date_obj = date(
            int(year),
            month_num,
            int(day))

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

    def set_price(self, price):
        logger.debug('set_price: <{}>'.format(price))
        self.price = int(price)

    def set_beds(self, beds):
        logger.debug('set_beds: <{}>'.format(beds))
        if beds:
            self.beds = int(beds)

    def set_baths(self, baths):
        logger.debug('set_baths: <{}>'.format(baths))
        if baths:
            self.baths = float(baths)

    def get_all(self, formatting=True):
        all_data = []

        all_data.append(self.get_address())
        all_data.append(self.sale_date)
        all_data.append(
            locale.currency(self.price, grouping=True))

        logger.debug('get_all: <{}>'.format(all_data))
        return all_data

    def validate_raw_data(self):
        logger.debug('validate_raw_data: START')

        # Is the data valid
        is_valid = True

        # Get the raw_data
        raw_data = self.raw_data
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
        (header, data) = self.raw_data

        # Address
        street = string.capwords(data[header.index('ADDRESS')])
        city = string.capwords(data[header.index('CITY')])
        state = data[header.index('STATE')]
        zipcode = data[header.index('ZIP')]
        full_address = '{}, {}, {}, {}'.format(street, city, state, zipcode)
        self.set_address(full_address)

        # Sale Info
        self.sale_date = data[header.index('SOLD DATE')]
        self.set_price(data[header.index('PRICE')])

        # Bedroom and Bathroom count
        self.set_beds(data[header.index('BEDS')])
        self.set_baths(data[header.index('BATHS')])

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

    # Open the csv file
    def open(self):
        logger.debug('open: START')

        f = self.filename
        logger.debug('open: filename=<{}>'.format(f))

        # Open the file, only if it's not already open
        if not self.csv_file_object:
            try:
                logger.debug('open: opening <{}>'.format(f))
                csvfile = open(f, 'rb')
                self.csv_file_object = csvfile
            except IOError as e:
                logger.error("IO Error({0}): {1}".format(e.errno, e.strerror))
        else:
            logger.debug('open: "{}" is already open'.format(f))

        logger.debug('open: END')


    # Close the csv file
    def close(self):
        logger.debug('close: START')

        f = self.filename
        f_obj = self.csv_file_object

        # Close it, if it's a file object
        if f_obj:
            logger.debug('close: closing <{}>'.format(f))
            try:
                f_obj.close()
                self.csv_file_object = None
            except IOError as e:
                logger.error("close: IO Error({0}): {1}".format(
                    e.errno, e.strerror))
        else:
            logger.debug('close: "{}" is already closed'.format(f))

        logger.debug('close: END')


    # Read the entire csv file
    def read(self):
        logger.debug('read: START')

        # Make sure the file is open
        self.open()

        # Get the File object
        f_obj = self.csv_file_object

        # Create the CSV Reader object
        logger.debug('Opening CSV for reading')
        csv_reader = csv.reader(f_obj, delimiter=',')
        self.csv_reader_object = csv_reader

        logger.debug('read: END')


    # Show the entire csv file
    def show(self):
        logger.debug('show: START')

        # Open the file for reading
        self.read()

        # Get the CSV Reader Object
        csv_reader = self.csv_reader_object
        for row in csv_reader:
            print ', '.join(row)

        # Close the file
        self.close()

        logger.debug('show: END')


    # Convert to a list of 1-line csv's
    def split(self):
        logger.debug('split: START')

        # Open the file for reading
        self.read()

        # Get the CSV Reader Object
        csv_reader = self.csv_reader_object

        # Get the header
        header = csv_reader.next()

        # Generate the mini-csvs
        mini_csv_list = []
        for row in csv_reader:
            mini_csv_list.append([header, row])

        # Close the file
        self.close()

        logger.debug('split: END')
        return mini_csv_list
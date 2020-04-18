'''Script to convert inventory from ncr to shopkeep

Script to convert a directory of ncr inventory snapshopt csv files into a csv
for import into shopkeep.
'''

import argparse
import csv
import glob
import sys

SHOPKEEP_FIELDS = [
    'Item UUID',
    'Name',
    'Department',
    'Category',
    'UPC',
    'Store Code (SKU)',
    'Price',
    'Discountable',
    'Taxable',
    'Tracking Inventory',
    'Cost',
    'Assigned Cost',
    'Quantity',
    'Reorder Trigger',
    'Recommended Order',
    'Last Sold Date',
    'Supplier',
    'Liability Item',
    'Liability Redemption Tender',
    'Tax Rate'
]
# Map shopkeep fields to ncr fields
INVENTORY_MAP = {
    'Name': 'Item Name',
    'UPC': 'Barcode',
    'Supplier': 'Vendor',
    'Cost': 'Unit Cost',
    'Price': 'Unit Price',
    'Quantity': 'Qty On Hand (Units)'
}


def fix_barcode(barcode):
    '''For shopkeep barcode/UPC a length of 8 12 or 13
    '''
    barcode_length = len(barcode)
    if 0 < barcode_length < 8:
        difference = 8 - barcode_length
        return '0' * difference + barcode
    if 8 < barcode_length < 12:
        difference = 12 - barcode_length
        return '0' * difference + barcode
    return barcode


def fix_category(ncr_category):
    '''This is specific for the inventory that is being moved.

    Args:
        ncr_category: category from ncr point of sale

    Returns:
        {
            'category': <some category>
            'department': <some department>
        }

    The ncr system only had categories where shopkeep has both categories and
    departments. Also the ncr system had a maximum length of string and this
    function converts the shortened strings
    '''

    category = ncr_category
    department = ''

    wines = [
        'Argentina',
        'Australia',
        'California',
        'Chile',
        'France',
        'Germany',
        'Glogg',
        'Mexico',
        'Italy',
        'New York',
        'NewZealand',
        'Oregon',
        'Portugal',
        'South Afri',
        'Spain',
        'Texas',
        'Washington',
        'Mead',
        'Marsala',
        'Sherry'
    ]

    if ncr_category in wines:
        department = 'wine'
        if ncr_category == 'NewZealand':
            category = 'New Zealand'
        if ncr_category == 'South Afri':
            category = 'South Africa'

    liqours = [
        'Am Whiskey',
        'Bourbon',
        'Brandy',
        'CAN Whisky',
        'Cognac',
        'Everclear',
        'Gin',
        'IrishCream',
        'IrishWhisk',
        'JapanWhisk',
        'Liqueur',
        'Mezcal',
        'Moonshine',
        'Pisco',
        'Rum',
        'Rye',
        'Schnapps',
        'Scotch',
        'Sotol',
        'Tequila',
        'Vodka',
        'Vermouth',
        'Apertif'
    ]

    if ncr_category in liqours:
        department = 'Liquor'
        if ncr_category == 'Am Whiskey':
            category = 'American Whiskey'
        if ncr_category == 'CAN Whisky':
            category = 'Canadian Whiskey'
        if ncr_category == 'IrishCream':
            category = 'Irish Cream'
        if ncr_category == 'IrishWhisk':
            category = 'Irish Whiskey'
        if ncr_category == 'JapanWhisk':
            category = 'Japanese Whiskey'

    if ncr_category == 'Sake':
        department = 'Sake'
    if ncr_category == 'Beer':
        department = 'Beer'
    if ncr_category == 'Cider':
        department = 'Cider'
    if ncr_category == 'Bubbles':
        department = 'Bubbles'
    if ncr_category == 'HardSeltzr':
        category = 'Hard Seltzer'
        department = 'Hard Seltzer'
    if ncr_category == 'RTD':
        department = 'RTD'
    if ncr_category == 'Bar Stuff':
        department = 'Bar Accessories'
    if ncr_category == 'Kombucha':
        department = 'Hard Kombucha'

    tobaccos = ['Cigar', 'Cigarettes']

    if ncr_category in tobaccos:
        department = 'Tobacco'

    non_alcoholic_beverages = ['Nonalcohol', 'Mixer']
    if ncr_category in non_alcoholic_beverages:
        department = 'Non Alcoholic Beverages'

    groceries = ['Gift Bag', 'Grocery', 'J/SpiceOil', 'Lighter']
    if ncr_category in groceries:
        department = 'Grocery'

    return {'department': department, 'category': category}


def main(directory):
    '''The main function make pylint ignore this'''
    out_writer = csv.DictWriter(sys.stdout, fieldnames=SHOPKEEP_FIELDS)
    out_writer.writeheader()
    files = glob.glob(directory + '/*.csv')
    for filename in files:
        with open(filename) as in_csv:
            in_reader = csv.DictReader(in_csv)
            for row in in_reader:
                real_barcode = fix_barcode(row[INVENTORY_MAP['UPC']])
                result = fix_category(row['Category'])
                out_dict = dict()
                out_dict['Name'] = row[INVENTORY_MAP['Name']]
                # out_dict['UPC'] = row[INVENTORY_MAP['UPC']]
                out_dict['UPC'] = real_barcode
                out_dict['Quantity'] = row[INVENTORY_MAP['Quantity']]
                out_dict['Supplier'] = row[INVENTORY_MAP['Supplier']]
                out_dict['Cost'] = row[INVENTORY_MAP['Cost']]
                out_dict['Price'] = row[INVENTORY_MAP['Price']]
                out_dict['Department'] = result['department']
                out_dict['Category'] = result['category']
                out_writer.writerow(out_dict)


if __name__ == '__main__':
    DESCRIPTION = '''
Script to convert a directory of ncr inventory snapshopt csv files into a csv
for import into shopkeep.
'''
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('directory', help='directory of csv files to convert')
    args = parser.parse_args()
    main(args.directory)

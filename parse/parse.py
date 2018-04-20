#!/usr/bin/python

import sys
import csv
### Robust Parser ###

"""Assumption 1: File is a csvFile in a readable format - see ASCII/utf8 formatting for details."""

"""Takes in CSV files as arguments, as many as you would like and processing them into individual tables."""
def main():
	for csvFileName in sys.argv[1:]:
		with open(csvFileName, 'r') as csvFile:
			rowReader = csv.reader(csvFile, delimiter=' ', quotechar='|')
			#Assumption 2: First row is the schema for the table: use this schema to build a table
			schema = next(rowReader)
			print(type(schema))
			print(', '.join(schema))



if __name__ == "__main__":
	main()


"""Takes in particular feature title to build schema for the template column."""
def parse_columns():
	return None

"""Opens the CSV file. """



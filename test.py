#!/usr/bin/python
from db_helper import MyDB

db = MyDB('localhost', 'root', '', 'test')

def main():
	show_version()
	get_names()

	for row in db.get_inputs_status():
		print 'Name:', row[0]
		print 'Status:', row[1]

def show_version():
	db.show_version()

def get_names():
	db.test1()
	db.test2()

if __name__ == '__main__':  # If it's executed like a script (not imported)
	main()
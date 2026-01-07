from models import Base, session, Product, engine, inspect, text
import pandas as pd
import os
import sqlite3
import datetime
import csv
import time

def menu():
	while True:
		print('''
			\nStore Products
			\rV) View a Product
			\rA) Add New Product
			\rB) Backup the DB
			\rZ) Exit
			\n''')
		choice = input('What would you like to do? ')
		if choice.upper() in ['V', 'A', 'B', 'Z']:
			return choice.upper()
		else:
			input('''
				\rPlease choose one of the options
				\rV, A, B, Z
				\rPress enter to try again 
				\n''')


def clean_price(price_str):
	try:
		clean_str = price_str.strip().replace('$', '')

		price_float = float(clean_str)

		return_price = int(price_float * 100)

	except ValueError:
		input('''
			\n***** Price Error ****
			\r Price Format should be a number
			\rEx: 10.99 or $10.99
			\rPress enter to try again
			\r************************
			''')
		return
	else:
		return return_price


def clean_date(date_str):

	split_date = date_str.split('/')

	try:
		if len(split_date) != 3:
			raise ValueError

		month = int(split_date[0])
		day = int(split_date[1])
		year = int(split_date[2])

		return_date = datetime.date(year, month, day)

	except ValueError:
		input('''
			\n***** Date Error ****
			\r Date format should include a valid month, day, year
			\rEx: 11/1/2018
			\rPress enter to try again
			\r************************
			''')
		return
	else:
		return return_date

def clean_quantity(quantity_str):
	try:
		quantity = int(quantity_str)
		return quantity
	except ValueError:
		print('That is not a valid number!')

def add_csv():
	with open("inventory.csv") as csvfile:
		data = csv.reader(csvfile)
		next(data)

		for row in data:

			product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()

			if product_in_db == None:
				#need to make functinos to clean
				name = row[0].strip()
				price = clean_price(row[1])
				quantity = row[2]
				date = clean_date(row[3])

				new_product = Product(product_name=name, product_quantity=quantity, product_price=price, date_updated=date)
				session.add(new_product)

		session.commit()

def backup_csv():
	#backup .db into .csv


def view_product():
	id_options = []

	for product in session.query(Product):
		id_options.append(product.product_id)
		print(f'\n{product.product_id} | {product.product_name}')

	while True:

		try:
			id_choice = int(input("Which Id would you like to view: "))

			if id_choice in id_options:
				break
			else:
				print('Id not found please enter a valid id.')

		except ValueError:
			print('Invalid input. Please enter a number for the ID')

	the_product = session.query(Product).filter(Product.product_id == id_choice).first()

	print(f'''
		\n ID: {the_product.product_id}
		\r Name: {the_product.product_name}
		\r Quantity: {the_product.product_quantity}
		\r Price: {the_product.product_price / 100}
		\r Last Updated: {the_product.date_updated}
		\n
		''')


def app():
	app_running = True

	while app_running:
		choice = menu()

		if choice == 'V':
			# view a product
			view_product()
			input('\nPress enter to return to main menu.')

		elif choice == 'A':
			# add new product
			# {self.product_name}, Quantity: {self.product_quantity}, 
			# Price: {self.product_price}, Updated: {self.date_updated}
			name = input('Product Name: ')

			quantity_error = True
			while quantity_error:
				quantity = input('Quantity (EX: 28): ')
				quantity = clean_quantity(quantity)
				if type(quantity) == int:
					quantity_error = False

			price_error = True
			while price_error:
				price = input('Price (Ex: 10.99): ')
				price = clean_price(price)
				if type(price) == int:
					price_error = False

			date_error = True
			while date_error:
				date = input('Date Published (Ex: 12/28/2018 - M/D/Y): ')
				date = clean_date(date)
				if type(date) == datetime.date:
					date_error = False

			new_product = Product(product_name=name, product_quantity=quantity, product_price=price, date_updated=date)
			print(new_product)

			session.add(new_product)
			session.commit()

			print('Product Added!')
			time.sleep(1.5)


		elif choice == 'B':

			backup_csv():
			input('Press enter to return to menu.')
			

		else:
			print("Goodbye")
			app_running = False


if __name__ == '__main__':
	Base.metadata.create_all(engine)
	add_csv()
	app()

from __future__ import print_function

import mysql.connector
import hashlib
import json
import boto3


def lambda_handler(event, context):
	sqs = boto3.resource("sqs", region_name="eu-west-1") # FIXME change region.
	queue = sqs.get_queue_by_name(QueueName="ordernator-requests")
	for order in get_orders():
		queue.send_message(MessageBody=json.dumps(order))


def get_orders():
	connection = mysql.connector.connect(
		user="username", # FIXME change user name.
		password="password", # FIXME change password.
		host="host", # FIXME change host DNS address.
		database="ordernator")

	cursor = connection.cursor()
	try:
		cursor.execute(
			"""SELECT a.full_name, a.email_address, a.address, DATE_FORMAT(o.create_date, '%Y-%m-%dT%TZ'), p.name, op.quantity
				FROM accounts a, products p, orders o, orders_products op
				WHERE op.order_id = o.id AND op.product_sku = p.sku AND o.account_id = a.id""")
		return group_products(cursor)

	finally:
		cursor.close()
		connection.close()


def group_products(cursor):
	orders = {}
	for (client_name, email_address, address, date, product_name, quantity) in cursor:
		key = hashlib.md5((email_address+date).encode("utf-8"))
		if key not in orders:
			order = {
				"client_name": client_name,
				"email_address": email_address,
				"address": address,
				"date": date,
				"products": []
			}
			orders[key] = order

		orders[key]["products"].append({
				"product": product_name,
				"quantity": quantity
			})

	return list(orders.values())


if __name__ == "__main__":
	lambda_handler(None, None)
from Project.model.DB import Session
from flask import request, jsonify
from Project.errors.custom_errors import AppServiceError

'''
Creating factory functions for the common CRUD operations on resources.
'''


def get_all_factory( Model, schema ):
	def func():
		# Create Session
		db_sess = Session()

		# Get query string (if any)
		query = request.args

		# Find the documents from the query
		raw_data = Model.search( db_sess, query )

		# Serialize data
		serialized_data = schema.dump( raw_data )

		return jsonify(
			{ "status": "success", "msg": "Search Result", "results": len( serialized_data ),
			  "data": serialized_data } ), 200

	return func


def create_factory( Model, schema ):
	def func():
		# Load and validate data against the Schema
		raw_data = request.json
		serialized_data = schema.load( raw_data )

		# If valid - create a DB-Session and try to create a record
		db_sess = Session()

		new_record = Model( **serialized_data )
		new_record.create( db_sess )
		db_sess.commit()

		return jsonify(
			{ "status": "success", "msg": "Record Created",
			  "data": { "username": serialized_data } } ), 201

	return func


def get_one_factory( Model, schema ):
	def func( id ):
		# Create Session
		db_sess = Session()

		# Get Record
		raw_data = Model.get_by_id( db_sess, id )

		# Serialize Data
		serialized_data = schema.dump( raw_data )

		return jsonify(
			{ "status": "success", "msg": "Record by ID",
			  "data": serialized_data } ), 200

	return func


def update_factory( Model, schema ):
	def func( id ):
		# Load and validate data against the Schema
		raw_data = request.json
		serialized_data = schema.load( raw_data )

		if not serialized_data:
			raise AppServiceError( "No data to update", 401 )

		# If valid - create a DB-Session and try to update the record
		db_sess = Session()

		# Update record
		result = Model.update( db_sess, id, serialized_data )

		# Commit changes
		db_sess.commit()

		return jsonify(
			{ "status": "success", "msg": "Record updated",
			  "data": serialized_data } ), 200

	return func


def delete_factory( Model ):
	def func( id ):
		# Create Session
		db_sess = Session()

		# Find Record
		record = Model.get_by_id( db_sess, id )

		# If exists -  delete it
		record.delete( db_sess )

		# Commit changes
		db_sess.commit()

		return jsonify(
			{ "status": "success", "msg": "Record deleted",
			  "data": { } } ), 200

	return func
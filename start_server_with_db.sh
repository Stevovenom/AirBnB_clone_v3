#!/bin/bash

# Drop the database if it exists
mysql -u root -p < drop_dev_database.sql

# Create and initialize the database
mysql -u root -p < create_dev_database.sql

# Start the Flask server
python3 api/v1/app.py

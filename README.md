#Tic Tac Toe

## Requirements:

1. Python 2.6 or greater
2. PIP 

## Installation Instructions

These instructions are intended for running locally

1. (optional) Setup up a fresh virtual environment and activate it

		virtualenv ~/tictactoe
		source ~/tictactoe/bin/activate
2. Install required packages via PIP

		pip install -r requirements.txt
		
3. Run syncdb to set up database

		./manage.py syncdb
		
4. Run the local server and browser to localhost:8000

		./manage.py runserver
		

## Overriding Settings

Settings are overridable by assigning values to tictactoe/local_settings.py. local_settings.py is ignored by git and is intended for local overrides only

## Admin

Game records are available via Django's built-in admin
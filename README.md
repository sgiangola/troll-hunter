# Troll Hunter
For our noble task of rooting out alien trolls we will be utilizing Python, the Flask framework and a SQLite database.

Our server-side application utilizes HTTP requests to provide a string of text for a potential alien troll to count the occurrence of each word and a list of words to exclude from the final count. The application receives the alien troll's answer in the form of a post request and checks for the correct solution.

## API parameters
JSON requests are received at http://localhost:5000/

All requests require the following header: {'Content-Type':'application/json'}

a 'GET' request will contain the following elements.
* 'text': a string to count the occurrences of each word
* 'exclude': a list of words to NOT count, if there are none, this will consist of an empty list

a 'POST' request must contain the following elements.
* 'text': a string to count words from
* 'exclude': a list containing the words that will not be counted, if no words are to be excluded an empty list must be returned
* 'count' : a dictionary containing a key, value pair of word and count

A malformed request or wrong answer will result in a 400 status code error, whereas a correct solution will result in a 200 status code.

## Setup

The source code includes a file ('load_db.py') that will create the local database that will contain the random samples to serve the client. Once the requirements, listed in the requirements.txt file, are met, run this script to create and load the database.

To run the app, run 'app.py' through the Python shell, at which point it will be up and running and ready to accept requests.

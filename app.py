from flask import Flask, request, abort
import sqlalchemy as sa
import json
import random
import re

# create sqlalchemy connection object
engine = sa.create_engine('sqlite:///local_db.db')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
	'''Return a randomly selected string of text to be counted
	by the clientand a list of words from that string
	to NOT be counted.'''

	random_sample = get_random_sample()

	# get random words in sample text to exclude from count
	words_to_exclude = get_words_to_exclude(random_sample)

	return json.dumps(
		{
		'text': random_sample,
	 	'exclude': words_to_exclude
		}
	)

@app.route('/', methods=['POST'])
def post():
	'''Validates a post request to ensure that the given string has been
	properly counted with words to exclude considered. Return a 200 on match
	and a 400 on failure.'''

	# get request in JSON
	user_input = request.json

	# validation to ensure the request contains all of necessary elements
	try:
		text = user_input['text']
		exclude = user_input['exclude']
		count = user_input['count']
	except:
		abort(400)

	# validate the types of each arg, return 400 if they are not what is expected
	if type(text) != str or type(exclude) != list or type(count) != dict:
		abort(400)

	# get correct count of words in text minus the exclude words
	solution = count_words(
		user_input.get('text'),
	 	exclude=user_input.get('exclude')
		)

	# compare word count objects to validate request
	if count == solution:
		return ''
	else:
		abort(400)

def get_random_sample():
	'''Return a random sample of text contained in sqlite db: local_db.db'''
	# connect to db
	conn = engine.connect()

	# select a random text sample by executing raw sql
	query = conn.execute(
	'''
	select *
	from sample_text
	order by random()
	limit 1;
	'''
	)

	# get query result
	result = query.cursor.fetchall()[0][0]

	return result

def get_words_to_exclude(text):
	'''Given a string of text, return up to 3 words from that string,
	selected at random.'''

	# get word count in order to see if the text is made up of just one word
	count = count_words(text)

	# if it is, return an empty list
	if len(count) == 1:
		return []

	# replace punctuation to leave just words and split the result
	text = format_text(text)

	# get random index values of
	random_index = [random.randrange(0, len(text)) for i in range(0, 3)]

	# if the number of words to exclude is the length of the word list then
	# we will remove one element
	if len(text) == random_index:
		random_index.pop()

	# get up to 3 unique random words from the list of words
	# to exclude for the test
	words = list(set([text[ix] for ix in random_index]))

	return words

def count_words(text, exclude=[]):
	'''Given a string of a text, counts the occurences of each word
	in that string, except for those words included in the exclude list.'''

	# convert text string to lowercase and split it
	text_list = format_text(text)

	# get unique list of words in the input text
	unique_words = set(text_list)

	# eliminate words passed as an exclusion list
	words_to_count = [i for i in text_list if i not in exclude]

	# return count of each unique word
	count = {i:text_list.count(i) for i in words_to_count}

	return count

def format_text(text):
	'''Return the given string in lowercase, minus punctuation, in a list object
	containing each word.'''

	# retain only lower case words and spaces via regex pattern and force string
	# to lowercase
	text_sub = re.sub('[^a-z|\s+]', '', text.lower())

	# return string split by spaces
	return text_sub.split()
	#return re.sub('[.|,|!|:|-|;|?|\'|\"]', '', text.lower()).split()

if __name__ == '__main__':
	app.run(debug=True, host='localhost', port=8000)

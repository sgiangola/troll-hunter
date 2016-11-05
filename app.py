from flask import Flask, request
from flask_restful import Api, Resource, abort
import sqlalchemy as sa
from json import dumps
import random
import re

# create sqlalchemy connection object
engine = sa.create_engine('sqlite:///local_db.db')

app = Flask(__name__)
api = Api(app)

class ProvideSample(Resource):
	def get(self):

		# connect to db
		conn = engine.connect()

		# select a random text sample by executing
		query = conn.execute(
		'''
		select *
		from sample_text
		order by random()
		limit 1;'''
		)

		# get query result
		result = query.cursor.fetchall()[0][0]

		# get random words in sample text to exclude from count
		words_to_exclude = get_words_to_exclude(result)

		return {'text': result, 'exclude': words_to_exclude}

# create class which will serve as our post method to get the input data
class ReceiveInput(Resource):
	def post(self):

		# get request in JSON
		user_input = request.get_json(force=True)

		text = user_input.get('text')
		exclude = user_input.get('exclude')
		count = user_input.get('count')

		# get count from defined function below
		solution = count_words(user_input.get('text'),
		 	exclude=user_input.get('exclude'))

		# compare word count objects to validate request
		if count == solution:
			return 200, 'OK'
		else:
			return 400, 'Bad Request'

def get_words_to_exclude(text):

	# convert text to lower case
	text = text.lower()

	# replace punctuation to leave just words and split the result
	text = remove_punctuation(text)

	# get random index values of
	random_index = [random.randrange(0, len(text)) for i in range(0, 3)]

	# select 3 random words from the list of words to exclude for the test
	words = [text[ix] for ix in random_index]

	return words

def count_words(text, exclude=[]):

	# convert text string to lowercase and split it
	text_list = text.lower().split()

	# get unique list of words in the input text
	unique_words = set(text_list)

	# eliminate words passed as an exclusion list
	words_to_count = [i for i in text_list if i not in exclude]

	# return count of each unique word
	count = {i:text_list.count(i) for i in words_to_count}

	return count

def remove_punctuation(text):
	# converts text to lowercase and replaces punctuation
	return re.sub('[.|,|!|:|-|;]', '', text.lower()).split()

api.add_resource(ProvideSample, '/')
api.add_resource(ReceiveInput, '/')

if __name__ == '__main__':
	app.run(debug=True)

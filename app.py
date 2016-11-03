from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import random
import re

# create sqlalchemy connection object
engine = create_engine('sqlite:///local_db.db')

app = Flask(__name__)
api = Api(app)

class ProvideSample(Resource):
	def get(self):

		# connect to db
		conn = engine.connect()

		# select a random text sample
		query = conn.execute(
		'''
		select *
		from sample_text
		order by random()
		limit 1;'''
		)

		# get query result
		result = query.cursor.fetchall()[0][0]

		words_to_exclude = get_words_to_exclude(result)

		print(words_to_exclude)

		return {'sample_text': result, 'exclude': words_to_exclude}

def get_words_to_exclude(text):

	# convert text to lower case
	text = text.lower()

	# replace punctuation to leave just words and split the result
	text = re.sub('[.|,|!|:|-]', '', text).split()

	# get random index values of
	random_index = [random.randrange(0, len(text)) for i in range(0, 3)]

	# select 3 random words from the list of words to exclude for the test
	words = [text[ix] for ix in random_index]

	return words

# create class which will serve as our post method to get the insput data
class ReceiveInput(Resource):
	def post(self):

		# get request in JSON
		req = request.get_json(force=True)

		# split the input text via str method
		text_split = [i for i in req['text'].split()]

		# get count from defined function below
		if req.get('exclude'):
			count = list_counter(text_split, exclude=req.get('exclude'))
		else:
			count = list_counter(text_split)

		print(count)

def list_counter(text_list, exclude=[]):

	# get unique list of words in the input text
	unique_words = set(text_list)

	# eliminate words passed as an exclusion list
	words_to_count = [i for i in text_list if i not in exclude]

	# return count of each unique word
	count = {i:text_list.count(i) for i in words_to_count}

	return count

api.add_resource(ProvideSample, '/')
api.add_resource(ReceiveInput, '/')

if __name__ == '__main__':
	app.run(debug=True)

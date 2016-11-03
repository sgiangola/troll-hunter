from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#
e = create_engine('sqlite:///local_db.db')

app = Flask(__name__)
api = Api(app)

class ProvideSample(Resource):
	def get(self):
		#Connect to databse
		conn = e.connect()
		#Perform query and return JSON data
		query = conn.execute("select samples from sample_text")
		return {'sample_text': [i[0] for i in query.cursor.fetchall()]}

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

		print(req['exclude'])

def list_counter(text_list, exclude=None):

	# get unique list of words in the input text
	unique_words = set(text_list)

	# return count of each unique word
	count = {i:text_list.count(i) for i in unique_words}

	return count

api.add_resource(ProvideSample, '/')
api.add_resource(ReceiveInput, '/')

#api.add_resource(Sample, '/dept/<string:department_name>')

if __name__ == '__main__':
	app.run(debug=True)

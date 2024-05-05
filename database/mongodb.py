
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from constants import *

class MongoDB:
	def __init__(self, user, password):
		self.user = user
		self.password = password
	def get_db_conn(self):
		uri = f"mongodb+srv://{self.user}:{self.password}@cluster0.7rjggmk.mongodb.net?retryWrites=true&w=majority&appName=Cluster0"
		client = MongoClient(uri, server_api=ServerApi('1'))
		return client


if __name__ == "__main__":
	# create a MongoDB object
	mongodb = MongoDB(MONGO_USER, MONGO_PASSWORD)
	# create a connection to the database
	client = mongodb.get_db_conn()
	# create a database
	db = client['codecontest']
	# create a collection
	collection = db['problems']
	# insert a document
	problem = {
		"problem_name": "Test name",
		"problem_generated_editorial": "Test editorial",
	}
	collection.insert_one(problem)
	# query the collection
	print("After inserting")
	problems = collection.find()
	for problem in problems:
		print(problem)
	# delete the document
	collection.delete_one(problem)
	# query the collection
	print("After deleting")
	problems = collection.find()
	for problem in problems:
		print(problem)
	# close the connection
	client.close()

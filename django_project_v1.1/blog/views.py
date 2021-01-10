from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import pandas as pd
import os
from pymongo import MongoClient            
import urllib
import pandas as pd
import jwt

def home(request):
	return render(request, 'blog/home.html', {'title':'Namma Mane'})

def about(request):
	return render(request, 'blog/about.html', {'title':'Namma Bagge'})

def upload(request):
	if request.method == 'POST':
		uploaded_file = request.FILES['document']

		#TO CHECK IF FILE IS .CSV/.XLSX FORMAT ONLY

		_, file_ext = os.path.splitext(str(uploaded_file))
		file_ext = file_ext.lower()
		if file_ext == '.csv' or file_ext == '.xlsx':
			messages.add_message(request, messages.INFO, 'File Successfully Loaded')		
			file = pd.read_csv('creds.csv', header = None)
			my_id =  file[0][0]
			my_pass = file[0][1]
			democlient = MongoClient("mongodb+srv://"+my_id+":"+urllib.parse.quote(my_pass)+"@cluster0.ioawf.mongodb.net/<sample_analytics>?retryWrites=true&w=majority")

			#ESTABLISH MONGODB CONNECTION, CREATE DATABASE AND COLLECTION
			db = democlient['Test_Database']
			db_coll = db["Test_coll"]
			
			if file_ext == '.csv':
				data = pd.read_csv(uploaded_file)
			elif file_ext == '.xlsx':
				data = pd.read_excel(uploaded_file)

			#RETRIEVE DATA FROM MONGO SERVER AND STORE IT IN A TEMPORARY FILE
			#INSERTION TO SERVER IS DONE ONLY DATA IS STORED IN DICTIONARY
			df = data.to_dict('records')
			db_coll.insert_many(df)
			db_name = democlient.Test_Database
			coll_name = db_name.Test_coll
			cursor = coll_name.find()
			list_cur = list(cursor)
			df = pd.DataFrame(list_cur)
			df.to_csv('Temproary.csv', index=False)

			#USE THE ID's GENERATED TO CREATE JWT TOKENS
			data2 = pd.read_csv('Temproary.csv', usecols=['_id']).to_dict(orient='records')
			jwt_df = pd.DataFrame(columns=['JWT_Tokens'])
			ls=[]

			for i in range(0, len(data2),1):
			    ls.append(jwt.encode(data2[i], 'Secret'))

			ls2=[]

			for i in range(len(ls)):
			    ls2.append(ls[i].decode('utf-8').replace('\'', ''))

			df['JWT Tokens'] = ls2
			df.to_csv('Data_and_JWT_Tokens.csv', index=False)

		else:
		    messages.add_message(request, messages.ERROR, 'Invalid File Selection!!! Please Select Proper File')
	return render(request, 'blog/upload.html', {'title':'Upload Madiri'})
	




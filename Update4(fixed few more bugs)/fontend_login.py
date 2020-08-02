import requests
import urllib.parse
import numpy as np
import pandas as pd
import json
import sys
def add_data(path):
    try:
        login_url='https://rnsit-ecert.herokuapp.com/users/login'
        login_data={
                    "userName":"admin",
                    "password":"password"
        }
        session = requests.session()

        r = session.post(login_url,data=login_data)
        user_token = (json.loads(r.text))['data']['userToken']
        print(user_token)

        datagram = pd.read_excel(path,sheet_name="one")
        datagram.to_csv("here.csv",header=True,index=None)
        path2="here.csv"
        datagram=pd.read_csv(path2)

        datagram['verifyUrl']=np.nan
        datagram.drop(datagram.index,inplace=True)
        #print(r.text)
        #print(user_token)
        file_data = {
            'file': (path2, open(path2, 'rb'))
        }
        form_data = {
            'file': path2,
            'usertoken': user_token
        }
        response = requests.post('https://rnsit-ecert.herokuapp.com/data/add-files', files=file_data, data=form_data)
        print(response.text)
        l=[]
        print("here")
        for i in json.loads(response.text)['data']['result']:

            k = pd.DataFrame(i, index=[0])
            datagram=datagram.append(k)
           # datagram.append(k)
            #datagram.append(i)

        logout_url = 'https://rnsit-ecert.herokuapp.com/users/logout/' + user_token
        logout_response = requests.get(logout_url)
        print(datagram)
        #print(logout_response.text)
        #datagram['serial']=l
        datagram.rename(columns={'verifyUrl':'serial'},inplace=True)
        datagram.to_csv(path2)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("error")
        logout_url = 'https://rnsit-ecert.herokuapp.com/users/logout/' + user_token
        logout_response = requests.get(logout_url)
        print(logout_response.text)
add_data('Book1.xlsx')
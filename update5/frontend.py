import requests
import urllib.parse
import pandas
import json
try:
    login_url='https://rnsit-ecert.herokuapp.com/users/login'
    login_data={
                "userName":"admin",
                "password":"password"
    }
    session = requests.session()

    r = session.post(login_url,data=login_data)
    user_token = (json.loads(r.text))['data']['userToken']
    print(r.text)
    print(user_token)
    file_data = {
        'file': ("web2t.csv", open("web2t.csv", 'rb'))
    }
    form_data = {
        'file': "web2t.csv",
        'usertoken': user_token
    }
    response = requests.post('https://rnsit-ecert.herokuapp.com/data/add-files', files=file_data, data=form_data)
    print(response.text)


    logout_url = 'https://rnsit-ecert.herokuapp.com/users/logout/' + user_token
    logout_response = requests.get(logout_url)
    print(logout_response.text)
except:
    print("error")
    logout_url = 'https://rnsit-ecert.herokuapp.com/users/logout/' + user_token
    logout_response = requests.get(logout_url)
    print(logout_response.text)
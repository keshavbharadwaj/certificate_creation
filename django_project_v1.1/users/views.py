#6. UserCreationForm exists by default in DJANGO which provides registration page

#10. If get a POST request, instantiates a user creation form with POST data(data from the form), any other request like GET just create a form.

#17. cleaned_data is a dictionary which converts data into appropriate types

#24. blog-home is a name for home page given during creation of the blog site


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
import datetime as dt
from django_project import logger


def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		#VAILDATE FORM
		try:
			if form.is_valid():
				form.save()
				username = form.cleaned_data.get('username')
				messages.success(request, f'Account Created for {username}!')
				logger.info("Account Successfully Created For "+username+"\n")
				return redirect('login')
			else:		
				logger.warning("A user tried to create an account with existing username")
		except:
			messages.error(request, f'Unknown Error')
	else:
		form = UserCreationForm()
	return render(request, 'users/register.html', {'form': form})

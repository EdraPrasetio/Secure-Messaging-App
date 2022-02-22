from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
def index(request):
    all_users = User.objects.distinct().order_by('username')
    return render(request, 'conversations/index.html', {
			'user_list': all_users
		}
	)

def settings(request):
    return render(request, 'accounts/settings.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/registration_successful')
        return render(request, 'accounts/register.html', {'form': form })

    else:
        form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form })

@login_required
def del_user(request):
    del_username = request.POST.get("del_username")
    curr_username = request.POST.get("curr_username")

    print(del_username)
    print(curr_username)
    if del_username == curr_username:
        try:
            u = User.objects.get(username = curr_username)
            logout(request)
            u.delete()

        except Exception as e: 
            return render(request, 'accounts/settings.html' , {'error': e})

        return render(request, 'accounts/account_deleted.html') 

    return render(request, 'accounts/settings.html', {'error' : 'The username you entered does not match the user you are logged in as.'})

def registration_successful(request):
    return render(request, 'accounts/registration_successful.html')

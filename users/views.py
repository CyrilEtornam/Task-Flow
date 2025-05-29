from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# from django.contrib import messages


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log new user in and redirect to homepage
            login(request, new_user)
            return redirect('task_app:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


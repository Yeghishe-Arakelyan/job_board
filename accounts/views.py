from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .forms import UserRegistrationForm, UserLoginForm,  EditProfileForm, EditJobForm, AddJobForm, ManagerLoginForm
from accounts.models import User
from django.db import IntegrityError


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(
                    data['email'], data['full_name'], data['password']
                )
                return redirect('accounts:user_login')
            except IntegrityError:
                # Handle the exception for duplicate email
                form.add_error('email', 'An account with this email already exists.')
    else:
        form = UserRegistrationForm()
    context = {'title': 'Signup', 'form': form}
    return render(request, 'register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('jobs:home_page')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:user_login')
    else:
        form = UserLoginForm()
    context = {'title':'Login', 'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


def edit_profile(request):
    form = EditProfileForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your profile has been updated', 'success')
        return redirect('accounts:edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'title':'Edit Profile', 'form':form}
    return render(request, 'edit_profile.html', context)



@login_required
def jobs(request):
    jobs = Job.objects.filter(posted_by=request.user)
    context = {'title':'Jobs' ,'jobs':jobs}
    return render(request, 'jobs.html', context)



@login_required
def add_job(request):
    if request.method == 'POST':
        form = AddJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user 
            form.save()
            messages.success(request, 'Job added Successfuly!')
            return redirect('accounts:add_job')
        else:
            messages.error(request, 'Invalid job. Please correct the errors below.')
    else:
        form = AddJobForm()
    context = {'title':'Add Job', 'form':form}
    return render(request, 'add_job.html', context)



@login_required
def delete_job(request, id):
    if request.user != job.posted_by:
        messages.error(request, 'You do not have permission to delete this job.', 'danger')
        return redirect('accounts:jobs')
    job = Job.objects.filter(id=id).delete()
    messages.success(request, 'Job has been deleted!', 'success')
    return redirect('accounts:jobs')



@login_required
def edit_job(request, id):
    job = get_object_or_404(Job, id=id)
    if request.user != job.posted_by:
        messages.error(request, 'You do not have permission to edit this job.', 'danger')
        return redirect('accounts:jobs')
    if request.method == 'POST':
        form = EditJobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job has been updated', 'success')
            return redirect('accounts:jobs')
    else:
        form = EditJobForm(instance=job)
    context = {'title': 'Edit Job', 'form':form}
    return render(request, 'edit_job.html', context)


def create_manager():
    """
    to execute once on startup:
    this function will call in job/urls.py
    """
    if not User.objects.filter(email="manager@example.com").first():
        user = User.objects.create_user(
            "manager@example.com", 'job manager' ,'managerpass1234'
        )
        # give this user manager role
        user.is_manager = True
        user.save()


def manager_login(request):
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None and user.is_manager:
                login(request, user)
                return redirect('dashboard:jobs')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:manager_login')
    else:
        form = ManagerLoginForm()
    context = {'form': form}
    return render(request, 'manager_login.html', context)

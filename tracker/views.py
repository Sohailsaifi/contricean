# myapp/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect

from tracker.utils.github_api_functions import *
from tracker.data.repo_list import *
from config import github_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json


   

def authentication(request):
    # If the user is already authenticated, redirect to the homepage
    # if request.session.get('github_api_token'):
    #     return redirect('homepage')

    error_message = ""
    if request.method == 'POST':
        auth_type = request.POST.get('auth_type')
        auth_token = request.POST.get('auth_token', '')

        # Now you can handle the authentication data as needed
        if auth_type == 'authenticated':
            # Process authenticated user with auth_token
            # Example: Check the token against your authentication logic
            if auth_token:
                # Perform actions for authenticated users
                # You might want to store the authentication state in the session or a custom authentication mechanism
                is_valid = is_valid_github_token(auth_token)
                if is_valid:
                    request.session['github_api_token'] = auth_token
                    error_message = ''
                else:
                    # If the token is not valid, set the error message
                    error_message = 'Invalid GitHub API token. Please check and try again.'
            else:
                # Handle invalid token
                error_message = 'No token was provided'

        elif auth_type == 'unauthenticated':
            # Process unauthenticated user
            request.session.pop('github_api_token', None)
            request.session['github_api_token'] = ''
            error_message = ''

    request.session['error_message'] = error_message
    return redirect('homepage')


# @login_required(login_url='authentication')
def homepage(request):

    try:
        github_api_token = request.session['github_api_token']
    except:
        github_api_token = None

    final_result = []
    languages_set = set()
    repo_set = set()

    is_error = False

    try:
        if request.session['error_message']:
            is_error = True
        error_message = request.session['error_message']
    except:
        error_message = ''

    for github_username, github_repo in github_usernames.items():
        result, languages_used = get_open_issues(github_username, github_repo, github_api_token)
        final_result.extend(result)
        languages_set.update(languages_used)
        repo_set.add(github_repo)
    
    
    final_result = sorted(final_result, key=lambda x: x['parsed_date'], reverse=True)

    # languages_set.update(['HTML', 'CSS', 'Makefile', 'Python', 'Shell', 'XSLT', 'TypeScript', 'MDX', 'PLpgSQL', 'JavaScript', 'Handlebars', 'Dockerfile', 'SCSS', 'Random'])
    # repo_set.update(['Ghost', 'supabase', 'obs-studio'])
    # file_path = "tracker\\data\\api-test-data.json"
    # with open(file_path, 'r') as file:
    #     file_contents = file.read()
    #     final_result = json.loads(file_contents)

    context = {
        'issues': final_result,
        'unique_languages': languages_set,
        'unique_repos': repo_set,
        'authentication': True if github_api_token else False,
        'is_error': is_error,
        'error_message': error_message
    }
    return render(request, 'tracker/homepage.html', context)
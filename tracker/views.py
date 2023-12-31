# myapp/views.py
from django.http import HttpResponse
from django.shortcuts import render

from tracker.utils.github_api_functions import *
from tracker.data.repo_list import *
from config import github_token

def hello(request):
    return HttpResponse("Hello, Django!")



def homepage(request):
    final_result = {}

    for github_username, github_repo in github_usernames.items():
        result = get_open_issues(github_username, github_repo, github_token)
        final_result[github_repo] = result
    print("FINAL RESULT", final_result)
    context = {
        'issues': result
    }
    return render(request, 'tracker/homepage.html', context)
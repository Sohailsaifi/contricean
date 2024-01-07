from dateutil.parser import parse
import requests

def get_open_issues(owner, repo, token=None):
    print(token)
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    api_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    response = requests.get(api_url)
    response.raise_for_status()
    languages_used = list(response.json().keys())
    # print(languages_used)
    
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    params = {"state": "open", "per_page":60, "page": 1}
    response = requests.get(url, headers=headers, params=params)
    
    result = []

    if response.status_code == 200:
        issues = response.json()
        print(f"Number of open issues: {len(issues)}")
        
        for i, issue in enumerate(issues, start=1):
            issue["repo_name"] = repo
            issue['parsed_date'] = parse(issue['created_at'])
            issue["languages_used"] = languages_used
            result.append(issue)
        
        return result, languages_used
    else:
        print(f"Failed to retrieve issues. Status code: {response.status_code}")
        print(response.text)


def get_all_issues(owner, repo, token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    # Initialize variables for pagination
    issues = []
    page = 1
    result = []
    while True:
        # Include the 'state' parameter to get all issues, including those closed
        params = {"state": "open", "page": page}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            page_issues = response.json()
            if not page_issues:
                break  # No more issues to fetch
            
            issues.extend(page_issues)
            page += 1
        else:
            print(f"Failed to retrieve issues. Status code: {response.status_code}")
            print(response.text)
            break

    print(f"New Number of issues: {len(issues)}")
    
    for i, issue in enumerate(issues, start=1):
        title = issue["title"]
        url = issue["html_url"]
        # print(f"Issue #{i}: {title} ({url})")
        result.append(issue)
    return result



def is_valid_github_token(token):
    """
    Verify if a GitHub API token is valid.

    Args:
        token (str): GitHub API token to be verified.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    headers = {
        'Authorization': f'token {token}'
    }

    # Send a request to the GitHub API using the provided token
    response = requests.get('https://api.github.com/user', headers=headers)

    # Check the response status code to determine if the token is valid
    if response.status_code == 200:
        # Status code 200 means a successful request, i.e., the token is valid
        return True
    else:
        # Any other status code indicates an issue with the token
        return False
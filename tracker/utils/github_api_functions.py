from dateutil.parser import parse
import requests

def get_open_issues(owner, repo, token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    # api_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    # response = requests.get(api_url)
    # response.raise_for_status()
    # languages_used = response.json()
    # print(list(languages_used.keys()))
    
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    params = {"state": "open", "per_page":100, "page": 1}
    response = requests.get(url, headers=headers, params=params)
    
    result = []

    if response.status_code == 200:
        issues = response.json()
        print(f"Number of open issues: {len(issues)}")
        
        for i, issue in enumerate(issues, start=1):
            # print(issue.keys())
            # title = issue["title"]
            # url = issue["html_url"]
            # print(f"Issue #{i}: {title} ({url})")
            issue['parsed_date'] = parse(issue['created_at'])
            result.append(issue)
        
        return result
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
import os
from github import Github
import sys
import re

def find_external_repositories(owner, repository, exclusion_list):
    try:
        # Retrieve the access token from the environment variable
        access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
        if access_token is None:
            print("Error: GitHub access token not found. Please set the GITHUB_ACCESS_TOKEN environment variable.")
            return []

        # Initialize a GitHub instance with authentication
        g = Github(access_token)

        # Search code in the repository
        query = f'repo:{owner}/{repository} {search_text}'
        code_search_results = g.search_code(query=query)

        # Initialize a set to store unique external repositories
        external_repositories = set()

        # Iterate over code search results
        for result in code_search_results:
            file_content = result.decoded_content.decode('utf-8')
            lines = file_content.split('\n')
            for i, line in enumerate(lines, start=1):
                    if search_text in line:
                        org,repo = extract_org_repo_from_url(line)
                        if org not in exclusion_list:
                            repo_name = f"{org}/{repo}"
                            if repo_name not in external_repositories:
                                external_repositories.add(repo_name)
                                # print(f"repo_name: {repo_name}")

        # Convert set to list for returning
        return list(external_repositories)

    except Exception as e:
        print(f"Error: {e}")
        return []

def extract_org_repo_from_url(url):
    # Regular expression pattern to match GitHub URLs
    pattern = r"github\.com[\/|:]([^\/]+)\/([^\/\.]+)(?:\.git|\/|\s|$)"

    # Search for the pattern in the URL
    match = re.search(pattern, url)

    if match:
        org = match.group(1)
        repo = match.group(2)
        return org, repo
    else:
        print (f"didn't match {url}")
        return None, None


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <owner/org> <repository> <search string> <exclusion_list>")
        sys.exit(1)

    owner = sys.argv[1]
    repository = sys.argv[2]
    search_text = sys.argv[3]
    exclusion_list = sys.argv[4:]

    external_repositories = find_external_repositories(owner, repository, exclusion_list)
    print("External repositories:")
    for repo in external_repositories:
        print(repo)

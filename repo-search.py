from github import Github
import sys

def find_external_repositories(owner, repository, exclusion_list):
    # Authenticate with GitHub using a personal access token
    access_token = 'your_access_token_here'
    g = Github(access_token)

    try:
        # Get the repository
        repo = g.get_repo(f"{owner}/{repository}")

        # Initialize a set to store unique external repositories
        external_repositories = set()

        # Iterate through all files in the repository
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "file" and file_content.name.endswith('.py'):
                # Analyze Python files for imports
                file_content = file_content.decoded_content.decode('utf-8')
                lines = file_content.split('\n')
                for line in lines:
                    if line.startswith('import ') or line.startswith('from '):
                        # Extract the imported module
                        module = line.split()[1]
                        # Check if the module is from an external GitHub repository
                        if '/' in module:
                            repo_owner = module.split('/')[0]
                            if repo_owner not in exclusion_list:
                                external_repositories.add(module)

        # Convert set to list for returning
        return list(external_repositories)

    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <owner/org> <repository> <exclusion_list>")
        sys.exit(1)

    owner = sys.argv[1]
    repository = sys.argv[2]
    exclusion_list = sys.argv[3:]

    external_repositories = find_external_repositories(owner, repository, exclusion_list)
    print("External repositories:")
    for repo in external_repositories:
        print(repo)
# Read a file from a Github repo, replace text (as a whole word), and push the changes back.
# Author: Carmine Giardino

import requests
import json
import base64
import re
from config import api_keys
from config import assignment04_github_config as conf

# Configuration
GITHUB_TOKEN = api_keys['github_aprivateone']
REPO_OWNER = conf['repo_owner']
REPO_NAME = conf['repo_name']
FILE_PATH = conf['file_path']
OLD_TEXT = conf['old_text']
NEW_TEXT = conf['new_text']
ENCODING = conf['encoding']

# GitHub API endpoints
BASE_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}'
CONTENTS_URL = f'{BASE_URL}/contents/{FILE_PATH}'

def get_file_content():
    """Get the README file from GitHub"""
    response = requests.get(CONTENTS_URL, auth=('token', GITHUB_TOKEN))
    
    if response.status_code == 200:
        data = response.json()
        # Decode base64 content
        content = base64.b64decode(data['content']).decode(ENCODING)
        sha = data['sha']  # Need SHA for updating
        return content, sha
    else:
        print(f"Error fetching file: {response.status_code}")
        print(response.json())
        return None, None

def update_file(new_content, sha, commit_message):
    """Push updated content back to GitHub"""
    # Encode content to base64
    encoded_content = base64.b64encode(new_content.encode(ENCODING)).decode(ENCODING)
    
    data = {
        'message': commit_message,
        'content': encoded_content,
        'sha': sha
    }
    
    response = requests.put(CONTENTS_URL, auth=('token', GITHUB_TOKEN), json=data)
    
    if response.status_code == 200:
        print("File updated successfully!")
        result = response.json()
        print(f"Commit: {result['commit']['html_url']}")
        return True
    else:
        print(f"Error updating file: {response.status_code}")
        print(response.json())
        return False

def main():
    print(f"Fetching {FILE_PATH} from {REPO_OWNER}/{REPO_NAME}")
    
    # Get current file content
    content, sha = get_file_content()
    
    if content is None:
        print("Failed to retrieve file content. Exiting.")
        return
    
    print(f"File retrieved successfully")
    
    # Count occurrences (whole words only)
    count = len(re.findall(rf'\b{re.escape(OLD_TEXT)}\b', content))
    
    if count == 0:
        print(f"Text '{OLD_TEXT}' not found as a whole word in file")
        return
    
    print(f"Found {count} whole word instance(s) of '{OLD_TEXT}'")
    
    # Replace text (whole words only)
    new_content = re.sub(rf'\b{re.escape(OLD_TEXT)}\b', NEW_TEXT, content)
    print(f"Replacing '{OLD_TEXT}' with '{NEW_TEXT}'")
    
    # Create a commit message
    commit_message = f"Replace '{OLD_TEXT}' with '{NEW_TEXT}' in {FILE_PATH}"
    
    # Push changes
    if update_file(new_content, sha, commit_message):
        print(f"Successfully replaced {count} instance(s)")

if __name__ == '__main__':
    main()

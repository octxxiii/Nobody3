"""Create GitHub release using GitHub API."""

import os
import sys
import json
import requests
from pathlib import Path

def create_release():
    """Create GitHub release for v1.0.0."""
    
    # GitHub repository info
    repo_owner = "octxxiii"
    repo_name = "Nobody3"
    tag = "v1.0.0"
    
    # Read release notes
    release_notes_path = Path("RELEASE_NOTES_v1.0.0.md")
    if not release_notes_path.exists():
        print(f"Error: {release_notes_path} not found")
        return False
    
    with open(release_notes_path, "r", encoding="utf-8") as f:
        release_notes = f.read()
    
    # Check for GitHub token
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("GitHub Personal Access Token required.")
        print("\nOption 1: Enter token now (will not be saved)")
        print("Option 2: Create release manually on GitHub website")
        print("\nTo get a token:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Generate new token (classic) with 'repo' scope")
        print("3. Copy the token")
        print("\nEnter token (or press Enter to skip and create manually): ", end="")
        github_token = input().strip()
        
        if not github_token:
            print("\n" + "="*60)
            print("MANUAL RELEASE CREATION GUIDE")
            print("="*60)
            print(f"\n1. Go to: https://github.com/{repo_owner}/{repo_name}/releases/new")
            print(f"2. Select tag: {tag}")
            print(f"3. Title: Nobody 3 v1.0.0")
            print(f"4. Description: Copy content from RELEASE_NOTES_v1.0.0.md")
            print(f"5. Upload: releases/Nobody3-Windows.zip")
            print(f"6. Click 'Publish release'")
            print("\n" + "="*60)
            return False
    
    # API endpoint
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    
    # Release data
    release_data = {
        "tag_name": tag,
        "name": "Nobody 3 v1.0.0",
        "body": release_notes,
        "draft": False,
        "prerelease": False
    }
    
    # Headers
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"Creating release {tag}...")
    
    try:
        # Create release
        response = requests.post(url, headers=headers, json=release_data)
        
        if response.status_code == 201:
            release_info = response.json()
            release_id = release_info["id"]
            upload_url = release_info["upload_url"].split("{")[0]
            
            print(f"✓ Release created successfully!")
            print(f"  Release ID: {release_id}")
            print(f"  URL: {release_info['html_url']}")
            
            # Upload binary if exists
            zip_path = Path("releases/Nobody3-Windows.zip")
            if zip_path.exists():
                print(f"\nUploading {zip_path.name}...")
                upload_binary(upload_url, zip_path, github_token)
            else:
                print(f"\nWarning: {zip_path} not found. Skipping binary upload.")
                print("You can upload it manually from the release page.")
            
            return True
        else:
            print(f"Error creating release: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def upload_binary(upload_url, file_path, token):
    """Upload binary file to release."""
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/zip"
    }
    
    file_name = file_path.name
    
    with open(file_path, "rb") as f:
        data = f.read()
    
    url = f"{upload_url}?name={file_name}"
    
    try:
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 201:
            print(f"✓ {file_name} uploaded successfully!")
            print(f"  Size: {len(data) / (1024*1024):.2f} MB")
            return True
        else:
            print(f"Error uploading {file_name}: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error uploading {file_name}: {e}")
        return False

if __name__ == "__main__":
    success = create_release()
    sys.exit(0 if success else 1)


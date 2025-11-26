"""Create GitHub release using API."""

import os
import sys
import json
import requests
from pathlib import Path

def create_github_release():
    """Create GitHub release with asset upload."""
    
    # Read release notes
    notes_path = Path("RELEASE_NOTES_v1.0.1.md")
    if not notes_path.exists():
        print(f"Error: {notes_path} not found")
        return False
    
    with open(notes_path, "r", encoding="utf-8") as f:
        release_notes = f.read()
    
    # Find zip file
    zip_path = Path("releases/Nobody3-v1.0.1-20251126.zip")
    if not zip_path.exists():
        print(f"Error: {zip_path} not found")
        return False
    
    # GitHub API endpoint
    repo = "octxxiii/Nobody3"
    tag = "v1.0.1"
    api_url = f"https://api.github.com/repos/{repo}/releases"
    
    # Get GitHub token from environment
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Please set GITHUB_TOKEN environment variable with your GitHub personal access token")
        print("You can create one at: https://github.com/settings/tokens")
        return False
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if release already exists
    check_url = f"{api_url}/tags/{tag}"
    response = requests.get(check_url, headers=headers)
    if response.status_code == 200:
        release_id = response.json()["id"]
        print(f"Release {tag} already exists (ID: {release_id})")
        print("Updating release...")
        
        # Update existing release
        update_url = f"{api_url}/{release_id}"
        data = {
            "name": "Nobody 3 v1.0.1 - WebEngine Crash Fix",
            "body": release_notes,
            "draft": False,
            "prerelease": False
        }
        response = requests.patch(update_url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"Error updating release: {response.status_code}")
            print(response.text)
            return False
        release_id = response.json()["id"]
    else:
        # Create new release
        print(f"Creating release {tag}...")
        data = {
            "tag_name": tag,
            "name": "Nobody 3 v1.0.1 - WebEngine Crash Fix",
            "body": release_notes,
            "draft": False,
            "prerelease": False
        }
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code != 201:
            print(f"Error creating release: {response.status_code}")
            print(response.text)
            return False
        release_id = response.json()["id"]
        print(f"Release created successfully (ID: {release_id})")
    
    # Upload asset
    print(f"Uploading asset: {zip_path.name}...")
    upload_url = f"https://uploads.github.com/repos/{repo}/releases/{release_id}/assets"
    
    with open(zip_path, "rb") as f:
        asset_headers = headers.copy()
        asset_headers["Content-Type"] = "application/zip"
        params = {"name": zip_path.name}
        response = requests.post(
            upload_url,
            headers=asset_headers,
            params=params,
            data=f
        )
        
        if response.status_code == 201:
            print(f"Asset uploaded successfully!")
            print(f"Release URL: https://github.com/{repo}/releases/tag/{tag}")
            return True
        else:
            print(f"Error uploading asset: {response.status_code}")
            print(response.text)
            return False

if __name__ == "__main__":
    success = create_github_release()
    sys.exit(0 if success else 1)


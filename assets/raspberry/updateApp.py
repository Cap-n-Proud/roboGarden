import os
import requests
import shutil


def download_latest_release(repo_owner, repo_name):
    # Get the latest release information
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        release_info = response.json()
        print(url)
        # print(release_info)
        if 'assets_url' in release_info:
            a_url = release_info['zipball_url']
            asset_name = "latest.zip"

            # Download the asset file
            print(f"Downloading {asset_name}...")
            response = requests.get(a_url, stream=True)
            with open(asset_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            print("Download complete!")
            return asset_name
        else:
            raise Exception("No assets found for the latest release.")
    else:
        raise Exception(
            f"Failed to fetch the latest release information. Status code: {response.status_code}")


def unpack_release(asset_path, app_path):
    # Unpack the asset file to a temporary directory
    temp_dir = os.path.join(app_path, "temp")
    shutil.unpack_archive(asset_path, temp_dir)

    # Rename the extracted folder as "roboGarden"
    extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
    renamed_dir = os.path.join(app_path, "roboGarden")
    shutil.move(extracted_dir, renamed_dir)

    # Remove the temporary directory
    shutil.rmtree(temp_dir)


def update_app(repo_owner, repo_name, app_path):
    asset_path = download_latest_release(repo_owner, repo_name)
    unpack_release(asset_path, app_path)
    # Remove the downloaded asset file
    os.remove(asset_path)


if __name__ == "__main__":
    repo_owner = "Cap-n-Proud"
    repo_name = "roboGarden"
    app_path = "/app"
    update_app(repo_owner, repo_name, app_path)

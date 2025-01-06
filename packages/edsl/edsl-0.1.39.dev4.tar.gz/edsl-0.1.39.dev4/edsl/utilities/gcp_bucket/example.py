from edsl.utilities.gcp_bucket.cloud_storage import CloudStorageManager

# API URLs
secret_token = "your-secret-token"

# File paths and names
upload_file_path = "./app.py"
upload_file_name = "new_upload.py"

# Initialize CloudStorageManager
manager = CloudStorageManager(secret_token=secret_token) # secret_token only for upload operations

# Upload Process
try:
    manager.upload_file(upload_file_path, upload_file_name)
    print("File upload process completed.")
except Exception as e:
    print(f"Upload error: {str(e)}")

# Download Process
file_name = "new_upload.py"  # Name for the downloaded file
save_name = "res_download.py"
try:
    manager.download_file(file_name, save_name)
    print("File download process completed.")
except Exception as e:
    print(f"Download error: {str(e)}")

# List files
try:
    print("listing files")
    out = manager.list_files()
    for x in out["data"]:
        print(f"file_name: {x['file_name']}", f"url: {x['url']}")
except Exception as e:
    print(f"Exception in listing files", str(e))

# Delete file
try:
    manager.delete_file("new_upload.py")
except Exception as e:
    print(f"Exception in deleting file", str(e))
# List files
try:
    print("listing files")
    out = manager.list_files()
    for x in out["data"]:
        print(f"file_name: {x['file_name']}", f"url: {x['url']}")
except Exception as e:
    print(f"Exception in listing files", str(e))

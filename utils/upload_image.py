import dropbox
from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode


def upload_image(image_content: bytes, file_name: str, dropbox_access_token: str):
    try:
        dbx = dropbox.Dropbox(dropbox_access_token)
        dropbox_path = f"/{file_name}"
        dbx.files_upload(image_content, dropbox_path, mode=WriteMode('add'))
        return f"Successfully uploaded {file_name} to Dropbox.", None

    except Exception as e:
        return None, f"There was an error: {e}"

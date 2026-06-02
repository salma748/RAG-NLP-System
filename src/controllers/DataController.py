from pathlib import Path

from fastapi import UploadFile


from helpers.config import get_settings

class DataController:

    def __init__(self):
       self.app_settings = get_settings()


    def validate_file(self, file: UploadFile):

        allowed_types = set(
            self.app_settings.FILE_ALLOWED_EXTENSIONS
        )

        file_name = file.filename or ""
        file_suffix = Path(file_name).suffix.lower()

        allowed_extensions = {
            ".txt",
            ".pdf",
            ".html",
            ".htm",
        }

        # Validate MIME type OR extension
        is_allowed_content_type = (
            file.content_type in allowed_types
        )

        is_allowed_extension = (
            file_suffix in allowed_extensions
        )

        if not is_allowed_content_type and not is_allowed_extension:
            return False, (
                "Unsupported file type. "
                "Upload TXT, PDF, HTML, or HTM."
            )

        # Validate file size
        if file.size and (
            file.size >
            self.app_settings.FILE_MAX_SIZE_MB * 1024 * 1024
        ):
            return False, "File size exceeds limit"

        return True, "File is valid."
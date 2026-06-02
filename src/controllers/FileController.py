import os

from helpers.config import get_settings


class FileController:

    def __init__(self):

        self.app_settings = get_settings()


    def get_file_path(
        self,
        project_id: str,
        filename: str
    ):

        base_dir = self.app_settings.FILE_DIR

        project_dir = os.path.join(
            base_dir,
            project_id
        )

        # Create project directory
        os.makedirs(
            project_dir,
            exist_ok=True
        )

        return os.path.join(
            project_dir,
            filename
        )
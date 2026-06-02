from pathlib import Path

from helpers.config import get_settings


class BaseController:
    def __init__(self):
        self.app_settings = get_settings()

        self.base_dir = Path(__file__).resolve().parents[1]
        self.assets_dir = self.base_dir / "assets"
        self.file_dir = self.assets_dir / "files"
        self.db_dir = self.assets_dir / "db"

        self.file_dir.mkdir(parents=True, exist_ok=True)
        self.db_dir.mkdir(parents=True, exist_ok=True)

    def get_db_path(self, db_name: str):
        db_path = self.db_dir / db_name
        db_path.mkdir(parents=True, exist_ok=True)
        return str(db_path)

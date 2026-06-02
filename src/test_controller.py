from controllers.BaseController import BaseController
from controllers.DataController import DataController


base = BaseController()

print("App Name:", base.app_settings.APP_NAME)
print("Files Path:", base.file_dir)
print("DB Path:", base.db_dir)


data_controller = DataController()

print("DataController created successfully!")
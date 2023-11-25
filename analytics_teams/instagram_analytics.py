import autogen
from utils.file_utils import save_to_csv
from enums.platform import Platform
import requests
from configs.app_config import AppConfig
import shutil
import os


# TODO: Make a more refined method to retrieve the data from the CSV file
# TODO: Check if we can use pandas for some parts of the analytics
class InstagramAnalytics:
    def __init__(self) -> None:
        self.config = AppConfig()

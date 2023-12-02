import os
from dotenv import load_dotenv

load_dotenv()

KAGGLE_KEY = os.getenv('KAGGLE_KEY')
KAGGLE_USERNAME = os.getenv('KAGGLE_USERNAME')
DEFAULT_USERNAME = 'yufengsui'
DEFAULT_DATASET = 'mobile-games-ab-testing'
DEFAULT_FILE = 'cookie_cats.csv'
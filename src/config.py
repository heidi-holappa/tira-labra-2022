import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    print("Warning! .env file not found.")

path = os.getenv("DEFAULT_DATA_DIRECTORY") or "data"
testing_path = os.getenv("DEFAULT_EXTENSIVE_TESTING_DIRECTORY") or "test-data"
graph_directory = os.getenv("DEFAULT_HTML_REPORT_IMAGES") or "test-data/images"

DEFAULT_DATA_PATH = os.path.join(dirname, '..', path)
DEFAULT_TEST_DATA_PATH = os.path.join(dirname, '..', testing_path)
DEFAULT_TEST_GRAPH_FOLDER = os.path.join(dirname, '..', graph_directory)

HTML_LOG = os.getenv("HTML_LOG_FILE") or "compression-log.html"
CSV_LOG = os.getenv("CSV_LOG") or "compression-log.csv"
ARCHIVE_LOG = os.getenv("LOG_ARCHIVE_FILE") or "compression_archive.log"
TKINTER_LOG = os.getenv("TKINTER_LOG_CONTENT") or "compression.log"
import os

THREADS_FOLDER_NAME = "threads"
TEMP_FOLDER_NAME = "temp"


#
THREADS_FOLDER_PATH = "./" + THREADS_FOLDER_NAME + "/"
TEMP_FOLDER_PATH = "./" + TEMP_FOLDER_NAME + "/"


if not os.path.exists(THREADS_FOLDER_PATH): os.mkdir(THREADS_FOLDER_PATH)
if not os.path.exists(TEMP_FOLDER_PATH): os.mkdir(TEMP_FOLDER_PATH)
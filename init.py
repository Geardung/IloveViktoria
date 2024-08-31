print("Init...", end="")
import os, datetime

THREADS_FOLDER_NAME = "threads"
TEMP_FOLDER_NAME = "temp"
TT_JSON_NAME = "timetables.json"

#
THREADS_FOLDER_PATH = "./" + THREADS_FOLDER_NAME + "/"
TEMP_FOLDER_PATH = "./" + TEMP_FOLDER_NAME + "/"
TT_JSON_PATH = TEMP_FOLDER_PATH + TT_JSON_NAME


if not os.path.exists(THREADS_FOLDER_PATH): os.mkdir(THREADS_FOLDER_PATH)
if not os.path.exists(TEMP_FOLDER_PATH): os.mkdir(TEMP_FOLDER_PATH)
else:
    for file in os.listdir(TEMP_FOLDER_PATH):
        if file == TT_JSON_NAME: continue
        elif ("_" in file) and (datetime.datetime.fromtimestamp(float(file.split("_")[1])) <= (datetime.timedelta(days=7) - datetime.datetime.now())): os.remove(TEMP_FOLDER_PATH+file)
    
if not os.path.exists(TT_JSON_PATH): open(TT_JSON_PATH, "w", encoding="utf-8").write("{\"last_check\": 0}")

print("Completed!")
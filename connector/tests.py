from django.test import TestCase
from datetime import datetime, timezone
from myproject.settings import  *
import sys
import logging
# Create your tests here.
try:
    os.mkdir('Logs')
except FileExistsError:
    null = 0

try:   
    MainPath = os.getcwd()
    os.chdir('Logs')
    LogPath = os.getcwd()
    os.chdir(MainPath)
except:
    print('\nError in Assigning Path!!!')
    sys.exit()


def WriteIntoLog(f_status, f_filename,f_function, f_message):
    try:
        dt = datetime.now()
        x = dt.strftime("%Y-%m-%d %H:%M:%S")
        logmessage = str(x) + ("             ") + f_status + ("             ") + f_filename + ("             ") +f_function + ("             ") + f_message + "\n"
        print("log path")
        print(LogPath)
        os.chdir(LogPath)
        strdate = datetime.now()
        Logfile = open(str(strdate.strftime("%d-%b-%Y")) + "_OpenApiLibrary(python).Log","a+")
        os.chdir(MainPath)
        Logfile.write(logmessage)
        Logfile.close()
    except:
        print('\nError in Writing Logs!!!')
        sys.exit()
# try:
#     MainPath = os.getcwd()
#     os.chdir('Logs')
#     LogPath = os.getcwd()
#     os.chdir(MainPath)
# except:
#     print("exr")
# def ensure_logs_directory():
#     if not os.path.exists(LogPath):
#         os.makedirs(LogPath)

# def WriteIntoLog(f_status, f_filename, f_message):
#     try:
#         ensure_logs_directory()
#         dt = datetime.now()
#         x = dt.strftime("%Y-%m-%d %H:%M:%S")
#         logmessage = str(x) + ("             ") + f_status + ("             ") + f_filename + ("             ") + f_message + "\n"
#         print("log path")
#         print(LogPath)
#         os.chdir(LogPath)
#         strdate = datetime.now()
#         Logfile = open(str(strdate.strftime("%d-%b-%Y")) + "_OpenApiLibrary(python).Log","a+")
#         os.chdir(MainPath)
#         Logfile.write(logmessage)
#         Logfile.close()

#         # dt = datetime.now()
#         # x = dt.strftime("%Y-%m-%d")
#         # log_message = str(x) + ("             ") + f_status + ("             ") + f_filename + ("             ") + f_message + "\n"


#         # log_file_path = os.path.join(LOGGING_DIR, f"{dt.strftime('%d-%b-%Y')}_OpenApiBroadcast(python).log")

#         # logging.basicConfig(
#         #     filename=log_file_path,
#         #     format='%(asctime)s - %(levelname)s - %(message)s',
#         # )

#         # logging.info(log_message)
#         return True
#     except Exception as e:
#         print(f'\nError in Writing Logs: {e}')
#         return False
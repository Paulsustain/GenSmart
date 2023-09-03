import os

FOLDER_PATH="/home/pi/smarteye/logs/smarteye_logs.log"
MAX_FILE_SIZE=0

def get_folder_size():
    size=0
    for path,dirs,files in os.walk(FOLDER_PATH):
        for single_file in files:
            file_path=os.path.join(path,single_file)
            size += os.path.getsize(file_path)

    print('Folder size in byte is: {}'.format(size))

def check_overflow(file_size):
    if file_size > MAX_FILE_SIZE:
        return True
    else:
        return False

def delete_older_logs():
    pass

def zip_older_logs():
    pass

if __name__ == "__main__":
    get_folder_size()
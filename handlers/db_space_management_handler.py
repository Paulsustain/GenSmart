import sys
sys.path.append('/home/pi/smarteye/services/atg')
sys.path.append('/home/pi/smarteye/helpers')
import main_logger
my_logger=main_logger.get_logger(__name__)
import sqlite_service
MAX_LOG=144000
TOLERANCE=100
CHUNK=2000

def manage_deletion(uploaded,unuploaded):
    del_uploaded=del_unuploaded=0
    if uploaded > CHUNK:
        del_uploaded=2000
    else:
        del_uploaded=uploaded
        del_unuploaded=CHUNK-uploaded
    return (del_uploaded,del_unuploaded)
    
def manage_db_space():
    try:
        total_number=sqlite_service.get_total_number_of_logs()
        uploaded_logs=sqlite_service.get_number_of_uploaded_logs()
        unuploaded_logs=sqlite_service.get_number_of_unuploaded_logs()
        if total_number > MAX_LOG-TOLERANCE:
            del_uploaded,del_unuploaded=manage_deletion(uploaded_logs,unuploaded_logs)
            sqlite_service.delete_chunk_of_uploaded_logs(del_uploaded)
            if del_unuploaded:
                sqlite_service.delete_chunk_of_unuploaded_logs(del_unuploaded)
        return True
    except Exception as e:
        print(e)
        my_logger.exception(e)
        return False

if __name__ =="__main__":
    manage_db_space()

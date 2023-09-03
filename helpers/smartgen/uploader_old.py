import time
import requests
import json
import sys
from DFM_enumerators import Upload_type

class UploaderClass:
    '''This class manages the uploading of the unploaded logs '''
    un_uploaded_indexes=None
    upload_type=None
    def __init__(self,upload_type):
        #This constructor accept upload-tyoe enumerator which can either be for genhours or DFM
        self.upload_type=upload_type
        
    def get_indexes(self,un_uploaded_logs):
        #This function gets only the unuploaded logs out the logs read
        indexes=[(x[0],) for x in un_uploaded_logs]
        print(indexes)
        self.un_uploaded_indexes=indexes
    
    def push_log(self,un_uploaded_logs):
        #This function pushes only the unploaded logs
        print("there are uploads")
        self.get_indexes(un_uploaded_logs)
        if self.internet_push(un_uploaded_logs):
            return True
        else:
            return False
    
    def internet_push(self,logs):
        print("got to internet_push")
        print ("the logs are")
        print(logs)
        #This part selects the api to push data to based on the type of data
        if self.upload_type == Upload_type.sources:
            url='https://api.smarteye.com.au/api/v1/genhours_logger/'
        elif self.upload_type==Upload_type.dfm:
            url='https://api.smarteye.com.au/api/v1/fm_logger/'
        else:
            return False
        
        headers = {'Content-type': 'application/json'}
        try:
            response = requests.post(url,data=json.dumps(logs),headers=headers)
            # If the response was successful, no Exception will be raised
            print("This is the status code {}".format(response.status_code))
            #if 200 is received means that uplaod was successful
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as err:
            print('Other error occurred: {}'.format(err))  # Python 3.6
            return False

        
        
    
   
        
        

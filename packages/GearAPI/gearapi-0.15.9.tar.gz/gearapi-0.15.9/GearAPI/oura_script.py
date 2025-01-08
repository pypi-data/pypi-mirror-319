import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime, timezone, timedelta
import logging
from logging.handlers import RotatingFileHandler
import time
from GearAPI import client

"""
TODO:
1. use cumulocity-python-api to work with pushing data down to cumulocity?
2. create device digital twin

"""

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set up a rotating log handler (max size 5MB, keep 5 backups)
handler = RotatingFileHandler("exporter.log", maxBytes=5 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# oura credentials
# OURA_BASE_URL = ""
# OURA_BASE_TOKEN = ""

# Cumulocity credentials
# CUMULOCITY_BASE_URL = "https://thegear.jp.cumulocity.com"
# CUMULOCITY_USERNAME = "IoTOuraRing"
# CUMULOCITY_PASSWORD = r'?70R"89Z6Vqq!'

# STAGING Cumulocity credentials
CUMULOCITY_BASE_URL = "https://thegear-staging.jp.cumulocity.com"
CUMULOCITY_USERNAME = "hy.lim@kajima.com.sg"
CUMULOCITY_PASSWORD = "56ggO#123"


###utilities###
def utcdatetimenow() -> str:
        # Generate the current UTC time
        utc_now = datetime.now(timezone.utc)

        # Format the time to the desired format with UTC+8 offset
        utc_plus_8 = utc_now.astimezone(timezone(timedelta(hours=8)))
        formatted_time = utc_plus_8.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + utc_plus_8.strftime('%z')

        # Add the colon back into the timezone offset
        formatted_time = formatted_time[:-2] + ':' + formatted_time[-2:]

        return formatted_time

def cumulocity_datetimenow() -> str:
        # Generate the current UTC time
        utc_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        return utc_now

def make_request_with_retry(method, url, headers=None, params=None,data = None, auth= None, max_retries=3, backoff_factor=2):
    retry_attempts = 0
    while retry_attempts < max_retries:
        try:
            response = requests.request(method,url,headers=headers,params=params, data = json.dumps(data), auth=auth)
            response.raise_for_status()  # Check for HTTP errors
            print("response successful!")
            return response
        except requests.exceptions.RequestException as e:
            retry_attempts += 1
            if retry_attempts < max_retries:
                # Calculate backoff time (exponential)
                backoff_time = backoff_factor ** retry_attempts
                logging.info(f"Attempt {retry_attempts} failed. Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
            else:
                logging.info(f"Max retries reached. Request failed.")
                raise e
            

##END#####


def get_oura_data() -> dict:
    """
    daily ingestion of daily oura ring metrics data

    TODO: depend on how the data is return, might want to implement per participant_id ingestion strategy

    return:
        oura data of all participants in a day. JSON format.
    """

    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    logger.info(f"ingesting oura data between {yesterday} to {today}")

    def authenticate_users():
        """
        get credential for a particular user data
        """
        url = 'https://api.ouraring.com//v2/usercollection/personal_info'

        headers = { 
            'host': 'api.ouraring.com',
            'Authorization': 'Bearer <token>' 
        }

        print('authenticated!')


    authenticate_users()

    participants_ids = ('participant_id_001','participant_id_002','participant_id_003')


    data_dict = {'enhanced_tag': 'https://api.ouraring.com/v2/sandbox/usercollection/enhanced_tag',
        'workout': 'https://api.ouraring.com/v2/sandbox/usercollection/workout',
        'session' : 'https://api.ouraring.com/v2/sandbox/usercollection/session',
        'daily_activity': 'https://api.ouraring.com/v2/sandbox/usercollection/daily_activity',
        'daily_sleep' : 'https://api.ouraring.com/v2/sandbox/usercollection/daily_sleep',
        'daily_spo2' : 'https://api.ouraring.com/v2/sandbox/usercollection/daily_spo2',
        'daily_readiness' : 'https://api.ouraring.com/v2/sandbox/usercollection/daily_readiness',
        'sleep' : 'https://api.ouraring.com/v2/sandbox/usercollection/sleep',
        'sleep_time' : 'https://api.ouraring.com/v2/sandbox/usercollection/sleep_time',
        'rest_mode_period' : 'https://api.ouraring.com/v2/sandbox/usercollection/rest_mode_period',
        #'ring_configuration' : 'https://api.ouraring.com/v2/sandbox/usercollection/ring_configuration', #multiple user doesn't work
        'daily_stress' : 'https://api.ouraring.com/v2/sandbox/usercollection/daily_stress',
        'daily_resilience' : 'https://api.ouraring.com/v2/sandbox/usercollection/daily_resilience' ,
        'daily_cardiovascular_age' : 'https://api.ouraring.com/v2/sandbox/usercollection/daily_cardiovascular_age' ,
        'vO2_max' : 'https://api.ouraring.com/v2/sandbox/usercollection/vO2_max' ,
        
    }

    params={ 
        'start_date': yesterday, 
        'end_date': today
    }
    headers = { 
    'Authorization': 'Bearer <token>' 
    }

    data_to_ingest = {}

    for participants_id in participants_ids:
        
        participants_id_starttime = utcdatetimenow()

        data_to_ingest[participants_id] = {
            'data_start_date': yesterday,
            'data_end_date': today,
            'response_start_time': participants_id_starttime,
            'response_end_time': '',
            'data': {}
            } 
                          
        location_to_ingest = data_to_ingest[participants_id]['data']

        for k,v in data_dict.items():
            
            response = make_request_with_retry('GET', v, headers=headers, params=params) 

            try:

                data = response.json()
                data = data.get('data','')

                if isinstance(data,list):
                    location_to_ingest[k] = data[0]
                else:
                    location_to_ingest[k] = data
                

            except requests.exceptions.JSONDecodeError:
                logger.warning(f" {k} has JSONDecodeError for : {response.text}")

        participants_id_endtime = utcdatetimenow()
        data_to_ingest[participants_id]['response_end_time'] = participants_id_endtime
        logging.info(f"data for participant id {participants_id} is done!")

        print(data_to_ingest)

    return data_to_ingest


def transform_oura_data(data_to_ingest) -> json:
    """
    have to fake transform the data id into the oura device id
    """

    print('sensitive information masked!')

    masked_data_to_ingest = data_to_ingest

    return masked_data_to_ingest



def ingest_oura_data(oura_data) -> None:

    data_keys = ['enhanced_tag','workout','session','daily_activity','daily_sleep','daily_spo2','daily_readiness','sleep','sleep_time','rest_mode_period','daily_stress','daily_resilience','daily_cardiovascular_age','vO2_max']

    oura_cumulocity_mapping_dict = {
        '48227439576': "participant_id_001",
        '74227439577': 'participant_id_002',
        '69227438487': 'participant_id_003'
    }

    client.upload()
    

    def return_managed_object(id):
        url = f"{CUMULOCITY_BASE_URL}/inventory/managedObjects/{id}"
        managed_object = make_request_with_retry("GET", url, auth=HTTPBasicAuth(CUMULOCITY_USERNAME, CUMULOCITY_PASSWORD))
        json_object = managed_object.json()
        return json_object

    def create_event_data(data):
        url = f"{CUMULOCITY_BASE_URL}/event/events"


        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        make_request_with_retry("POST", url,auth=HTTPBasicAuth(CUMULOCITY_USERNAME, CUMULOCITY_PASSWORD), headers=headers, data = data)
        print('data posted successfully')


    for k,v in oura_cumulocity_mapping_dict.items():
        
        participant_oura_data = oura_data[v]['data']  #all participants_ids data -> single participant id data

        for data_key in data_keys:
            timenow = cumulocity_datetimenow()
            params = {
                'source': return_managed_object(k),
                'text': f" oura ring data with type {str(data_key)} from participant {v}",
                'time': str(timenow),
                'type': str(data_key),
                'c8y_ouraParticipantId': str(v),
                "c8y_ouraData": participant_oura_data.get(data_key)
            }
            print(params)
            create_event_data(params)
    


def create_oura_device():
        # Example device data to bulk create
    device_data = [
        {"name": "oura-001", "type": "oura_gen3", "c8y_IsDevice": {}, 'deviceType': "oura", 'subType': 'participant_id_001'},
        {"name": "oura-002", "type": "oura_gen3", "c8y_IsDevice": {}, 'deviceType': "oura", 'subType': 'participant_id_002'},
        {"name": "oura-003", "type": "oura_gen3", "c8y_IsDevice": {}, 'deviceType': "oura", 'subType': 'participant_id_003'}
    ]

    # Function to create a single device
    def create_device(device):
        url = f"{CUMULOCITY_BASE_URL}/inventory/managedObjects"
        make_request_with_retry('POST', url, auth=HTTPBasicAuth(CUMULOCITY_USERNAME, CUMULOCITY_PASSWORD), data=device)

    # Loop to create devices in bulk
    for device in device_data:
        create_device(device)

    #generated device id for each device name. go to cumulocity to see.

def main():
    # data = get_oura_data()
    # masked_data = transform_oura_data(data)

    # Specify the file path
    file_path = 'masked_data.json'

    # # Open the file in write mode and dump the JSON data
    # with open(file_path, 'w') as file:
    #     json.dump(masked_data, file, indent=4)

    with open(file_path, 'r') as file:
        masked_data = json.load(file)

    #create_oura_device()
    ingest_oura_data(masked_data)

if __name__ == "__main__":
    # Start Prometheus metrics server on port 8000
    main()
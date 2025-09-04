import logging
import requests


def initiated(data):
    initiated_data = {
        "cmd": "event",
        "type": "out",
        "event": "OUTGOING",
        "phone": "+380977032547",
        "diversion": data["from_number"],
        "ext": "vlad",
        "callid": data["call_sid"],
        "duration": "",
        "is_recorded": "",
        "status": "",
        "record_link": "",
        "planfix_token": data["planfix_auth_key"],
        "data_utm_source": "",
        "data_utm_medium": "",
    }

    url = data["planfix_api_url"]

    try:
        requests.post(url, data=initiated_data)
    except Exception as e:
        logging.exception(f"ERROR: {e}")


def ringing(data):
    ringing_data = {
        "cmd": "event",
        "type": "out",
        "event": "ACCEPTED",
        "phone": "+380977032547",
        "diversion": data["from_number"],
        "ext": "vlad",
        "callid": data["call_sid"],
        "duration": "",
        "is_recorded": "",
        "status": "",
        "record_link": "",
        "planfix_token": data["planfix_auth_key"],
        "data_utm_source": "",
        "data_utm_medium": "",
    }

    url = data["planfix_api_url"]

    try:
        requests.post(url, data=ringing_data)
    except Exception as e:
        logging.exception(f"ERROR: {e}")


def busy(data):
    busy_data = {
        "cmd": "event",
        "type": "out",
        "event": "COMPLETED",
        "phone": "+380977032547",
        "diversion": data["from_number"],
        "ext": "vlad",
        "callid": data["call_sid"],
        "duration": "0",
        "is_recorded": "0",
        "status": "Busy",
        "record_link": "",
        "planfix_token": data["planfix_auth_key"],
        "data_utm_source": "",
        "data_utm_medium": "",
    }

    url = data["planfix_api_url"]

    try:
        requests.post(url, data=busy_data)
    except Exception as e:
        logging.exception(f"ERROR: {e}")


def in_progress(data):
    in_progress_data = {
        "cmd": "event",
        "type": "out",
        "event": "OUTGOING",
        "phone": "+380977032547",
        "diversion": data["from_number"],
        "ext": "vlad",
        "callid": data["call_sid"],
        "duration": "",
        "is_recorded": "",
        "status": "",
        "record_link": "",
        "planfix_token": data["planfix_auth_key"],
        "data_utm_source": "",
        "data_utm_medium": "",
    }

    url = data["planfix_api_url"]

    try:
        requests.post(url, data=in_progress_data)
    except Exception as e:
        logging.exception(f"ERROR: {e}")


def completed(data):
    completed_data = {
        "cmd": "event",
        "type": "out",
        "event": "COMPLETED",
        "phone": "+380977032547",
        "diversion": data["from_number"],
        "ext": "vlad",
        "callid": data["call_sid"],
        "duration": "",
        "is_recorded": "1",
        "status": "Success",
        "planfix_token": data["planfix_auth_key"],
        "data_utm_source": "",
        "data_utm_medium": "",
    }

    if "record_link" in data:
        completed_data.update({"record_link": data["record_link"]})

    url = data["planfix_api_url"]

    try:
        requests.post(url, data=completed_data)
    except Exception as e:
        logging.exception(f"ERROR: {e}")

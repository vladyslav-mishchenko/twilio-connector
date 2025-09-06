import logging
import requests


def incoming_call_ringing(data):
    ringing_data = {
        "cmd": "event",
        "type": "in",
        "event": "INCOMING",
        "phone": data["phone"],
        "diversion": data["from_number"],
        "ext": data["ext"],
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


def incoming_call_failed(data):
    ringing_data = {
        "cmd": "event",
        "type": "in",
        "event": "INCOMING",
        "phone": data["phone"],
        "diversion": data["from_number"],
        "ext": data["ext"],
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


def incoming_call_busy(data):
    ringing_data = {
        "cmd": "event",
        "type": "in",
        "event": "INCOMING",
        "phone": data["phone"],
        "diversion": data["from_number"],
        "ext": data["ext"],
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


def incoming_call_no_answer(data):
    ringing_data = {
        "cmd": "event",
        "type": "in",
        "event": "INCOMING",
        "phone": data["phone"],
        "diversion": data["from_number"],
        "ext": data["ext"],
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


def incoming_call_completed(data):
    ringing_data = {
        "cmd": "event",
        "type": "in",
        "event": "COMPLETED",
        "phone": data["phone"],
        "diversion": data["from_number"],
        "ext": data["ext"],
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

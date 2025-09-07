import logging
import requests


def incoming_call_ringing(data):
    ringing_data = {
        "cmd": "event",
        "type": "in",
        "event": "INCOMING",
        "phone": data["from"],
        "diversion": data["to"],
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
    failed_data = {
        "cmd": "event",
        "type": "in",
        "event": "COMPLETED",
        "phone": data["from"],
        "diversion": data["to"],
        "ext": data["ext"],
        "callid": data["call_sid"],
        "duration": "",
        "is_recorded": "",
        "status": "Cancelled",
        "record_link": "",
        "planfix_token": data["planfix_auth_key"],
        "data_utm_source": "",
        "data_utm_medium": "",
    }

    url = data["planfix_api_url"]

    try:
        requests.post(url, data=failed_data)
    except Exception as e:
        logging.exception(f"ERROR: {e}")


def incoming_call_busy(data):
    busy_data = {
        "cmd": "event",
        "type": "in",
        "event": "COMPLETED",
        "phone": data["from"],
        "diversion": data["to"],
        "ext": data["ext"],
        "callid": data["call_sid"],
        "duration": "",
        "is_recorded": "",
        "status": "Missed",
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


def incoming_call_no_answer(data):
    no_answer_data = {
        "cmd": "event",
        "type": "in",
        "event": "COMPLETED",
        "phone": data["from"],
        "diversion": data["to"],
        "ext": data["ext"],
        "callid": data["call_sid"],
        "duration": "",
        "is_recorded": "",
        "status": "Missed",
        "record_link": "",
        "planfix_token": data["planfix_auth_key"],
        "data_utm_source": "",
        "data_utm_medium": "",
    }

    url = data["planfix_api_url"]

    try:
        requests.post(url, data=no_answer_data)
    except Exception as e:
        logging.exception(f"ERROR: {e}")


def incoming_call_completed(data):
    completed_data = {
        "cmd": "event",
        "type": "in",
        "event": "COMPLETED",
        "phone": data["from"],
        "diversion": data["to"],
        "ext": data["ext"],
        "callid": data["call_sid"],
        "status": "Success",
        "planfix_token": data["planfix_auth_key"],
        "data_utm_source": "",
        "data_utm_medium": "",
    }

    if "record" in data:
        completed_data.update({"is_recorded": data["record"]})
    else:
        completed_data.update({"is_recorded": "0"})

    if "record_link" in data:
        completed_data.update({"record_link": data["record_link"]})

    if "duration" in data:
        completed_data.update({"duration": data["duration"]})

    url = data["planfix_api_url"]

    try:
        requests.post(url, data=completed_data)
    except Exception as e:
        logging.exception(f"ERROR: {e}")

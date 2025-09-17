import os
import logging

import redis

import requests
from requests.auth import HTTPBasicAuth

from flask import Flask, jsonify, request, Response, render_template, make_response

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Dial

from call_statuses.outgoing import outgoing_call_initiated
from call_statuses.outgoing import outgoing_call_ringing
from call_statuses.outgoing import outgoing_call_busy
from call_statuses.outgoing import outgoing_call_in_progress
from call_statuses.outgoing import outgoing_call_completed

from call_statuses.incoming import incoming_call_ringing
from call_statuses.incoming import incoming_call_failed
from call_statuses.incoming import incoming_call_busy
from call_statuses.incoming import incoming_call_no_answer
from call_statuses.incoming import incoming_call_completed

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

# APP
APP_HOST = os.getenv("APP_HOST") or "Not found"
APP_TOKEN = os.getenv("APP_TOKEN") or "Not found"

# CRM
CRM_USER = os.getenv("CRM_USER") or "Not found"
CRM_API_URL = os.getenv("CRM_API_URL") or "Not found"
CRM_AUTH_KEY = os.getenv("CRM_AUTH_KEY") or "Not found"

# TWILIO
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID") or "Not found"
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN") or "Not found"
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER") or "Not found"

# SIP
SIP_CLIENT_ADDRESS = os.getenv("SIP_CLIENT_ADDRESS") or "Not found"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.route("/", methods=["GET"])
def home():
    """
    Render the homepage as an HTML page.

    Returns:
        Response: home.html
    """

    return render_template("home.html", title="Twilio Connector")


@app.route("/outgoing-call", methods=["POST"])
def outgoing_call():
    """
    Initiates an outgoing call using the Twilio SDK.

    - Extracts the phone number from the POST request form data.
    - Initiates a call to the specified phone number.

    Returns:

    """

    r.delete("ext_name", "destination_number", "twilio_number")

    form_data = request.form
    data = form_data.to_dict()

    to_number = data.get("to")
    ext = data.get("from")
    cmd = data.get("cmd")

    if cmd == "makeCall":

        r.set("ext_name", ext)
        r.set("destination_number", to_number)
        r.set("twilio_number", TWILIO_NUMBER)

        try:
            call = client.calls.create(
                to=SIP_CLIENT_ADDRESS,
                from_=TWILIO_NUMBER,
                url=f"{APP_HOST}/twilio/outgoing/twiml",
                status_callback=f"{APP_HOST}/twilio/outgoing/status",
                status_callback_method="POST",
                status_callback_event=["initiated", "ringing", "answered", "completed"],
            )

            logging.info(f"Call to SIP initiated. Call SID: {call.sid}")

            return make_response("", 200)
        except Exception:
            return make_response(jsonify(error="Invalid parameters"), 400)

    if cmd == "setup":
        return make_response("", 200)


@app.route("/twilio/outgoing/twiml", methods=["POST"])
def outgoing_twiml():
    """
    Generate TwiML instructions to handle an outgoing call via Twilio.

    This endpoint is called by Twilio when initiating an outgoing call. It
    builds and returns TwiML XML that instructs Twilio to dial the specified
    destination number with call recording enabled and answer on bridge behavior.

    Query Parameters:
        to (str): The destination phone number to dial.

    Returns:
        Response: An XML response containing TwiML instructions for the call.
    """

    response = VoiceResponse()
    destination_number = r.get("destination_number")

    dial = Dial(
        answer_on_bridge=True,
        record="record-from-answer-dual",
        caller_id=TWILIO_NUMBER,
        method="POST",
    )
    dial.number(destination_number)

    response.append(dial)

    return Response(str(response), mimetype="text/xml")


@app.route("/twilio/outgoing/status", methods=["POST"])
def outgoing_call_status():
    """
    Handle Twilio status callbacks for outgoing calls.

    This endpoint receives POST requests from Twilio containing updates
    about the status of an outgoing call.

    Returns:
        Response: HTTP 200
    """

    ext_name = r.get("ext_name")
    destination_number = r.get("destination_number")

    request_form_data = request.form
    form_data = request_form_data.to_dict()

    call_status = form_data.get("CallStatus")
    call_duration = form_data.get("CallDuration")

    call_data = {
        "from_number": form_data.get("From"),
        "call_sid": form_data.get("CallSid"),
        "phone": destination_number,
        "ext": ext_name,
        "planfix_api_url": CRM_API_URL,
        "planfix_auth_key": CRM_AUTH_KEY,
    }

    if call_status == "initiated":
        outgoing_call_initiated(call_data)

    if call_status == "ringing":
        outgoing_call_ringing(call_data)

    if call_status == "busy":
        outgoing_call_busy(call_data)

    if call_status == "in-progress":
        outgoing_call_in_progress(call_data)

    if call_status == "completed":
        call_sid = form_data.get("CallSid")

        recordings = client.calls(call_sid).recordings.list()

        for recording in recordings:
            recording_sid = recording.sid
            recording_url = f"{APP_HOST}/recording/{recording_sid}.mp3"

            call_data.update({"record": "1"})
            call_data.update({"record_link": recording_url})
            call_data.update({"duration": call_duration})

        outgoing_call_completed(call_data)

    return Response("OK", status=200)


@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    """
    Handle incoming call data sent via a JSON POST request.

    This endpoint expects a JSON payload containing information about an
    incoming call.

    Expected JSON structure:
        {
            "from": "<caller number>",
            "to": "<receiver number>",
            "callSid": "<unique call SID>",
            "callStatus": "<status of the call>"
        }

    Returns:
        Response: JSON response indicating success or failure.
            - On success: {"status": "received"} with HTTP 200.
            - On failure: {"error": <error message>} with HTTP 400 or 500.
    """

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        from_number = data.get("from")
        to_number = data.get("to")
        call_sid = data.get("callSid")
        call_status = data.get("callStatus")

        call_data = {
            "from": from_number,
            "call_sid": call_sid,
            "to": to_number,
            "ext": CRM_USER,
            "planfix_api_url": CRM_API_URL,
            "planfix_auth_key": CRM_AUTH_KEY,
        }

        if call_status == "ringing":
            incoming_call_ringing(call_data)

        return jsonify({"status": "received"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/twilio/incoming/status", methods=["POST"])
def incoming_call_status():
    """
    Handle Twilio status callbacks for incoming calls.

    Returns:
        Response: HTTP 204.
    """

    from_number = request.form.get("From")
    to_number = request.form.get("To")
    call_sid = request.form.get("CallSid")
    dial_call_status = request.form.get("DialCallStatus")
    dial_call_duration = request.form.get("DialCallDuration")

    call_data = {
        "from": from_number,
        "call_sid": call_sid,
        "to": to_number,
        "ext": CRM_USER,
        "planfix_api_url": CRM_API_URL,
        "planfix_auth_key": CRM_AUTH_KEY,
    }

    if dial_call_status == "failed":
        incoming_call_failed(call_data)

    if dial_call_status == "busy":
        incoming_call_busy(call_data)

    if dial_call_status == "no-answer":
        incoming_call_no_answer(call_data)

    if dial_call_status == "completed":

        call_sid = request.form.get("CallSid")

        recordings = client.calls(call_sid).recordings.list()

        for recording in recordings:
            recording_sid = recording.sid
            recording_url = f"{APP_HOST}/recording/{recording_sid}.mp3"

            call_data.update({"record": "1"})
            call_data.update({"record_link": recording_url})
            call_data.update({"duration": dial_call_duration})

        incoming_call_completed(call_data)

    return ("", 204)


@app.route("/recording/<recording_sid>.mp3")
def proxy_recording(recording_sid):
    twilio_url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Recordings/{recording_sid}.mp3"

    twilio_response = requests.get(
        twilio_url,
        auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
        stream=True,
    )

    if twilio_response.status_code == 200:
        return Response(
            twilio_response.iter_content(chunk_size=1024), content_type="audio/mpeg"
        )
    else:
        return f"Error: {twilio_response.status_code}", twilio_response.status_code

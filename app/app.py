from flask import Flask, jsonify, request, Response, render_template
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Dial
import os

# APP
APP_HOST = os.getenv("APP_HOST") or "Not found"
APP_TOKEN = os.getenv("APP_TOKEN") or "Not found"

# PLANFIX
PANFIX_API_URL = os.getenv("PANFIX_API_URL") or "Not found"
PANFIX_AUTH_KEY = os.getenv("PANFIX_AUTH_KEY") or "Not found"

# TWILIO
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID") or "Not found"
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN") or "Not found"
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER") or "Not found"
SIP_CLIENT_ADDRESS = os.getenv("SIP_CLIENT_ADDRESS") or "Not found"


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
        Response: JSON response indicating success or failure.
            - On success: {"status": "success", "message": "Call accepted"} with HTTP 200.
            - On failure: {"error": <error message>} with HTTP 500.
    """

    form_data = request.form
    data = form_data.to_dict()
    to_number = data.get("to")
    # from_name = data.get("from")

    print(data)

    try:
        call = client.calls.create(
            to=SIP_CLIENT_ADDRESS,
            from_=TWILIO_NUMBER,
            url=f"{APP_HOST}/twilio/outgoing/twiml?to={to_number}",
            status_callback=f"{APP_HOST}/twilio/outgoing/status",
            status_callback_method="POST",
            status_callback_event=["initiated", "ringing", "answered", "completed"],
        )

        print(f"Call to SIP initiated. Call SID: {call.sid}")

        return jsonify({"status": "success", "message": "Call accepted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

    print("outgoing call twiml")

    response = VoiceResponse()
    destination_number = request.args.get("to")

    dial = Dial(
        answer_on_bridge=True,
        record="record-from-answer-dual",
        caller_id=TWILIO_NUMBER,
        method="POST",
    )
    dial.number(destination_number)

    response.append(dial)

    return Response(str(response), mimetype="text/xml")


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

        print("Incoming call info:")
        print(f"  From       : {from_number}")
        print(f"  To         : {to_number}")
        print(f"  CallSid    : {call_sid}")
        print(f"  CallStatus : {call_status}")

        return jsonify({"status": "received"}), 200

    except Exception as e:
        print("Error handling incoming call:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/twilio/outgoing/status", methods=["POST"])
def outgoing_call_status():
    """
    Handle Twilio status callbacks for outgoing calls.

    This endpoint receives POST requests from Twilio containing updates
    about the status of an outgoing call.

    Returns:
        Response: HTTP 200
    """

    call_sid = request.form.get("CallSid")
    call_status = request.form.get("CallStatus")
    from_number = request.form.get("From")
    to_number = request.form.get("To")

    print("--------------------------------------")
    print(f"Status: {call_status}")
    print(f"From: {from_number} → To: {to_number}")
    print(f"SID: {call_sid}")
    print("--------------------------------------")

    return Response("OK", status=200)


@app.route("/twilio/incoming/status", methods=["POST"])
def incoming_call_status():
    """
    Handle Twilio status callbacks for incoming calls.

    Returns:
        Response: HTTP 200.
    """

    pass

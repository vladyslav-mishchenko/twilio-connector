exports.handler = async function (context, event, callback) {
  const axios = require('axios');
  const twiml = new Twilio.twiml.VoiceResponse();

  const callData = {
    from: event.From,
    to: event.To,
    callSid: event.CallSid,
    callStatus: event.CallStatus,
    direction: event.Direction,
  };

  try {
    await axios.post('https://app-host.app/incoming-call', callData, {
      timeout: 3000,
    });
  } catch (error) {
    console.error('Initial call data error:', error.message);
  }

  const dial = twiml.dial({
    record: 'record-from-answer-dual',
    action: 'https://app-host.app/twilio/incoming/status',
    method: 'POST',
  });

  // SIP URI (must be registered)
  dial.sip('sip:login@domain.sip.twilio.com');

  // Return valid TwiML
  return callback(null, twiml);
};

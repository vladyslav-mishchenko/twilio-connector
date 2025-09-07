exports.handler = function(context, event, callback) {
  const twilio = require('twilio');
  const VoiceResponse = twilio.twiml.VoiceResponse;

  const twiml = new VoiceResponse();

  const toHeader = event.To || '';
  
  // Extract phone number from the SIP URI (digits and optional leading +)
  const match = toHeader.match(/\+?\d+/);
  const phoneNumber = match ? match[0] : null;

  if (!phoneNumber) {
    twiml.say("Sorry, no valid phone number found to dial.");
    return callback(null, twiml);
  }

  // Dial with callerId (must be your Twilio verified number) and record the call
  const dial = twiml.dial({
    callerId: context.CALLER_ID || '+00000000000',
    record: 'record-from-answer-dual',
  });

  dial.number(phoneNumber);

  // Return TwiML response
  callback(null, twiml);
};
"""
One-time setup: Create inbound dispatch rule
Run this ONCE after setting up Twilio SIP trunk to route calls to the agent.
"""

import os
from dotenv import load_dotenv
from siphon.telephony.inbound import Dispatch
from siphon.plugins import openai, deepgram, cartesia

load_dotenv()

PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+18442585813")

llm = openai.LLM(model="gpt-4o-mini")
stt = deepgram.STT(model="nova-2")
tts = cartesia.TTS(voice_id=os.getenv("CARTESIA_VOICE_ID", "a0e99841-438c-4a64-b679-ae501e7d6091"))

dispatch = Dispatch(
    dispatch_name="mysterious-enterprise-inbound",
    agent_name="MysteriousReceptionist",
    sip_number=PHONE_NUMBER,
    llm=llm,
    stt=stt,
    tts=tts,
    system_instructions="You are a helpful AI receptionist for Mysterious Enterprise LLC.",
    greeting_instructions="Thank you for calling Mysterious Enterprise! This is your AI assistant. How can I help you today?",
)

result = dispatch.agent()
print(f"✅ Dispatch rule created for {PHONE_NUMBER}")
print(result)

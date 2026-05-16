"""
Mysterious Enterprise AI Receptionist
Built with LiveKit Agents — handles inbound phone calls 24/7.

Run locally:   uv run agent.py dev
Run console:   uv run agent.py console
Deploy:        lk app deploy
"""

import logging
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    RunContext,
    cli,
    function_tool,
    metrics,
    room_io,
)
from livekit.plugins import deepgram, openai, cartesia, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("mysterious-receptionist")

load_dotenv()


SYSTEM_PROMPT = """You are the AI receptionist for Mysterious Enterprise LLC, a premier mobile DJ and entertainment company based in Sacramento, California, owned by MC Mysterious (Marc Anthony).

YOUR PERSONALITY:
- Professional, friendly, and high-energy
- Confident but not pushy
- You represent a top-tier entertainment brand
- Keep it conversational — this is a phone call, not a lecture

COMPANY INFORMATION:
- Business: Mobile DJ & Entertainment Services
- Owner: MC Mysterious (Marc Anthony)
- Location: Sacramento, CA — travels up to 200 miles for events
- Email: ceo@mysteriousdj.com
- Website: crypticstore.shop
- BBB Accredited since February 2025

SERVICES & PRICING:
- Weddings: $500–$5,000 depending on package
- Corporate Events: $500–$3,000
- Private Parties & Birthdays: $100–$2,000
- Special Occasions: Custom quotes available
- Languages: English and Spanish
- Union Member: AFM & SAG-AFTRA
- 128+ verified bookings on GigSalad with top ratings

WHAT YOU CAN DO:
1. Answer questions about services, pricing, and availability
2. Collect caller's name, event date, event type, location, and phone/email
3. Let callers know Marc will follow up personally within 24 hours
4. Provide the email (ceo@mysteriousdj.com) for written inquiries

WHAT YOU CANNOT DO:
- Confirm bookings (only Marc can do that)
- Give exact quotes without Marc's approval — provide ranges instead
- Access Marc's calendar in real-time

CALL FLOW:
1. Greet: "Thank you for calling Mysterious Enterprise! This is your AI assistant. How can I help you today?"
2. Listen and help with their question
3. If they want to book: collect their info (name, event date, type, location, contact)
4. Close: "Awesome! I've got all your details. Marc — MC Mysterious himself — will get back to you within 24 hours. You know we do magic!"

RULES:
- Keep responses SHORT and conversational (this is a phone call, not an essay)
- If you don't know something, say "Let me have Marc get back to you on that"
- Always be enthusiastic about their event
- End calls with energy: "You know we do magic!" or "We're gonna make it legendary!"
- If someone asks for Marc directly, let them know he's currently unavailable but will call back ASAP
- If asked about the Cryptic Store or merchandise, mention crypticstore.shop
"""


class MysteriousReceptionist(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_PROMPT)

    async def on_enter(self):
        """Greet the caller when they connect."""
        self.session.generate_reply(
            instructions="Greet the caller warmly. Say: Thank you for calling Mysterious Enterprise! This is your AI assistant. How can I help you today?"
        )


server = AgentServer()


def prewarm(proc: JobProcess):
    """Pre-load VAD model for faster startup."""
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="mysterious-receptionist")
async def entrypoint(ctx: JobContext):
    """Main entrypoint — called for each incoming phone call."""
    ctx.log_context_fields = {"room": ctx.room.name}

    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(
            model="sonic-2",
            voice="a0e99841-438c-4a64-b679-ae501e7d6091",
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
    )

    # Metrics collection for observability
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics(ev):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Call usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    await session.start(
        agent=MysteriousReceptionist(),
        room=ctx.room,
        room_options=room_io.RoomOptions(),
    )


if __name__ == "__main__":
    cli.run_app(server)

# 🎧 Mysterious Enterprise AI Receptionist

AI-powered phone receptionist for Mysterious Enterprise LLC. Answers calls 24/7, provides service info, collects booking inquiries, and routes to MC Mysterious.

Built with [Siphon](https://github.com/blackdwarftech/siphon) — open-source voice AI.

## Cost

- **Twilio phone number:** $1.15/mo
- **Inbound calls:** $0.0085/min (Twilio) + ~$0.005/min (Deepgram) + ~$0.002/min (GPT-4o-mini) + ~$0.01/min (Cartesia)
- **Total:** ~$1.15/mo + ~$0.03/min per call
- **For 50 calls/mo × 2 min avg:** ~$4/mo total

## Quick Setup

### 1. Create Accounts (all have free tiers)

| Service | Purpose | Sign Up | Free Tier |
|---------|---------|---------|-----------|
| LiveKit | Media bridge | [cloud.livekit.io](https://cloud.livekit.io) | Free tier available |
| OpenAI | AI brain | [platform.openai.com](https://platform.openai.com) | Pay-as-you-go |
| Deepgram | Speech-to-text | [console.deepgram.com](https://console.deepgram.com) | $200 free credit |
| Cartesia | Text-to-speech | [play.cartesia.ai](https://play.cartesia.ai) | Free tier |
| Twilio | Phone number | [twilio.com](https://www.twilio.com) | Free trial |

### 2. Install & Configure

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run

```bash
python agent.py
```

### 4. Connect Twilio

Follow Siphon's [inbound setup guide](https://siphon.blackdwarf.in/docs) to connect your Twilio SIP trunk to the agent.

## Deployment

Use the included `Dockerfile` to deploy on any cloud:

```bash
docker build -t mysterious-receptionist .
docker run --env-file .env mysterious-receptionist
```

**Cheap hosting options:**
- [Railway](https://railway.app) — free tier available
- [Render](https://render.com) — free tier
- [Fly.io](https://fly.io) — free tier
- Any $4-5/mo VPS (DigitalOcean, Vultr)

## Customization

Edit `agent.py` to change:
- **System prompt** — update services, pricing, personality
- **Voice** — change `CARTESIA_VOICE_ID` in `.env`
- **LLM model** — swap `gpt-4o-mini` for any OpenAI model

# 🎧 Mysterious Enterprise AI Receptionist

AI-powered phone receptionist for Mysterious Enterprise LLC. Answers calls 24/7, provides service info, collects booking inquiries, and routes to MC Mysterious.

**Phone Number:** (844) 258-5813

## Architecture

```
Caller → Twilio → LiveKit SIP → AI Agent → Caller hears response
                                    ↓
                              Deepgram (STT)
                              GPT-4o-mini (LLM)
                              Cartesia (TTS)
```

## Cost Estimate

| Component | Cost |
|-----------|------|
| Twilio phone number | ~$1.15/mo |
| Deepgram STT | ~$0.005/min |
| GPT-4o-mini | ~$0.002/min |
| Cartesia TTS | ~$0.01/min |
| **Total per call** | **~$0.03/min** |
| **50 calls × 2 min avg** | **~$4/mo** |

## LiveKit SIP Infrastructure (Already Configured)

- **Inbound Trunk ID:** `ST_8tr2VFrGtSub`
- **Dispatch Rule ID:** `SDR_LCyaSJf7GMCy`
- **Agent Name:** `mysterious-receptionist`
- **SIP Endpoint:** `lux-lsvipm9g.sip.livekit.cloud`
- **SIP Auth User:** `mysterious_sip`
- **SIP Auth Password:** `Myst3r10us_SIP_2026!`

## Setup

### 1. Configure Twilio

In [Twilio Console](https://console.twilio.com):

1. Go to **Phone Numbers** → **Manage** → **Active Numbers** → select (844) 258-5813
2. Under **Voice Configuration** → **A call comes in**, select **TwiML Bin**
3. Create a new TwiML Bin with this content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial>
    <Sip username="mysterious_sip" password="Myst3r10us_SIP_2026!">
      sip:+18442585813@lux-lsvipm9g.sip.livekit.cloud;transport=tcp
    </Sip>
  </Dial>
</Response>
```

4. Save and assign the TwiML Bin to the phone number

### 2. Deploy the Agent

#### Option A: LiveKit Cloud (Recommended)

```bash
# Install LiveKit CLI
curl -sSL https://docs.livekit.io/install-cli.sh | bash

# Login to LiveKit Cloud
lk cloud auth

# Deploy
lk app deploy
```

#### Option B: Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Push this repo to GitHub
2. Connect Railway to the GitHub repo
3. Add environment variables (see `.env.example`)
4. Deploy

#### Option C: Any Docker host

```bash
docker build -t mysterious-receptionist .
docker run --env-file .env.local mysterious-receptionist
```

### 3. Set Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LIVEKIT_URL` | ✅ | `wss://lux-lsvipm9g.livekit.cloud` |
| `LIVEKIT_API_KEY` | ✅ | LiveKit API key |
| `LIVEKIT_API_SECRET` | ✅ | LiveKit API secret |
| `OPENAI_API_KEY` | ✅ | For GPT-4o-mini |
| `DEEPGRAM_API_KEY` | ✅ | For speech-to-text |
| `CARTESIA_API_KEY` | ✅ | For text-to-speech |

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run in dev mode (connects to LiveKit Cloud)
python agent.py dev

# Run in console mode (test without phone)
python agent.py console
```

## Customization

Edit `agent.py` to change:
- **System prompt** — update services, pricing, personality
- **Voice** — change voice ID in Cartesia TTS config
- **LLM** — swap `gpt-4o-mini` for `gpt-4o` or other models
- **STT** — change Deepgram model (e.g., `nova-3` for latest)

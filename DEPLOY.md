# Kascade Cloud - Deployment Guide

## Frontend (Vercel) - DONE ✅
```
URL: https://kascade-cloud.vercel.app
```

## Backend API (Render.com)

### Option 1: Connect GitHub Repo
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect: https://github.com/mizzleclawd/kascade-cloud
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn api.app:app`
   - Env Vars:
     - `STRIPE_SECRET_KEY` = your-stripe-key
     - `WHATSAPP_NUMBER` = +16155108553

### Option 2: CLI Deployment
```bash
railway login
railway init
railway up
```

## Environment Variables Needed
```bash
STRIPE_SECRET_KEY=sk_live_...
WHATSAPP_NUMBER=+16155108553
TELEGRAM_BOT_TOKEN=...
```

## Features Implemented
- [x] Landing page (Vercel)
- [x] Signup wizard (3 steps)
- [x] Customer dashboard
- [x] Usage tracking
- [x] WhatsApp integration

## Next Features
- [ ] Stripe payment processing
- [ ] Email notifications
- [ ] CRM integrations
- [ ] Multi-tenant isolation
- [ ] Analytics dashboard

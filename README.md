# Telegram UserBot (Heroku Deploy)

This is a Telegram UserBot controller that allows logging in with a session string and sending automated messages from your user account.

## Commands

- `/login` – Send session string
- `/setmessage <text>` – Set auto message
- `/settime <minutes>` – Set interval
- `/startauto` – Start messaging loop
- `/stopauto` – Stop messaging
- `/help` – Show help

## Deploy to Heroku

1. Get `API_ID`, `API_HASH` from https://my.telegram.org
2. Create bot using [@BotFather](https://t.me/BotFather)
3. Deploy this repo on Heroku
4. Set config vars
5. Send `/login` in bot and reply with session string (use Pyrogram to generate)

✅ Done!

# TalkMate

A small English conversation-practice web app built for real-life situations.

## Run locally

```powershell
cd D:\App\GiaoTiepAI
python app.py
```

Then open `http://127.0.0.1:5001`.

The app works in guided offline mode by default. To enable AI role-play and more tailored feedback, create a `.env` file in this folder:

```text
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## What is included

- Six role-play scenes across everyday and work contexts.
- A focused coach note after each response, including a natural rewrite when needed.
- Browser speech recognition for speaking replies where supported.
- Text-to-speech playback for partner replies.
- Speech clarity check after a microphone reply, including words to rehearse and slow/normal playback.
- Local progress, daily streak, completed scenes, and average score.
- Personal learning path: A1-C1 level plus travel, interview, work, or dating goal.
- Review Studio automatically creates small rewrite exercises from corrected learner sentences.
- Daily five-minute mission, XP, levels, streak, and unlockable badges.
- A 60-second Brave Mode speaking challenge with live transcript where browser speech recognition is available.
- Ten practical scenes, including phone calls, doctor visits, apartment rental, restaurant ordering, presentations, and meeting international travelers.
- Local TalkMate accounts with hashed passwords, cross-device progress sync through the server, completed-session history, and a seven-day activity chart.

## Pronunciation note

The pronunciation feature uses the browser's English speech recognition confidence as a transparent clarity estimate. It is useful for practice and targeted repetition, but it is not a replacement for a dedicated phoneme-level accent assessment service.

## Accounts and sync

Create an account from the **Sign in** button to sync learning data. When running locally, this stores data in `talkmate.db` on that computer. For multiple devices, deploy the same project to a shared host or run it on the same local network with a fixed `TALKMATE_SECRET_KEY`; both devices must open that same server address.

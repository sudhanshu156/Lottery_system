A terminal-based lottery system built in Python that allows users to register within a 1-hour window. After registration, a random winner is automatically selected and logged.

---

## Features

- ⏳ **1-Hour User Registration Window**
- ❌ Prevents duplicate and invalid usernames
- 📢 Displays remaining time every 10 minutes
- 👥 Live count of registered users
- ⏱️ Extends registration by 30 minutes if fewer than 5 users
- 🏆 Automatically selects a random winner
- 💾 Logs all users, timestamps, and winner in `lottery_log.txt`
- 🔄 Auto-save every 5 minutes (crash-resistant)

---

## 📁 Files

| File | Description |
|------|-------------|
| `lottery_system.py` | Main Python script |
| `users.json` | Stores registered users (used for crash recovery) |
| `lottery_log.txt` | Logs usernames, timestamps, and the winner |


---

## 🚀 How to Run

### Step 1: Clone or Download the Repo
```bash
git clone https://github.com/yourusername/lottery-system.git
cd lottery-system

import time
import threading
import json
import os
import random
from datetime import datetime, timedelta

USERS_FILE = 'users.json'
LOG_FILE = 'lottery_log.txt'
SAVE_INTERVAL = 300  # 5 minutes in seconds
UPDATE_INTERVAL = 600  # 10 minutes in seconds

registered_users = {}

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users():
    with open(USERS_FILE, 'w') as f:
        json.dump(registered_users, f)

def log_to_file(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()} - {message}\n")

def is_valid_username(username):
    return username.isalnum() and username.strip() != ""

def registration_phase(duration_seconds):
    global registered_users
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration_seconds)
    
    def autosave():
        while datetime.now() < end_time:
            save_users()
            time.sleep(SAVE_INTERVAL)

    def show_time_updates():
        while datetime.now() < end_time:
            time.sleep(UPDATE_INTERVAL)
            remaining = end_time - datetime.now()
            mins = remaining.seconds // 60
            print(f"\n[INFO] {mins} minutes left for registration.")
            print(f"[INFO] Registered Users: {len(registered_users)}\n")
    
    threading.Thread(target=autosave, daemon=True).start()
    threading.Thread(target=show_time_updates, daemon=True).start()

    print("\n--- Lottery Registration Open for 1 Hour ---\n")
    while datetime.now() < end_time:
        username = input("Enter a unique username to register: ").strip()
        if not is_valid_username(username):
            print("[ERROR] Invalid username. Use only letters/numbers. Try again.")
            continue
        if username in registered_users:
            print("[ERROR] Username already registered. Try another.")
            continue
        registered_users[username] = str(datetime.now())
        log_to_file(f"User Registered: {username}")
        print(f"[SUCCESS] {username} registered successfully!")

    return len(registered_users)

def draw_winner():
    users = list(registered_users.keys())
    winner = random.choice(users)
    log_to_file("\n--- Lottery Draw Complete ---")
    log_to_file(f"Participants: {', '.join(users)}")
    log_to_file(f"Winner: {winner}")
    
    print("\n🎉🎉🎉 Lottery Winner 🎉🎉🎉")
    print(f"Total Participants: {len(users)}")
    print(f"Congratulations, {winner}!")
    print("-------------------------------")

def main():
    global registered_users
    print("Welcome to the Terminal Lottery System!\n")
    registered_users = load_users()
    total_duration = 3600  # 1 hour

    user_count = registration_phase(total_duration)

    # Extend by 30 minutes if <5 users
    if user_count < 5:
        print("\n[NOTICE] Less than 5 users registered. Extending by 30 minutes...\n")
        log_to_file("Extension Triggered: Less than 5 users")
        user_count = registration_phase(1800)  # extra 30 minutes

    if len(registered_users) == 0:
        print("[INFO] No users registered. Exiting program.")
        log_to_file("No users registered. Program exited.")
        return

    draw_winner()

    # Final Save
    save_users()

    # Clean up (optional)
    os.remove(USERS_FILE)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted. Saving progress...")
        save_users()
        log_to_file("Program interrupted. Users saved.")


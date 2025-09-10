import os
import sys
import pandas as pd
import requests
import getpass

PAGERDUTY_API_URL = "https://api.pagerduty.com"
HEADERS = {
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Content-Type": "application/json"
}

def get_api_token():
    token = getpass.getpass("Enter your PagerDuty API token: ")
    HEADERS["Authorization"] = f"Token token={token}"
    return token

def get_csv_path():
    while True:
        path = input("Enter the full path to your CSV file with user emails: ").strip()
        if os.path.isfile(path):
            return path
        print("File not found. Please try again.")

def read_user_emails(csv_path):
    df = pd.read_csv(csv_path)
    if 'email' not in df.columns:
        print("CSV must have a column named 'email'.")
        sys.exit(1)
    return df['email'].tolist()

def get_user_id(email):
    resp = requests.get(f"{PAGERDUTY_API_URL}/users", headers=HEADERS, params={"query": email})
    resp.raise_for_status()
    users = resp.json().get("users", [])
    for user in users:
        if user["email"].lower() == email.lower():
            return user["id"]
    return None

def get_open_incidents(user_id):
    resp = requests.get(f"{PAGERDUTY_API_URL}/incidents", headers=HEADERS, params={
        "user_ids[]": user_id,
        "statuses[]": ["triggered", "acknowledged"]
    })
    resp.raise_for_status()
    return resp.json().get("incidents", [])

def close_incident(incident_id):
    data = {
        "incident": {
            "type": "incident_reference",
            "status": "resolved"
        }
    }
    resp = requests.put(f"{PAGERDUTY_API_URL}/incidents/{incident_id}", headers=HEADERS, json=data)
    resp.raise_for_status()

def delete_user(user_id):
    resp = requests.delete(f"{PAGERDUTY_API_URL}/users/{user_id}", headers=HEADERS)
    if resp.status_code not in (204, 202):
        print(f"Failed to delete user {user_id}: {resp.text}")

def main():
    print("PagerDuty Bulk User Deletion Script")
    get_api_token()
    csv_path = get_csv_path()
    emails = read_user_emails(csv_path)
    print(f"\nFound {len(emails)} users in the CSV.")

    # Gather user IDs and open incidents
    user_map = {}
    users_with_open_incidents = []
    total_open_incidents = 0

    print("\nChecking users and their open incidents...")
    for email in emails:
        user_id = get_user_id(email)
        if not user_id:
            print(f"User not found: {email}")
            continue
        incidents = get_open_incidents(user_id)
        user_map[email] = {"id": user_id, "incidents": incidents}
        if incidents:
            users_with_open_incidents.append(email)
            total_open_incidents += len(incidents)

    print(f"\nSummary:")
    print(f"Total users found: {len(user_map)}")
    print(f"Users with open incidents: {len(users_with_open_incidents)}")
    print(f"Total open incidents: {total_open_incidents}")

    # Confirm deletion
    confirm = input(f"\nAre you sure you want to delete {len(user_map)} users? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Aborted.")
        sys.exit(0)

    # Incident handling options
    if users_with_open_incidents:
        print("\nSome users have open incidents. Choose an option:")
        print("1. Only delete users with no open incidents")
        print("2. Delete users with no open incidents, plus select from users with open incidents")
        print("3. Delete all users and close all their open incidents")
        choice = input("Enter 1, 2, or 3: ").strip()
    else:
        choice = "3"

    users_to_delete = []
    incidents_to_close = []

    if choice == "1":
        users_to_delete = [email for email in user_map if email not in users_with_open_incidents]
    elif choice == "2":
        users_to_delete = [email for email in user_map if email not in users_with_open_incidents]
        print("\nSelect users with open incidents to also delete (comma-separated numbers):")
        for idx, email in enumerate(users_with_open_incidents, 1):
            print(f"{idx}. {email} ({len(user_map[email]['incidents'])} open incidents)")
        selected = input("Enter numbers (e.g., 1,3,5): ").strip()
        selected_idxs = [int(x) for x in selected.split(",") if x.strip().isdigit()]
        for idx in selected_idxs:
            if 1 <= idx <= len(users_with_open_incidents):
                users_to_delete.append(users_with_open_incidents[idx-1])
    elif choice == "3":
        users_to_delete = list(user_map.keys())
        for email in users_with_open_incidents:
            incidents_to_close.extend(user_map[email]['incidents'])
    else:
        print("Invalid choice. Aborted.")
        sys.exit(1)

    print(f"\nUsers to delete: {len(users_to_delete)}")
    if choice == "3":
        print(f"Incidents to close: {len(incidents_to_close)}")

    final_confirm = input("Proceed with these actions? (yes/no): ").strip().lower()
    if final_confirm != "yes":
        print("Aborted.")
        sys.exit(0)

    # Close incidents if needed
    if choice == "3":
        print("\nClosing incidents...")
        for incident in incidents_to_close:
            close_incident(incident["id"])
        print("All incidents closed.")

    # Delete users
    print("\nDeleting users...")
    for email in users_to_delete:
        user_id = user_map[email]["id"]
        delete_user(user_id)
        print(f"Deleted user: {email}")

    print("\nDone!")

if __name__ == "__main__":
    main()

# Bulk PagerDuty User Deletion Script

This script allows you to safely and interactively delete multiple PagerDuty users in bulk, with options for handling open incidents. It works on both Mac and Windows.

## Features

- Select a CSV file containing user emails.
- See a summary of users and their open incidents before deletion.
- Choose how to handle users with open incidents (skip, select, or close all).
- Double confirmation before any destructive action.
- Closes incidents if you choose.

---

## Prerequisites

- **Python 3.7+** installed on your system.
- A **PagerDuty API token** with permissions to manage users and incidents.
- A **CSV file** with a column named `email` containing the users you want to delete.

---

## Step-by-Step Instructions

### 1. Download the Script

- Download the script file (e.g., `bulk_pd_user_delete.py`) from this repository.
- Save it to a folder on your computer.

### 2. Install Required Python Packages

Open a terminal (Mac/Linux) or Command Prompt (Windows) and run: **pip install pandas requests**

If you have multiple versions of Python, you may need to use `pip3` instead of `pip`.

### 3. Prepare Your CSV File

Create a CSV file with a column named `email`.

**Example:**

**email**
user1@example.com
user2@example.com
user3@example.com

Save this file somewhere you can easily find it (e.g., your Desktop or Downloads folder).

### 4. Get Your PagerDuty API Token

- Log in to PagerDuty.
- Go to **Integrations > API Access Keys**.
- Click **Create New API Key**.
- Copy the generated token and keep it handy (you’ll be prompted for it when running the script).

---

### 5. Run the Script

In your terminal or command prompt, navigate to the folder where you saved the script. For example: **cd /path/to/your/script.csv**

Then run: **python bulk_pd_user_delete.py**

### 6. Follow the Prompts

- **Enter your PagerDuty API token** when prompted (it will not be shown on screen).
- **Enter the full path to your CSV file** (e.g., `/Users/yourname/Desktop/users.csv` or `C:\Users\yourname\Desktop\users.csv`).

The script will:

- Show you how many users were found.
- Check for open incidents for each user.
- Show a summary and ask for confirmation.
- If users have open incidents, you’ll be given three options:
    1. Only delete users with no open incidents.
    2. Delete users with no open incidents, plus select from users with open incidents.
    3. Delete all users and close all their open incidents.
- You’ll be asked to confirm your choices before anything is deleted or closed.

---

### 7. Review Results

- The script will print the status of each user deletion and any incidents closed.
- When finished, you’ll see a “Done!” message.

---

### Troubleshooting

- **File Not Found:** Double-check the path to your CSV file.
- **Permission Errors:** Make sure your API token has the correct permissions.
- **CSV Format Issues:** Ensure your CSV has a column named `email`.

---

### Safety Notes

- The script is interactive and will not delete anything without your explicit confirmation.
- Always review the summary before confirming deletion.

---

### License

MIT

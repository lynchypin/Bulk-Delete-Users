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

Open a terminal (Mac/Linux) or Command Prompt (Windows) and run:

```sh
pip install pandas requests

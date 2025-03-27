# Monadscore Auto Referral & Node Automation

This project provides an automated Python script to manage and run accounts on the Monadscore platform.

## Features

- **Auto Referral Mode:**
  - Registers new accounts with a referral code (from `codes.txt` or user input).
  - Claims three tasks in a randomized order.
  - Starts the node immediately after account creation.
  - Logs detailed, color-coded messages.
  - Saves account details to `accounts.json` and referral codes to `createdaccrefs.txt`.

- **Auto Run Node Mode:**
  - Automatically detects and processes all accounts in `accounts.json`.
  - Updates each node’s status and retrieves total points via a login endpoint.
  - Supports proxy modes (rotating or private) with fallback to alternate proxies if one fails.
  - Runs in a continuous loop (cycles every hour) for 24/7 operation.
  - Displays colorful logs for each operation.

## Requirements

- Python 3.6+
- VPS(Optional)
- Proxy(Optional but recommended)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kelliark/MonadScore-AutoBot.git
   cd MonadScore-AutoBot
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare configuration files:**
   - **accounts.json:** Stores account details (created by the script).
   - **codes.txt:** Contains referral codes (one per line).
   - **proxy.txt:** Contains proxy addresses (one per line).
   - **createdaccrefs.txt:** Will store referral codes of created accounts.

2. **Run the script:**

   ```bash
   python main.py
   ```

3. **Follow on-screen instructions:**
   - Choose **Auto Referral Mode** to create accounts, claim tasks, and start nodes.
   - Choose **Auto Run Node Mode** to continuously update the status of existing accounts every hour.
   - Configure proxy usage as desired.


## Contributing

Contributions, issues, and feature requests are welcome!

---

**Disclaimer:**  
This project is provided for educational purposes only. Use it responsibly and at your own risk. The author is not responsible for any misuse or damage caused by this script.

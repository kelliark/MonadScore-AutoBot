import random
import requests
import json
from eth_account import Account
import time
from colorama import Fore, Style

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; U; Android 12; en-US; SM-A515F) AppleWebKit/537.36 Chrome/95.0.4638.74 Mobile Safari/537.36"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_headers():
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }

def get_task_headers():
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://monadscore.xyz/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

def get_public_ip(proxy=None, fallback_proxies=None):
    proxies_to_try = []
    if proxy:
        proxies_to_try.append(proxy)
    if fallback_proxies:
        for p in fallback_proxies:
            if p != proxy:
                proxies_to_try.append(p)
    # Try using each proxy
    for p in proxies_to_try:
        try:
            proxies_dict = {"http": p, "https": p}
            resp = requests.get("http://ip-api.com/json", headers=get_headers(), proxies=proxies_dict, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("query", "IP not found"), p
        except Exception as e:
            print(f"{Fore.RED}Error fetching IP with proxy {p}: {e}{Style.RESET_ALL}")
            continue
    # Finally, try without any proxy
    try:
        resp = requests.get("http://ip-api.com/json", headers=get_headers(), timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("query", "IP not found"), None
        else:
            return "IP not found", None
    except Exception as e:
        return f"Error: {e}", None

def read_codes(filename="codes.txt"):
    try:
        with open(filename, "r") as f:
            codes = [line.strip() for line in f if line.strip()]
        return codes
    except Exception:
        return []

def read_proxies(filename="proxy.txt"):
    try:
        with open(filename, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies
    except Exception:
        return []

def read_accounts(filename="accounts.json"):
    try:
        with open(filename, "r") as f:
            accounts = json.load(f)
        return accounts
    except Exception:
        return []

def write_accounts(accounts, filename="accounts.json"):
    try:
        with open(filename, "w") as f:
            json.dump(accounts, f, indent=2)
    except Exception as e:
        print(f"Error writing accounts: {str(e)}")

def generate_wallet():
    acct = Account.create()
    return {"address": acct.address, "private_key": acct.key.hex()}

def write_created_ref_code(ref_code, filename="createdaccrefs.txt"):
    try:
        with open(filename, "a") as f:
            f.write(ref_code + "\n")
    except Exception as e:
        print(f"Error writing referral code: {str(e)}")

def delay(seconds):
    time.sleep(seconds)

def update_start_time(wallet_obj, proxy):
    wallet_address = wallet_obj.get("address") or wallet_obj.get("walletAddress")
    try:
        payload = {"wallet": wallet_address, "startTime": int(time.time() * 1000)}
        proxies_dict = {"http": proxy, "https": proxy} if proxy else None
        resp = requests.put("https://mscore.onrender.com/user/update-start-time",
                            json=payload,
                            headers=get_task_headers(),
                            timeout=30,
                            proxies=proxies_dict)
        if resp.status_code == 200:
            data = resp.json()
            msg = data.get("message", "").lower()
            totalPoints = data.get("user", {}).get("totalPoints", "N/A")
            if "already" in msg:
                return True, "Node is already running!", totalPoints
            elif data.get("success") is True:
                return True, "Running Node Successfully!", totalPoints
            else:
                return False, f"Update start time failed: {resp.text}", "N/A"
        else:
            return False, f"Update start time failed: {resp.text}", "N/A"
    except Exception as e:
        return False, f"Error updating start time: {e}", "N/A"

def login_account(wallet_obj, proxy):
    wallet_address = wallet_obj.get("address") or wallet_obj.get("walletAddress")
    try:
        payload = {"wallet": wallet_address}
        proxies_dict = {"http": proxy, "https": proxy} if proxy else None
        resp = requests.post("https://mscore.onrender.com/user/login",
                             json=payload,
                             headers=get_task_headers(),
                             timeout=30,
                             proxies=proxies_dict)
        if resp.status_code == 200:
            data = resp.json()
            totalPoints = data.get("user", {}).get("totalPoints", "N/A")
            return True, totalPoints
        else:
            return False, "N/A"
    except Exception as e:
        return False, "N/A"

def claim_tasks(wallet, proxy):
    from colorama import Fore, Style
    import random
    print(f"{Fore.CYAN}Doing Task...{Style.RESET_ALL}")
    all_success = True
    TASKS = ["task003", "task002", "task001"]
    random.shuffle(TASKS)
    print(f"{Fore.MAGENTA}Task order: {TASKS}{Style.RESET_ALL}")
    for task in TASKS:
        try:
            payload = {"wallet": wallet["address"], "taskId": task}
            proxies_dict = {"http": proxy, "https": proxy} if proxy else None
            resp = requests.post("https://mscore.onrender.com/user/claim-task",
                                 json=payload,
                                 headers=get_task_headers(),
                                 timeout=30,
                                 proxies=proxies_dict)
            if resp.status_code == 200 and resp.json().get("success") is True:
                print(f"{Fore.GREEN}Claim task {task} succeeded.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Claim task {task} failed: {resp.text}{Style.RESET_ALL}")
                all_success = False
        except Exception as e:
            print(f"{Fore.RED}Error claiming task {task}: {e}{Style.RESET_ALL}")
            all_success = False
    if all_success:
        print(f"{Fore.GREEN}All tasks succeeded!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Some tasks failed.{Style.RESET_ALL}")
    return all_success

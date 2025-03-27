import random
import time
import requests
from core.banner import show_banner_referral, show_banner_run_node
from core.utils import (
    get_headers,
    get_task_headers,
    get_public_ip,
    read_codes,
    read_proxies,
    read_accounts,
    write_accounts,
    generate_wallet,
    write_created_ref_code,
    delay,
    update_start_time,
    login_account,
    claim_tasks
)
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def auto_referral():
    show_banner_referral()
    
    use_proxy_input = input(f"{Fore.CYAN}Use proxy for referral mode? (y/n): {Style.RESET_ALL}").strip().lower()
    referral_proxy = None
    if use_proxy_input == 'y':
        proxies = read_proxies()
        if proxies:
            referral_proxy = random.choice(proxies)
            print(f"{Fore.MAGENTA}Using proxy: {referral_proxy}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No proxies found in proxy.txt. Continuing without proxy.{Style.RESET_ALL}")
    
    codes = read_codes()
    if codes:
        referral = random.choice(codes)
        print(f"{Fore.CYAN}Using referral code from file: {referral}{Style.RESET_ALL}")
    else:
        referral = input(f"{Fore.CYAN}Enter referral code: {Style.RESET_ALL}").strip()
    
    try:
        count = int(input(f"{Fore.CYAN}Enter number of accounts to create: {Style.RESET_ALL}").strip())
    except ValueError:
        print(f"{Fore.RED}Invalid number.{Style.RESET_ALL}")
        return
    
    accounts = read_accounts()
    success = 0
    fail = 0
    
    for i in range(count):
        print(f"\n{Fore.CYAN}Creating account {i+1}/{count}{Style.RESET_ALL}")
        ip = get_public_ip(referral_proxy)
        print(f"{Fore.YELLOW}Ip used: {ip}{Style.RESET_ALL}")
        wallet = generate_wallet()
        print(f"{Fore.YELLOW}Generated Wallet: {wallet['address']}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}Registering account...{Style.RESET_ALL}")
        try:
            payload = {"wallet": wallet["address"], "invite": referral}
            proxies_dict = {"http": referral_proxy, "https": referral_proxy} if referral_proxy else None
            resp = requests.post("https://mscore.onrender.com/user", json=payload,
                                 headers=get_headers(), timeout=50, proxies=proxies_dict)
            data = resp.json()
            if data.get("success") is True:
                print(f"{Fore.GREEN}Registration Successful! Saved to accounts.json{Style.RESET_ALL}")
                success += 1
                accounts.append({
                    "walletAddress": wallet["address"],
                    "privateKey": wallet["private_key"]
                })
                write_accounts(accounts)
                if data.get("user", {}).get("referralCode"):
                    write_created_ref_code(data["user"]["referralCode"])
            else:
                print(f"{Fore.RED}Registration failed: {data.get('message', 'No message')}{Style.RESET_ALL}")
                fail += 1
                continue
        except Exception as e:
            print(f"{Fore.RED}Error during registration: {e}{Style.RESET_ALL}")
            fail += 1
            continue
        
        # Claim tasks
        claim_tasks(wallet, referral_proxy)
        
        # Start the node immediately after referral
        success_node, node_msg, _ = update_start_time(wallet, referral_proxy)
        print(f"{Fore.YELLOW}Running Node...{Style.RESET_ALL}")
        if success_node:
            print(f"{Fore.GREEN}{node_msg}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{node_msg}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Node Started Successfully for {wallet['address']}!{Style.RESET_ALL}")
        
        wait_time = random.randint(3, 5)
        print(f"{Fore.MAGENTA}Waiting {wait_time} seconds before next account...{Style.RESET_ALL}\n")
        delay(wait_time)
    print(f"\n{Fore.CYAN}Finished registration. Success: {success}, Fail: {fail}{Style.RESET_ALL}")

def auto_run_node():
    show_banner_run_node()
    print(f"{Fore.CYAN}Choose Proxy Mode:{Style.RESET_ALL}")
    print("1. Auto run with Monosans Proxies (Rotating)")
    print("2. Auto run with Private Proxies")
    print("3. Auto run without any proxies")
    proxy_choice = input(f"{Fore.CYAN}Enter your choice (1/2/3): {Style.RESET_ALL}").strip()
    
    base_proxies = []
    proxy = None
    if proxy_choice in ["1", "2"]:
        base_proxies = read_proxies()
        if not base_proxies:
            print(f"{Fore.RED}No proxies found in proxy.txt. Running without proxies.{Style.RESET_ALL}")
            proxy_choice = "3"
        elif proxy_choice == "2":
            proxy = base_proxies.pop(0)
    
    while True:
        accounts = read_accounts()
        if not accounts:
            print(f"{Fore.RED}No accounts found in accounts.json. Exiting.{Style.RESET_ALL}")
            return
        
        total_accounts = len(accounts)
        print(f"{Fore.CYAN}Found {total_accounts} account(s) in accounts.json.{Style.RESET_ALL}")
        last_refresh = time.time()
        
        for i, account in enumerate(accounts):
            print(f"\n{Fore.CYAN}Account {i+1}/{total_accounts}{Style.RESET_ALL}")
            current_proxy = None
            if proxy_choice == "1":
                if time.time() - last_refresh > 300:
                    base_proxies = read_proxies()
                    last_refresh = time.time()
                if base_proxies:
                    current_proxy = random.choice(base_proxies)
            elif proxy_choice == "2":
                current_proxy = proxy

            # Use fallback proxies in get_public_ip call.
            ip, used_proxy = get_public_ip(current_proxy, fallback_proxies=base_proxies)
            if used_proxy and used_proxy != current_proxy:
                current_proxy = used_proxy
            print(f"{Fore.YELLOW}Ip Used: {ip}{Style.RESET_ALL}")
            
            # Print "Running Node..." on its own line
            print(f"{Fore.YELLOW}Running Node...{Style.RESET_ALL}")
            attempt = 0
            success_flag = False
            message = ""
            totalPoints = "N/A"
            while attempt < 3 and not success_flag:
                success_flag, message, totalPoints = update_start_time(account, current_proxy)
                if not success_flag:
                    if proxy_choice in ["1", "2"]:
                        available = read_proxies()
                        if available:
                            current_proxy = random.choice(available)
                            print(f"{Fore.MAGENTA}Proxy failed; switching to: {current_proxy}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}No alternative proxies available; proceeding without proxy.{Style.RESET_ALL}")
                            current_proxy = None
                    attempt += 1
                else:
                    break
            # Print node result on a new line
            print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Total Points: {totalPoints}{Style.RESET_ALL}")
            
            wait_time = random.randint(1, 3)
            print(f"{Fore.MAGENTA}Waiting {wait_time} seconds to activate next account...{Style.RESET_ALL}\n")
            delay(wait_time)
        
        print(f"\n{Fore.CYAN}Auto Run Node processing completed for this cycle.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Waiting 1 hour before reprocessing all accounts...{Style.RESET_ALL}\n")
        delay(3600)

def main():
    print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
    print("1. Auto Referral")
    print("2. Auto Run Node")
    choice = input(f"{Fore.CYAN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
    if choice == "1":
        auto_referral()
    elif choice == "2":
        auto_run_node()
    else:
        print(f"{Fore.RED}Invalid choice. Exiting.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
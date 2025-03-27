import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner_referral():
    clear_terminal()
    banner = r"""
===========================================
             AUTO REFERRAL MODE
                BY KELLIARK
===========================================
    """
    print(banner)

def show_banner_run_node():
    clear_terminal()
    banner = r"""
===========================================
              AUTO RUN NODE MODE
                 BY KELLIARK
===========================================
    """
    print(banner)
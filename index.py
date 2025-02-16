import requests
import random
import os
import time
from dataclasses import dataclass
from data.logger import NovaLogger
from typing import List, Optional
from datetime import datetime
from threading import Lock, Thread
from queue import Queue, Empty
from colorama import init, Fore, Style




banner = f"""
{Fore.CYAN}
                        █████▒██▓ ██▓     ██▓   ▓██   ██▓
                        ▓██   ▒▓██▒▓██▒    ▓██▒    ▒██  ██▒
                        ▒████ ░▒██▒▒██░    ▒██░     ▒██ ██░
                        ░▓█▒  ░░██░▒██░    ▒██░     ░ ▐██▓░
                        ░▒█░   ░██░░██████▒░██████▒ ░ ██▒▓░
                        ▒ ░   ░▓  ░ ▒░▓  ░░ ▒░▓  ░  ██▒▒▒ 
                        ░      ▒ ░░ ░ ▒  ░░ ░ ▒  ░▓██ ░▒░ 
                        ░ ░    ▒ ░  ░ ░     ░ ░   ▒ ▒ ░░  
                                ░      ░  ░    ░  ░░ ░     
                                                ░ ░     

                        {Fore.LIGHTCYAN_EX}https://discord.gg/api{Style.RESET_ALL}

                {Fore.YELLOW}HypeSquad Badge Claimer {Style.RESET_ALL}
"""

init(autoreset=True)

@dataclass
class DiscordAccount:
    email: str
    password: str
    token: str
    
    @property
    def masked_token(self) -> str:
        if len(self.token) > 10:
            return f"{self.token[:6]}...{self.token[-4:]}"
        return "INVALID_TOKEN"

    @classmethod
    def from_combo_line(cls, line: str) -> Optional['DiscordAccount']:
        try:
            parts = line.strip().split(':')
            if len(parts) == 3:
                email, password, token = parts
                return cls(email=email, password=password, token=token)
            elif len(parts) == 1 and len(parts[0]) > 50:  
                token = parts[0]
                return cls(email="unknown", password="unknown", token=token)
            return None
        except Exception:
            return None

class HypeSquadClaimer:
    HOUSE_NAMES = {
        1: "Bravery",
        2: "Brilliance",
        3: "Balance"
    }

    def __init__(self, max_threads: int = 3, debug: bool = True, log_file: str = 'hypesquad.log'):
        """Initialize the HypeSquad claimer."""
        NovaLogger.config(debug=debug, log_file=log_file)
        self.max_threads = max_threads
        self.queue = Queue()
        self.successful_claims = 0
        self.failed_claims = 0
        self.rate_limited_accounts = []
        self._lock = Lock()
        self._running = True

    def read_accounts(self, file_path: str) -> List[DiscordAccount]:
        accounts = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    if account := DiscordAccount.from_combo_line(line):
                        accounts.append(account)
                    else:
                        NovaLogger.fail(f"Invalid format at line {line_num}: {line.strip()}")
            
            NovaLogger.note(f"Successfully loaded {len(accounts)} accounts")
            return accounts
        except FileNotFoundError:
            NovaLogger.fail(f"Error: Accounts file '{file_path}' not found")
            return []
        except Exception as e:
            NovaLogger.fail(f"Error reading accounts file: {str(e)}")
            return []

    def claim_hypesquad_badge(self, account: DiscordAccount) -> bool:
        session = requests.Session()
        session.headers.update({
            'Authorization': account.token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        house_id = random.randint(1, 3)
        json_data = {'house_id': house_id}

        try:
            NovaLogger.trace(f"Attempting to claim house {self.HOUSE_NAMES[house_id]} for {account.email}")
            
            response = session.post(
                'https://discord.com/api/v9/hypesquad/online',
                json=json_data,
                timeout=10
            )
            
            if response.status_code == 204:
                with self._lock:
                    self.successful_claims += 1
                NovaLogger.win(
                    f"Claimed {self.HOUSE_NAMES[house_id]} badge",
                    email=account.email,
                    token=account.masked_token
                )
                return True
            
            elif response.status_code == 401:
                with self._lock:
                    self.failed_claims += 1
                NovaLogger.fail(
                    "Invalid token",
                    email=account.email,
                    token=account.masked_token
                )
            
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                with self._lock:
                    self.rate_limited_accounts.append(account)
                NovaLogger.alert(
                    f"Rate limited",
                    email=account.email,
                    retry_after=f"{retry_after}s"
                )
            
            else:
                with self._lock:
                    self.failed_claims += 1
                NovaLogger.fail(
                    f"Failed to claim badge",
                    email=account.email,
                    status=response.status_code,
                    response=response.text[:100]
                )
            
            return False

        except requests.RequestException as e:
            with self._lock:
                self.failed_claims += 1
            NovaLogger.fail(
                f"Request error",
                email=account.email,
                error=str(e)
            )
            return False
        
        finally:
            session.close()

    def worker(self):
        while self._running:
            try:
                try:
                    account = self.queue.get_nowait()
                except Empty:
                    break
                
                self.claim_hypesquad_badge(account)
                self.queue.task_done()
                time.sleep(random.uniform(1, 3)) 
            
            except Exception as e:
                NovaLogger.fail(f"Worker thread error: {str(e)}")
                break

    def run(self, accounts_file: str = 'input/accounts.txt'):
        start_time = time.time()
        accounts = self.read_accounts(accounts_file)
        
        if not accounts:
            NovaLogger.alert("No valid accounts found. Exiting.")
            return

        NovaLogger.event(f"Starting badge claimer with {self.max_threads} threads")

        for account in accounts:
            self.queue.put(account)

        threads = []
        for _ in range(min(self.max_threads, len(accounts))):
            thread = Thread(target=self.worker)
            thread.daemon = True  
            thread.start()
            threads.append(thread)

        self.queue.join()
        
        self._running = False
        
        for thread in threads:
            thread.join(timeout=1.0)  

        if self.rate_limited_accounts:
            NovaLogger.alert(f"Processing {len(self.rate_limited_accounts)} rate-limited accounts...")
            time.sleep(60)  
            for account in self.rate_limited_accounts:
                self.claim_hypesquad_badge(account)

        elapsed_time = time.time() - start_time
        
        NovaLogger.note("\nResults Summary:")
        NovaLogger.note(f"Total accounts processed: {len(accounts)}")
        NovaLogger.win(f"Successful claims: {self.successful_claims}")
        NovaLogger.fail(f"Failed claims: {self.failed_claims}")
        NovaLogger.event(f"Time elapsed: {elapsed_time:.2f} seconds")

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        
        claimer = HypeSquadClaimer(max_threads=3)
        claimer.run()
    except KeyboardInterrupt:
        NovaLogger.alert("\nProcess interrupted by user. Cleaning up...")
    except Exception as e:
        NovaLogger.fail(f"Unexpected error: {str(e)}")
    finally:
        NovaLogger.close()

if __name__ == "__main__":
    main()
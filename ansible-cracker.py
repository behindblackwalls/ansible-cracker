import threading
import subprocess
import queue
import sys

ascii_art = """---------------------------------------------
                       _
                   _ooOoo_
                  o8888888o
                  88\" . \"88
                  (| -_- |)
                  O\\  =  /O
               ____/`---'\\____
             .'  \\\\|     |//  `.
            /  \\\\|||  :  |||//  \\
           /  _||||| -:- |||||_  \\
           |   | \\\\\\  -  /'| |   |
           | \\_|  `\\`---'//  |_/ |
           \\  .-\\__ `-. -'__/-.  /
         ___`. .'  /--.--\\  `. .'___
      .\"\" '<  `.___\\_<|>_/___.' _> \\"\".
     | | :  `- \\`. ;`. _/; .'/ /  .' ; |
     \\  \\ `-.   \\_\\_`. _.'_/_/  -' _.' /
===========`-.`___`-.__\\ \\___  /__.-'_.'_.-'================
---------------------------------------------"""
print(ascii_art)

import threading
import subprocess
import queue
import sys

# Get the path to the wordlist
wordlist_path = input("Enter the path to your wordlist: ")

# Create a queue to hold passwords to try
password_queue = queue.Queue()

# Load the wordlist into the queue
with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        password_queue.put(line.strip())

# Initialize counters
success = 0
counter = 0
lock = threading.Lock()

# Function to try decrypting
def decrypt_attempt(q):
    global success
    global counter

    while not q.empty() and success == 0:
        password = q.get()
        result = subprocess.run(
            ["ansible-vault", "decrypt", "--vault-password-file=<(echo -n '{}')".format(password), "main.yml"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        with lock:
            if result.returncode == 0:
                print(f"\nFound password: {password}")
                success = 1
                return
            else:
                counter += 1
                sys.stdout.write(f"\rFailed attempts: {counter}")
                sys.stdout.flush()

# Create threads
threads = []
for i in range(10):  # Number of threads
    t = threading.Thread(target=decrypt_attempt, args=(password_queue,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

if success == 0:
    print(f"\nDecryption failed after {counter} attempts.")


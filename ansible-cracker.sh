#!/bin/bash

# ASCII Art Header
cat << "EOF"
---------------------------------------------
           _
                           _ooOoo_
                          o8888888o
                          88" . "88
                          (| -_- |)
                          O\  =  /O
                       ____/`---'\____
                     .'  \\|     |//  `.
                    /  \\|||  :  |||//  \
                   /  _||||| -:- |||||_  \
                   |   | \\\  -  /'| |   |
                   | \_|  `\`---'//  |_/ |
                   \  .-\__ `-. -'__/-.  /
                 ___`. .'  /--.--\  `. .'___
              ."" '<  `.___\_<|>_/___.' _> \"".
             | | :  `- \`. ;`. _/; .'/ /  .' ; |
             \  \ `-.   \_\_`. _.'_/_/  -' _.' /
   ===========`-.`___`-.__\ \___  /__.-'_.'_.-'================               
---------------------------------------------
EOF

# Ask user for wordlist location
read -p "Enter the path to your wordlist: " wordlist

# Initialize variables
counter=0
success=0

# Perform parallel decryption attempts
parallel -j 4 --halt now,success=1 "ansible-vault decrypt --vault-password-file=<(echo -n '{}') main.yml 2>/dev/null; if [[ $? -eq 0 ]]; then echo Found password: {}; success=1; else ((counter++)); echo Failed attempts: $counter; fi" :::: "$wordlist"

if [[ $success -eq 1 ]]; then
  echo "Decryption successful."
else
  echo "Decryption failed after $counter attempts."
fi

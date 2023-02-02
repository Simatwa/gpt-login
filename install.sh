#!/usr/bin/bash
apt-get install python3
pip install -r requirements.txt
chmod +x main.py
DIR="/data/data/com.termux/files/usr/bin"
if [[ -d '$DIR' ]]; then 
   cp main.py "$DIR"/gpt-login
else
  cp main.py /usr/bin/gpt-login
fi
echo "gpt-login installation succedeed"
gpt-login -v
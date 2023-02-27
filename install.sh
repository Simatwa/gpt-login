#!/usr/bin/bash
apt-get install python3
apt-get install git
pip install -r requirements.txt
pip install git+https://github.com/Simatwa/undetected-chromedriver.git
chmod +x main.py
DIR="/data/data/com.termux/files/usr/bin"
if [[ -d '$DIR' ]]; then 
   cp main.py "$DIR"/gpt-login
else
  cp main.py /usr/bin/gpt-login
fi
echo "gpt-login installation succeeded"
gpt-login -v

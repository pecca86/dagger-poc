# #!/bin/bash

# apt update -y
# apt upgrade -y
# apt-get install -y python3-pip python3-dev build-essential
# pip install --upgrade pip
# # Install curl
# apt install curl -y
# apt install python3-pycurl -y
# # Install Rust compiler
# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -y | sh
# # Install Ngrok
# curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && apt update && apt install ngrok
# pip install --no-cache-dir -r /app/requirements.txt
# pip install --upgrade openai==1.1.1
# echo $NGROK_TOKEN
# ngrok config add-authtoken $NGROK_TOKEN
# cd app
# python3 project_gin.py -t "Stookers Gin" -p twitter
echo "Hello World"
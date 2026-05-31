# Solace Python Pub/Sub Lab

## Overview

This project demonstrates how to connect to a Solace PubSub+ broker using Python, publish messages to topics, and subscribe to topics or queues.

The project includes utilities for:

* Connecting to a Solace PubSub+ broker
* Publishing messages to topics
* Subscribing to topics
* Subscribing to queues
* Downloading and storing the Solace server certificate
* Running tests from the command line

---

# Prerequisites

Before starting, ensure you have:

* Python 3.12 or later
* GitHub account
* GitHub Codespaces access
* Solace Cloud account
* Internet access

---

# Project Setup

## 1. Fork Repository

Open the repository:

```text
https://github.com/koko-aye/PubSubLab
```

Click **Fork**.

Select your GitHub account.

Click **Create Fork**.

Example:

```text
Original Repository:
https://github.com/koko-aye/PubSubLab

↓

Fork

↓

https://github.com/<your-github-id>/PubSubLab
```

---

## 2. Create GitHub Codespace

1. Open your forked repository.
2. Click **Code**.
3. Select the **Codespaces** tab.
4. Click **Create codespace on main**.
5. Wait for the Codespace environment to start.
6. Once VS Code opens in the browser, open a Terminal.

Verify the workspace:

```bash
pwd
ls -l
```

Expected:

```text
/workspaces/PubSubLab
```

---

## 3. Create Python Virtual Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

---

## 4. Activate Virtual Environment

Linux / GitHub Codespaces:

```bash
source venv/bin/activate
```

Expected:

```text
(venv) codespace ➜ /workspaces/PubSubLab $
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

---

## 5. Install Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Verify installation:

```bash
pip list
```

---

## 6. Verify Python Version

```bash
python3 --version
```

Expected:

```text
Python 3.12.x
```

---

## 7. Verify Internet Connectivity

```bash
curl https://www.google.com
```

or

```bash
ping google.com
```

---

# Solace Cloud Setup

## 1. Provision a Solace Broker

Login to Solace Cloud:

```text
https://console.solace.cloud/mc/services
```

Create a new PubSub+ broker service.

After provisioning, take note of the following information:

### Broker Details

| Parameter   | Description            |
| ----------- | ---------------------- |
| Server FQDN | Solace broker hostname |
| VPN Name    | Message VPN            |
| Username    | Client username        |
| Password    | Client password        |
| Secure Port | Usually 55443          |

Example:

```text
Server FQDN:
mr-connection-xxxxxxxx.messaging.solace.cloud

VPN Name:
my_vpn

Username:
solace-cloud-client

Password:
xxxxxxxxxxxxxxxx

Secure Port:
55443
```

---

# Download Solace Server Certificate

The client requires the Solace server certificate for TLS validation.

Run:

```bash
python3 createServerCert.py --host "tcps://your-server-fqdn:55443"
```

Example:

```bash
python3 createServerCert.py --host "tcps://mr-connection-xxxxxxxx.messaging.solace.cloud:55443"
```

Generated files:

```text
certs/
├── solace-server-chain.crt
└── sol-ca-bundle.crt
```

---

# Test Connection

Verify connectivity to the Solace broker.

```bash
python testClient.py \
  --action connect \
  --host tcps://XXX.messaging.solace.cloud:55443 \
  --vpn vpn_name \
  --username solace-cloud-client \
  --password password
```

Expected output:

```text
Connection test passed.
```

---

# Test Publish

Publish a test message to a topic.

```bash
python testClient.py \
  --action pub \
  --host tcps://XXX.messaging.solace.cloud:55443 \
  --vpn vpn_name \
  --username solace-cloud-client \
  --password password \
  --topic test/topic
```

Expected output:

```text
Message published successfully.
```

---

# Test Topic Subscription

Subscribe to a topic and receive messages.

```bash
python testClient.py \
  --action subOnTopic \
  --host tcps://XXX.messaging.solace.cloud:55443 \
  --vpn vpn_name \
  --username solace-cloud-client \
  --password password \
  --topic test/topic
```

Expected output:

```text
Subscribed to topic: test/topic

Press ENTER to stop subscribing...
```

Received message example:

```text
Received message: Hello, Solace!
```

Stop subscription:

```text
Press ENTER
```

---

# Test Queue Subscription

Ensure the queue exists in Solace Cloud before testing.

```bash
python testClient.py \
  --action subOnQueue \
  --host tcps://XXX.messaging.solace.cloud:55443 \
  --vpn vpn_name \
  --username solace-cloud-client \
  --password password \
  --queue Q_TEST
```

Expected output:

```text
Subscribed to queue: Q_TEST

Press ENTER to stop subscribing...
```

---

# Project Structure

```text
.
├── base_uti.py
├── sol_uti.py
├── createServerCert.py
├── testClient.py
├── requirements.txt
├── README.md
├── certs/
│   ├── solace-server-chain.crt
│   └── sol-ca-bundle.crt
└── venv/
```

---

# Troubleshooting

## Unresolved Host

Error:

```text
SOLCLIENT_SUBCODE_UNRESOLVED_HOST
```

Verify DNS resolution:

```bash
nslookup <broker-host>
```

Verify host value:

```text
tcps://your-broker.messaging.solace.cloud:55443
```

---

## TLS Certificate Error

Error:

```text
SOLCLIENT_SUBCODE_UNTRUSTED_CERTIFICATE
```

Verify certificate files exist:

```bash
ls certs
```

Expected:

```text
solace-server-chain.crt
```

Regenerate certificates if necessary.

---

## Authentication Error

Verify:

* VPN Name
* Username
* Password
* Client Profile permissions

---

## Tkinter Error in GitHub Codespaces

Error:

```text
_tkinter.TclError: no display name and no $DISPLAY environment variable
```

Cause:

GitHub Codespaces is a headless Linux environment and does not support desktop GUI applications.

Recommended alternatives:

* FastAPI
* Flask
* Streamlit
* Gradio

---

# Git Ignore Recommendations

Create a `.gitignore` file:

```gitignore
venv/
.venv/
__pycache__/
*.pyc

certs/
*.crt
*.pem
*.key
*.p12
*.jks

.env
.vscode/
```

Do not commit:

* Passwords
* Certificates
* Private keys
* Environment files

---

# License
Internal training and development use only.

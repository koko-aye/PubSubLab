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

* Python 3.10 or later
* GitHub Codespaces or Linux environment
* A Solace Cloud account
* Internet access to connect to Solace Cloud

---

# Project Setup

## 1. Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

---

## 2. Create Python Virtual Environment

```bash
python3 -m venv venv
```

---

## 3. Activate Virtual Environment

Linux / GitHub Codespaces:

```bash
source venv/bin/activate
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

## 4. Install Dependencies

```bash
pip install -r requirement.txt
```

Verify installation:

```bash
pip list
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

Subscribe to a queue.

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

# Command Reference

## Connection Test

```bash
python testClient.py \
  --action connect \
  --host <broker-host> \
  --vpn <vpn-name> \
  --username <username> \
  --password <password>
```

## Publish Message

```bash
python testClient.py \
  --action pub \
  --host <broker-host> \
  --vpn <vpn-name> \
  --username <username> \
  --password <password> \
  --topic <topic-name>
```

## Subscribe to Topic

```bash
python testClient.py \
  --action subOnTopic \
  --host <broker-host> \
  --vpn <vpn-name> \
  --username <username> \
  --password <password> \
  --topic <topic-name>
```

## Subscribe to Queue

```bash
python testClient.py \
  --action subOnQueue \
  --host <broker-host> \
  --vpn <vpn-name> \
  --username <username> \
  --password <password> \
  --queue <queue-name>
```

---

# Project Structure

```text
.
├── base_uti.py
├── sol_uti.py
├── createServerCert.py
├── testClient.py
├── requirement.txt
├── README.md
└── certs/
    ├── solace-server-chain.crt
    └── sol-ca-bundle.crt
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
sol-ca-bundle.crt
```

Regenerate certificates if necessary.

---

## Authentication Error

Verify:

* VPN name
* Username
* Password
* Client profile permissions

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

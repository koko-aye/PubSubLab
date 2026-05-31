from urllib.parse import urlparse
import argparse
import ssl
import os
import shutil
import certifi

parser = argparse.ArgumentParser()
parser.add_argument("--host", required=True)
args = parser.parse_args()

host_input = args.host

if host_input.startswith(("tcp://", "tcps://")):
    parsed = urlparse(host_input)
    HOST = parsed.hostname
    PORT = parsed.port or 55443
else:
    HOST = host_input
    PORT = 55443

print(f"Connecting to {HOST}:{PORT}")

PEM_FILE = r"certs\solace-server-chain.crt"


# Download server certificate
cert_pem = ssl.get_server_certificate((HOST, PORT))

with open(PEM_FILE, "w") as f:
    f.write(cert_pem)

print(f"Server certificate saved to {PEM_FILE}")


cert_dir = "certs"
os.makedirs(cert_dir, exist_ok=True)

shutil.copy(certifi.where(), os.path.join(cert_dir, "sol-ca-bundle.crt"))

print("CA bundle copied to:", cert_dir)
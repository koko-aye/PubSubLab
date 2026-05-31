#create python virtual env 
python3 -m venv venv

#activate virtual env
source venv/bin/activate

#install deppendency
pip install -r requirement.txt

#create solace broker in solace cloud 
go to https://console.solace.cloud/mc/services and provison solace broker 
Pls take note on following server details
- Server FQDN
- VPN Name
- UserName and Password

#goback to GitHub Codesapces and run createServerCert.py to donwnload Solace Server Cert
python3 createServerCert.py --host "tcps://your Server FQDN"

#Test connection
python testClient.py \
  --action connect \
  --host tcps://XXX.messaging.solace.cloud:55443 \
  --vpn vpn_name \
  --username solace-cloud-client \
  --password password

#Test publish
python testClient.py \
  --action pub \
  --host tcps://XXX.messaging.solace.cloud:55443 \
  --vpn vpn_name \
  --username solace-cloud-client \
  --password password \
  --topic test/topic

python testClient.py \
  --action subOnTopic \
  --host tcps://XXX.messaging.solace.cloud:55443 \
  --vpn vpn_name \
  --username solace-cloud-client \
  --password password \
  --topic test/topic

python testClient.py \
  --action subOnQueue \
  --host tcps://XXX.messaging.solace.cloud:55443 \
  --vpn vpn_name \
  --username solace-cloud-client \
  --password password \
  --queue Q_TEST
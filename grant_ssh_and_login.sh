#!/bin/sh
spinaltap_user=kun
keymaker_user=kun_zhu
host=$1
name=ec2-user
if [ ! -z $2 ]; then
  name=$2
fi
keypair=MyCorp-Q2-2016.key
if [ ! -z $3 ]; then
  keypair=$3
fi

ssh -o "ProxyCommand ssh -q -o StrictHostKeyChecking=no -A ${spinaltap_user}@spinaltap-prod.grindr.io nc -w90 %h %p" ${keymaker_user}@keymaker.grindr.com "cd /opt/keymaker/ && sudo -u keymaker -- fab -i /home/keymaker/.ssh/${keypair} -u ${name} -H ${host} ssh_grant"
#ssh -o "ProxyCommand ssh -q -o StrictHostKeyChecking=no -A ${spinaltap_user}@spinaltap-prod.grindr.io nc -w90 %h %p" ${keymaker_user}@${host}
ssh ${keymaker_user}@${host}

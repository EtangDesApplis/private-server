# Generate certificates with Let's Encrypt

Install certbot
```
sudo snap install core; sudo snap refresh core
sudo apt-get remove certbot
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```
Perform the challenge (prove that you are the owner of this domain name):

```
certbot certonly --manual --preferred-challenges dns
```
For wildcard, provide: 
```
*.chefphan.com chefphan.com
```

Create through DNS provider interface the DNS TXT record

```
TYPE: DNS TXT
HOST: _acme-challenge # even if you are asked to create _acme-challenge.chefphan.com namecheap requirement
VALUE: <TOKEN>
```

To check if the DNS TXT record is active (before proceed further on certbot process):
```
dig -t txt _acme-challenge.chefphan.com
```
Otherwise, use the following url
```
https://toolbox.googleapps.com/apps/dig/#TXT/_acme-challenge.chefphan.com
```
To auto renew with traefik:
```
https://sysadmins.co.za/https-using-letsencrypt-and-traefik-with-k3s/
```

Ingress Nginx is deployed with helm in kube-system
```
controller:
  extraArgs:
    default-ssl-certificate: kube-system/ssl-secret
  image:
    digest: sha256:9f61cdb1cd1dd720be2ef1a69002ad92cd5dc25302c36cc806ff36889d5a8f6d
    repository: quay.io/kubernetes-ingress-controller/nginx-ingress-controller-arm
    tag: 0.32.0
```
In secret ssl-secret, type kubernetes.io/tls:
```
tls.crt => fullchain.pem
tls.key => privkey.pem
```
Do not forget to restart the nginx ingress pods

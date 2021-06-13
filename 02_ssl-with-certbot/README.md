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
NAME: _acme-challenge.chefphan.com
VALUE: <TOKEN>
```

To check if the DNS TXT record is active (before proceed further on certbot process):
```
dig -t txt _acme-challenge.chefphan.com
```
To auto renew with traefik:
```
https://sysadmins.co.za/https-using-letsencrypt-and-traefik-with-k3s/
```

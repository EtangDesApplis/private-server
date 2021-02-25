# Arhitecture
![nginx-with-private-ca](./nginx-with-private-ca.png)

# NGINX with HTTP
Nginx is a web server sofware
```
sudo apt install nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```
To check the status of the nginx daemon
```
sudo systemctl status nginx
```
Associate a domain name to IPv4 of the vm
```
echo "192.168.1.X mysite.com" >> /etc/hosts
```
Access to the web service through web navigator
```
http://mysite.com
```
The default web page is defined in the file
```
ls -lrt /var/www/html/
```
Create a new index.html with the following content
```
rm -f /var/www/html/index*.html
vi /var/www/html/index.html
```
```
<!DOCTYPE html>
<html>
    <head>
        <title>Welcome to nginx!</title>
    </head>
    <body>
        <h1>Hello world</h1>
    </body>
</html>

```
This web page is not secured. It means that information exchange between your web navigator and web server is not encrypted.
For example, credit card number sent to http web server can be captured and read by hacker
# Certificates

## CA
Certificate Authority is an organiastion that certifies that the certificate (public rsa key) provided when using HTTPS protocol correponds to the domain name that user accesses to.
Let's Encrypt, for example is a CA that provide free certificate signing service.
In the on-premise environment, we will have the private CA to do the job.

To create the CA private key:
```
openssl genrsa -des3 -out CA-key.pem 2048
#provide password to protect private key, e.g. capass
```
To generate the CA public certificat:
```
openssl req -new -key CA-key.pem -x509 -days 1000 -out CA-cert.pem
#provide information when asked
#e.g. #capass , FR , Garonne , Toulouse ,PrivateCA , IT ,privateca.com , privateca@privateca.com
```
User will then import this certificat in their trust store to trust any web server certificat signed (approuved) by this private CA.

## Server
Create server private key
```
openssl genrsa  -out privkey.pem 2048
```
Create certificate signing request to be signed by CA
```
openssl req -new -key privkey.pem -out cert.csr
#FR , Garonne , Toulouse , MySite , IT , mysite.com , myemail@gmail.com
```

## CSR & Signature

CA uses their private key (CA-key.pem) to sign the CSR (cert.csr)
```
openssl x509 -req -days 365 -in cert.csr -CA CA-cert.pem -CAkey CA-key.pem -CAcreateserial -out server-cert.pem 
```
CA sends back the signed certificate (server-cert.pem) to the requester.

# NGINX with HTTPS
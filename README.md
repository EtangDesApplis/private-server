# ip-exporter

## How to run

```
docker run -d -v /home/minwoo/.ssh/rsa_pi:/root/.ssh \
           -e GIT_SSH="git@github.com:EtangDesApplis/network-info.git" \
           -e TARGET_FILE="retex.json" \
           --net=host \
           etangdesapplis/ip-exporter
```

## How to fine-tuning
By default, the IPs verification is done every 300s (5 minutes), and the git repository is updated no matter what every 86400s (24 hours). To override the default, for example:
```
docker run -d -v /home/minwoo/.ssh/rsa_pi:/root/.ssh \
           -e GIT_SSH="git@github.com:EtangDesApplis/network-info.git" \
           -e TARGET_FILE="retex.json" \
           -e VERIF_COOLDOWN=30 \
           -e UPDATE_COOLDOWN=3600 \
           --net=host \
           etangdesapplis/ip-exporter
```


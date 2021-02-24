#FROM python:3.8.0-alpine
#LABEL author="nguyen.ensma@gmail.com"
#USER root
#RUN apk update &&\
#    apk add --no-cache git vim curl openssh-client
##create worker user
#RUN addgroup --gid 1001 worker \
#    && adduser -u 1001 -D -G worker -s /bin/bash -h /home/worker worker
##copy files
#COPY src/ip-exporter.py /home/worker/ip-exporter.py
#COPY id_rsa /home/worker/.ssh/id_rsa
#COPY .gitconfig /home/worker/.gitconfig
#RUN chown -R 1001:1001 /home/worker/.ssh && \
#    chown 1001:1001 /home/worker/ip-exporter.py && \
#    chown 1001:1001 /home/worker/.gitconfig
#USER 1001
#WORKDIR /home/worker
#ENV GIT_SSH_COMMAND="/usr/bin/ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
#CMD ["python","-u","ip-exporter.py"]

FROM python:3.8.0-alpine
LABEL author="nguyen.ensma@gmail.com"
USER root
RUN apk update &&\
    apk add --no-cache git vim curl openssh-client
#copy files
WORKDIR /home/worker
COPY src/ip-exporter.py /home/worker/ip-exporter.py
COPY .gitconfig /root/.gitconfig
ENV GIT_SSH_COMMAND="/usr/bin/ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
CMD ["python","-u","ip-exporter.py"]
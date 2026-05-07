FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    apt-get install -y rsyslog && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 
    

RUN echo 'root:root' | chpasswd

RUN sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

RUN echo "PROMPT_COMMAND='history -a >(logger -t "[$USER] $SSH_CONNECTION")'" >> /etc/bash.bashrc

EXPOSE 22

CMD ["/bin/bash", "-c", "rsyslogd || true; exec /usr/sbin/sshd -D"]
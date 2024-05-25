FROM python:3.8

RUN apt-get update && apt-get install -y \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -rm -d /home/sshuser -s /bin/bash -g root -G sudo -u 1000 sshuser
RUN echo 'sshuser:sshuserpassword' | chpasswd

RUN mkdir /var/run/sshd
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'PermitTunnel yes' >> /etc/ssh/sshd_config
RUN echo 'GatewayPorts yes' >> /etc/ssh/sshd_config
RUN echo 'AllowTcpForwarding yes' >> /etc/ssh/sshd_config
RUN echo 'ClientAliveInterval 60' >> /etc/ssh/sshd_config
RUN echo 'ClientAliveCountMax 10' >> /etc/ssh/sshd_config
RUN echo 'TCPKeepAlive yes' >> /etc/ssh/sshd_config

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 22 8080

CMD ["/start.sh"]

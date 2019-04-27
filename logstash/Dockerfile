FROM ubuntu:18.04
RUN sh -c 'echo dash dash/sh boolean false | debconf-set-selections' && \
    sh -c 'DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash' && \
    apt-get update && \
    apt-get install -y vim curl ca-certificates jq gnupg default-jdk && \
    rm -rf /var/lib/apt/lists/*
RUN curl -Lso - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - && \
    apt-get install apt-transport-https && \
    echo "deb https://artifacts.elastic.co/packages/oss-7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list && \
    apt-get update && apt-get install -y logstash && \
    rm -rf /var/lib/apt/lists/*
ADD entrypoint.sh /sbin/entrypoint.sh
# ADD filebeat*.yml /etc/filebeat/
# RUN chmod 600 /etc/filebeat/*.yml && chown root:root /etc/filebeat/*.yml
ENTRYPOINT ["/sbin/entrypoint.sh"]
CMD ["start"]

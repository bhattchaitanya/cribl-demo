FROM alpine:latest
ADD https://api.gogen.io/linux/gogen /usr/bin/gogen
RUN chmod 755 /usr/bin/gogen
ADD gogen /etc/gogen
RUN apk --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ add filebeat
ADD entrypoint.sh /sbin/entrypoint.sh
ADD filebeat*.yml /etc/filebeat/
RUN chmod 600 /etc/filebeat/*.yml && chown root:root /etc/filebeat/*.yml
ENTRYPOINT ["/sbin/entrypoint.sh"]
CMD ["start-direct"]
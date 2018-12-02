# Cribl Demo

This repo is used for building and running Cribl demos. All demos contained within utilize Docker. There are a few scenarios we have built:

1. Cribl with Splunk - Single Container
2. Cribl Routing Demo
3. Cribl Routing Demo with Kafka

All demos have Cribl and Splunk running. In demos 2 and 2, the Cribl credentials are `admin/admin`. In 1, we use the Splunk credentials, which in all demos are `admin/cribldemo`. Here are the URLs:

* https://localhost:8000/en-US/account/insecurelogin?loginType=splunk&username=admin&password=cribldemo- Splunk
* https://localhost:9000/login?username=admin&password=cribldemo - Cribl Demo 1
* http://localhost:9000/login?username=admin&password=admin - Cribl Demo 2 & 3

## Cribl with Splunk - Single Container

This demo has everything contained in a single container. This demo grabs `cribl-demo-splunk-app`, which contains a data generator (mirrored in the `gogen-filebeat` directory as well). Data flows like:

    Gogen
    `- Stdout Modinput XML
    `- Splunk
    `- S2S -> Localhost:9999
    `- Cribl
    `- S2S -> Localhost:10000
    `- Splunk Indexer

Data is deposited in Splunk in the `cribl` index and Cribl mirrors it to the `cribl-modified` index.

To run the demo, run `start.sh` in the `splunk` directory. To stop the demo, run `stop.sh` in the `splunk` directory.

## Cribl Routing Demo

This demo splits out data generation and Cribl out into seperate containers. Data flows like:

    Gogen
    `- TCP -> cribl:10001
    `- Cribl
      `- S2S -> splunk:9997
      `- Elastic Bulk Ingestion -> elastic:9200
      `- S3 -> minio:80

Data in Splunk also ends up in the `cribl` index. Elastic index is also named `cribl` and `minio` ends up in the `cribl` bucket.

To run the demo, run `docker-compose up -d`. To stop the demo, run `docker-compose down`.

## Cribl Routing Demo with Kafka

This demo adds Kafka in the middle between the data generation and Cribl. Data flows like:

    Gogen
    `- Files -> /opt/be/log/(auth|transaction).log, /var/log/httpd/access.log
    `- Filebeat
    `- Kafka - topic cribl
    `- Cribl
      `- S2S -> splunk:9997
      `- Elastic Bulk Ingestion -> elastic:9200
      `- S3 -> minio:80

To run the demo, run `docker-compose -f docker-compose-kafka.yml up -d`. To stop the demo, run `docker-compose -f docker-compose-kafka.yml down`.

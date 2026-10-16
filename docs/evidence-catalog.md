# Original evidence catalog

All images below were extracted unchanged from S1. The manifest records each source member and SHA-256 hash. No terminal output, log screenshot or Kibana result was generated. The academic cover/logo and unneeded installation screenshots were omitted.

The original architecture uses VM1/VM2/VM3; later runbooks use VM1/VM3/VM4. IPs and roles agree. Some earlier Cowrie screenshots use root fields; the later pipeline uses `cowrie.*`.

| Figure | Evidence | Source member |
|---|---|---|
| 2.1 | [Original three-VM architecture](../docs/architecture.png) | `word/media/image2.png` |
| 2.2 | [VMnet3 subnet](../screenshots/infrastructure/vmware-host-only-network.png) | `word/media/image3.png` |
| 2.3 | [Cowrie listener excerpt](../screenshots/cowrie/ssh-listener.png) | `word/media/image4.png` |
| 2.4 | [Honeypot test credentials](../screenshots/cowrie/lab-userdb.png) | `word/media/image5.png` |
| 2.5 | [Published service ports](../screenshots/dionaea/listening-ports.png) | `word/media/image6.png` |
| 2.6 | [Container and persistent host log](../screenshots/dionaea/container-and-source-log.png) | `word/media/image7.png` |
| 2.7 | [Filebeat configuration](../screenshots/elk/filebeat-configuration.png) | `word/media/image8.png` |
| 2.8 | [Logstash input and filter](../screenshots/elk/logstash-input-filter.png) | `word/media/image9.png` |
| 2.9 | [Logstash output](../screenshots/elk/logstash-output.png) | `word/media/image10.png` |
| 2.10 | [Elasticsearch Compose section](../screenshots/elk/compose-elasticsearch.png) | `word/media/image11.png` |
| 2.11 | [Logstash and Kibana Compose sections](../screenshots/elk/compose-logstash-kibana.png) | `word/media/image12.png` |
| 2.12 | [Honeynet data view](../screenshots/elk/kibana-data-view.png) | `word/media/image13.png` |
| 2.13 | [Historical Filebeat output test](../screenshots/elk/filebeat-output-test.png) | `word/media/image14.png` |
| 2.14 | [Historical container status](../screenshots/infrastructure/elastic-stack-status.png) | `word/media/image15.png` |
| 3.1 | [Nmap service scan](../screenshots/dionaea/nmap-service-scan.png) | `word/media/image16.png` |
| 3.2 | [Dionaea scan events](../screenshots/dionaea/kibana-scan-events.png) | `word/media/image17.png` |
| 3.3 | [SSH client authentication](../screenshots/cowrie/ssh-authentication-client.png) | `word/media/image18.png` |
| 3.4 | [Authentication outcomes](../screenshots/cowrie/kibana-authentication-events.png) | `word/media/image19.png` |
| 3.5 | [Emulated shell interaction](../screenshots/cowrie/simulated-shell-client.png) | `word/media/image20.png` |
| 3.6 | [Command events grouped by session](../screenshots/cowrie/kibana-command-events.png) | `word/media/image21.png` |
| 3.7 | [HTTP marker request and 404 response](../screenshots/dionaea/http-marker-client.png) | `word/media/image22.png` |
| 3.8 | [HTTP marker in Discover](../screenshots/dionaea/kibana-http-marker.png) | `word/media/image23.png` |
| 3.9 | [FTP connection](../screenshots/dionaea/ftp-client.png) | `word/media/image24.png` |
| 3.10 | [FTP event with parsed fields](../screenshots/dionaea/kibana-ftp-event.png) | `word/media/image25.png` |
| 3.11 | [Marker entered into Cowrie](../screenshots/cowrie/pipeline-marker-client.png) | `word/media/image26.png` |
| 3.12 | [Original Cowrie marker JSON](../screenshots/cowrie/pipeline-marker-source-log.png) | `word/media/image27.png` |
| 3.13 | [Filebeat connection during pipeline experiment](../screenshots/elk/pipeline-filebeat-output.png) | `word/media/image28.png` |
| 3.14 | [Namespaced marker at Logstash](../screenshots/elk/pipeline-logstash-event.png) | `word/media/image29.png` |
| 3.15 | [Marker search hit in Elasticsearch](../screenshots/elk/pipeline-elasticsearch-hit.png) | `word/media/image30.png` |
| 3.16 | [Marker in Kibana Discover](../screenshots/elk/pipeline-kibana-marker.png) | `word/media/image31.png` |
| PL.1 | [Cowrie package dependencies](../screenshots/infrastructure/cowrie-dependencies.png) | `word/media/image32.png` |
| PL.2 | [Cowrie virtual environment installation](../screenshots/cowrie/python-environment-installation.png) | `word/media/image33.png` |
| PL.6 | [Filebeat 9.5.4 package](../screenshots/elk/filebeat-package-installation.png) | `word/media/image37.png` |
| PL.8 | [Kernel setting and Docker version](../screenshots/infrastructure/elasticsearch-kernel-setting.png) | `word/media/image39.png` |

Original document filenames and source roles are described in [source analysis](source-analysis.md). The source reports remain local. Generic lab hostnames, private lab addresses and session/event identifiers are retained as technical evidence; source personal identities/student IDs are excluded.

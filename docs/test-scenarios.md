# Experimental scenarios

The procedures below come from S3/S4; observed outcomes come from S1 section 3.2 and its original screenshots. They describe historical controlled-lab tests, not new executions during repository preparation. Run only within the authorized Host-Only lab.

## Shared test environment

Kali `192.168.100.10` generates traffic; Honeypot `192.168.100.20` runs Cowrie, Dionaea and Filebeat; Dashboard `192.168.100.30` runs Logstash, Elasticsearch and Kibana. Use VMnet3 `192.168.100.0/24`, disconnect NAT, confirm clocks and service readiness using the [setup guide](setup-guide.md). Commands and queries are maintained in [commands](../tests/commands.md) and [KQL](../tests/kibana-queries.md).

## 01 Network service scanning

**Objective:** confirm published service endpoints and record connections from the known test host.

**Test environment:** shared environment; five Dionaea TCP ports `21,80,445,1433,3306` and Cowrie SSH `2222` on the Honeypot Server.

**Tools:** Nmap, Dionaea/Cowrie logs, Kibana Discover.

**Procedure:** run the scenario 01 Nmap command on Kali. Query Dionaea events for source `192.168.100.10` and the five service ports. Inspect parsed `src_ip`, `src_port`, `dst_port` and `protocol`. Query Cowrie separately when checking the additional SSH port.

**Expected evidence:** advertised ports accessible and connection events associated with the controlled scan. Nmap service descriptions are emulated banners, not proof of actual installed service versions.

**Observed results:** S1 figure 3.1 shows the five Dionaea ports open; figure 3.2 shows filtered Dionaea connections, including a parsed destination port `1433` and internal destination `172.17.0.2`. The screenshot does not show port `2222`; the repeat command includes it. Connection events support the limited scan observation, not a successful exploit.

**Screenshots:** [Nmap](../screenshots/dionaea/nmap-service-scan.png), [Discover scan events](../screenshots/dionaea/kibana-scan-events.png).

## 02 SSH authentication attempts

**Objective:** capture deliberately rejected and accepted decoy credentials.

**Test environment:** Kali to Cowrie at `192.168.100.20:2222`; original userdb rules shown in figure 2.4.

**Tools:** OpenSSH client, Cowrie JSON log, Kibana Discover.

**Procedure:** use password authentication with public-key authentication disabled. Enter `123456` for the documented rejection test, reconnect and enter `toor` for the accepted `root` login. Read the source JSON and query login failure/success events. Compare account, result, event time and session.

**Expected evidence:** `cowrie.login.failed` and `cowrie.login.success`; one TCP session may include several attempts. Lab userdb values are decoy credentials only.

**Observed results:** S1 figures 3.3–3.4 show refused attempts and accepted `root/toor`. The visible outcome table includes `1234567` and other rejected values, so it is not described as a screenshot of the exact `123456` repeat attempt. Early screenshots use root-level fields; current queries use `cowrie.*`.

**Screenshots:** [SSH client](../screenshots/cowrie/ssh-authentication-client.png), [authentication outcomes](../screenshots/cowrie/kibana-authentication-events.png), [visible userdb rules](../screenshots/cowrie/lab-userdb.png).

## 03 Simulated SSH shell interaction

**Objective:** capture shell input and reconstruct the command order within a session.

**Test environment:** accepted Cowrie login from Kali; shared pipeline and Discover.

**Tools:** SSH client, Cowrie source JSON, Kibana session/event fields.

**Procedure:** log in as decoy `root/toor`, then enter `whoami`, `pwd`, `ls -la`, `cat /etc/passwd`, `uname -a`, `exit`. Query command-input events, filter one session, and sort by `@timestamp` ascending. Compare input with the source log.

**Expected evidence:** `cowrie.command.input` records with matching session and the typed commands. These are simulated-shell interactions.

**Observed results:** figure 3.6 shows all six inputs for session `ab4d94ca9157`, displayed in descending time order. The session also appears in the source summary table. A separate earlier-session `exit` row appears in the screenshot and must not be combined with this session.

**Screenshots:** [simulated shell](../screenshots/cowrie/simulated-shell-client.png), [command events](../screenshots/cowrie/kibana-command-events.png).

## 04 Dionaea service interactions

**Objective:** trace a recognizable HTTP request and observe service-specific connections.

**Test environment:** Kali to Dionaea TCP `80`, `21`, `445`, `1433`, `3306` on the Honeypot Server.

**Tools:** curl, Netcat, Dionaea text log, Kibana Discover.

**Procedure:** send the documented HTTP request with marker `DIONAEA-DEMO-GV-001` and user agent `DIONAEA-DEMO-GV`; connect to FTP using Netcat, then optionally repeat the documented TCP probes for other service ports. Check the host log and query the HTTP marker in `message`/`event.original`; query FTP by source IP and `dst_port:21`.

**Expected evidence:** HTTP marker text and parsed connection records where Grok matches. A 404 from a nonexistent URI can coexist with successful logging.

**Observed results:** figures 3.7–3.8 show the HTTP 404 response and the same marker in Discover. Figures 3.9–3.10 show an FTP banner and a parsed event for source `192.168.100.10`, internal destination `172.17.0.2:21`. SMB/MSSQL/MySQL connection observations are supported by scenario 01 scan evidence; separate successful application-level sessions are not established.

**Screenshots:** [HTTP client](../screenshots/dionaea/http-marker-client.png), [HTTP marker](../screenshots/dionaea/kibana-http-marker.png), [FTP client](../screenshots/dionaea/ftp-client.png), [FTP event](../screenshots/dionaea/kibana-ftp-event.png).

## 05 End-to-end log collection

**Objective:** trace a known event through each collection stage.

**Test environment:** Cowrie on the Honeypot Server; Filebeat to Dashboard Logstash `5044`, Elasticsearch `9200`, Kibana `5601`.

**Tools:** SSH, grep, systemctl, Filebeat output test, Docker Compose logs, Elasticsearch search API, Kibana Discover.

**Procedure:** enter `echo PIPELINE-DEMO-001` in Cowrie. Locate the original event in `cowrie.json`; check Filebeat service/output; search Logstash stdout and Elasticsearch; query the marker in Discover. Match input, session and source timestamp across stages. Adjust log/time windows to the experiment time.

**Expected evidence:** the same marker event at source, Logstash, Elasticsearch and Kibana. Connectivity alone is insufficient. Index totals and Discover counts need the same scope before comparison.

**Observed results:** S1 figures 3.11–3.16 show the marker client input, source JSON, Filebeat connection, Logstash event, Elasticsearch hit and Discover result. Session `279acf641142` and source timestamp `2026-09-29T02:10:22.564012Z` identify the event. Elasticsearch shows one hit in `honeynet-2026.09.29`; Discover displays it at `09:10:22.564` (UTC+7). This confirms historical delivery of that event, without proving lossless collection or a general latency bound.

**Screenshots:** [client](../screenshots/cowrie/pipeline-marker-client.png), [source](../screenshots/cowrie/pipeline-marker-source-log.png), [Filebeat](../screenshots/elk/pipeline-filebeat-output.png), [Logstash](../screenshots/elk/pipeline-logstash-event.png), [Elasticsearch](../screenshots/elk/pipeline-elasticsearch-hit.png), [Discover](../screenshots/elk/pipeline-kibana-marker.png).

# Kibana Discover queries

Sources: S5 query sheet, S3 experiment guide and S2 operational runbook. Select Data View **Honeynet**, `honeynet-*`, `@timestamp`. These are KQL expressions for Discover, not Elasticsearch JSON DSL. Refresh and use a time range covering the test. The original evidence is from September 2026, so Last 15 minutes will not retrieve those historical records.

## 01 Network scan

```kql
honeypot:"dionaea" and src_ip:"192.168.100.10" and dst_port:(21 or 80 or 445 or 1433 or 3306)
```

Optional Cowrie source filter:

```kql
honeypot:"cowrie"
```

## 02 SSH authentication

```kql
honeypot:"cowrie" and
(
  cowrie.eventid:"cowrie.login.failed"
  or cowrie.eventid:"cowrie.login.success"
)
```

Columns: `@timestamp`, `cowrie.src_ip`, `cowrie.username`, `cowrie.password`, `cowrie.eventid`, `cowrie.session`. Multiple attempts can belong to one session.

## 03 SSH commands

```kql
honeypot:"cowrie" and cowrie.eventid:"cowrie.command.input"
```

Columns: `@timestamp`, `cowrie.src_ip`, `cowrie.input`, `cowrie.session`. Filter a session and sort ascending by event time to reconstruct order.

## 04 Dionaea interactions

HTTP marker:

```kql
honeypot:"dionaea" and
(
  message:"DIONAEA-DEMO-GV-001"
  or event.original:"DIONAEA-DEMO-GV-001"
)
```

FTP connection:

```kql
honeypot : "dionaea" AND src_ip : "192.168.100.10" AND dst_port : 21
```

Other service connections, from S3:

```kql
honeypot:"dionaea" and src_ip:"192.168.100.10" and dst_port:(445 or 1433 or 3306)
```

HTTP/debug lines may lack parsed connection fields; use the marker/text fields rather than requiring `dst_port` on every line.

## 05 Pipeline marker

```kql
honeypot:"cowrie" and cowrie.input:"echo PIPELINE-DEMO-001"
```

## Earlier root-level Cowrie records

S2 and earlier report screenshots use a previous root-level schema:

```kql
honeypot:"cowrie" and eventid:"cowrie.command.input"
```

For those older records, replace `cowrie.eventid`, `cowrie.input`, `cowrie.session`, `cowrie.src_ip`, `cowrie.username` and `cowrie.password` with their root equivalents. This is a schema difference, not a second simultaneously guaranteed field set. The final Filebeat configuration targets the `cowrie` namespace. Inspect an actual document before choosing a query; do not merge counts across schema/time ranges without defining the population.

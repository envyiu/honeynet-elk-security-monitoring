# Limitations and interpretation

## Demonstrated scope

Historical source screenshots support authentication and command capture in Cowrie, service connections in Dionaea, and a marker transported through Filebeat, Logstash, Elasticsearch and Kibana. Investigations can filter by source, port, command and session within the fields actually present.

## Observation boundaries

Cowrie provides an emulated shell. A `cowrie.command.input` event establishes that input was received, not that a real kernel executed it. Dionaea banners emulate services; Nmap's reported Synology/nginx/MySQL identities are advertised fingerprints, not installed product/version inventory. TCP connection evidence for SMB/MSSQL/MySQL does not prove exploitation or successful application-level authentication.

The source scan screenshot covers five Dionaea ports; the documented repeat command additionally includes Cowrie `2222`. Event counts in screenshots depend on filters/time windows and are not attack totals. One SSH session may generate multiple authentication and command events.

## Architecture and protection

All guests share one Host-Only network. No gateway or Honeywall enforces inter-zone controls. NAT is disconnected before experiments, but no full egress/IPv6 policy validation is supplied. Elasticsearch security is disabled and Beats/HTTP traffic is plaintext in the original configuration. This lab setup has not been assessed for production exposure.

## Parsing and time

Cowrie records are under `cowrie.*` after NDJSON parsing; earlier screenshots use root fields. Dionaea accepted-connection lines receive structured fields, whereas HTTP/debug lines may have `_dionaea_grok_failure` and remain searchable as text. `dst_ip` can be `172.17.0.2` inside the container; `target_ip=192.168.100.20` is the configured logical destination. A configured `protocol=tcp` label should not be treated as independent protocol detection.

Only Cowrie source timestamps are parsed. Dionaea `@timestamp` can reflect Filebeat ingestion instead of source event time. Differences between source text time, UTC and browser display time prevent defensible latency calculations from these screenshots.

## Reproducibility and evaluation

The original standalone configuration files, complete Cowrie bootstrap/defaults, Dionaea mounts/service files and image digest are missing. Some installation commands are visible only partially. A complete fresh deployment cannot be guaranteed. YAML/Compose validation checks structure; it does not validate plugin behavior, image availability, port reachability or runtime success.

No raw bulk logs, PCAP, dashboard/alert export, representative Internet dataset, ground-truth labels, throughput benchmark, ingestion-loss experiment or measured detection accuracy was supplied. The source report describes stable operation, but its small experiment set cannot establish a lossless or continuously reliable pipeline.

## Proposed next work

1. Recover complete sanitized VM/container configuration exports, pin package/image versions and document a fresh-VM rebuild.
2. Add a routed Honeywall/segmented network and test allowed traffic, egress denial and recovery boundaries.
3. Export dashboards and detection rules, then evaluate them using labeled repeatable events with explicit counts and timing definitions.

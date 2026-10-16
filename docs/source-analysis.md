# Source inventory and verification levels

All five available input files were read, including the report tables and its 40 embedded images. The request refers to four inputs; the workspace actually provides the five sources below. Cover-page identities, student IDs, academic logo and editorial residue are omitted from publication.

| ID | Local source | Role |
|---|---|---|
| S1 | `baocao_ATMMT_final.docx` | Main report: theory, deployment, 5 experiments, observed results, 40 images and installation appendix |
| S2 | `Huong_dan_thuc_hanh_demo_Honeynet_3VM.docx` | Operational startup/demo/shutdown runbook, dated 26 September 2026 |
| S3 | `Huong_dan_thuc_nghiem_5_kich_ban_Honeynet.docx` | Repeat procedures, expected results and schema migration note |
| S4 | `lenh_thuc_nghiem_5_kich_ban_honeynet.txt` | Exact experiment command reference |
| S5 | `lenh_test_Kibana.txt` | Scenario KQL queries |

## Verified

“Verified” means directly supported by the supplied material. It does not imply that the rebuilt files have been deployed.

- Three-VM topology, Host-Only VMnet3, subnet, addresses and ports: S1 section 2.3.1 and figures 2.1–2.2; S2/S3 topology tables.
- Cowrie listener, five visible decoy userdb rules and JSON log path: S1 section 2.3.2, figures 2.3–2.4; S2/S4 source log commands.
- Dionaea image `dinotools/dionaea:latest`, container name `dionaea`, five published TCP ports and host log: S1 figures 2.5–2.6.
- Two Filebeat inputs, `cowrie` NDJSON namespace, root `honeypot` field and Logstash output: S1 figure 2.7.
- Logstash Beats input, Cowrie date filter, accepted-connection Grok, mutate fields and output: S1 figures 2.8–2.9.
- ELK image tags `9.5.4`, heaps, fixed IP bindings, volume `esdata`, healthcheck, pipeline mount and dependencies: S1 figures 2.10–2.11.
- Data View Honeynet, index pattern `honeynet-*`, time field `@timestamp`: S1 figure 2.12 and text.
- Five controlled experiment groups and historical results: S1 section 3.2, figures 3.1–3.16; S3–S5 repeat procedures.
- Filebeat `9.5.4`: source installation and agent metadata. Cowrie `3.0.15` is visible at download time only (PL.2); Dashboard Docker `29.1.3` appears in PL.8.

## Documented but incomplete

- Cowrie installation: dependencies and Python environment are shown, but user creation, generated configuration initialization, complete configuration/defaults and final package inventory are absent.
- Dionaea deployment: host configuration/data/log persistence is described, but mount destinations, full creation command, service configuration and immutable image digest are absent.
- Ubuntu LTS / Kali guests: exact release manifests, ISO checksums, disk sizing and complete CPU/RAM allocations absent. S2 requests 6 GB for the Dashboard; a complete VM resource manifest is absent.
- Log permissions, clock synchronization policy, rotation behavior and service restart integration are not fully documented.
- Kibana charts/dashboard capability is mentioned; evidence supplied is primarily Discover, with no custom saved-object export.

## Not provided

Dedicated Honeywall/gateway deployment, segmentation/egress enforcement rules, IDS/IPS integration, TLS/authentication configuration for ELK, automated blocking, AI detection, alert rule exports, a bulk log archive, packet capture, a labeled dataset, reliability/latency measurements, and complete fresh-VM automation.

These are not represented as implemented features. Future work is labeled as proposed.

## Differences retained explicitly

1. **VM numbering:** S1 original diagram/appendix uses VM1=Kali, VM2=Honeypot, VM3=Dashboard; S2/S3 use VM1/VM3/VM4. Roles and IPs match. Repository instructions use roles and IPs; extracted screenshots remain unchanged.
2. **Cowrie schema:** early S1 screenshots and S2 queries use `eventid`, `input`, `session`; the Filebeat screenshot, S3–S5 and pipeline evidence use `cowrie.eventid`, `cowrie.input`, `cowrie.session`. Both query variants are explained, not silently conflated.
3. **Scan scope:** S3/S4 request six ports including `2222`; S1 figure 3.1 shows five Dionaea ports only. It cannot prove the SSH port was included in that particular scan.
4. **Credentials:** S2/S4 specify rejected `123456`; figure 3.4 visibly includes a `1234567` attempt among other rejected values. Those records are not described as the exact same attempt. `root/toor` is an accepted honeypot credential.
5. **Timing:** S2's runbook date precedes S1's September 29 experiment screenshots; it is an operating guide, not a timestamped record of those tests. Older Dionaea text timestamps differ from ingestion/display timestamps. No ingestion latency is inferred.
6. **Search command:** S4 uses an unqualified Elasticsearch query-string marker. S1 figure 3.15 uses `cowrie.input` explicitly. Both are preserved with explanation in the command reference.
7. **Memory:** S2 recommends 6 GB Dashboard RAM; figure 2.14 displays about 5.8 GiB total and container limits around 5.788 GiB. Treat 6 GB as the runbook allocation, not a benchmark minimum.

The report's theoretical discussion of PCAP, default-deny policies, snapshots and sensors is background, not implementation evidence.

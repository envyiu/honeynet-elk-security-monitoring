# Configuration provenance

These files reconstruct material visible in the supplied report. No original standalone configuration files were supplied, and none of these reconstructions has been deployed in this workspace.

| File | Classification | Source and scope |
|---|---|---|
| [Cowrie listener](cowrie/cowrie.cfg.example) | Verified excerpt | S1 figure 2.3; `[ssh]` header added for context; remaining defaults absent |
| [Cowrie userdb](cowrie/userdb.txt.example) | Verified visible rules | S1 figure 2.4; five lab-only rules, comments added |
| [Filebeat](filebeat/filebeat.yml) | Verified transcription | S1 figure 2.7; complete visible two-input and output configuration |
| [Logstash](elk/logstash/pipeline/honeynet.conf) | Verified transcription | S1 figures 2.8–2.9; joined input/filter/output, whitespace normalized |
| [ELK Compose](elk/docker-compose.yml) | Verified transcription | S1 figures 2.10–2.11; joined sections; implicit Compose default network |
| [Dionaea Compose](dionaea/compose.template.yml) | Documented but incomplete template | Image/name/ports shown, original launch command, mount destinations and service files absent |

For each source figure, see the [evidence catalog](../docs/evidence-catalog.md). “Verified” means checked against the document, not executed successfully here. Deployment gaps are recorded in the [setup guide](../docs/setup-guide.md).

The Dionaea screenshot displays `dinotools/dionaea:latest`. Its version/digest is unknown; the template requires an explicit image reference and log mount destination. Configuration and data mount targets are also missing and are not invented. Recover the original container inspection and service files before attempting a faithful rebuild.

The ELK file retains `xpack.security.enabled=false`, plaintext Beats/HTTP, fixed lab IP bindings, and the source healthcheck. This healthcheck verifies an HTTP response, not a particular green/yellow cluster state. No TLS, access control, ILM, explicit network definition, or custom dashboard export was supplied. Keep this configuration on the isolated Host-Only lab.

The Grok pattern intentionally matches only `accepted connection` text. Other Dionaea lines remain in `message`/`event.original` with `_dionaea_grok_failure`; the `protocol=tcp` value is a configured label, not protocol inference for arbitrary log lines. Dionaea source timestamps are not parsed. Cowrie uses `cowrie.timestamp` for `@timestamp`.

Apply only the listener excerpt to an existing Cowrie installation. The sample userdb contains deliberate honeypot credentials (`root/toor`, `admin/admin123`) and rejected passwords; never reuse them as VM administrator credentials. Filebeat requires filesystem read access to both log paths; the original permission setup was not supplied.

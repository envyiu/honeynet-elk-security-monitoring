# Verification record

Repository preparation date: 16 October 2026 (Asia/Ho_Chi_Minh).

## Documentation reviewed

All five local sources were extracted/read, including report tables and 40 embedded images. Published configurations were manually compared against their source images. Thirty-four selected images retain the original embedded bytes, with SHA-256 values in the evidence manifest. Internal links, image references, fenced code blocks, YAML/JSON structure and expected source-derived event fields are checked by [validate_repository.py](../scripts/validate_repository.py).

Academic personal identities, student IDs, cover/logo and editorial residue are excluded. Original DOCX/TXT inputs remain local and ignored by Git. The published credentials are explicitly decoy honeypot inputs. The source-derived sample command event contains no administrator password, API key, token or private key. Selected image contents were visually reviewed for the same distinction.

## Configuration syntax checked

See the generated [validation results](validation-results.json) for actual check outcomes. YAML is parsed with duplicate-key rejection; ELK Compose is normalized with `docker compose config --quiet` and no service startup. The Dionaea template is checked using an explicit image reference from the source and a deliberately temporary log destination solely to resolve Compose interpolation. That temporary value is not a recovered mount path and must never be interpreted as deployment evidence.

Cowrie's listener excerpt is parsed as INI; the sample event is parsed as JSON. The Logstash text and Grok pattern are checked against the screenshots, and braces/string structure are checked statically. A Logstash plugin configuration test and Filebeat binary test have not been run because those binaries/runtime containers are not available for the documented lab here. No image pull or VM deployment is part of syntax validation.

## Runtime deployment verified

**Not performed during repository preparation.** Historical source images show working services and one traced marker event. That historical evidence is distinct from validating the newly transcribed files in a running lab. No new live-VM success, package availability, loss rate, latency or performance result is claimed.

## Publication

This repository is prepared for Private publication. Public visibility requires the user's approval. Source ownership/redistribution rights must be resolved before assigning an open-source license; see [rights](../RIGHTS.md). GitHub branch/commit/visibility are verified after pushing and reported to the owner.

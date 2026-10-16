# Static repository validation

Run from the repository root using Python 3.12 or a compatible Python 3 installation:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/validate_repository.py
```

Docker with the Compose plugin is required for `docker compose config`. The validator does not start containers, pull images or probe lab hosts. It checks Markdown rendering/links, YAML duplicate keys, Compose normalization, original image hashes, JSON/INI parsing, basic Logstash delimiters and selected secret/PII patterns. Its generated record is `docs/validation-results.json`.

Dionaea template interpolation uses `/syntax-check-only` as an artificial destination during normalization. That string is a validator fixture, not a known container mount. Recover the actual path before deployment. Static Logstash checks do not replace Logstash's own configuration test or Grok runtime testing. Secret pattern checks do not replace manual review of documents/images.

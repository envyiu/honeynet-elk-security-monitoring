# Source-derived sample event

[cowrie-pipeline-marker.json](cowrie-pipeline-marker.json) is a manual transcription of the full event visible in S1 figure 3.12, cross-checked against figure 3.14. It is an observed controlled-lab event, not a generated example or an exported log archive. JSON whitespace was reformatted; values were retained. It contains private lab addresses, a generic VM hostname and event/session identifiers; no login password or administrator secret is present.

[Source screenshot](../screenshots/cowrie/pipeline-marker-source-log.png). Figure 3.15 shows the same event in Elasticsearch; figure 3.16 shows it in Discover. The UTC source time `02:10:22.564012Z` corresponds to `09:10:22.564` displayed at UTC+7. No Dionaea raw log file was supplied; use the unmodified screenshots rather than inventing a dataset.

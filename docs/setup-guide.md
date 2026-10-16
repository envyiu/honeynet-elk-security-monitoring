# Setup and operations guide

This guide reconstructs supported steps from S1–S4. It includes an operating runbook for the already prepared lab and identifies missing bootstrap work for a new installation. It is not a claim of a fresh deployment verified from this repository.

## 1. Prepare the environment

Create three VMware guests: Kali (`192.168.100.10`), an Ubuntu LTS Honeypot Server (`192.168.100.20`) and an Ubuntu LTS Dashboard (`192.168.100.30`). Configure static `/24` addresses on Custom **VMnet3**, Host-Only `192.168.100.0/24`. The original network screenshot is [here](../screenshots/infrastructure/vmware-host-only-network.png). Guest interface names vary; the source Kali runbook uses `eth1`. Full netplan/NetworkManager files and exact guest releases are not supplied.

The demo guide allocates 6 GB RAM to the Dashboard. CPU, disk sizing and other VM allocations require local planning; no tested minimum is established. NAT may be temporarily connected for downloads, then disconnected on every guest before tests. Keep all traffic within the authorized lab. There is no gateway/Honeywall VM.

Confirm addresses and clocks on each guest:

```bash
ip -br -4 addr
date
```

## 2. Dashboard prerequisites

S1 appendix PL.8 shows Docker enabled and `vm.max_map_count=1048576`. Docker/Compose installation details for this VM are incomplete. After installing the tools and confirming permissions, the documented kernel setup is:

```bash
sudo systemctl enable --now docker
echo 'vm.max_map_count=1048576' | sudo tee /etc/sysctl.d/99-elasticsearch.conf
sudo sysctl --system
```

Preserve any pre-existing setting file before adapting this command. [Original kernel-setting evidence](../screenshots/infrastructure/elasticsearch-kernel-setting.png).

Copy `configs/elk/` from this checkout into `~/honeynet-elk/` on the Dashboard VM, keeping `docker-compose.yml` beside `logstash/pipeline/honeynet.conf`. This staging layout follows the source bind mount; copying is a repository packaging step, not a command recovered from the report.

The [Compose file](../configs/elk/docker-compose.yml) reconstructs the source image tags, heaps, ports, persistence and healthcheck. Its default Docker network connects the three services; no explicit custom network appeared in the source. It retains the isolated lab's disabled Elasticsearch security and plaintext transport. Image availability and service-specific behavior still require runtime validation.

## 3. Honeypot Server prerequisites

### Cowrie

PL.1 shows these dependency packages:

```bash
sudo apt install -y python3-pip python3-venv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind
```

A dedicated `cowrie` user must already exist; its creation command and exact ownership setup were not supplied. PL.2 shows the following environment steps:

```bash
sudo -iu cowrie
mkdir -p ~/my-honeypot
cd ~/my-honeypot
python3 -m venv cowrie-env
source cowrie-env/bin/activate
python -m pip install --upgrade pip
python -m pip install cowrie
```

The screenshot shows `cowrie-3.0.15` downloading, not the final installed package inventory. The install command above is the source command and is unpinned. Configuration initialization, template copying and complete startup defaults were not supplied. Resolve those steps for the chosen Cowrie package before proceeding.

Merge the [listener excerpt](../configs/cowrie/cowrie.cfg.example) into `etc/cowrie.cfg` and review the visible [userdb rules](../configs/cowrie/userdb.txt.example) against the installed defaults. Do not assume other pre-existing userdb rules are absent. The source listener is `tcp:2222:interface=192.168.100.20`. Source JSON logs are at `/home/cowrie/my-honeypot/var/log/cowrie/cowrie.json`.

Use `root/toor` only inside Cowrie's simulated service. `123456` is deliberately rejected; these are not administrator login instructions. Run Cowrie as the dedicated user, not root. Exit that user shell when configuration is complete.

### Dionaea

S1 shows Docker installation and an existing container named `dionaea` using `dinotools/dionaea:latest`, with five ports bound to `192.168.100.20`. The reported host persistence root is `/opt/honeynet/dionaea`, and the source text log path is `/opt/honeynet/dionaea/var-log/dionaea/dionaea.log`.

The original container creation command, container-side mount paths and service configurations were not supplied. Recover these from the original VM with `docker inspect dionaea` and sanitize its output before sharing. The [reference template](../configs/dionaea/compose.template.yml) requires `DIONAEA_IMAGE` and `DIONAEA_LOG_TARGET`; it cannot recreate the original container alone. Additional configuration/data mount details remain open. Do not replace the working container using this incomplete template.

### Filebeat

PL.6 shows Filebeat 9.5.4 installed from an amd64 package; the exact source operations are:

```bash
cd /tmp
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-9.5.4-amd64.deb
sudo dpkg -i filebeat-9.5.4-amd64.deb
```

Package download/availability and checksum verification were not performed here. Apply the [transcribed configuration](../configs/filebeat/filebeat.yml) at `/etc/filebeat/filebeat.yml`, backing up any existing configuration. This path is supported by the Filebeat test-output screenshot. Confirm that the service can read both source paths; the source permission/ACL setup was not supplied.

Configuration validation to perform on that VM:

```bash
sudo filebeat test config -e
```

This command is an added verification step, not a historical result. Check its outcome before starting the service.

## 4. Start the prepared lab

Start in this order: **Dashboard → Honeypot Server → Kali**.

### Dashboard (`192.168.100.30`)

```bash
cd ~/honeynet-elk
sudo docker compose up -d
sudo docker compose ps
curl -fsS http://192.168.100.30:9200
curl -fsS 'http://192.168.100.30:9200/_cluster/health?pretty'
curl -fsS http://192.168.100.30:5601/api/status
sudo ss -lnt | grep -E ':(5044|5601|9200)[[:space:]]'
curl -fsS 'http://192.168.100.30:9200/honeynet-*/_count?pretty'
```

Wait for Elasticsearch's configured healthcheck and running Logstash/Kibana. Kibana may need another 1–2 minutes. Save the initial count for comparison; on a fresh stack without matching indices, establish the baseline after the first successful event. The source count procedure assumes existing lab data.

### Honeypot Server (`192.168.100.20`)

For an already created Dionaea container and configured Filebeat service:

```bash
sudo docker start dionaea
sudo systemctl start filebeat
sudo docker ps --filter name=dionaea
sudo systemctl is-active filebeat
sudo -iu cowrie
cd ~/my-honeypot
source cowrie-env/bin/activate
cowrie status
# Run only if status says Cowrie is not running:
cowrie start
cowrie status
exit
```

```bash
sudo ss -lnt | grep ':2222[[:space:]]'
sudo ss -lntup | grep -E ':(21|80|445|1433|3306)[[:space:]]'
sudo filebeat test output -e
```

Confirm port `2222`, all five Dionaea TCP ports, Filebeat `active`, and `dial up... OK` / `talk to server... OK` for `192.168.100.30:5044`. Filebeat initiates the connection; it does not require an inbound collection port on this VM.

### Kali (`192.168.100.10`)

```bash
ip -4 addr show eth1
date
ping -c 3 192.168.100.20
ping -c 3 192.168.100.30
```

Use the actual Host-Only interface if it is not `eth1`. Require network connectivity before running the [experiments](test-scenarios.md).

## 5. Configure and use Kibana

Open `http://192.168.100.30:5601` from the host. Create Data View **Honeynet**, index pattern `honeynet-*`, time field `@timestamp`, after events exist. Use Discover with [documented KQL queries](../tests/kibana-queries.md). Start with **Last 15 minutes**; if investigating the historical September 29 evidence, use its actual date range instead. Refresh after new events and verify clocks when the expected event is missing.

Cowrie columns for current data: `@timestamp`, `cowrie.src_ip`, `cowrie.username`, `cowrie.password`, `cowrie.input`, `cowrie.eventid`, `cowrie.session`. Dionaea columns: `@timestamp`, `src_ip`, `dst_port`, `message`, `event.original`, `log.file.path`, `agent.name` as available. HTTP/debug lines need not have parsed connection fields. No saved dashboard export was supplied.

## 6. Verify the event path

Run scenario 05 in [commands](../tests/commands.md). Require the same marker, session and source event time at Cowrie, Logstash, Elasticsearch and Kibana. Filebeat output success alone proves connectivity, not end-to-end delivery. Compare the count after new events, but do not equate total index count with time-filtered Discover hits.

## 7. Troubleshoot

| Symptom | Check | Next action |
|---|---|---|
| Kibana unavailable | `sudo docker compose ps`, `sudo docker compose logs --tail 50 kibana` | Wait for startup; inspect errors |
| Elasticsearch unhealthy | Cluster health, Dashboard memory and container logs | Resolve resource/startup issue |
| Cowrie unreachable | Port 2222, `cowrie status` as the Cowrie user | Activate its environment and start if stopped |
| Dionaea ports absent | `sudo docker ps -a --filter name=dionaea` | Start the existing container; inspect logs |
| Filebeat output fails | `sudo filebeat test output -e`; `journalctl -u filebeat -n 30 --no-pager` | Check Dashboard 5044 and source read permissions |
| Only old events visible | Guest clocks, Discover time range, new marker | Expand range and trace the event stage by stage |
| SSH host key mismatch | Confirm IP/port belong to the intended VM | Only then remove the old key with `ssh-keygen -R '[192.168.100.20]:2222'` |

## 8. Stop without discarding evidence

Stop Kali first with `sudo poweroff`. On the Honeypot Server:

```bash
sudo -iu cowrie
cd ~/my-honeypot
source cowrie-env/bin/activate
cowrie stop
exit
sudo docker stop dionaea
sleep 10
sudo systemctl stop filebeat
sudo poweroff
```

The source allows ten seconds for forwarding; this is not a measured delivery guarantee. On the Dashboard last:

```bash
cd ~/honeynet-elk
sudo docker compose stop -t 30
sudo docker compose ps
sudo poweroff
```

Preserve Elasticsearch volumes and source logs. Avoid `docker compose down -v`, container removal and pruning during the evidence workflow. Wait until all VMware guests are Powered Off.

## Fresh-install gaps

Recover complete Cowrie setup/defaults and final package versions, Dionaea inspect/mount/service exports and image digest, Filebeat permissions, guest networking/clock files and Dashboard Docker/Compose installation details. Export Kibana saved objects if a reusable dashboard is intended. The [configuration provenance](../configs/README.md) and [limitations](limitations.md) describe these boundaries.

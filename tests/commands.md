# Controlled lab command reference

Sources: S4 command sheet, supplemented by S2 for FTP/shutdown operations and S1 figure 3.15 for a field-specific search. Run tests only against systems you control and are authorized to test. All targets below belong to the isolated Host-Only lab; disconnect guest NAT first. These commands have not been executed against the VMs during repository preparation.

## 01 Network service scanning — Kali

```bash
nmap -sT -sV -p 21,80,445,1433,3306,2222 192.168.100.20
```

The supplied Nmap screenshot shows five Dionaea ports; the repeat command includes SSH `2222` as well. Service fingerprints are emulated identities.

## 02 SSH authentication — Kali

```bash
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no -p 2222 root@192.168.100.20
```

Enter `123456` interactively for the rejected lab test. Reconnect using the same command and enter `toor` for an accepted Cowrie test. The source userdb also rejects `root` and `password`; `admin/admin123` is another visible decoy rule. These credentials belong only to the honeypot simulation.

On the Honeypot Server:

```bash
sudo tail -n 50 /home/cowrie/my-honeypot/var/log/cowrie/cowrie.json
```

## 03 Simulated SSH shell — Kali

```bash
ssh -p 2222 root@192.168.100.20
```

After entering `toor`, type these commands inside Cowrie's simulated shell:

```bash
whoami
pwd
ls -la
cat /etc/passwd
uname -a
exit
```

Check the same source log with the tail command above. Compare session identifiers and timestamps; shell output is emulated.

## 04 Dionaea service interactions — Kali

```bash
curl -v -A "DIONAEA-DEMO-GV" "http://192.168.100.20/DIONAEA-DEMO-GV-001?probe=vm1"
nc -nv -w 5 192.168.100.20 21
nc -nv -w 5 192.168.100.20 445
nc -nv -w 5 192.168.100.20 1433
nc -nv -w 5 192.168.100.20 3306
```

The HTTP URI may return 404 while still generating useful evidence. S2 supplies these optional demo variants:

```bash
curl --max-time 10 -v -A "DIONAEA-DEMO-GV" "http://192.168.100.20/DIONAEA-DEMO-GV-001?probe=vm1"
printf 'USER demo\r\nPASS demo123\r\nQUIT\r\n' | nc -nv -w 5 192.168.100.20 21
```

The FTP `demo/demo123` values are lab protocol inputs, not administrator credentials. On the Honeypot Server:

```bash
sudo tail -n 50 /opt/honeynet/dionaea/var-log/dionaea/dionaea.log
sudo grep -R 'DIONAEA-DEMO-GV-001' /opt/honeynet/dionaea/var-log/dionaea/
```

## 05 End-to-end collection

On Kali, connect and enter `toor`:

```bash
ssh -p 2222 root@192.168.100.20
```

Inside Cowrie:

```bash
echo PIPELINE-DEMO-001
exit
```

On the Honeypot Server:

```bash
sudo grep 'PIPELINE-DEMO-001' /home/cowrie/my-honeypot/var/log/cowrie/cowrie.json
sudo systemctl is-active filebeat
sudo filebeat test output -e
```

On the Dashboard:

```bash
cd ~/honeynet-elk
sudo docker compose logs --since 10m logstash | grep -A10 -B10 'PIPELINE-DEMO-001'
curl -s 'http://192.168.100.30:9200/honeynet-*/_search?q=PIPELINE-DEMO-001&pretty'
```

The unqualified query is preserved from S4. S1 figure 3.15 instead uses the explicit field query below; use it when the marker is stored in `cowrie.input`:

```bash
curl -s 'http://192.168.100.30:9200/honeynet-*/_search?q=cowrie.input:"echo%20PIPELINE-DEMO-001"&pretty'
```

Compare the event session and input at each stage, then use [KQL scenario 05](kibana-queries.md#05-pipeline-marker) in Discover. If the event predates the log window, widen `--since` as the source screenshot does; do not infer delivery failure from an unsuitable window.

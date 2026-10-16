#!/usr/bin/env python3
"""Validate repository artifacts without contacting or starting lab systems."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import configparser, hashlib, ipaddress, json, re, subprocess, os
import yaml
from PIL import Image
from markdown_it import MarkdownIt

ROOT=Path(__file__).resolve().parents[1]
class UniqueLoader(yaml.SafeLoader):
    pass

def mapping(loader,node,deep=False):
    result={}
    for k,v in node.value:
        key=loader.construct_object(k,deep=deep)
        if key in result: raise ValueError(f'Duplicate YAML key: {key}')
        result[key]=loader.construct_object(v,deep=deep)
    return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
EXCLUDED={'.git','.private-review','.venv','venv','node_modules','__pycache__'}
def publishable(p):
    return not EXCLUDED.intersection(p.relative_to(ROOT).parts)

checks=[]
def check(name,fn):
    try:
        detail=fn()
        checks.append({'check':name,'status':'passed','detail':detail})
    except Exception as exc:
        checks.append({'check':name,'status':'failed','detail':str(exc)})

def markdown():
    files=sorted(p for p in ROOT.rglob('*.md') if publishable(p)); links=0
    for p in files:
        if '.git' in p.parts: continue
        s=p.read_text(); MarkdownIt('commonmark').enable('table').render(s)
        assert sum(line.startswith('```') for line in s.splitlines())%2==0,p
        for raw in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',s):
            u=urlsplit(raw)
            if u.scheme:continue
            dst=(p.parent/unquote(u.path)).resolve() if u.path else p
            assert dst.is_relative_to(ROOT),f'Outside repo: {p}: {raw}'
            assert dst.exists(),f'Missing: {p}: {raw}'
            if u.fragment:
                assert dst.suffix=='.md',f'Unsupported fragment: {raw}'
                headings=[]
                for line in dst.read_text().splitlines():
                    if line.startswith('#'):
                        title=line.lstrip('#').strip().lower()
                        headings.append(re.sub(r'[^\w\- ]','',title).replace(' ','-'))
                assert unquote(u.fragment) in headings,f'Missing anchor: {raw}'
            links+=1
    return {'markdown_files':len(files),'internal_references':links}

def yamls():
    files=sorted((ROOT/'configs').rglob('*.yml'))
    for p in files:
        data=yaml.load(p.read_text(),Loader=UniqueLoader);assert isinstance(data,dict),p
    fb=yaml.safe_load((ROOT/'configs/filebeat/filebeat.yml').read_text())
    assert fb['filebeat.inputs'][0]['parsers'][0]['ndjson']['target']=='cowrie'
    assert fb['output.logstash']['hosts']==['192.168.100.30:5044']
    return {'yaml_files':len(files),'duplicate_keys':'rejected'}

def compose():
    env=os.environ.copy()
    env.update(DIONAEA_IMAGE='dinotools/dionaea:latest',DIONAEA_LOG_TARGET='/syntax-check-only')
    for name in ['configs/elk/docker-compose.yml','configs/dionaea/compose.template.yml']:
        p=subprocess.run(['docker','compose','-f',str(ROOT/name),'config','--quiet'],env=env,capture_output=True,text=True)
        assert p.returncode==0,p.stderr
    return 'Both Compose files normalized; Dionaea mount value is syntax-only, not recovered; no services started'

def images():
    records=json.loads((ROOT/'docs/evidence-manifest.json').read_text())
    for e in records:
        p=ROOT/e['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'],p
        with Image.open(p) as im:im.verify()
    return {'images':len(records),'integrity':'SHA-256 and image decode passed'}

def sample():
    event=json.loads((ROOT/'sample-logs/cowrie-pipeline-marker.json').read_text())
    assert event['session']=='279acf641142' and event['input']=='echo PIPELINE-DEMO-001'
    assert event['timestamp']=='2026-09-29T02:10:22.564012Z'
    cfg=configparser.ConfigParser();cfg.read(ROOT/'configs/cowrie/cowrie.cfg.example')
    assert cfg['ssh']['listen_endpoints']=='tcp:2222:interface=192.168.100.20'
    return 'Source event JSON and Cowrie listener INI parsed'

def logstash():
    s=(ROOT/'configs/elk/logstash/pipeline/honeynet.conf').read_text()
    # Check delimiters outside quoted strings/comments. This is not Logstash's parser.
    unquoted=re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*','',s)
    stack=[];pairs={'}':'{',']':'['}
    for ch in unquoted:
        if ch in '{[':stack.append(ch)
        elif ch in '}]':assert stack and stack.pop()==pairs[ch],'Unbalanced Logstash delimiters'
    assert not stack,'Unclosed Logstash delimiters'
    assert 'honeynet-%{+YYYY.MM.dd}' in s
    return 'Delimiter/static reference checks only; no Logstash plugin syntax or Grok runtime test'

def privacy():
    # Source documents are intentionally excluded. Scan only publishable text artifacts.
    files=[p for p in ROOT.rglob('*') if p.is_file() and publishable(p) and p.suffix in {'.md','.yml','.json','.conf','.example','.py'}]
    patterns={
      'github_token':r'gh[pousr]_[A-Za-z0-9]{30,}',
      'private_key':r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',
      'aws_access_key':r'AKIA[0-9A-Z]{16}',
      'academic_id':r'\bAT[0-9]{6}\b',
    }
    # Do not scan this checker for its intentional detector expressions.
    for p in files:
        if p.resolve()==Path(__file__).resolve():continue
        s=p.read_text()
        for name,pat in patterns.items():assert not re.search(pat,s),f'{name}: {p.relative_to(ROOT)}'
        assert 'thêm vào đi em guộc' not in s,p
    return {'text_files':len(files),'finding':'No matches for selected secret/PII patterns; visual/manual review required for images'}

for name,fn in [('markdown_links_and_fences',markdown),('yaml_structure',yamls),('compose_structure',compose),('image_integrity',images),('source_sample_and_ini',sample),('logstash_static_structure',logstash),('selected_secret_and_pii_patterns',privacy)]:check(name,fn)
report={'scope':'Static repository validation; no live lab deployment','checks':checks}
(ROOT/'docs/validation-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(any(c['status']=='failed' for c in checks))

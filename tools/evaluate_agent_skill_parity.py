#!/usr/bin/env python3
"""Deterministic source-vs-package Agent Skill parity evaluation.

This is a CI routing proxy, not a live-model/host trigger evaluation.
"""
from __future__ import annotations
import argparse, json, math, re, statistics
from collections import Counter
from pathlib import Path

STOP = {
    'a','an','and','are','as','at','be','before','but','by','can','do','does','for','from','how','i','if','in','into','is','it','me','my','of','on','or','our','should','the','this','to','use','using','we','what','when','where','which','with','without','you','your','need','help'
}
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_.+-]*")


def parse_frontmatter(text: str) -> dict[str,str]:
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---\n', 4)
    if end < 0:
        return {}
    out = {}
    for line in text[4:end].splitlines():
        if not line or line[0].isspace() or ':' not in line:
            continue
        k,v=line.split(':',1)
        v=v.strip()
        if len(v)>=2 and v[0]==v[-1] and v[0] in {'"',"'"}:
            v=v[1:-1]
        out[k.strip()]=v
    return out


def toks(text: str) -> list[str]:
    vals=[]
    for t in TOKEN_RE.findall(text.lower().replace('-', ' ')):
        if t not in STOP and len(t) > 1:
            vals.append(t)
    return vals


def build_index(docs: dict[str,str]):
    tokenized={k:toks(v) for k,v in docs.items()}
    n=len(tokenized)
    df=Counter()
    for ts in tokenized.values():
        df.update(set(ts))
    avg=sum(len(x) for x in tokenized.values())/max(n,1)
    return tokenized, df, avg


def bm25_rank(query: str, docs: dict[str,str]) -> list[tuple[str,float]]:
    tokenized,df,avg=build_index(docs)
    q=toks(query)
    n=len(tokenized); k1=1.4; b=.72
    scores=[]
    for name,ts in tokenized.items():
        tf=Counter(ts); dl=len(ts); s=0.0
        for term in q:
            if term not in df: continue
            idf=math.log(1 + (n-df[term]+0.5)/(df[term]+0.5))
            f=tf[term]
            s += idf * (f*(k1+1))/(f+k1*(1-b+b*dl/max(avg,1e-9)))
        scores.append((name,s))
    return sorted(scores,key=lambda x:(-x[1],x[0]))


def read_tree_text(path: Path) -> str:
    parts=[]
    for p in sorted(path.rglob('*')):
        if p.is_file() and p.suffix.lower() in {'.md','.txt','.json','.yaml','.yml','.py','.js','.ts'}:
            try: parts.append(p.read_text(encoding='utf-8'))
            except UnicodeDecodeError: pass
    return '\n'.join(parts).lower()


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default='.')
    ap.add_argument('--dist',default='dist/agent-skills-v1.32.0')
    ap.add_argument('--trigger-cases',default='evals/agent-skills/trigger-cases.json')
    ap.add_argument('--capability-assertions',default='evals/agent-skills/capability-assertions.json')
    ap.add_argument('--out-json',default='reports/agent-skill-evaluation-v1.32.0.json')
    ap.add_argument('--out-md',default='reports/agent-skill-evaluation-v1.32.0.md')
    args=ap.parse_args()
    root=Path(args.root).resolve(); dist=(root/args.dist).resolve()
    manifest=json.loads((dist/'manifest.json').read_text(encoding='utf-8'))
    records=manifest['skills']

    src_docs={}; pkg_docs={}; meta_rows=[]
    source_corpora={}; package_corpora={}
    for rec in records:
        key=rec['name']
        src_dir=root/rec['source']; pkg_dir=dist/'skills'/key
        sm=parse_frontmatter((src_dir/'SKILL.md').read_text(encoding='utf-8'))
        pm=parse_frontmatter((pkg_dir/'SKILL.md').read_text(encoding='utf-8'))
        # Name is repeated to approximate host discovery significance.
        src_docs[key]=f"{sm.get('name','')} {sm.get('name','')} {sm.get('description','')}"
        pkg_docs[key]=f"{pm.get('name','')} {pm.get('name','')} {pm.get('description','')}"
        meta_rows.append({
            'skill':key,
            'source_name':sm.get('name'), 'package_name':pm.get('name'),
            'source_description':sm.get('description'), 'package_description':pm.get('description'),
            'description_equal':sm.get('description')==pm.get('description')
        })
        source_corpora[key]=read_tree_text(src_dir)
        package_corpora[key]=read_tree_text(pkg_dir)

    trigger_data=json.loads((root/args.trigger_cases).read_text(encoding='utf-8'))
    cases=trigger_data['cases']
    negative_cases=trigger_data.get('negative_cases', [])
    route_rows=[]; src_hits=0; pkg_hits=0; src_top3=0; pkg_top3=0; class_parity=0
    per_skill={k:{'cases':0,'source_top1':0,'package_top1':0,'source_top3':0,'package_top3':0,'classification_parity':0,'source_ranks':[],'package_ranks':[]} for k in src_docs}
    for c in cases:
        exp=c['expected_skill']
        sr=bm25_rank(c['query'],src_docs); pr=bm25_rank(c['query'],pkg_docs)
        s_names=[x[0] for x in sr]; p_names=[x[0] for x in pr]
        s_rank=s_names.index(exp)+1; p_rank=p_names.index(exp)+1
        s_top=sr[0][0]; p_top=pr[0][0]
        s_pass=s_rank<=3; p_pass=p_rank<=3
        src_hits += s_top==exp; pkg_hits += p_top==exp; src_top3 += s_pass; pkg_top3 += p_pass; class_parity += s_pass==p_pass
        ps=per_skill[exp]; ps['cases']+=1; ps['source_top1']+=s_top==exp; ps['package_top1']+=p_top==exp; ps['source_top3']+=s_pass; ps['package_top3']+=p_pass; ps['classification_parity']+=s_pass==p_pass; ps['source_ranks'].append(s_rank); ps['package_ranks'].append(p_rank)
        route_rows.append({'id':c['id'],'expected_skill':exp,'query':c['query'],'source_top1':s_top,'package_top1':p_top,'source_rank':s_rank,'package_rank':p_rank,'source_positive_pass':s_pass,'package_positive_pass':p_pass,'classification_parity':s_pass==p_pass})

    negative_rows=[]; src_neg=0; pkg_neg=0; neg_parity=0
    for c in negative_cases:
        bad=c['forbidden_skill']
        sr=bm25_rank(c['query'],src_docs); pr=bm25_rank(c['query'],pkg_docs)
        s_names=[x[0] for x in sr]; p_names=[x[0] for x in pr]
        s_rank=s_names.index(bad)+1; p_rank=p_names.index(bad)+1
        s_pass=s_rank>1; p_pass=p_rank>1
        src_neg += s_pass; pkg_neg += p_pass; neg_parity += s_pass==p_pass
        negative_rows.append({'id':c['id'],'forbidden_skill':bad,'query':c['query'],'source_rank':s_rank,'package_rank':p_rank,'source_negative_pass':s_pass,'package_negative_pass':p_pass,'classification_parity':s_pass==p_pass})

    cap=json.loads((root/args.capability_assertions).read_text(encoding='utf-8'))['assertions']
    cap_rows=[]; cap_src=cap_pkg=cap_parity=0
    for a in cap:
        s=source_corpora[a['skill']]; p=package_corpora[a['skill']]
        s_ok=all(term.lower() in s for term in a['all_of'])
        p_ok=all(term.lower() in p for term in a['all_of'])
        cap_src+=s_ok; cap_pkg+=p_ok; cap_parity+=(s_ok==p_ok)
        cap_rows.append({**a,'source_pass':s_ok,'package_pass':p_ok,'parity':s_ok==p_ok})

    reductions=[r['activation_line_reduction_pct'] for r in records if r.get('activation_line_reduction_pct') is not None]
    summary={
        'repository_version':manifest['repository_version'],
        'skill_count':len(records),
        'description_parity':{'passed':sum(r['description_equal'] for r in meta_rows),'total':len(meta_rows)},
        'trigger_proxy':{
            'method':'deterministic BM25 over discovery name+description; positive top-3 is the candidate threshold; explicit negatives fail only when the forbidden skill ranks #1; NOT a live-model trigger evaluation',
            'positive_cases':len(cases),
            'negative_cases':len(negative_cases),
            'source_top1_accuracy':round(src_hits/len(cases),4),
            'package_top1_accuracy':round(pkg_hits/len(cases),4),
            'source_positive_top3_recall':round(src_top3/len(cases),4),
            'package_positive_top3_recall':round(pkg_top3/len(cases),4),
            'positive_classification_parity':round(class_parity/len(cases),4),
            'source_negative_specificity':round(src_neg/max(len(negative_cases),1),4),
            'package_negative_specificity':round(pkg_neg/max(len(negative_cases),1),4),
            'negative_classification_parity':round(neg_parity/max(len(negative_cases),1),4),
        },
        'capability_assertions':{'source_passed':cap_src,'package_passed':cap_pkg,'parity':cap_parity,'total':len(cap)},
        'activation_line_reduction_pct':{'mean':round(statistics.mean(reductions),2),'min':round(min(reductions),2),'max':round(max(reductions),2)},
        'live_host_trigger_eval':{'status':'NOT_RUN','reason':'No live host/model runner is configured in deterministic repository CI. Runtime trigger claims are deferred to host-specific evaluation.'},
    }
    summary['gate_pass']=(
        summary['description_parity']['passed']==len(meta_rows)
        and summary['trigger_proxy']['package_positive_top3_recall']>=0.95
        and summary['trigger_proxy']['package_positive_top3_recall']>=summary['trigger_proxy']['source_positive_top3_recall']
        and summary['trigger_proxy']['package_negative_specificity']>=0.95
        and summary['trigger_proxy']['positive_classification_parity']==1.0
        and summary['trigger_proxy']['negative_classification_parity']==1.0
        and cap_pkg==len(cap) and cap_src==len(cap) and cap_parity==len(cap)
    )

    report={'summary':summary,'metadata_parity':meta_rows,'per_skill':per_skill,'trigger_cases':route_rows,'negative_trigger_cases':negative_rows,'capability_assertions':cap_rows}
    outj=root/args.out_json; outm=root/args.out_md; outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')

    md=[f"# Agent Skill Evaluation & Trigger Parity — {summary['repository_version']}",'',f"Gate: **{'PASS' if summary['gate_pass'] else 'FAIL'}**",'', '## Deterministic Gate','',f"- Description parity: {summary['description_parity']['passed']}/{summary['description_parity']['total']}",f"- Positive routing cases: {len(cases)}",f"- Explicit negative cases: {len(negative_cases)}",f"- Canonical positive top-3 recall: {summary['trigger_proxy']['source_positive_top3_recall']:.1%}",f"- Package positive top-3 recall: {summary['trigger_proxy']['package_positive_top3_recall']:.1%}",f"- Package negative specificity: {summary['trigger_proxy']['package_negative_specificity']:.1%}",f"- Positive source/package classification parity: {summary['trigger_proxy']['positive_classification_parity']:.1%}",f"- Negative source/package classification parity: {summary['trigger_proxy']['negative_classification_parity']:.1%}",f"- Top-1 proxy accuracy (informational): {summary['trigger_proxy']['package_top1_accuracy']:.1%}",f"- Capability assertions: {cap_pkg}/{len(cap)}",f"- Mean activation-line reduction: {summary['activation_line_reduction_pct']['mean']:.2f}%",'', '## Important Limitation','', '**Live host/model trigger evaluation: NOT_RUN.**', '', 'The routing metric is a deterministic BM25 proxy over discovery `name + description`. Positive top-3 is used as a candidate-recall threshold because neighboring skills can legitimately overlap. Explicit negatives fail only when the forbidden skill becomes the proxy top-ranked route. This is a CI drift/parity gate, not evidence that a specific LLM host will activate identically.', '', '## Per Skill','', '| Skill | Cases | Source top-3 | Package top-3 | Classification parity |','|---|---:|---:|---:|---:|']
    for k,v in per_skill.items():
        md.append(f"| `{k}` | {v['cases']} | {v['source_top3']}/{v['cases']} | {v['package_top3']}/{v['cases']} | {v['classification_parity']}/{v['cases']} |")
    md += ['', '## Gate Semantics','', 'A PASS means the packaging migration preserved discovery metadata/routing under the deterministic proxy and retained the committed capability landmarks. It does **not** convert unavailable live-model evidence into a pass.', '']
    outm.write_text('\n'.join(md),encoding='utf-8')
    print('EVALUATION GATE', 'PASSED' if summary['gate_pass'] else 'FAILED')
    print(json.dumps(summary,indent=2))
    return 0 if summary['gate_pass'] else 2

if __name__=='__main__':
    raise SystemExit(main())

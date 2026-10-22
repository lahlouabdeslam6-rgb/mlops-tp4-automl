"""Contrôles de cohérence des mesures, journaux et runs réels."""
import json
import math
from pathlib import Path
import mlflow
from common import ROOT, REPORTS, split_data, setup_tracking, save_json

setup_tracking()
Xtr,Xte,ytr,yte=split_data()
assert len(Xtr)==3750 and len(Xte)==1250
assert set(Xtr.index).isdisjoint(Xte.index)
refs=json.loads((REPORTS/'references.json').read_text())
assert {x['nom'] for x in refs}=={'reference-logistique','manuel-rf-500-16'}
manuel=next(x for x in refs if x['nom']=='manuel-rf-500-16')
assert math.isclose(manuel['f1'],.8669,abs_tol=.0001),manuel
results=[]
for budget in [10,30,60,120]:
    result=json.loads((REPORTS/f'automl_{budget}s.json').read_text())
    records=[json.loads(s) for s in (REPORTS/f'flaml_{budget}s.log').read_text().splitlines() if s.startswith('{')]
    records=[r for r in records if 'learner' in r and r.get('validation_loss') is not None]
    assert records and len(records)==result['nb_essais']
    assert math.isclose(1-min(r['validation_loss'] for r in records),result['f1_validation'],abs_tol=.0001)
    assert all(0<=result[k]<=1 for k in ['f1','f1_validation'])
    run=mlflow.get_run(result['run_id'])
    assert run.info.status=='FINISHED'
    assert run.data.params['budget_s']==str(budget)
    assert run.data.metrics['f1']==result['f1']
    assert any(a.path==f'flaml_{budget}s.log' for a in mlflow.MlflowClient().list_artifacts(result['run_id']))
    results.append(result)
runs=mlflow.search_runs(experiment_names=['tp4-automl'])
expected={r['nom'] for r in refs}|{f'flaml-{b}s' for b in [10,30,60,120]}
assert set(runs['tags.mlflow.runName'])==expected
assert len(runs)==6
fuite=json.loads((REPORTS/'fuite.json').read_text())
assert fuite['f1_test_fuite']>.95, fuite
assert fuite['f1_production_simulee']<.1, fuite
assert (REPORTS/'rendement.png').stat().st_size>1000
save_json('validation.json',dict(controles='OK',donnees=5000,fraudes=568,train=3750,test=1250,
                                nb_runs=6,references=refs,automl=results,fuite=fuite))
print('VALIDATION OK : donnees, separation train/test, 6 runs, 4 journaux, scores et fuite.')

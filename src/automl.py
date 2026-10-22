"""FLAML choisit sur validation interne ; le test externe reste hors fit()."""
import json
import sys
import time
import mlflow
from flaml import AutoML
from sklearn.metrics import f1_score
from common import split_data, setup_tracking, trace_tags, save_json, REPORTS

budget = int(sys.argv[1]) if len(sys.argv)>1 else 60
if budget <= 0:
    raise SystemExit('Le budget doit être strictement positif.')
Xtr, Xte, ytr, yte = split_data()
journal = REPORTS/f'flaml_{budget}s.log'
if journal.exists():
    raise SystemExit(f'{journal.name} existe déjà : archiver cet essai avant de le remplacer.')
a = AutoML()
t0 = time.perf_counter()
a.fit(Xtr, ytr, task='classification', metric='f1', time_budget=budget,
      seed=42, verbose=0, log_file_name=str(journal), log_type='all',
      mlflow_logging=False)
duree = round(time.perf_counter()-t0, 3)
f1 = round(f1_score(yte, a.predict(Xte)), 4)
familles = [k for k,v in a.best_config_per_estimator.items() if v is not None]
essais = [json.loads(s) for s in journal.read_text().splitlines() if s.startswith('{')]
essais = [e for e in essais if 'learner' in e and e.get('validation_loss') is not None]
resultat = dict(budget_s=budget, famille=a.best_estimator, f1=f1,
                f1_validation=round(1-a.best_loss,4), duree_s=duree,
                familles_essayees=familles, nb_essais=len(essais),
                meilleure_config=a.best_config)
print(f'budget {budget} s | famille retenue : {a.best_estimator} | F1 test = {f1} | {duree} s')
print('familles essayees :', familles)
print('meilleure config :', a.best_config)
setup_tracking()
with mlflow.start_run(run_name=f'flaml-{budget}s') as run:
    mlflow.log_params({'outil':'flaml','budget_s':budget,'famille':a.best_estimator})
    mlflow.log_metrics({k:resultat[k] for k in ['f1','f1_validation','duree_s','nb_essais']})
    mlflow.set_tags(trace_tags())
    mlflow.log_dict(a.best_config,'meilleure_config.json')
    mlflow.log_artifact(str(journal))
    resultat['run_id'] = run.info.run_id
save_json(f'automl_{budget}s.json',resultat)

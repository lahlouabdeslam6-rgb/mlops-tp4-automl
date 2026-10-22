import time
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from common import split_data, setup_tracking, trace_tags, save_json

Xtr, Xte, ytr, yte = split_data()
modeles = {
    'reference-logistique': LogisticRegression(max_iter=1000),
    'manuel-rf-500-16': RandomForestClassifier(n_estimators=500, max_depth=16,
                                               random_state=42),
}
setup_tracking()
resultats = []
for nom, m in modeles.items():
    t0 = time.perf_counter()
    m.fit(Xtr, ytr)
    duree = round(time.perf_counter()-t0, 4)
    f1 = round(f1_score(yte, m.predict(Xte)), 4)
    with mlflow.start_run(run_name=nom) as run:
        mlflow.log_params({'outil': 'scikit-learn', 'approche': nom})
        mlflow.log_metrics({'f1': f1, 'duree_s': duree})
        mlflow.set_tags(trace_tags())
        resultats.append(dict(nom=nom, f1=f1, duree_s=duree, run_id=run.info.run_id))
    print(f'{nom:22s} F1 = {f1:.4f} (entrainement : {duree:.4f} s)', flush=True)
save_json('references.json', resultats)

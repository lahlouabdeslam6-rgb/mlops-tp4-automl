import json
import time
import numpy as np
import pandas as pd
import mlflow
from flaml import AutoML
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from common import ROOT, REPORTS, save_json, setup_tracking, trace_tags

df=pd.read_csv(ROOT/'data/transactions.csv')
rng=np.random.default_rng(0)
df['num_dossier_litige']=np.where(df['fraude']==1,rng.integers(10000,99999,len(df)),0)
X,y=df.drop(columns='fraude'),df['fraude']
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.25,random_state=42)
a=AutoML()
t0=time.perf_counter()
a.fit(Xtr,ytr,task='classification',metric='f1',time_budget=30,seed=42,verbose=0,
      log_file_name=str(REPORTS/'flaml_fuite_30s.log'),log_type='all',mlflow_logging=False)
print('famille retenue :',a.best_estimator)
modele=a.model.estimator
imp=[]
if hasattr(modele,'feature_importances_'):
    imp=sorted([(c,float(v)) for c,v in zip(X.columns,modele.feature_importances_)],
               key=lambda t:-t[1])
    print('importance des variables :',[(c,round(v,3)) for c,v in imp])
f1_test=round(f1_score(yte,a.predict(Xte)),4)
Xprod=Xte.copy()
Xprod['num_dossier_litige']=0
f1_prod=round(f1_score(yte,a.predict(Xprod),zero_division=0),4)
print('F1 en test, avec la colonne piegee :',f1_test)
print('F1 "en production" (colonne vide) :',f1_prod)
resultat=dict(famille=a.best_estimator,f1_test_fuite=f1_test,f1_production_simulee=f1_prod,
              importances=imp,meilleure_config=a.best_config,
              duree_s=round(time.perf_counter()-t0,3))
save_json('fuite.json',resultat)
# Expérience distincte : ne pas mélanger cette simulation à la courbe de rendement.
setup_tracking()
mlflow.set_experiment('tp4-fuite')
with mlflow.start_run(run_name='fuite-dossier-litige'):
    mlflow.set_tags(trace_tags())
    mlflow.log_param('colonne_fuite','num_dossier_litige')
    mlflow.log_metrics({'f1_test_fuite':f1_test,'f1_production_simulee':f1_prod})
    mlflow.log_artifact(str(REPORTS/'fuite.json'))

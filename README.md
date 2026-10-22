# TP04 - AutoML et plateformes MLOps low-code

**Zakaria Abdelbaki, Amine Khabot, Ismail Lahlou et Rayane Hafidi - AI, G6**

Projet de fraude bancaire : deux références, recherche FLAML sur quatre budgets, inspection des essais, démonstration de fuite de données et comparaison documentaire du cloud.

## Installation

Python **3.12** est utilisé pour rester dans les versions prises en charge par FLAML 2.7. Pas de plan B scikit-learn. Un projet, un dépôt, un environnement indépendant.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# Pour reproduire l'environnement testé :
# python -m pip install -r requirements-lock.txt
New-Item -ItemType Directory -Force data, reports | Out-Null
python donnees.py
python -c "import flaml, lightgbm, sklearn; print(flaml.__version__, lightgbm.__version__, sklearn.__version__)"
```

Le générateur du TP2 recrée 5 000 transactions (568 fraudes), graine 7. Les observations sont partagées de la même manière dans chaque expérience : test_size=0.25, random_state=42. Le test externe n'entre jamais dans l'appel FLAML `fit()`.

## Serveur MLflow - terminal 1

À la racine du projet, venv activé :

```powershell
$env:PYTHONIOENCODING = 'utf-8'
$env:MLFLOW_DISABLE_AGENT_HINT = '1'
mlflow server --host 127.0.0.1 --port 5001 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts
```

Le port **5001** évite un conflit avec le serveur du TP2 sur 5000. Les scripts utilisent 5001 par défaut ; la variable `MLFLOW_TRACKING_URI` permet de changer l'adresse. L'interface est <http://127.0.0.1:5001> : sélectionner **Model training**, puis `tp4-automl`.

## Expériences - terminal 2

```powershell
.venv\Scripts\Activate.ps1
$env:PYTHONIOENCODING = 'utf-8'
python src/references.py
python src/automl.py 10
python src/automl.py 30
python src/automl.py 60
python src/automl.py 120
python src/rendement.py
python src/inspecter.py reports/flaml_60s.log
python src/inspecter.py reports/flaml_10s.log
python src/fuite.py
python src/verifier.py
```

La recherche écrit tous les essais (`log_type='all'`) dans un journal distinct par budget et le joint au run. La journalisation MLflow automatique de FLAML est désactivée pour conserver un run récapitulatif par budget. Chaque JSON `automl_XXs.json` conserve le gagnant, sa configuration, le score de validation interne, le F1 de test externe, la durée et le nombre d'essais.

Les résultats dépendent du temps disponible et de la vitesse de la machine, même avec seed=42. Le budget est indicatif : initialisation et réentraînement du gagnant peuvent provoquer un dépassement. La sélection utilise uniquement la validation interne ; le test est évalué à la fin. Les scores de test des différents budgets servent à l'analyse du TP, pas à une nouvelle optimisation sur ce test.

Les journaux livrés sont les résultats réels de la première exécution. Pour préserver ces preuves, `automl.py` refuse d'écraser un journal existant. Pour refaire une étude, cloner le dépôt dans un nouveau dossier et déplacer les quatre journaux `flaml_XXs.log` dans un sous-dossier d'archive avant les commandes. Relancer les références crée de nouveaux runs ; `verifier.py` est volontairement strict et attend la première expérience de six runs dans une base neuve.

## Fuite de données

`fuite.py` ajoute `num_dossier_litige`, une information produite après la transaction. La simulation conserve la même séparation, puis met cette colonne à zéro pour représenter sa disponibilité au paiement. Les deux scores sont conservés dans `reports/fuite.json` et dans l'expérience distincte `tp4-fuite`.

Ce test est une **simulation locale**, sans déploiement en production. Un score élevé sur l'historique ne remplace pas une vérification métier de la date de disponibilité des variables.

## Livrables et sources

- [Comparatif des approches](reports/comparatif.md), complété avec les mesures réelles et cinq recommandations.
- [Exploration cloud et sources officielles](reports/sources_cloud.md), consultation du 22 octobre 2026. Aucun compte ou entraînement cloud utilisé ; scores cloud non mesurés.
- [Résultats vérifiés](reports/validation.json), journaux FLAML et [graphique de rendement](reports/rendement.png).
- Scripts de référence, recherche, inspection, fuite et contrôle dans `src/`.

`data/`, `.venv/`, la base MLflow et ses artefacts sont exclus de Git. Les journaux de recherche et résultats dans `reports/` sont publiés comme demandé. Ils permettent d'inspecter les essais sans reconstruire la base MLflow.

## Rapport de groupe

- [Compte rendu PDF (12 pages)](rapport/TP04_AutoML_Abdelbaki_Khabot_Lahlou_Hafidi_AI_G6.pdf) : page de garde EMSI/Honoris, cinq captures, résultats réels, comparatif et réponses aux six questions.
- [Captures originales](rapport/captures/) ; le graphique complet est dans [reports/rendement.png](reports/rendement.png).
- [Réponses en texte](reports/questions.md).

Auteurs : **Zakaria Abdelbaki, Amine Khabot, Ismail Lahlou et Rayane Hafidi - AI, G6**.

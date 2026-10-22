# Exploration documentaire des plateformes - TP04

Consultation : **22 octobre 2026**. Aucun compte cloud créé, aucun entraînement ou endpoint cloud lancé ; F1 et temps d'exécution cloud **non mesurés**. Les montants ci-dessous sont des exemples documentaires en USD, hors taxes, à confirmer par région, machine et contrat.

## Google Vertex AI AutoML tabulaire

- Démarrage : projet Google Cloud, facturation, API, autorisations IAM, données et quotas de calcul dans une région compatible [G1].
- Facturation : entraînement en nœud-heures ; tarif à la demande affiché **21,252 USD/nœud-heure** pour classification/régression [G2]. Le produit `21,252 / 60 = 0,3542 USD` est seulement une conversion théorique d'une minute de nœud, pas un devis de job AutoML de 60 secondes. L'endpoint et l'inférence ont leur propre coût ; un modèle déployé peut être facturé sans requête.
- Explications et suivi : évaluations du modèle, importances/attributions selon le mode de service ; suivi des entraînements et des versions du modèle.
- Export : classification/régression tabulaire exportable vers Cloud Storage et exécutable en conteneur Docker sur CPU x86 avec AVX ; explications Vertex indisponibles sur le modèle exporté ; forecasting non exportable par cette procédure [G3]. Réversibilité possible, avec contraintes.

## Amazon SageMaker Autopilot / Canvas

- Démarrage : compte AWS avec facturation, rôle IAM, stockage S3, accès Canvas/Studio et quotas régionaux [A1, A3].
- Facturation : ressources d'entraînement et stockage, hébergement séparé ; Canvas ajoute **1,90 USD/heure de session**. Exemple officiel pour petit jeu tabulaire (<100 Mo) : **2,3 à 9,2 USD d'entraînement**, sans garantie pour ce TP [A2]. La taille du CSV ne permet pas de déduire seule un prix.
- Explications et suivi : candidats classés, métriques, importances, rapports de performance et notebooks de préparation/recherche pour le tabulaire [A1].
- Export : artefacts de modèle disponibles dans S3 et conteneurs d'inférence référencés ; transfert possible, mais l'environnement, les étapes de transformation et les images doivent être reproduits [A4]. Dépendances cloud à examiner avant migration.

## Azure Automated ML

- Démarrage : abonnement Azure, workspace, droits, données et quota de VM par famille/région [M1, M3].
- Facturation : pas de supplément Azure ML annoncé ; VM/compute et services annexes (stockage, registre de conteneurs, logs, etc.) facturés séparément [M2]. Prix dynamique non restitué sur la page consultée : pas de faux tarif VM attribué à Microsoft. Scénario de calcul **hypothétique**, à 0,20 USD/heure pour une VM : 60 s = 0,00333 USD de compute seul ; 24 h d'endpoint à ce même taux = 4,80 USD. Ces valeurs ne sont pas un tarif Azure vérifié.
- Explications et suivi : métriques des jobs/enfants et importance des variables ; modèle sérialisé et prétraitements conservés [M1].
- Export : téléchargement du modèle `.pkl`, du script de scoring et de l'environnement conda [M4]. Migration possible si l'environnement et les dépendances sont compatibles ; ONNX uniquement pour les modèles compatibles.

## Sources officielles

- [G1 - Entraînement AutoML tabulaire](https://docs.cloud.google.com/vertex-ai/docs/tutorials/tabular-automl/dataset-train)
- [G2 - Tarification Google, rubrique AutoML / Tabular data](https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing?hl=en)
- [G3 - Export des modèles tabulaires](https://docs.cloud.google.com/vertex-ai/docs/export/export-model-tabular)
- [A1 - SageMaker Autopilot](https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-automate-model-development.html)
- [A2 - Tarification SageMaker Canvas](https://aws.amazon.com/sagemaker/ai/canvas/pricing/)
- [A3 - Quotas Autopilot](https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-quotas.html)
- [A4 - Artefacts et déploiement Autopilot](https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-deploy-models-realtime.html)
- [M1 - Automated ML](https://learn.microsoft.com/en-us/azure/machine-learning/concept-automated-ml?view=azureml-api-2)
- [M2 - Tarification Azure ML](https://azure.microsoft.com/en-us/pricing/details/machine-learning/)
- [M3 - Quotas Azure ML](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-quotas?view=azureml-api-2)
- [M4 - Télécharger les artefacts AutoML](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-automl-endpoint?view=azureml-api-2)

Certaines anciennes pages Vertex AI redirigent vers les nouvelles rubriques Gemini Enterprise Agent Platform. Les noms de plateformes du sujet sont conservés pour la comparaison.

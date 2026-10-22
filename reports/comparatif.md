# Comparatif des approches - projet fraude (TP04)

Mesures locales sur le même jeu externe de 1 250 transactions ; consultation documentaire du **22 octobre 2026**. Les temps humains sont des estimations de préparation pour un étudiant déjà équipé, **pas un chronométrage**. La durée machine correspond à fit(), hors installation et journalisation MLflow. Aucun score cloud n'a été mesuré.

| Approche | F1 test | Temps humain | Temps machine | Coût estimé (source, date) | Explicabilité | Export / réversibilité |
|---|---:|---|---|---|---|---|
| Logistique (réf.) | 0.7407 | 5-15 min (est.) | 0.0827 s mesurées | 0 de facturation cloud ; énergie et matériel locaux à compter | Coefficients interprétables ; effets des unités à contrôler | Modèle et code locaux, environnement à reproduire |
| Manuel (TP2) | 0.8669 | 30-60 min (est. de réglage ; historique non chronométré) | 1.3822 s pour ce réentraînement | 0 de facturation cloud ; coût humain de sélection distinct | Importances, inspection des erreurs ; forêt moins directe qu'une logistique | Code et modèle locaux ; dépendances Python |
| FLAML 60 s (lgbm) | 0.8409 | 10-20 min (est. de configuration) | 60.571 s mesurées, budget 60 s | 0 de facture cloud ; CPU, énergie et suivi humain | Journal complet et config gagnante ; explication selon famille | Bibliothèque et estimateur locaux, environnement à conserver |
| Vertex AI AutoML | non mesuré | 30-90 min (est., compte déjà disponible) | non mesuré | 21,252 USD/nœud-heure affichés ; endpoint en plus [G2, 22/10/2026] | Évaluations et attributions selon mode | Export tabulaire classification/régression en conteneur ; contraintes AVX, explications exportées limitées [G3] |
| SageMaker Autopilot / Canvas | non mesuré | 30-90 min (est.) | non mesuré | Session Canvas 1,90 USD/h ; exemple <100 Mo : 2,3-9,2 USD de training ; hébergement en plus [A2, 22/10/2026] | Rapports, importances et notebooks de candidats [A1] | Artefacts S3 et conteneurs ; environnement et transformations à reproduire [A4] |
| Azure Automated ML | non mesuré | 30-90 min (est.) | non mesuré | VM × durée + services annexes ; pas de supplément Azure ML annoncé ; montant VM dépend de la région [M2, 22/10/2026] | Métriques des jobs et importance des variables [M1] | Téléchargement modèle, scoring et environnement [M4] ; portabilité à vérifier |

## Commentaire (5 lignes)
1. La logistique convient à une première référence rapide et lisible ; le réglage manuel est utile pour exploiter une expertise déjà acquise sur une famille.
2. FLAML convient pour explorer plusieurs familles sans écrire chaque grille ; le gain à 60 s est ici de -0.0260 point F1 par rapport au RF manuel.
3. Vertex AI est pertinent lorsque les données et l'exploitation sont déjà chez Google ; l'export tabulaire réduit une partie de la dépendance mais conserve des contraintes.
4. Autopilot/Canvas est adapté à une équipe AWS qui veut des candidats et des notebooks inspectables avec une interface low-code.
5. Azure Automated ML est pertinent dans un environnement Azure existant ; les trois clouds exigent un contrôle des coûts, des données, de la disponibilité des variables et des conditions d'export.

## Coût réel : hypothèses explicites

Le coût local n'est pas nul : temps humain, amortissement et énergie. À titre d'illustration, une consommation **supposée** de 60 W pendant 60.571 s donne 0.001010 kWh. Le prix réel de l'électricité et la puissance n'ont pas été mesurés. Pour le cloud, les 60 s de FLAML ne sont pas transposables en un prix de job managé : essais parallèles, ressources, minimums et stockage changent le calcul. Les références tarifaires et leurs limites sont dans [sources_cloud.md](sources_cloud.md).

**Réversibilité** : les plateformes cloud ne sont pas toutes inexportables. Distinguer le fichier ou conteneur exporté de la reproduction de toute la chaîne (prétraitements, environnement, explications, monitoring).

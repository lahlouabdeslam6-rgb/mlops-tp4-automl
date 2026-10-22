# Réponses aux six questions du TP04

## 1. Réglage manuel ou AutoML ?
Le RF manuel réentraîné obtient 0.8669 ; FLAML 60 s (lgbm) obtient 0.8409, soit -0.0260. Une faible différence ne supprime pas l'intérêt de l'AutoML : il fournit une exploration de familles et de configurations dans un budget explicite. En revanche, le choix final doit considérer stabilité, coût, interprétabilité et erreurs métier. Les budgets indépendants ne garantissent pas une progression monotone du F1 externe.

## 2. Le coût réel
Le fit() FLAML de 60 s a duré 60.571 s. Aucune facture cloud locale, mais le CPU, l'énergie, le matériel et la préparation ont un coût. La puissance et le travail humain n'ont pas été mesurés ; les estimations du comparatif sont identifiées. Dans le cloud, calculer la somme des ressources × durées, puis ajouter stockage, sessions, inférence et services associés. Les exemples documentaires ne sont pas des devis du TP et aucun job cloud n'a été exécuté.

## 3. Ce qui reste à notre charge
1. Définir le problème et contrôler les labels, les variables et leur date de disponibilité.
2. Concevoir un découpage d'évaluation pertinent, sans fuite, avec une métrique alignée sur les coûts des faux positifs et faux négatifs.
3. Valider les modèles et organiser l'exploitation : contrôle humain, sécurité, traçabilité, coûts, dérive et surveillance des erreurs.

## 4. Managé ou local ?
Une plateforme managée est utile à une équipe disposant déjà de données dans ce cloud et ayant besoin de calcul élastique, de rôles d'accès, d'un registre et d'endpoints partagés. Une bibliothèque locale convient à ce petit jeu de 5 000 lignes, à un budget limité et à une expérimentation contrôlée. Comparer les coûts complets et l'effort d'exploitation, pas seulement le prix du fit().

## 5. Secteur régulé
Il faut pouvoir documenter la provenance et les versions des données, la disponibilité temporelle des variables, les transformations, les essais et réglages, le protocole d'évaluation, les erreurs par sous-groupe, les explications et limites. Les versions du code, de l'environnement et du modèle, les accès, approbations et décisions de promotion doivent être auditables. L'existence d'un rapport d'importance des variables ne garantit pas à elle seule la conformité ou l'absence de fuite.

## 6. La fuite de données
Dans notre simulation, F1 historique=1.0000, contre 0.0000 lorsque num_dossier_litige est mis à zéro. Cette colonne révèle la fraude après contestation et ne peut pas être connue au paiement. Un découpage aléatoire conserve ce raccourci dans train et test : FLAML l'exploite sans connaître sa signification métier. Avant déploiement, auditer les dates de création, interdire les variables postérieures à la décision, contrôler les importances et refaire un test temporel reproduisant l'information disponible en ligne. Le second score est une production simulée, pas un déploiement réel.

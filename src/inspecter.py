import json
import sys
from pathlib import Path
from collections import Counter
from common import ROOT, REPORTS, save_json

fichier=Path(sys.argv[1]) if len(sys.argv)>1 else REPORTS/'flaml_60s.log'
if not fichier.is_absolute():
    fichier=ROOT/fichier
essais=[]
for ligne in fichier.read_text(encoding='utf-8').splitlines():
    if ligne.strip().startswith('{'):
        e=json.loads(ligne)
        if 'learner' in e and e.get('validation_loss') is not None:
            essais.append(e)
if not essais:
    raise SystemExit('Aucun essai lisible : vérifier le format du journal.')
compte=dict(Counter(e['learner'] for e in essais))
print(len(essais),'essais journalises dans',fichier.name)
print('essais par famille :',compte)
meilleurs={}
for e in essais:
    f=e['learner']
    if f not in meilleurs or e['validation_loss']<meilleurs[f]['validation_loss']:
        meilleurs[f]=e
print('\nMeilleur F1 de validation par famille (F1 = 1 - perte) :')
for f,e in sorted(meilleurs.items(),key=lambda kv:kv[1]['validation_loss']):
    print(f"  {f:15s} F1 val = {1-e['validation_loss']:.4f} (trouve apres {e.get('wall_clock_time',0):.1f} s)")
gagnant=min(essais,key=lambda e:e['validation_loss'])
print('\nEssai gagnant :',gagnant['learner'],gagnant.get('config'))
save_json(f'inspection_{fichier.stem}.json',dict(nb_essais=len(essais),par_famille=compte,
          meilleurs=meilleurs,gagnant=gagnant))

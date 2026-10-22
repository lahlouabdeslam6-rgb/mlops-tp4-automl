import mlflow
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import setup_tracking, REPORTS

setup_tracking()
runs=mlflow.search_runs(experiment_names=['tp4-automl'])
auto=runs[runs['params.outil'].isin(['flaml','sklearn-maison'])].copy()
auto['budget']=auto['params.budget_s'].astype(int)
auto=auto.drop_duplicates(['params.outil','budget']).sort_values('budget')
refs=runs[runs['params.outil']=='scikit-learn'].drop_duplicates('tags.mlflow.runName')
fig,ax=plt.subplots(figsize=(8,4.7))
for outil,g in auto.groupby('params.outil'):
    ax.plot(g.budget,g['metrics.f1'],'o-',color='#00894a',label=f'AutoML ({outil})')
    for b,f in zip(g.budget,g['metrics.f1']):
        print(f'{outil:15s} budget {b:4d} s -> F1 {f:.4f}')
        ax.annotate(f'{f:.4f}',(b,f),xytext=(0,8),textcoords='offset points',ha='center',fontsize=9)
for idx,(_,r) in enumerate(refs.iterrows()):
    nom,f=r['tags.mlflow.runName'],r['metrics.f1']
    ax.axhline(f,ls='--',lw=1.3,color=['#26364d','#aa6530'][idx],label=f'{nom} ({f:.4f})')
    print(f'{nom:22s} F1 {f:.4f}')
ax.set_xscale('log')
budgets=sorted(auto.budget.unique())
ax.set_xticks(budgets,[str(b) for b in budgets]);ax.minorticks_off()
ax.set_xlabel('Budget de calcul (secondes, echelle log)');ax.set_ylabel('F1 sur le jeu de test')
ax.set_title('Rendement du budget de calcul');ax.grid(alpha=.2)
ax.margins(y=.2);ax.legend(loc='best',fontsize=8)
fig.savefig(REPORTS/'rendement.png',dpi=180,bbox_inches='tight');plt.close(fig)
print('graphique ecrit : reports/rendement.png')

# HR Attrition Analysis

**Auteur :** Bouziane Samir — Data Analyst & BI Developer  
**Stack :** Python · Pandas · SQL · Tableau  
**Dataset :** IBM HR Analytics — 1 470 employés, 33 variables

---

## Problématique

> Une entreprise perd **16.4% de ses effectifs** chaque année.  
> Quels sont les profils à risque ? Quels leviers activer pour réduire ce coût ?

---

## Résultats clés

| Insight | Constat | Action |
|---------|---------|--------|
| **Overtime** | Taux x2.0 vs employés sans heures sup (25.6% vs 13%) | Plafonner les heures, compenser financièrement |
| **Salaire** | < $3K/mois → 27.7% d'attrition | Revalorisation ciblée |
| **Ancienneté** | Pic de départs avant 3 ans (30.3% en < 1 an) | Onboarding renforcé |
| **Département** | Sales : 17.7% vs HR : 12% | Revoir quotas et incentives |
| **Satisfaction** | Score très faible → 31.2% d'attrition | Enquêtes trimestrielles |

**Impact estimé :** réduire l'attrition de 16% → 10% = **$880K–$2.2M économisés/an**

---

## Structure du projet

```
hr-attrition-analysis/
├── data/
│   ├── raw/
│   │   ├── generate_dataset.py   ← génère hr_raw.csv
│   │   └── hr_raw.csv            ← données brutes (avec erreurs intentionnelles)
│   └── cleaned/
│       └── hr_cleaned.csv        ← données nettoyées + features dérivées
├── notebooks/
│   ├── 01_data_cleaning.py       ← audit qualité + nettoyage complet
│   └── 02_eda_insights.py        ← EDA + 6 insights business
├── sql/
│   └── hr_analysis.sql           ← 10 requêtes d'analyse (window functions incluses)
├── dashboard/
│   └── tableau_specs.md          ← spécifications du dashboard Tableau
└── README.md
```

---

## Étapes du projet

### 1. Data Cleaning (`01_data_cleaning.py`)
- Audit qualité : valeurs manquantes, doublons, aberrants
- Normalisation texte (casse, espaces)
- Imputation `MonthlyIncome` par médiane/JobLevel
- Correction des âges négatifs
- Création de features : `AgeGroup`, `SalaryBand`, `SatisfactionScore`, `AttritionBinary`

### 2. EDA & Insights (`02_eda_insights.py`)
- 6 insights business avec recommandations chiffrées
- Résumé exécutif avec impact financier estimé

### 3. SQL (`hr_analysis.sql`)
- 10 requêtes analytiques
- Window functions (RANK, PARTITION BY)
- Profil comparatif : employé parti vs resté
- Estimation du coût de l'attrition

### 4. Dashboard Tableau
- 7 vues interactives
- Filtres : département, genre, tranche d'âge, overtime

---

## Lancer le projet

```bash
# 1. Générer le dataset
cd data/raw && python3 generate_dataset.py

# 2. Nettoyage
cd notebooks && python3 01_data_cleaning.py

# 3. EDA
python3 02_eda_insights.py

# 4. SQL → importer hr_cleaned.csv dans DB Browser for SQLite
# puis exécuter sql/hr_analysis.sql
```

---

## Contact

**Bouziane Samir** — Data Analyst & BI Developer  
[LinkedIn](https://linkedin.com/in/bouzianesamir) · [GitHub](https://github.com/samir-data-cloud) · m.salahbouziane@gmail.com

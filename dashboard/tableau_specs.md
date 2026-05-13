# HR Attrition Dashboard — Spécifications Tableau

## Source de données
Fichier : `data/cleaned/hr_cleaned.csv`

## Vues à créer

### 1. KPI Header (texte dynamique)
- Taux d'attrition global
- Nombre de départs
- Effectif total
- Salaire médian

### 2. Attrition par département (Bar chart horizontal)
- Dimension : Department
- Mesure : AVG(AttritionBinary) → format %
- Couleur : gradient rouge (haut) → vert (bas)
- Trier : décroissant

### 3. Impact Overtime (Side-by-side bar)
- Dimension : OverTime
- Mesure : COUNT() + AVG(AttritionBinary)
- Annotation : "x2.5 plus de départs en overtime"

### 4. Attrition par tranche d'âge (Bar chart)
- Dimension : AgeGroup
- Mesure : AVG(AttritionBinary)
- Référence : ligne moyenne globale

### 5. Salaire vs Attrition (Scatter plot)
- X : MonthlyIncome
- Y : SatisfactionScore
- Couleur : Attrition (Yes = rouge, No = gris)
- Taille : YearsAtCompany

### 6. Ancienneté critique (Line chart)
- Dimension : YearsAtCompany (0 à 15)
- Mesure : AVG(AttritionBinary)
- Annotation zone critique : 0-3 ans

### 7. Heatmap satisfaction (Text table)
- Lignes : JobSatisfaction (1-4)
- Colonnes : WorkLifeBalance (1-4)
- Valeur : AVG(AttritionBinary) → couleur

## Filtres interactifs
- Department (multi-select)
- Gender
- AgeGroup
- OverTime (Yes/No)

## Palette couleurs
- Rouge attrition : #E24B4A
- Vert rétention  : #1D9E75
- Fond            : #F5F4F0
- Texte           : #1A1A18

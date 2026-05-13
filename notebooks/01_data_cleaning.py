"""
HR Attrition Analysis — Étape 1 : Data Cleaning
Auteur : Bouziane Samir — Data Analyst & BI Developer
Dataset : IBM HR Analytics (1470 employés, 33 colonnes)
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# 1. CHARGEMENT
# ─────────────────────────────────────────────
df = pd.read_csv("../data/raw/hr_raw.csv")

print("=" * 55)
print("  HR ATTRITION — DATA CLEANING REPORT")
print("=" * 55)
print(f"\n{'Shape initial':<30} {df.shape}")
print(f"{'Colonnes':<30} {df.shape[1]}")
print(f"{'Lignes':<30} {df.shape[0]}")

# ─────────────────────────────────────────────
# 2. AUDIT QUALITÉ INITIALE
# ─────────────────────────────────────────────
print("\n── Valeurs manquantes ──────────────────────")
missing = df.isnull().sum()
print(missing[missing > 0].to_string())

print("\n── Doublons ────────────────────────────────")
dupes = df.duplicated().sum()
print(f"Doublons détectés : {dupes}")

print("\n── Valeurs aberrantes (Age) ────────────────")
print(df["Age"].describe())
neg_age = (df["Age"] < 0).sum()
print(f"Ages négatifs : {neg_age}")

print("\n── Valeurs mal formatées (Department) ──────")
print(df["Department"].value_counts())

print("\n── Valeurs mal formatées (Gender) ──────────")
print(df["Gender"].value_counts())

# ─────────────────────────────────────────────
# 3. NETTOYAGE
# ─────────────────────────────────────────────
df_clean = df.copy()

# 3a. Colonnes inutiles (constantes)
cols_to_drop = ["EmployeeCount", "Over18", "StandardHours"]
df_clean.drop(columns=cols_to_drop, inplace=True)
print(f"\n── Colonnes supprimées (constantes) : {cols_to_drop}")

# 3b. Normalisation texte
df_clean["Department"] = df_clean["Department"].str.strip().str.title()
df_clean["Gender"] = df_clean["Gender"].str.strip().str.capitalize()
print("── Normalisation texte : Department, Gender ✓")

# 3c. Ages aberrants → médiane par département
median_age = df_clean.loc[df_clean["Age"] > 0, "Age"].median()
invalid_age = df_clean["Age"] < 18
df_clean.loc[invalid_age, "Age"] = int(median_age)
print(f"── Ages invalides corrigés ({invalid_age.sum()}) → médiane {int(median_age)} ✓")

# 3d. MonthlyIncome manquant → médiane par JobLevel
for level in df_clean["JobLevel"].unique():
    mask_null = df_clean["MonthlyIncome"].isnull() & (df_clean["JobLevel"] == level)
    med = df_clean.loc[df_clean["JobLevel"] == level, "MonthlyIncome"].median()
    df_clean.loc[mask_null, "MonthlyIncome"] = med
print(f"── MonthlyIncome manquant imputé par médiane/JobLevel ✓")

# 3e. Types
df_clean["MonthlyIncome"] = df_clean["MonthlyIncome"].astype(int)

# 3f. Features dérivées
df_clean["AgeGroup"] = pd.cut(
    df_clean["Age"],
    bins=[17, 25, 35, 45, 60],
    labels=["18-25", "26-35", "36-45", "46-60"]
)
df_clean["SalaryBand"] = pd.cut(
    df_clean["MonthlyIncome"],
    bins=[0, 3000, 6000, 10000, 25000],
    labels=["< 3K", "3K-6K", "6K-10K", "> 10K"]
)
df_clean["SatisfactionScore"] = (
    df_clean["JobSatisfaction"] +
    df_clean["EnvironmentSatisfaction"] +
    df_clean["WorkLifeBalance"]
) / 3
df_clean["SatisfactionScore"] = df_clean["SatisfactionScore"].round(2)

df_clean["AttritionBinary"] = (df_clean["Attrition"] == "Yes").astype(int)

print("── Features dérivées créées : AgeGroup, SalaryBand, SatisfactionScore, AttritionBinary ✓")

# ─────────────────────────────────────────────
# 4. RAPPORT FINAL
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  RÉSULTAT APRÈS NETTOYAGE")
print("=" * 55)
print(f"{'Shape final':<35} {df_clean.shape}")
print(f"{'Valeurs manquantes restantes':<35} {df_clean.isnull().sum().sum()}")
print(f"{'Taux d attrition global':<35} {df_clean['AttritionBinary'].mean():.1%}")
print(f"{'Âge moyen':<35} {df_clean['Age'].mean():.1f} ans")
print(f"{'Salaire mensuel médian':<35} ${df_clean['MonthlyIncome'].median():,.0f}")

print("\n── Attrition par département ───────────────")
dept_attr = df_clean.groupby("Department")["AttritionBinary"].agg(
    Effectif="count",
    Attrition_n="sum",
    Taux=lambda x: f"{x.mean():.1%}"
)
print(dept_attr.to_string())

print("\n── Attrition Overtime vs Non-Overtime ──────")
ot_attr = df_clean.groupby("OverTime")["AttritionBinary"].agg(
    Effectif="count",
    Taux=lambda x: f"{x.mean():.1%}"
)
print(ot_attr.to_string())

# ─────────────────────────────────────────────
# 5. EXPORT
# ─────────────────────────────────────────────
df_clean.to_csv("../data/cleaned/hr_cleaned.csv", index=False)
print(f"\n✓ Fichier exporté : data/cleaned/hr_cleaned.csv")
print("=" * 55)

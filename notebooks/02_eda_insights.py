"""
HR Attrition Analysis — Étape 2 : EDA & Insights
Auteur : Bouziane Samir — Data Analyst & BI Developer
"""

import pandas as pd
import numpy as np

df = pd.read_csv("../data/cleaned/hr_cleaned.csv")

SEP = "─" * 55

def section(title):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)

# ─────────────────────────────────────────────
# KPI GLOBAUX
# ─────────────────────────────────────────────
section("KPI GLOBAUX")

total = len(df)
attr_n = df["AttritionBinary"].sum()
attr_rate = df["AttritionBinary"].mean()
avg_age = df["Age"].mean()
avg_income = df["MonthlyIncome"].mean()
avg_tenure = df["YearsAtCompany"].mean()

print(f"{'Effectif total':<35} {total}")
print(f"{'Départs (Attrition = Yes)':<35} {attr_n}")
print(f"{'Taux d attrition':<35} {attr_rate:.1%}")
print(f"{'Âge moyen':<35} {avg_age:.1f} ans")
print(f"{'Salaire mensuel moyen':<35} ${avg_income:,.0f}")
print(f"{'Ancienneté moyenne':<35} {avg_tenure:.1f} ans")

# ─────────────────────────────────────────────
# INSIGHT 1 — ATTRITION PAR DÉPARTEMENT
# ─────────────────────────────────────────────
section("INSIGHT 1 — Attrition par département")

dept = df.groupby("Department").agg(
    Effectif=("AttritionBinary", "count"),
    Départs=("AttritionBinary", "sum"),
    Taux=("AttritionBinary", "mean")
).sort_values("Taux", ascending=False)
dept["Taux"] = dept["Taux"].map("{:.1%}".format)
print(dept.to_string())
print("\n→ ACTION : Le département Sales présente le taux d'attrition le plus élevé.")
print("  Investiguer : quotas trop élevés, management, rémunération variable.")

# ─────────────────────────────────────────────
# INSIGHT 2 — OVERTIME = FACTEUR CLÉ
# ─────────────────────────────────────────────
section("INSIGHT 2 — Impact des heures supplémentaires")

ot = df.groupby("OverTime").agg(
    Effectif=("AttritionBinary", "count"),
    Départs=("AttritionBinary", "sum"),
    Taux=("AttritionBinary", "mean")
)
ot["Taux"] = ot["Taux"].map("{:.1%}".format)
print(ot.to_string())

rate_yes = df.loc[df["OverTime"] == "Yes", "AttritionBinary"].mean()
rate_no  = df.loc[df["OverTime"] == "No",  "AttritionBinary"].mean()
print(f"\n→ ACTION : Les employés en overtime ont {rate_yes/rate_no:.1f}x plus de risque de partir.")
print("  Recommandation : plafonner les heures sup, compenser financièrement.")

# ─────────────────────────────────────────────
# INSIGHT 3 — ATTRITION PAR TRANCHE D'ÂGE
# ─────────────────────────────────────────────
section("INSIGHT 3 — Attrition par tranche d'âge")

age_g = df.groupby("AgeGroup", observed=True).agg(
    Effectif=("AttritionBinary", "count"),
    Départs=("AttritionBinary", "sum"),
    Taux=("AttritionBinary", "mean")
).sort_values("Taux", ascending=False)
age_g["Taux"] = age_g["Taux"].map("{:.1%}".format)
print(age_g.to_string())
print("\n→ ACTION : Les 18-25 ans sont les plus volatiles. Mettre en place")
print("  un programme d'onboarding renforcé et un plan de carrière clair.")

# ─────────────────────────────────────────────
# INSIGHT 4 — SALAIRE & ATTRITION
# ─────────────────────────────────────────────
section("INSIGHT 4 — Attrition par tranche salariale")

sal = df.groupby("SalaryBand", observed=True).agg(
    Effectif=("AttritionBinary", "count"),
    Départs=("AttritionBinary", "sum"),
    Taux=("AttritionBinary", "mean")
).sort_values("Taux", ascending=False)
sal["Taux"] = sal["Taux"].map("{:.1%}".format)
print(sal.to_string())
print("\n→ ACTION : Les bas salaires (< $3K/mois) concentrent le risque de départ.")
print("  Une revalorisation ciblée réduirait significativement le turnover.")

# ─────────────────────────────────────────────
# INSIGHT 5 — SATISFACTION & ATTRITION
# ─────────────────────────────────────────────
section("INSIGHT 5 — Score de satisfaction vs Attrition")

df["SatisfactionBand"] = pd.cut(
    df["SatisfactionScore"],
    bins=[0, 1.5, 2.5, 3.5, 4.0],
    labels=["Très faible", "Faible", "Moyen", "Élevé"]
)
sat = df.groupby("SatisfactionBand", observed=True).agg(
    Effectif=("AttritionBinary", "count"),
    Taux=("AttritionBinary", "mean")
).sort_values("Taux", ascending=False)
sat["Taux"] = sat["Taux"].map("{:.1%}".format)
print(sat.to_string())
print("\n→ ACTION : Corrélation forte satisfaction ↔ rétention.")
print("  Mettre en place des enquêtes de satisfaction trimestrielles.")

# ─────────────────────────────────────────────
# INSIGHT 6 — ANCIENNETÉ CRITIQUE
# ─────────────────────────────────────────────
section("INSIGHT 6 — Fenêtre d'ancienneté critique")

df["TenureGroup"] = pd.cut(
    df["YearsAtCompany"],
    bins=[-1, 1, 3, 5, 10, 40],
    labels=["< 1 an", "1-3 ans", "3-5 ans", "5-10 ans", "> 10 ans"]
)
tenure = df.groupby("TenureGroup", observed=True).agg(
    Effectif=("AttritionBinary", "count"),
    Départs=("AttritionBinary", "sum"),
    Taux=("AttritionBinary", "mean")
)
tenure["Taux"] = tenure["Taux"].map("{:.1%}".format)
print(tenure.to_string())
print("\n→ ACTION : Le pic de départs est dans les 3 premières années.")
print("  Investir dans l'onboarding et les promotions précoces.")

# ─────────────────────────────────────────────
# RÉSUMÉ EXÉCUTIF
# ─────────────────────────────────────────────
section("RÉSUMÉ EXÉCUTIF — TOP RECOMMANDATIONS")

print("""
  CONSTAT : Taux d'attrition global de {:.1%} ({} départs / {} employés)

  LEVIERS D'ACTION PRIORITAIRES :

  1. 🔴 OVERTIME   — Réduire les heures sup : impact x{:.1f} sur attrition
  2. 🟠 SALAIRE    — Revaloriser les < $3K/mois (taux le + élevé)
  3. 🟡 JEUNES     — Programme d'onboarding renforcé pour 18-25 ans
  4. 🟢 DEPT SALES — Revoir objectifs, incentives et management
  5. 🔵 RÉTENTION  — Agir avant 3 ans d'ancienneté (pic de départs)

  IMPACT ESTIMÉ : réduire l'attrition de ~16% → ~10% représente
  environ 88 départs évités/an, soit une économie estimée de
  $880K–$2.2M (coût moyen d'un départ = $10K–$25K).
""".format(
    attr_rate, attr_n, total,
    rate_yes / rate_no
))

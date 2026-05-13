"""
Génère un dataset RH réaliste de 1470 employés
inspiré du dataset IBM HR Analytics (domaine public).
"""
import pandas as pd
import numpy as np

np.random.seed(42)
n = 1470

departments = ["Sales", "Research & Development", "Human Resources"]
dept_weights = [0.30, 0.60, 0.10]

job_roles = {
    "Sales": ["Sales Executive", "Sales Representative", "Manager"],
    "Research & Development": ["Research Scientist", "Laboratory Technician",
                               "Healthcare Representative", "Manufacturing Director",
                               "Research Director", "Manager"],
    "Human Resources": ["Human Resources", "Manager"],
}

education_fields = ["Life Sciences", "Medical", "Marketing",
                    "Technical Degree", "Human Resources", "Other"]
business_travel = ["Non-Travel", "Travel_Rarely", "Travel_Frequently"]
marital_status = ["Single", "Married", "Divorced"]

dept_col = np.random.choice(departments, n, p=dept_weights)
role_col = [np.random.choice(job_roles[d]) for d in dept_col]

age = np.random.randint(18, 61, n)
monthly_income = np.random.randint(1000, 20000, n)
years_at_company = np.random.randint(0, 41, n)
years_in_role = np.clip(np.random.randint(0, years_at_company + 1), 0, years_at_company)
job_satisfaction = np.random.randint(1, 5, n)
environment_satisfaction = np.random.randint(1, 5, n)
work_life_balance = np.random.randint(1, 5, n)
overtime = np.random.choice(["Yes", "No"], n, p=[0.28, 0.72])
distance_from_home = np.random.randint(1, 30, n)
num_companies_worked = np.random.randint(0, 10, n)
percent_salary_hike = np.random.randint(11, 26, n)
training_times = np.random.randint(0, 7, n)
performance_rating = np.random.choice([3, 4], n, p=[0.85, 0.15])
job_level = np.random.randint(1, 6, n)
stock_option_level = np.random.randint(0, 4, n)

# Attrition logique : influencée par satisfaction, overtime, salaire, ancienneté
attrition_prob = (
    0.10
    + (overtime == "Yes") * 0.15
    + (job_satisfaction == 1) * 0.12
    + (monthly_income < 3000) * 0.10
    + (years_at_company <= 2) * 0.08
    + (work_life_balance == 1) * 0.08
    - (job_level >= 4) * 0.06
    - (years_at_company >= 10) * 0.05
)
attrition_prob = np.clip(attrition_prob, 0.02, 0.75)
attrition = np.where(np.random.random(n) < attrition_prob, "Yes", "No")

df = pd.DataFrame({
    "EmployeeID": range(1, n + 1),
    "Age": age,
    "Attrition": attrition,
    "BusinessTravel": np.random.choice(business_travel, n, p=[0.19, 0.71, 0.10]),
    "Department": dept_col,
    "DistanceFromHome": distance_from_home,
    "Education": np.random.randint(1, 6, n),
    "EducationField": np.random.choice(education_fields, n),
    "EmployeeCount": 1,
    "EnvironmentSatisfaction": environment_satisfaction,
    "Gender": np.random.choice(["Male", "Female"], n, p=[0.60, 0.40]),
    "JobInvolvement": np.random.randint(1, 5, n),
    "JobLevel": job_level,
    "JobRole": role_col,
    "JobSatisfaction": job_satisfaction,
    "MaritalStatus": np.random.choice(marital_status, n, p=[0.32, 0.46, 0.22]),
    "MonthlyIncome": monthly_income,
    "MonthlyRate": np.random.randint(2000, 27000, n),
    "NumCompaniesWorked": num_companies_worked,
    "Over18": "Y",
    "OverTime": overtime,
    "PercentSalaryHike": percent_salary_hike,
    "PerformanceRating": performance_rating,
    "RelationshipSatisfaction": np.random.randint(1, 5, n),
    "StandardHours": 80,
    "StockOptionLevel": stock_option_level,
    "TotalWorkingYears": np.random.randint(0, 41, n),
    "TrainingTimesLastYear": training_times,
    "WorkLifeBalance": work_life_balance,
    "YearsAtCompany": years_at_company,
    "YearsInCurrentRole": years_in_role,
    "YearsSinceLastPromotion": np.random.randint(0, 16, n),
    "YearsWithCurrManager": np.random.randint(0, 18, n),
})

# Introduce intentional dirty data for cleaning exercise
dirty_idx = np.random.choice(n, 45, replace=False)
df.loc[dirty_idx[:15], "MonthlyIncome"] = None
df.loc[dirty_idx[15:25], "Age"] = -1
df.loc[dirty_idx[25:35], "Department"] = "  research & development  "
df.loc[dirty_idx[35:45], "Gender"] = "male"

df.to_csv("hr_raw.csv", index=False)
print(f"Dataset généré : {n} lignes, {df.shape[1]} colonnes")
print(f"Attrition rate : {(df['Attrition']=='Yes').mean():.1%}")
print(f"Valeurs manquantes : {df.isnull().sum().sum()}")
print("Fichier : data/raw/hr_raw.csv")

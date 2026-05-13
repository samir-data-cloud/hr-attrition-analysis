-- ============================================================
-- HR Attrition Analysis — Requêtes SQL
-- Auteur : Bouziane Samir — Data Analyst & BI Developer
-- Base   : hr_cleaned (1470 lignes, 32 colonnes)
-- ============================================================

-- ─────────────────────────────────────────────────────────────
-- 0. CRÉATION DE LA TABLE (SQLite / PostgreSQL compatible)
-- ─────────────────────────────────────────────────────────────
/*
CREATE TABLE hr_employees (
    EmployeeID          INTEGER PRIMARY KEY,
    Age                 INTEGER,
    Attrition           TEXT,
    AttritionBinary     INTEGER,
    BusinessTravel      TEXT,
    Department          TEXT,
    DistanceFromHome    INTEGER,
    Education           INTEGER,
    EducationField      TEXT,
    EnvironmentSatisfaction INTEGER,
    Gender              TEXT,
    JobInvolvement      INTEGER,
    JobLevel            INTEGER,
    JobRole             TEXT,
    JobSatisfaction     INTEGER,
    MaritalStatus       TEXT,
    MonthlyIncome       INTEGER,
    NumCompaniesWorked  INTEGER,
    OverTime            TEXT,
    PercentSalaryHike   INTEGER,
    PerformanceRating   INTEGER,
    RelationshipSatisfaction INTEGER,
    StockOptionLevel    INTEGER,
    TotalWorkingYears   INTEGER,
    TrainingTimesLastYear INTEGER,
    WorkLifeBalance     INTEGER,
    YearsAtCompany      INTEGER,
    YearsInCurrentRole  INTEGER,
    YearsSinceLastPromotion INTEGER,
    YearsWithCurrManager INTEGER,
    AgeGroup            TEXT,
    SalaryBand          TEXT,
    SatisfactionScore   REAL
);
*/

-- ─────────────────────────────────────────────────────────────
-- 1. KPI GLOBAUX
-- ─────────────────────────────────────────────────────────────
SELECT
    COUNT(*)                                        AS total_employes,
    SUM(AttritionBinary)                            AS total_departs,
    ROUND(AVG(AttritionBinary) * 100, 1)           AS taux_attrition_pct,
    ROUND(AVG(Age), 1)                              AS age_moyen,
    ROUND(AVG(MonthlyIncome), 0)                   AS salaire_moyen,
    ROUND(AVG(YearsAtCompany), 1)                  AS anciennete_moyenne
FROM hr_employees;


-- ─────────────────────────────────────────────────────────────
-- 2. ATTRITION PAR DÉPARTEMENT
-- ─────────────────────────────────────────────────────────────
SELECT
    Department,
    COUNT(*)                                        AS effectif,
    SUM(AttritionBinary)                            AS departs,
    ROUND(AVG(AttritionBinary) * 100, 1)           AS taux_pct,
    ROUND(AVG(MonthlyIncome), 0)                   AS salaire_moyen
FROM hr_employees
GROUP BY Department
ORDER BY taux_pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 3. IMPACT DE L'OVERTIME SUR L'ATTRITION
-- ─────────────────────────────────────────────────────────────
SELECT
    OverTime,
    COUNT(*)                                        AS effectif,
    SUM(AttritionBinary)                            AS departs,
    ROUND(AVG(AttritionBinary) * 100, 1)           AS taux_pct,
    ROUND(AVG(SatisfactionScore), 2)               AS satisfaction_moy
FROM hr_employees
GROUP BY OverTime
ORDER BY taux_pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 4. ATTRITION PAR TRANCHE D'ÂGE
-- ─────────────────────────────────────────────────────────────
SELECT
    AgeGroup,
    COUNT(*)                                        AS effectif,
    SUM(AttritionBinary)                            AS departs,
    ROUND(AVG(AttritionBinary) * 100, 1)           AS taux_pct
FROM hr_employees
GROUP BY AgeGroup
ORDER BY taux_pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 5. ATTRITION PAR TRANCHE SALARIALE
-- ─────────────────────────────────────────────────────────────
SELECT
    SalaryBand,
    COUNT(*)                                        AS effectif,
    SUM(AttritionBinary)                            AS departs,
    ROUND(AVG(AttritionBinary) * 100, 1)           AS taux_pct,
    ROUND(AVG(MonthlyIncome), 0)                   AS salaire_moyen
FROM hr_employees
GROUP BY SalaryBand
ORDER BY taux_pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 6. TOP 10 POSTES LES PLUS À RISQUE
-- ─────────────────────────────────────────────────────────────
SELECT
    JobRole,
    Department,
    COUNT(*)                                        AS effectif,
    SUM(AttritionBinary)                            AS departs,
    ROUND(AVG(AttritionBinary) * 100, 1)           AS taux_pct,
    ROUND(AVG(MonthlyIncome), 0)                   AS salaire_moyen,
    ROUND(AVG(SatisfactionScore), 2)               AS satisfaction_moy
FROM hr_employees
GROUP BY JobRole, Department
HAVING COUNT(*) >= 20
ORDER BY taux_pct DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- 7. FENÊTRE D'ANCIENNETÉ CRITIQUE (1-3 ANS)
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN YearsAtCompany < 1  THEN '< 1 an'
        WHEN YearsAtCompany <= 3 THEN '1-3 ans'
        WHEN YearsAtCompany <= 5 THEN '3-5 ans'
        WHEN YearsAtCompany <= 10 THEN '5-10 ans'
        ELSE '> 10 ans'
    END                                             AS tranche_anciennete,
    COUNT(*)                                        AS effectif,
    SUM(AttritionBinary)                            AS departs,
    ROUND(AVG(AttritionBinary) * 100, 1)           AS taux_pct
FROM hr_employees
GROUP BY tranche_anciennete
ORDER BY taux_pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 8. PROFIL TYPE DE L'EMPLOYÉ QUI PART
-- ─────────────────────────────────────────────────────────────
SELECT
    'Employé parti'                                 AS profil,
    ROUND(AVG(Age), 1)                              AS age_moyen,
    ROUND(AVG(MonthlyIncome), 0)                   AS salaire_moyen,
    ROUND(AVG(YearsAtCompany), 1)                  AS anciennete_moy,
    ROUND(AVG(SatisfactionScore), 2)               AS satisfaction_moy,
    ROUND(AVG(CASE WHEN OverTime='Yes' THEN 1.0 ELSE 0.0 END)*100,1) AS pct_overtime
FROM hr_employees WHERE AttritionBinary = 1

UNION ALL

SELECT
    'Employé resté',
    ROUND(AVG(Age), 1),
    ROUND(AVG(MonthlyIncome), 0),
    ROUND(AVG(YearsAtCompany), 1),
    ROUND(AVG(SatisfactionScore), 2),
    ROUND(AVG(CASE WHEN OverTime='Yes' THEN 1.0 ELSE 0.0 END)*100,1)
FROM hr_employees WHERE AttritionBinary = 0;


-- ─────────────────────────────────────────────────────────────
-- 9. WINDOW FUNCTION — RANG PAR TAUX D'ATTRITION PAR DEPT
-- ─────────────────────────────────────────────────────────────
SELECT
    Department,
    JobRole,
    COUNT(*)                                        AS effectif,
    ROUND(AVG(AttritionBinary)*100, 1)             AS taux_pct,
    RANK() OVER (
        PARTITION BY Department
        ORDER BY AVG(AttritionBinary) DESC
    )                                               AS rang_dept
FROM hr_employees
GROUP BY Department, JobRole
HAVING COUNT(*) >= 15
ORDER BY Department, rang_dept;


-- ─────────────────────────────────────────────────────────────
-- 10. COÛT ESTIMÉ DE L'ATTRITION
-- ─────────────────────────────────────────────────────────────
SELECT
    SUM(AttritionBinary)                            AS nb_departs,
    ROUND(AVG(MonthlyIncome) * 12, 0)              AS salaire_annuel_moyen,
    -- Coût estimé = 50% à 150% du salaire annuel selon le poste
    ROUND(SUM(AttritionBinary) * AVG(MonthlyIncome) * 12 * 0.75, 0) AS cout_estime_bas,
    ROUND(SUM(AttritionBinary) * AVG(MonthlyIncome) * 12 * 1.50, 0) AS cout_estime_haut
FROM hr_employees;

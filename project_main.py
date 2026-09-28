import csv
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
import pandas as pd
from sklearn.linear_model import LinearRegression

from project_patient import Patient

patients = []

with open('Metadata and Protein Data for Module 1.csv', 'r') as file: #open the csv file and read the data into a list of patient objects
    reader = csv.DictReader(file)

    for row in reader:
        patient = Patient(
            donor_id=row['Donor ID'],
            age_at_death=float(row['Age at Death']),
            sex=row['Sex'],
            years_of_education=float(row['Years of education']),
            apoe_genotype=row['APOE Genotype'],
            cognitive_status=row['Cognitive Status'],
            thal=row['Thal'],
            abeta40=float(row['ABeta40 pg/ug']),
            abeta42=float(row['ABeta42 pg/ug']),
            ttau=float(row['tTAU pg/ug']),
            ptau=float(row['pTAU pg/ug']),
            mmse_score=float(row['Last MMSE Score']) if row['Last MMSE Score'] != '' else np.nan,
        )

        patients.append(patient)

# Get years of education and MMSE scores
education = np.array([
    patient.years_of_education
    for patient in patients
    if not np.isnan(patient.mmse_score)
])

mmse_scores = np.array([
    patient.mmse_score
    for patient in patients
    if not np.isnan(patient.mmse_score)
])

# Create the linear regression model, reshape education data for the model, and train the model
model = LinearRegression()
education_reshaped = education.reshape(-1, 1)
model.fit(education_reshaped, mmse_scores)

# Predict MMSE scores
predicted_mmse = model.predict(education_reshaped)

# Get slope and intercept
slope = model.coef_[0]
intercept = model.intercept_

print(f"Slope: {slope}")
print(f"Intercept: {intercept}")

# Calculate R-squared
r_squared = model.score(education_reshaped, mmse_scores)

print(f"R-squared: {r_squared}")

# Calculate correlation and p-value
correlation, p_value = stats.pearsonr(education, mmse_scores)

print(f"Correlation: {correlation}")
print(f"P-value: {p_value}")

# Create scatter plot
plt.scatter(education, mmse_scores, label='Actual Data')

# Add regression line
plt.plot(education, predicted_mmse, color='red', label='Linear Regression')

# Add R-squared, slope, correlation, and p-value to the graph
plt.text(
    0.05, 0.95,
    f'$R^2 = {r_squared:.4f}$\n'
    f'Slope = {slope:.4f}\n'
    f'r = {correlation:.4f}\n'
    f'p = {p_value:.4f}',
    transform=plt.gca().transAxes,
    verticalalignment='top'
)

plt.xlabel('Years of Education')
plt.ylabel('MMSE Score')
plt.title('MMSE Score vs Years of Education')

plt.legend()

plt.savefig("mmse_vs_years_of_education.png")

plt.show()

#separate abeta42 vlaues into dementia and no dementia groups
dementia_abeta42 = np.array([
    patient.abeta42
    for patient in patients
    if patient.cognitive_status == "Dementia"
])

no_dementia_abeta42 = np.array([
    patient.abeta42
    for patient in patients
    if patient.cognitive_status == "No dementia"
])

#calculat mean abeta42 for each group
dementia_mean = np.mean(dementia_abeta42)
no_dementia_mean = np.mean(no_dementia_abeta42)

print(f"\nMean Abeta42 for dementia group: {dementia_mean}")
print("Mean Abeta42 for no dementia group: {no_dementia_mean}")

#independent t-test
t_statistic, p_value_abeta = stats.ttest_ind(
    dementia_abeta42,
    no_dementia_abeta42
)

print(f"T-statistic: {t_statistic}")
print(f"P-value: {p_value_abeta}")

#make bar graph
groups = ["Dementia", "No Dementia"]
means = [dementia_mean, no_dementia_mean]

plt.bar(groups, means)

plt.xlabel("Cognitive Status")
plt.ylabel("Mean ABeta42 (pg/ug)")
plt.title("Mean ABeta42 by Dementia Status")

plt.text(
    0.05, 0.95,
    f'Dementia Mean = {dementia_mean:.2f}\n'
    f'No Dementia Mean = {no_dementia_mean:.2f}\n'
    f'p = {p_value_abeta:.4f}',
    transform=plt.gca().transAxes,
    verticalalignment='top'
)

plt.savefig("mean_abeta42_dementia_groups.png")
plt.show()
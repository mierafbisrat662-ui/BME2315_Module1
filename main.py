import csv
import matplotlib.pyplot as plt
import numpy as np

from patient import Patient
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
            ptau=float(row['pTAU pg/ug'])
        )
        patients.append(patient)
patients.sort(key=lambda x: x.age_at_death) #sort the patients by age at death
for patient in patients:
    print(patient)

filtered_patients = Patient.filter_by_cognitive_status(patients, 'Dementia', 'Female') #filter the patients by cognitive status and sex
for patient in filtered_patients:
    print(patient)

female_abeta42 = [patient.abeta42 for patient in patients if patient.sex == 'Female']
male_abeta42 = [patient.abeta42 for patient in patients if patient.sex == 'Male']

female_mean = np.mean(female_abeta42)
male_mean = np.mean(male_abeta42)

female_std = np.std(female_abeta42)
male_std = np.std(male_abeta42)

plt.bar(['Female', 'Male'], [female_mean, male_mean], yerr=[female_std, male_std], capsize=5) #create a bar chart with error bars representing the mean and standard deviation of ABeta42 levels for females and males
plt.ylabel('Mean ABeta42 Levels (pg/ug)')
plt.title('ABeta42 Levels by Sex')
plt.show()

ages = [patient.age_at_death for patient in patients]
abeta42 = [patient.abeta42 for patient in patients]
plt.scatter(ages, abeta42) #create a scatter plot of ABeta42 levels vs age at death
plt.xlabel('Age at Death')
plt.ylabel('ABeta42 Levels (pg/ug)')
plt.title('ABeta42 Levels vs Age at Death')
plt.show()
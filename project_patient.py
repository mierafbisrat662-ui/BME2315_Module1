class Patient: # define the patient class with the attributes from the csv file
    def __init__(self, donor_id: str, age_at_death: float, sex: str, years_of_education: float,
                 apoe_genotype: str, cognitive_status: str, thal: str,
                 abeta40: float, abeta42: float, ttau: float, ptau: float, mmse_score: float):

        self.donor_id = donor_id
        self.age_at_death = age_at_death
        self.sex = sex
        self.years_of_education = years_of_education
        self.apoe_genotype = apoe_genotype
        self.cognitive_status = cognitive_status
        self.thal = thal
        self.abeta40 = abeta40
        self.abeta42 = abeta42
        self.ttau = ttau
        self.ptau = ptau
        self.mmse_score = mmse_score

    def __repr__(self): # define the string representation of the patient object
        return f"{self.donor_id}: ({self.sex} | {self.cognitive_status} | {self.years_of_education} | {self.mmse_score})"

    @classmethod
    def filter_by_cognitive_status(cls, patients, status, sex):
        return [patient for patient in patients
                if patient.cognitive_status == status and patient.sex == sex]
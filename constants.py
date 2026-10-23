# constants.py
COLUMNS = [
    'Patient ID', 'Patient Name', 'Sex', 'Age', 'Age Group',
    'Ward Admission Date', 'Date of Visit', 'Diagnosis', 'With Nutrition Support',
    'Ward', 'Subspecialty', 'Height', 'Weight', 'Type Of Visit', 'Purpose of Visit',
    'WFL Z-Score', 'BMI Percentile', 'Nutritional Status', 'Bowel Movement',
    'Emesis', 'Abdominal Distention', 'Disease and other Co-morbidities', 'RND Dietary Management', 'Diet Prescriptions(Current)',
    'With Documents','Given NCP',
    'Encoded By', 'Encoded Date', 'Last Updated'
]

EXCEL_FILE = 'Dietary Report.xlsx'

SEX_OPTIONS = ['Male', 'Female']
AGE_GROUP_OPTIONS = ['Below 1 Year','1-4 Years old', '5-9 Years old', '10-14 Years old', '15-19 Years old', '20-44 Years old', '45-64 Years old', '65 Years old and above']
WARD_OPTIONS = ['ICU', 'NICU', 'Observation', 'Recovery', 'Caring 1', 'Caring 2', 'Caring 3', 'Caring 4']
SUBSPECIALTY_OPTIONS = ['Pulmo', 'Infectious', 'Hema/Oncology', 'Endo/Metabolic Disorder', 'General Service', 'Surgery', 'Cardio', 'Neuro', 'Gastro', 'Renal']
TYPE_OF_VISIT_OPTIONS = ['Routine', 'Referred By Doctor', 'Referred By Nurse Through Screening form']
PURPOSE_OPTIONS = ['Apply NCP','MNT']
NUTRITION_SUPPORT_OPTIONS = ['Yes', 'No']
NUTRITIONAL_STATUS_OPTIONS = ['Normal','Wasting', 'Stunting', 'Underweight', 'Overweight', 'Obese', 'Moderate Acute Malnutrition', 'Severe Acute Malnutrition']
BOWEL_MOVEMENT_OPTIONS = ['Normal BM', 'Loose BM of >3x in 24h', 'No BM for 48hrs']
EMESIS_OPTIONS = ['Present', 'Absent']
ABDOMINAL_DISTENTION_OPTIONS = ['Present', 'Absent']
DISEASE_OPTIONS = ['Cancer','Cardiovascular','DM / Endocrine','Dengue', 'Gastrointestinal/Hepatobiliary Disease', 'HPN', 'Infectious Disease', 'OB Case', 'Renal','Respiratory','Surgical Case','Others']
RND_DIETARY_MANAGEMENT_OPTIONS = ['Maintain Current Feeding', 'Change of Feeding Prescription', 'Provision of Modulars']
ENCODED_BY_OPTIONS = ['RB', 'LA', 'JD', 'DM', 'Intern 1', 'Intern 2', 'Intern 3', 'Intern 4']
WITH_DOCUMENTS_OPTIONS = ['Yes', 'No']
GIVEN_NCP_OPTIONS = ['Yes', 'No']

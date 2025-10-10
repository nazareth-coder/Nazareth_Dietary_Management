# constants.py
COLUMNS = [
    'Patient ID', 'Patient Name', 'Sex', 'Age', 'Age Group',
    'Ward Admission Date', 'Date of Visit', 'Diagnosis', 'With Nutrition Support',
    'Ward', 'Subspecialty', 'Height', 'Weight', 'Type Of Visit', 'Purpose of Visit',
    'WFL Z-Score', 'BMI Percentile', 'Nutritional Status', 'Bowel Movement',
    'Emesis', 'Abdominal Distention', 'Biochemical Parameters', 'RND Dietary Management', 'Diet Prescriptions(Current)',
    'With Documents','Given NCP',
    'Encoded By', 'Encoded Date', 'Last Updated'
]

EXCEL_FILE = 'Dietary Report.xlsx'

SEX_OPTIONS = ['Male', 'Female']
AGE_GROUP_OPTIONS = ['0-4 years old', '5-9 years old', '10-14 years old', '15-18 years old', '19-29 years old', '30-39 years old', '40-49 years old', '50-59 years old', '60 years old and above']
WARD_OPTIONS = ['ICU', 'NICU', 'Observation', 'Recovery', 'Caring 1', 'Caring 2', 'Caring 3', 'Caring 4']
SUBSPECIALTY_OPTIONS = ['Pulmo', 'Infectious', 'Hema/Oncology', 'Endo/Metabolic Disorder', 'General Service', 'Surgery', 'Cardio', 'Neuro', 'Gastro', 'Renal']
TYPE_OF_VISIT_OPTIONS = ['Routine', 'Referred By Doctor', 'Referred By Nurse Through Screening form']
PURPOSE_OPTIONS = ['Monitoring', 'Reassessment', 'Initial Assessment', 'Nutrition Education']
NUTRITION_SUPPORT_OPTIONS = ['Yes', 'No']
NUTRITIONAL_STATUS_OPTIONS = ['Normal', 'Underweight', 'Stunting', 'Overweight', 'Obese', 'MAM', 'SAM']
BOWEL_MOVEMENT_OPTIONS = ['Normal BM', 'Loose BM of >3x in 24h', 'No BM for 48hrs']
EMESIS_OPTIONS = ['Present', 'Absent']
ABDOMINAL_DISTENTION_OPTIONS = ['Present', 'Absent']
BIOCHEMICAL_PARAMETERS_OPTIONS = ['Normal Lab Values', 'Elevated Liver Enzymes', 'Hypoalbuminemia', 'Elevated Serum Glucose', 'Hypo/Hyper Thyroidism', 'Electrolyte Derangement', 'Excess/ Deficit ABG Parameters','Elevated/Decreased Renal Profile', 'Elevated Lipid Profile']
RND_DIETARY_MANAGEMENT_OPTIONS = ['Maintain Current Feeding', 'Change of Feeding Prescription', 'Provision of Modulars']
ENCODED_BY_OPTIONS = ['RB', 'LA', 'JD', 'DM', 'Intern 1', 'Intern 2', 'Intern 3', 'Intern 4']
WITH_DOCUMENTS_OPTIONS = ['Yes', 'No']
GIVEN_NCP_OPTIONS = ['Yes', 'No']

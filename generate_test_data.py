import random
from datetime import datetime, timedelta
import os

# Configuration
NUM_RECORDS = 5000
OUTPUT_FILE = 'dietary_test_data.sql'
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)

# Data pools for random generation
first_names_male = ['Juan', 'Pedro', 'Miguel', 'Jose', 'Antonio', 'Carlos', 'Luis', 'Fernando', 'Ricardo', 'Eduardo',
                   'Rafael', 'Daniel', 'Manuel', 'Santiago', 'Andres', 'Roberto', 'Jorge', 'Alberto', 'Enrique', 'Francisco']

first_names_female = ['Maria', 'Ana', 'Carmen', 'Isabel', 'Rosa', 'Teresa', 'Patricia', 'Laura', 'Sofia', 'Elena',
                     'Claudia', 'Adriana', 'Gabriela', 'Andrea', 'Monica', 'Diana', 'Veronica', 'Alejandra', 'Beatriz', 'Carolina']

last_names = ['Santos', 'Reyes', 'Cruz', 'Bautista', 'Ocampo', 'Garcia', 'Reyes', 'Ramos', 'Mendoza', 'Aquino',
             'Gonzales', 'Torres', 'Dela Cruz', 'Gomez', 'Perez', 'Lopez', 'Diaz', 'Martinez', 'Rodriguez', 'Hernandez']

diagnoses = {
    'Pulmo': ['Pneumonia', 'Asthma', 'COPD', 'Bronchitis', 'Tuberculosis', 'Lung Cancer'],
    'Infectious': ['AGE', 'Dengue', 'Typhoid', 'UTI', 'Pneumonia', 'Tuberculosis', 'Hepatitis'],
    'Hema/Oncology': ['Anemia', 'Leukemia', 'Lymphoma', 'Breast CA', 'Lung CA', 'Colon CA'],
    'Endo/Metabolic': ['DM', 'GDM', 'Hypothyroidism', 'Hyperthyroidism', 'Obesity', 'Malnutrition'],
    'Cardio': ['HTN', 'CAD', 'CHF', 'Arrhythmia', 'MI'],
    'Renal': ['CKD', 'AKI', 'UTI', 'Nephrotic Syndrome'],
    'General': ['Fever', 'Dehydration', 'Malnutrition', 'Sepsis', 'UTI']
}

subspecialties = list(diagnoses.keys())

wards = ['Caring 1', 'Caring 2', 'Caring 3', 'Caring 4', 'ICU', 'NICU', 'PICU', 'Recovery', 'Observation']

visit_types = ['Routine', 'Referred By Doctor', 'Referred By Nurse Through Screening form']
visit_purposes = ['Initial Assessment', 'Monitoring', 'Reassessment', 'Nutrition Education']

bmi_percentiles = [f'P{p}' for p in [1, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 75, 80, 85, 90, 95, 97, 99]]
nutritional_statuses = ['Underweight', 'Normal', 'Overweight', 'Obese', 'MAM', 'SAM', 'Stunting']

bowel_movements = ['Normal BM', 'Loose BM of >3x in 24h', 'No BM for 48hrs', 'Constipation', 'Diarrhea']
emesis = ['Absent', 'Present']
abdominal_distention = ['Absent', 'Present']

biochemical_params = [
    'Elevated Liver Enzymes', 'Electrolyte Derangement', 'Hypoalbuminemia', 'Elevated Serum Glucose',
    'Elevated Lipid Profile', 'Elevated/Decreased Renal Profile', 'Normal Lab Values', 'Hypo/Hyper Thyroidism'
]

rnd_management = [
    'Maintain Current Feeding', 'Change of Feeding Prescription', 'Provision of Modulars',
    'Nutrition Education', 'Diet Modification', 'Supplementation'
]

diet_prescriptions = [
    'Regular', 'Soft Diet', 'Clear Fluids', 'Full Fluid', 'High Calorie', 'High Protein',
    'Low Salt', 'Low Fat', 'Diabetic Diet', 'Renal Diet', 'NGT Feeding', 'TPN'
]

encoded_by = ['RB', 'LA', 'JD', 'DM', 'AC', 'MJ', 'PT', 'SL']

def random_date(start, end):
    """Generate a random date between start and end"""
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

def get_age_group(age):
    if age < 1: return '0-4 years old'
    elif age < 5: return '0-4 years old'
    elif age < 10: return '5-9 years old'
    elif age < 15: return '10-14 years old'
    elif age < 19: return '15-18 years old'
    elif age < 30: return '19-29 years old'
    elif age < 40: return '30-39 years old'
    elif age < 50: return '40-49 years old'
    elif age < 60: return '50-59 years old'
    else: return '60 years old and above'

def generate_patient(patient_id):
    # Basic info
    sex = random.choice(['Male', 'Female'])
    first_name = random.choice(first_names_male if sex == 'Male' else first_names_female)
    last_name = random.choice(last_names)
    patient_name = f"{first_name} {last_name}"
    
    # Age and dates
    age = random.randint(0, 100)
    age_group = get_age_group(age)
    
    # Generate realistic height and weight based on age and sex
    if age == 0:  # Newborn
        height = round(random.uniform(45, 55), 2)
        weight = round(random.uniform(2.5, 4.5), 2)
    elif age < 2:  # Infant
        height = round(random.uniform(65, 85), 2)
        weight = round(random.uniform(7, 12), 2)
    elif age < 5:  # Toddler
        height = round(random.uniform(85, 110), 2)
        weight = round(random.uniform(10, 20), 2)
    elif age < 13:  # Child
        height = round(random.uniform(110, 155), 2)
        weight = round(random.uniform(18, 45), 2)
    elif age < 20:  # Teen
        if sex == 'Male':
            height = round(random.uniform(155, 185), 2)
            weight = round(random.uniform(45, 75), 2)
        else:
            height = round(random.uniform(150, 175), 2)
            weight = round(random.uniform(40, 70), 2)
    else:  # Adult
        if sex == 'Male':
            height = round(random.uniform(160, 195), 2)
            weight = round(random.uniform(55, 100), 2)
        else:
            height = round(random.uniform(150, 180), 2)
            weight = round(random.uniform(45, 90), 2)
    
    # Add some randomness to weight
    weight = round(weight * random.uniform(0.8, 1.2), 2)
    
    # Generate dates
    ward_admission_date = random_date(START_DATE, END_DATE)
    date_of_visit = ward_admission_date + timedelta(days=random.randint(0, 14))
    encoded_date = date_of_visit + timedelta(days=random.randint(0, 2))
    last_updated = encoded_date + timedelta(hours=random.randint(1, 72))
    
    # Medical info
    subspecialty = random.choice(subspecialties)
    diagnosis = random.choice(diagnoses[subspecialty])
    
    # Randomly select other fields
    with_nutrition_support = random.choice(['Yes', 'No'])
    ward = random.choice(wards)
    visit_type = random.choice(visit_types)
    visit_purpose = random.choice(visit_purposes)
    
    # Only include WFL Z-Score for children under 5
    wfl_z_score = None
    if age < 5:
        wfl_z_score = str(round(random.uniform(-3.5, 2.5), 1))
        if random.random() < 0.3:  # 30% chance of None
            wfl_z_score = 'None' if random.random() < 0.5 else None
    
    bmi_percentile = random.choice(bmi_percentiles)
    nutritional_status = random.choice(nutritional_statuses)
    bowel_movement = random.choice(bowel_movements)
    emesis_val = random.choice(emesis)
    abd_distention = random.choice(abdominal_distention)
    biochemical = random.choice(biochemical_params)
    rnd_mgmt = random.choice(rnd_management)
    diet_rx = random.choice(diet_prescriptions)
    with_docs = random.choice(['Yes', 'No'])
    given_ncp = random.choice(['Yes', 'No'])
    encoder = random.choice(encoded_by)
    
    # Format SQL values
    def sql_value(value):
        if value is None:
            return 'NULL'
        elif isinstance(value, str):
            return f"'{value.replace('\\', '\\\\').replace("'", "''")}'"
        elif isinstance(value, datetime):
            return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif isinstance(value, bool):
            return '1' if value else '0'
        return str(value)
    
    # Create the SQL values tuple
    values = [
        patient_id + 1,  # Start from ID 16
        patient_name,
        sex,
        age,
        age_group,
        ward_admission_date.strftime('%Y-%m-%d'),
        date_of_visit.strftime('%Y-%m-%d'),
        diagnosis,
        with_nutrition_support,
        ward,
        subspecialty,
        height,
        weight,
        visit_type,
        visit_purpose,
        wfl_z_score,
        bmi_percentile,
        nutritional_status,
        bowel_movement,
        emesis_val,
        abd_distention,
        biochemical,
        rnd_mgmt,
        diet_rx,
        with_docs,
        given_ncp,
        encoder,
        encoded_date.strftime('%Y-%m-%d'),
        last_updated.strftime('%Y-%m-%d %H:%M:%S')
    ]
    
    # Format the SQL INSERT statement
    sql = f"""INSERT INTO `patients` (`Patient ID`, `Patient Name`, `Sex`, `Age`, `Age Group`, `Ward Admission Date`, `Date of Visit`, `Diagnosis`, `With Nutrition Support`, `Ward`, `Subspecialty`, `Height`, `Weight`, `Type Of Visit`, `Purpose of Visit`, `WFL Z-Score`, `BMI Percentile`, `Nutritional Status`, `Bowel Movement`, `Emesis`, `Abdominal Distention`, `Biochemical Parameters`, `RND Dietary Management`, `Diet Prescriptions(Current)`, `With Documents`, `Given NCP`, `Encoded By`, `Encoded Date`, `Last Updated`) VALUES ({', '.join(sql_value(v) for v in values)});"""
    
    return sql

def generate_sql_file():
    # Create SQL file header
    sql_content = """-- Dietary Management System Test Data
-- Generated on {}
-- Total records: {}

-- Disable foreign key checks for faster import
SET FOREIGN_KEY_CHECKS = 0;

-- Clear existing data
TRUNCATE TABLE `patients`;

-- Insert test data
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), NUM_RECORDS)

    # Generate patient records
    print(f"Generating {NUM_RECORDS} patient records...")
    for i in range(NUM_RECORDS):
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1} records...")
        sql_content += generate_patient(i + 15) + "\n"  # Start from ID 16
    
    # Add footer
    sql_content += """
-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;
"""
    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print(f"\nGenerated {NUM_RECORDS} patient records in {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    generate_sql_file()

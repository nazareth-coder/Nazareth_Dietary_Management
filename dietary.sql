-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.32-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for dietary_mgmt
CREATE DATABASE IF NOT EXISTS `dietary_mgmt` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `dietary_mgmt`;

-- Dumping structure for table dietary_mgmt.patients
CREATE TABLE IF NOT EXISTS `patients` (
  `Patient ID` int(11) NOT NULL AUTO_INCREMENT,
  `Patient Name` varchar(255) NOT NULL,
  `Sex` enum('Male','Female') DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `Age Group` varchar(64) DEFAULT NULL,
  `Ward Admission Date` date DEFAULT NULL,
  `Date of Visit` date DEFAULT NULL,
  `Diagnosis` varchar(512) DEFAULT NULL,
  `With Nutrition Support` enum('Yes','No') DEFAULT NULL,
  `Ward` varchar(64) DEFAULT NULL,
  `Subspecialty` varchar(64) DEFAULT NULL,
  `Height` decimal(5,2) DEFAULT NULL,
  `Weight` decimal(5,2) DEFAULT NULL,
  `Type Of Visit` varchar(64) DEFAULT NULL,
  `Purpose of Visit` varchar(64) DEFAULT NULL,
  `WFL Z-Score` varchar(32) DEFAULT NULL,
  `BMI Percentile` varchar(32) DEFAULT NULL,
  `Nutritional Status` varchar(32) DEFAULT NULL,
  `Bowel Movement` varchar(64) DEFAULT NULL,
  `Emesis` varchar(32) DEFAULT NULL,
  `Abdominal Distention` varchar(32) DEFAULT NULL,
  `Biochemical Parameters` varchar(128) DEFAULT NULL,
  `RND Dietary Management` varchar(128) DEFAULT NULL,
  `Diet Prescriptions(Current)` varchar(512) DEFAULT NULL,
  `With Documents` enum('Yes','No') DEFAULT NULL,
  `Given NCP` enum('Yes','No') DEFAULT NULL,
  `Encoded By` varchar(64) DEFAULT NULL,
  `Encoded Date` date DEFAULT NULL,
  `Last Updated` datetime DEFAULT NULL,
  PRIMARY KEY (`Patient ID`),
  KEY `idx_date_of_visit` (`Date of Visit`),
  KEY `idx_age_group` (`Age Group`),
  KEY `idx_sex` (`Sex`),
  KEY `idx_nutritional_status` (`Nutritional Status`),
  KEY `idx_agegroup_sex` (`Age Group`,`Sex`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table dietary_mgmt.patients: ~13 rows (approximately)
INSERT INTO `patients` (`Patient ID`, `Patient Name`, `Sex`, `Age`, `Age Group`, `Ward Admission Date`, `Date of Visit`, `Diagnosis`, `With Nutrition Support`, `Ward`, `Subspecialty`, `Height`, `Weight`, `Type Of Visit`, `Purpose of Visit`, `WFL Z-Score`, `BMI Percentile`, `Nutritional Status`, `Bowel Movement`, `Emesis`, `Abdominal Distention`, `Biochemical Parameters`, `RND Dietary Management`, `Diet Prescriptions(Current)`, `With Documents`, `Given NCP`, `Encoded By`, `Encoded Date`, `Last Updated`) VALUES
	(2, 'Alice Santos', 'Female', 7, '5-9 years old', '2025-01-05', '2025-01-06', 'Pneumonia', 'Yes', 'Caring 1', 'Pulmo', 120.50, 22.30, 'Routine', 'Initial Assessment', NULL, 'P60', 'Underweight', 'Normal BM', 'Absent', 'Absent', 'Elevated Liver Enzymes', 'Maintain Current Feeding', 'Soft Diet', 'Yes', 'Yes', 'RB', '2025-01-06', '2025-01-06 09:15:00'),
	(3, 'Ben Cruz', 'Male', 3, '0-4 years old', '2025-01-10', '2025-01-11', 'AGE', 'No', 'Observation', 'Infectious', 98.00, 14.00, 'Referred By Doctor', 'Nutrition Education', NULL, 'P30', 'Normal', 'Loose BM of >3x in 24h', 'Present', 'Absent', 'Electrolyte Derangement', 'Change of Feeding Prescription', 'Clear Fluids', 'No', 'No', 'LA', '2025-01-11', '2025-01-11 10:10:00'),
	(4, 'Carla Dizon', 'Female', 15, '15-18 years old', '2025-03-02', '2025-03-02', 'Anemia', 'No', 'Caring 2', 'Hema/Oncology', 155.00, 45.00, 'Routine', 'Monitoring', NULL, 'P50', 'Normal', 'Normal BM', 'Absent', 'Absent', 'Hypoalbuminemia', 'Provision of Modulars', 'Regular', 'Yes', 'No', 'JD', '2025-03-02', '2025-03-02 14:22:00'),
	(5, 'Diego Ramos', 'Male', 11, '10-14 years old', '2025-03-15', '2025-03-16', 'Asthma', 'Yes', 'Caring 3', 'Pulmo', 140.00, 38.00, 'Referred By Nurse Through Screening form', 'Initial Assessment', NULL, 'P85', 'Overweight', 'Normal BM', 'Absent', 'Absent', 'Normal Lab Values', 'Maintain Current Feeding', 'Low Salt', 'No', 'Yes', 'DM', '2025-03-16', '2025-03-16 08:30:00'),
	(6, 'Ella Torres', 'Female', 5, '5-9 years old', '2025-06-01', '2025-06-03', 'Malnutrition', 'Yes', 'Caring 4', 'Endo/Metabolic Disorder', 110.00, 16.00, 'Routine', 'Reassessment', '-1.5', 'P5', 'MAM', 'No BM for 48hrs', 'Absent', 'Present', 'Hypo/Hyper Thyroidism', 'Change of Feeding Prescription', 'High Calorie', 'Yes', 'Yes', 'RB', '2025-06-03', '2025-06-03 11:45:00'),
	(7, 'Felix Yao', 'Male', 2, '0-4 years old', '2025-06-10', '2025-06-10', 'Severe malnutrition', 'Yes', 'NICU', 'General Service', 85.00, 10.00, 'Routine', 'Initial Assessment', '-3.2', 'P1', 'SAM', 'Loose BM of >3x in 24h', 'Present', 'Present', 'Electrolyte Derangement', 'Provision of Modulars', 'NGT Feeding', 'Yes', 'Yes', 'LA', '2025-06-10', '2025-06-10 12:10:00'),
	(8, 'Gina Uy', 'Female', 28, '19-29 years old', '2025-07-05', '2025-07-06', 'GDM', 'No', 'ICU', 'Endo/Metabolic Disorder', 160.00, 62.00, 'Routine', 'Monitoring', 'None', 'P70', 'Overweight', 'Normal BM', 'Absent', 'Absent', 'Elevated Serum Glucose', 'Maintain Current Feeding', 'Diabetic Diet', 'Yes', 'Yes', 'JD', '2025-07-06', '2025-08-28 13:53:59'),
	(9, 'Hector Lim', 'Male', 34, '30-39 years old', '2025-07-12', '2025-07-12', 'HTN', 'No', 'Recovery', 'Cardio', 172.00, 85.00, 'Routine', 'Monitoring', NULL, 'P90', 'Obese', 'Normal BM', 'Absent', 'Absent', 'Elevated Lipid Profile', 'Change of Feeding Prescription', 'Low Fat', 'No', 'No', 'DM', '2025-07-12', '2025-07-12 15:20:00'),
	(10, 'Ivy Pangan', 'Female', 42, '40-49 years old', '2025-09-01', '2025-09-02', 'Breast CA', 'Yes', 'Caring 2', 'Hema/Oncology', 158.00, 54.00, 'Referred By Doctor', 'Nutrition Education', NULL, 'P40', 'Underweight', 'Normal BM', 'Absent', 'Absent', 'Elevated Liver Enzymes', 'Provision of Modulars', 'High Protein', 'Yes', 'Yes', 'RB', '2025-09-02', '2025-09-02 10:00:00'),
	(11, 'Jomar Valdez', 'Male', 51, '50-59 years old', '2025-09-10', '2025-09-10', 'CKD', 'Yes', 'Caring 3', 'Renal', 168.00, 70.00, 'Routine', 'Reassessment', NULL, 'P30', 'Stunting', 'Normal BM', 'Absent', 'Present', 'Elevated/Decreased Renal Profile', 'Maintain Current Feeding', 'Renal Diet', 'Yes', 'No', 'LA', '2025-09-10', '2025-09-10 13:40:00'),
	(12, 'Karen Yu', 'Female', 62, '60 years old and above', '2025-11-05', '2025-11-05', 'DM', 'No', 'Observation', 'Endo/Metabolic Disorder', 155.00, 68.00, 'Routine', 'Monitoring', NULL, 'P75', 'Overweight', 'Normal BM', 'Absent', 'Absent', 'Elevated Serum Glucose', 'Change of Feeding Prescription', 'Diabetic Diet', 'Yes', 'Yes', 'JD', '2025-11-05', '2025-11-05 16:00:00'),
	(13, 'tresitntsgshshshsh', 'Male', 68, '60 years old and above', '2025-11-12', '2025-11-13', 'COPD', 'Yes', 'ICU', 'Pulmo', 170.00, 64.00, 'Referred By Doctor', 'Initial Assessment', 'None', 'P40', 'Underweight', 'No BM for 48hrs', 'Present', 'Present', 'Elevated Liver Enzymes', 'Provision of Modulars', 'Soft Diet', 'No', 'No', 'DM', '2025-11-13', '2025-08-28 14:05:08'),
	(14, 'sheshable', 'Female', 9, '5-9 years old', '2025-12-01', '2025-12-01', 'Pneumonia', 'Yes', 'Caring 1', 'Pulmo', 130.00, 28.00, 'Routine', 'Reassessment', 'None', 'P20', 'Underweight', 'Normal BM', 'Absent', 'Absent', 'Normal Lab Values', 'Maintain Current Feeding', 'Soft Diet', 'Yes', 'Yes', 'RB', '2025-12-01', '2025-10-10 10:49:25');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

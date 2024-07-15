CREATE TABLE `User` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255),
  `password` varchar(255),
  `email` varchar(255),
  `first_name` varchar(255),
  `last_name` varchar(255),
  `is_patient` boolean,
  `is_doctor` boolean,
  `is_pharmacist` boolean
);

CREATE TABLE `Patient` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `dob` date,
  `gender` varchar(10),
  `contact_info` varchar(255),
  `address` varchar(255),
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `Doctor` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `specialty` varchar(100),
  `contact_info` varchar(255),
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `Pharmacist` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `contact_info` varchar(255),
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `Medication` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(100),
  `description` text,
  `package_size` varchar(100),
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `Prescription` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `patient_id` int,
  `doctor_id` int,
  `code` varchar(50) UNIQUE,
  `sickness` varchar(100),
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `PrescriptionMedication` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `prescription_id` int,
  `medication_id` int,
  `dosage` varchar(100),
  `frequency` varchar(100),
  `duration` int,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `VendingMachine` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `location` varchar(255),
  `status` varchar(50),
  `last_stocked_by` int,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `Dispensation` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `vending_machine_id` int,
  `prescription_id` int,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `Inventory` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `vending_machine_id` int,
  `medication_id` int,
  `quantity` int,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `VendingSlot` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `vending_machine_id` int,
  `medication_id` int,
  `slot_number` int,
  `created_at` timestamp,
  `updated_at` timestamp
);

ALTER TABLE `Patient` ADD FOREIGN KEY (`user_id`) REFERENCES `User` (`id`);

ALTER TABLE `Doctor` ADD FOREIGN KEY (`user_id`) REFERENCES `User` (`id`);

ALTER TABLE `Pharmacist` ADD FOREIGN KEY (`user_id`) REFERENCES `User` (`id`);

ALTER TABLE `Prescription` ADD FOREIGN KEY (`patient_id`) REFERENCES `Patient` (`id`);

ALTER TABLE `Prescription` ADD FOREIGN KEY (`doctor_id`) REFERENCES `Doctor` (`id`);

ALTER TABLE `PrescriptionMedication` ADD FOREIGN KEY (`prescription_id`) REFERENCES `Prescription` (`id`);

ALTER TABLE `PrescriptionMedication` ADD FOREIGN KEY (`medication_id`) REFERENCES `Medication` (`id`);

ALTER TABLE `VendingMachine` ADD FOREIGN KEY (`last_stocked_by`) REFERENCES `Pharmacist` (`id`);

ALTER TABLE `Dispensation` ADD FOREIGN KEY (`vending_machine_id`) REFERENCES `VendingMachine` (`id`);

ALTER TABLE `Dispensation` ADD FOREIGN KEY (`prescription_id`) REFERENCES `Prescription` (`id`);

ALTER TABLE `Inventory` ADD FOREIGN KEY (`vending_machine_id`) REFERENCES `VendingMachine` (`id`);

ALTER TABLE `Inventory` ADD FOREIGN KEY (`medication_id`) REFERENCES `Medication` (`id`);

ALTER TABLE `VendingSlot` ADD FOREIGN KEY (`vending_machine_id`) REFERENCES `VendingMachine` (`id`);

ALTER TABLE `VendingSlot` ADD FOREIGN KEY (`medication_id`) REFERENCES `Medication` (`id`);

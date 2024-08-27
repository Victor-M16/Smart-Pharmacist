CREATE TABLE `auth_group` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(150) UNIQUE
);

CREATE TABLE `auth_group_permissions` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `group_id` integer,
  `permission_id` integer
);

CREATE TABLE `auth_permission` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `content_type_id` integer,
  `codename` varchar(100),
  `name` varchar(255)
);

CREATE TABLE `core_dispensation` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `updated_at` datetime,
  `prescription_id` integer,
  `vending_machine_id` integer
);

CREATE TABLE `core_inventory` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `quantity` integer,
  `created_at` datetime,
  `updated_at` datetime,
  `medication_id` integer,
  `vending_machine_id` integer
);

CREATE TABLE `core_medication` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(100),
  `description` text,
  `package_size` varchar(100),
  `created_at` datetime,
  `updated_at` datetime
);

CREATE TABLE `core_prescription` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `code` varchar(4) UNIQUE,
  `instructions` text,
  `sickness` varchar(100),
  `is_dispensed` bool,
  `created_at` datetime,
  `updated_at` datetime,
  `doctor_id` integer,
  `patient_id` integer
);

CREATE TABLE `core_prescriptionmedication` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `dosage` varchar(100),
  `frequency` varchar(100),
  `duration` integer,
  `created_at` datetime,
  `updated_at` datetime,
  `medication_id` integer,
  `prescription_id` integer
);

CREATE TABLE `core_user` (
  `password` varchar(128),
  `last_login` datetime,
  `is_superuser` bool,
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255) UNIQUE,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `account_type` varchar(150),
  `specialty` varchar(100),
  `email` varchar(254) UNIQUE,
  `phone` varchar(15),
  `national_id` varchar(20) UNIQUE,
  `dob` date,
  `gender` varchar(255),
  `id_data` text,
  `created_at` datetime,
  `updated_at` datetime,
  `is_patient` bool,
  `is_doctor` bool,
  `is_pharmacist` bool,
  `is_staff` bool,
  `is_active` bool
);

CREATE TABLE `core_user_groups` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `user_id` integer,
  `group_id` integer
);

CREATE TABLE `core_user_user_permissions` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `user_id` integer,
  `permission_id` integer
);

CREATE TABLE `core_vendingmachine` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `location` varchar(255),
  `status` varchar(50),
  `created_at` datetime,
  `updated_at` datetime
);

CREATE TABLE `core_vendingslot` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `slot_number` integer,
  `created_at` datetime,
  `updated_at` datetime,
  `medication_id` integer,
  `vending_machine_id` integer
);

ALTER TABLE `auth_group_permissions` ADD FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

ALTER TABLE `auth_group_permissions` ADD FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

ALTER TABLE `core_dispensation` ADD FOREIGN KEY (`prescription_id`) REFERENCES `core_prescription` (`id`);

ALTER TABLE `core_dispensation` ADD FOREIGN KEY (`vending_machine_id`) REFERENCES `core_vendingmachine` (`id`);

ALTER TABLE `core_inventory` ADD FOREIGN KEY (`medication_id`) REFERENCES `core_medication` (`id`);

ALTER TABLE `core_inventory` ADD FOREIGN KEY (`vending_machine_id`) REFERENCES `core_vendingmachine` (`id`);

ALTER TABLE `core_prescription` ADD FOREIGN KEY (`doctor_id`) REFERENCES `core_user` (`id`);

ALTER TABLE `core_prescription` ADD FOREIGN KEY (`patient_id`) REFERENCES `core_user` (`id`);

ALTER TABLE `core_prescriptionmedication` ADD FOREIGN KEY (`medication_id`) REFERENCES `core_medication` (`id`);

ALTER TABLE `core_prescriptionmedication` ADD FOREIGN KEY (`prescription_id`) REFERENCES `core_prescription` (`id`);

ALTER TABLE `core_user_groups` ADD FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

ALTER TABLE `core_user_groups` ADD FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

ALTER TABLE `core_user_user_permissions` ADD FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

ALTER TABLE `core_user_user_permissions` ADD FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

ALTER TABLE `core_vendingslot` ADD FOREIGN KEY (`medication_id`) REFERENCES `core_medication` (`id`);

ALTER TABLE `core_vendingslot` ADD FOREIGN KEY (`vending_machine_id`) REFERENCES `core_vendingmachine` (`id`);

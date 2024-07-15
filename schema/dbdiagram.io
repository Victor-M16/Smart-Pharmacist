Table User {
  id              int [pk, increment]
  username        varchar
  password        varchar
  email           varchar
  first_name      varchar
  last_name       varchar
  is_patient      boolean
  is_doctor       boolean
  is_pharmacist   boolean
}

Table Patient {
  id            int [pk, increment]
  user_id       int [ref: > User.id]
  dob           date
  gender        varchar(10)
  contact_info  varchar(255)
  address       varchar(255)
  created_at    timestamp
  updated_at    timestamp
}

Table Doctor {
  id            int [pk, increment]
  user_id       int [ref: > User.id]
  specialty     varchar(100)
  contact_info  varchar(255)
  created_at    timestamp
  updated_at    timestamp
}

Table Pharmacist {
  id            int [pk, increment]
  user_id       int [ref: > User.id]
  contact_info  varchar(255)
  created_at    timestamp
  updated_at    timestamp
}

Table Medication {
  id            int [pk, increment]
  name          varchar(100)
  description   text
  package_size  varchar(100)
  created_at    timestamp
  updated_at    timestamp
}

Table Prescription {
  id            int [pk, increment]
  patient_id    int [ref: > Patient.id]
  doctor_id     int [ref: > Doctor.id]
  code          varchar(50) [unique]
  sickness      varchar(100)
  created_at    timestamp
  updated_at    timestamp
}

Table PrescriptionMedication {
  id              int [pk, increment]
  prescription_id int [ref: > Prescription.id]
  medication_id   int [ref: > Medication.id]
  dosage          varchar(100)
  frequency       varchar(100)
  duration        int
  created_at      timestamp
  updated_at      timestamp
}

Table VendingMachine {
  id            int [pk, increment]
  location      varchar(255)
  status        varchar(50)
  last_stocked_by int [ref: > Pharmacist.id]
  created_at    timestamp
  updated_at    timestamp
}

Table Dispensation {
  id                  int [pk, increment]
  vending_machine_id  int [ref: > VendingMachine.id]
  prescription_id     int [ref: > Prescription.id]
  created_at          timestamp
  updated_at          timestamp
}

Table Inventory {
  id                  int [pk, increment]
  vending_machine_id  int [ref: > VendingMachine.id]
  medication_id       int [ref: > Medication.id]
  quantity            int
  created_at          timestamp
  updated_at          timestamp
}

Table VendingSlot {
  id                  int [pk, increment]
  vending_machine_id  int [ref: > VendingMachine.id]
  medication_id       int [ref: > Medication.id]
  slot_number         int
  created_at          timestamp
  updated_at          timestamp
}

## To start Development Server

1. cd raphacare_backend
2. create and enable virtual environment (venv) - use python3.12
3. install dependencies from requirements.txt file (pip install -r requirements.txt)
4. run uvicorn api.v1.main:app --reload
5. ctrl C to stop server

## Documentation

<details>
<summary>Authentication</summary>

- [Login User](docs/api/auth/login_user.md)
- [Register New Medical_Practitioner](docs/api/auth/register_medical_practitioner.md)
- [Register New Patient](docs/api/auth/register_patient.md)
- [Request Token](docs/api/auth/request_token.md)
- [Reset/Update Password](docs/api/auth/reset_password.md)
- [Verify New Email Registration](docs/api/auth/verify_email.md)

</details>
<details>
<summary>Medical Practitioners</summary>

- [Get All Medical Practitioners](docs/api/medical_practitioners/get_all_%20medical_practitioners.md)
- [Get Medical Practitioner By Id](docs/api/medical_practitioners/get_medical_practitioner_by_id.md)
- [Medical Practitioner Add Services](docs/api/medical_practitioners/add_services.md)
- [Register New Medical_Practitioner](docs/api/auth/register_medical_practitioner.md)

</details>

<details>
<summary>Patients</summary>

- [Get All Patients](docs/api/patients/get_all_patients.md)
- [Get Patient By Id](docs/api/patients/get_patient_by_id.md)
- [Register New Patient](docs/api/auth/register_patient.md)

</details>

<details>
<summary>Appointments</summary>

- [Create Appointment](docs/api/medical_services/appointment.md)

</details>

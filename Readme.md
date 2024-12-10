## To start Development Server

1. cd raphacare_backend
2. create and enable virtual environment (venv) - use python3.12
3. install dependencies from requirements.txt file (pip install -r requirements.txt)
4. run uvicorn api.v1.main:app --reload
5. ctrl C to stop server

## Documentation

<details>
<summary>Basic Endpoints</summary>

- [Login User](docs/api/auth/login_user.md)
- [Register New Medical_Practitioner](docs/api/auth/register_medical_practitioner.md)
- [Register New Patient](docs/api/auth/register_patient.md)
- [Request Token](docs/api/auth/request_token.md)
- [Reset/Update Password](docs/api/auth/reset_password.md)
- [Verify New Email Registration](docs/api/auth/verify_email.md)

</details>

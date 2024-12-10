

## Endpoint
`POST /medical-practitioners`

## Description
This endpoint is used to register a new medical practitioner in the system. It collects the practitioner's profile details and authentication details.

## Request

### Request Body
The request body should be a JSON object with the following structure:

#### Profile Details
| Field              | Type     | Required | Description                                      |
|--------------------|----------|----------|--------------------------------------------------|
| `first_name`       | string   | Yes      | The first name of the medical practitioner.      |
| `last_name`        | string   | Yes      | The last name of the medical practitioner.       |
| `other_names`      | string   | No       | Any additional names of the practitioner.        |
| `phone_number`     | string   | No       | The phone number of the practitioner.            |
| `practitioner_type`| string   | No       | The practitioner's type (e.g., doctor, nurse).   |
| `specialization`   | string   | No       | The specialization field of the practitioner.    |
| `license_number`   | string   | No       | The practitioner's license number.               |
| `is_verified`      | boolean  | No       | Whether the practitioner's credentials are verified. Defaults to `false`. |
| `availability`     | object   | No       | A schedule of the practitioner's availability.   |
| `is_available`     | boolean  | No       | Whether the practitioner is available for consultation. Defaults to `false`. |
| `user_type`        | string   | Yes      | Must be set to `medical_practitioner`.           |

#### Authentication Details
| Field               | Type     | Required | Description                                |
|---------------------|----------|----------|--------------------------------------------|
| `email`             | string   | Yes      | The email address of the practitioner.     |
| `password`          | string   | Conditional | Required for `auth_type` set to `local`.  |
| `auth_type`         | string   | Yes      | The authentication type. Allowed values: `local`, `google`, `facebook`. |
| `user_type`         | string   | Yes      | Must be set to `medical_practitioner`.     |
| `reset_token`       | string   | No       | Token for resetting the password.          |
| `token_created_at`  | datetime | No       | Timestamp when the reset token was created.|
| `email_verified`    | boolean  | No       | Indicates if the email is verified. Defaults to `false`. |
| `disabled`          | boolean  | No       | Indicates if the account is disabled. Defaults to `false`. |

### Example Request Body
```json
{
  "profile_details": {
    "first_name": "Jane",
    "last_name": "Doe",
    "other_names": "Middle",
    "phone_number": "1234567890",
    "practitioner_type": "doctor",
    "specialization": "Cardiology",
    "license_number": "ABC123456",
    "is_verified": true,
    "availability": {
      "monday": "9am-5pm",
      "tuesday": "9am-5pm"
    },
    "is_available": true,
    "user_type": "medical_practitioner"
  },
  "auth_details": {
    "email": "jane@example.com",
    "password": "password123",
    "auth_type": "local",
    "user_type": "medical_practitioner"
  }
}
```

## Response

### Success Response
- **Status Code:** `201 OK`
- **Body:** A JSON object containing the following keys:

```json
{
	"status": "success",
	"message": "User registered successfully",
	"data": {
		"first_name": "Jane",
		"last_name": "Doe",
		"other_names": "Middle",
		...
}


## Endpoint
`POST /patients`

## Description
This endpoint is used to register a new patient in the system. It collects the patient's profile details and authentication details.

## Request

### Request Body
The request body should be a JSON object with the following structure:

#### Profile Details
| Field            | Type     | Required | Description                         |
|------------------|----------|----------|-------------------------------------|
| `first_name`     | string   | Yes      | The first name of the patient.      |
| `last_name`      | string   | Yes      | The last name of the patient.       |
| `other_names`    | string   | No       | Any additional names of the patient.|
| `user_name`      | string   | No       | A unique username for the patient.  |
| `emergency_contact` | string| No       | Emergency contact phone number.     |
| `phone_number`   | string   | No       | The phone number of the patient.    |
| `gender`         | string   | No       | The gender of the patient.          |
| `address`        | string   | No       | The address of the patient.         |
| `city`           | string   | No       | The city of the patient.            |
| `state`          | string   | No       | The state of the patient.           |
| `country`        | string   | No       | The country of the patient.         |
| `date_of_birth`  | datetime | No       | The date of birth of the patient.   |
| `user_type`      | string   | Yes      | Must be set to `patient`.           |

#### Authentication Details
| Field               | Type     | Required | Description                                |
|---------------------|----------|----------|--------------------------------------------|
| `email`             | string   | Yes      | The email address of the patient.          |
| `password`          | string   | Conditional | Required for `auth_type` set to `local`.  |
| `auth_type`         | string   | Yes      | The authentication type. Allowed values: `local`, `google`, `facebook`. |
| `user_type`         | string   | Yes      | The user type. Must be one of `medical_practitioner`, `patient`, or `admin`. |
| `reset_token`       | string   | No       | Token for resetting the password.          |
| `token_created_at`  | datetime | No       | Timestamp when the reset token was created.|
| `email_verified`    | boolean  | No       | Indicates if the email is verified. Defaults to `false`. |
| `disabled`          | boolean  | No       | Indicates if the account is disabled. Defaults to `false`. |

### Example Request Body
```json
{
  "profile_details": {
    "first_name": "John",
    "last_name": "Doe",
    "other_names": "Middle",
    "user_name": "johndoe",
    "emergency_contact": "1234567890",
    "phone_number": "0987654321",
    "gender": "male",
    "address": "123 Main St",
    "city": "Anytown",
    "state": "Anystate",
    "country": "Anycountry",
    "date_of_birth": "1990-01-01T00:00:00",
    "user_type": "patient"
  },
  "auth_details": {
    "email": "johndoe2@example.com",
    "password": "password123",
    "auth_type": "local",
    "user_type": "patient"
  }
}

```

### Success Response
- **Status Code:** `201 OK`
- **Body:** A JSON object containing the following keys:

```json
{
	"status": "success",
	"message": "User registered successfully",
	"data": {
		"first_name": "John",
		"last_name": "Doe",
		"other_names": "Middle",
		"user_name": "johndoe",
		...
	}
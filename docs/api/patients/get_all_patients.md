## Get All Patients

### Request

- **Method:** `GET`
- **Endpoint:** `/patients`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>`

### Response

#### Success Response
- **Status Code:** `200 OK`
- **Body:** A JSON array of patients, each containing the following keys:

```json
[
  {
    "id": "123",
    "first_name": "John",
    "last_name": "Doe",
    "gender": "male",
    "address": "123 Main St",
    "city": "Anytown",
    "state": "Anystate",
    "country": "Anycountry",
    "date_of_birth": "1990-01-01T00:00:00",
    "user_type": "patient"
  },
  ...
]

```


#### Error Response
- **Status Code:** `401 Unauthorized`

```json
{
  "status": "error",
  "message": "Unauthorized"
}

```
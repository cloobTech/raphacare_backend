### Get Medical Practitioner by ID

## Get Medical Practitioner by ID

### Request

- **Method:** `GET`
- **Endpoint:** `/medical_practitioners/{medical_practitioner_id}`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>`

### Response

#### Success Response

- **Status Code:** `200 OK`
- **Body:** A JSON object containing the following keys:

```json
{
  "id": "123",
  "first_name": "Jane",
  "last_name": "Doe",
  "license_number": "ABC123456",
  "is_verified": true,
  "availability": {
    "monday": "9am-5pm",
    "tuesday": "9am-5pm"
  },
  "is_available": true,
  "user_type": "medical_practitioner"
}
```

#### Error Response

- **Status Code:** `404 Not Found`
- **Body:** A JSON object containing the following keys:

```json
{
  "status": "error",
  "message": "Medical practitioner not found"
}
```

#### Error Response

- **Status Code:** `401 Unauthorized`
- **Body:** A JSON object containing the following keys:

```json
{
  "status": "error",
  "message": "Unauthorized"
}
```

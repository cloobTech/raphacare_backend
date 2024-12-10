## Get All Medical Practitioners

### Request

- **Method:** `GET`
- **Endpoint:** `/medical_practitioners`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>`

### Response

#### Success Response
- **Status Code:** `200 OK`
- **Body:** A JSON array of medical practitioners, each containing the following keys:

```json
[
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
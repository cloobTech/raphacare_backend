## Add Health Centers to Medical Practitioner

### Request

- **Method:** `POST`
- **Endpoint:** `/medical_practitioners/{medical_practitioner_id}/add_health_centers`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>`
- **Path Parameters:**
  - `id`: The ID of the medical practitioner (e.g., `06ec8028-0197-4332-8163-9d25482b68de`)
- **Body:**
  - `health_centers`: A JSON array of health center objects to be added to the medical practitioner's list of health centers.

```json
{
  "health_centers": [
    {
      "name": "Health Center A",
      "address": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "postal_code": "12345",
      "medical_practitioner_id": "06ec8028-0197-4332-8163-9d25482b68de"
    },
    {
      "name": "Health Center B",
      "address": "456 Elm St",
      "city": "Othertown",
      "state": "TX",
      "postal_code": "67890",
      "medical_practitioner_id": "06ec8028-0197-4332-8163-9d25482b68de"
    }
  ]
}

```

### Response

#### Success Response
- **Status Code:** `200 OK`
- **Body:** A JSON object containing the updated list of services for the medical practitioner.

```json
{
	"status": "success",
	"message": "Health center added successfully",
	"data": [
		{
			"name": "Health Center A",
			"address": "123 Main St",
			"city": "Anytown",
			"state": "CA",
			"postal_code": "12345",
			"medical_practitioner_id": "06ec8028-0197-4332-8163-9d25482b68de",
			"id": "1aa05106-d1f2-4fad-b7a6-db5555b9a2a3",
			"created_at": "2024-12-26T12:51:29.310154Z",
			"updated_at": "2024-12-26T12:51:29.310157Z",
			"__class__": "HealthCenter"
		},
		{
			"name": "Health Center B",
			"address": "456 Elm St",
			"city": "Othertown",
			"state": "TX",
			"postal_code": "67890",
			"medical_practitioner_id": "06ec8028-0197-4332-8163-9d25482b68de",
			"id": "7be56d71-009e-4c84-bdb0-c7336d43eaaf",
			"created_at": "2024-12-26T12:51:29.310225Z",
			"updated_at": "2024-12-26T12:51:29.310225Z",
			"__class__": "HealthCenter"
		}
	]
}
```
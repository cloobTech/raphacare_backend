## Add New Services to Medical Practitioner

### Request

- **Method:** `POST`
- **Endpoint:** `/medical_practitioners/{id}/add_service`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>`
- **Path Parameters:**
  - `id`: The ID of the medical practitioner (e.g., `ff67ff99-6788-4091-9650-def1c4c3c110`)
- **Body:**
  - `services`: A JSON array of service IDs to be added to the medical practitioner's list of services.

```json
{
  "services": [
    "71533ea9-c921-48b9-8b7f-49fd7a88de895",
    "e8503397-e527-4fd6-947a-0f1f93704fff"
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
	"message": "Service(s) added to medical practitioner successfully",
	"data": [
		{
			"price": 200.0,
			"medical_practitioner_id": "ff67ff99-6788-4091-9650-def1c4c3c110",
			"is_admin_defined": true,
			"id": "71533ea9-c921-48b9-8b7f-49fd7a88de895",
			"updated_at": "2024-12-03T17:56:26.881931Z",
			"name": "Example Service 2",
			"description": "This is an example service description.",
			"admin_id": "e3ca984e-9c82-40ae-8159-925e0f5b4393",
			"approval_status": "approved",
			"created_at": "2024-12-03T17:56:26.881804Z",
			"__class__": "Service"
		},
		{
			"price": 100.0,
			"medical_practitioner_id": "ff67ff99-6788-4091-9650-def1c4c3c110",
			"is_admin_defined": true,
			"id": "e8503397-e527-4fd6-947a-0f1f93704fff",
			"updated_at": "2024-12-03T17:56:26.881931Z",
			"name": "Example Service 1",
			"description": "This is an example service description.",
			"admin_id": "e3ca984e-9c82-40ae-8159-925e0f5b4393",
			"approval_status": "approved",
			"created_at": "2024-12-03T17:56:26.881804Z",
			"__class__": "Service"
		}
	]
}
```




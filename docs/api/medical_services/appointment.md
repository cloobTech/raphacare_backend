## Book an Appointment

### Request

- **Method:** `POST`
- **Endpoint:** `/appointments`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>`
- **Body:**

## Home Service Request Body

```json
{
  "patient_id": "e926ff63-344e-46e1-866f-75a211694b3b",
  "medical_practitioner_id": "06ec8028-0197-4332-8163-9d25482b68de",
  "appointment_start_time": "2022-5-27T02:30:27.362490Z",
  "appointment_end_time": "2022-6-27T03:30:27.362490Z",
  "appointment_status": "pending",
  "appointment_type": "home_service",
  "appointment_reason": "Routine check-up",
  "appointment_note": "Patient requested an early appointment",
  "home_address": {
    "street": "street 2, 125 , Lake rd",
    "city": "City",
    "state": "State"
  }
}
```

## Physical Request Body

```json
{
  "patient_id": "e926ff63-344e-46e1-866f-75a211694b3b",
  "medical_practitioner_id": "06ec8028-0197-4332-8163-9d25482b68de",
  "appointment_start_time": "2022-5-27T02:30:27.362490Z",
  "appointment_end_time": "2022-6-27T03:30:27.362490Z",
  "appointment_status": "pending",
  "appointment_type": "physical",
  "appointment_reason": "Routine check-up",
  "appointment_note": "Patient requested an early appointment",
  "health_center_id": "1aa05106-d1f2-4fad-b7a6-db5555b9a2a3"
}
```

### Response

#### Success Response

- **Status Code:** `200 OK`
- **Body:** A JSON object.

```json
{
  "status": "success",
  "message": "Appointment created successfully",
  "data": {
    "patient_id": "60f2ea0c-a0d3-4a40-bfa5-efcc9b32c4ba",
    "medical_practitioner_id": "792d0ae2-24d3-4b48-afee-416e828887f3",
    "appointment_start_time": "2022-07-27T02:30:27.362490Z",
    "appointment_end_time": "2022-08-27T03:30:27.362490Z",
    "appointment_status": "pending",
    "appointment_reason": "Routine check-up",
    "appointment_note": "Patient requested an early appointment",
    "patient": "[Patient] (60f2ea0c-a0d3-4a40-bfa5-efcc9b32c4ba) {...}",
    "medical_practitioner": "[MedicalPractitioner] (792d0ae2-24d3-4b48-afee-416e828887f3) {...}",
    "id": "6aa4f0f0-28dc-4190-ba0d-23d45d43e613",
    "created_at": "2024-11-30T18:38:31.424857Z",
    "updated_at": "2024-11-30T18:38:31.425002Z",
    "appointment_type": "online",
    "__class__": "Appointment"
  }
}
```

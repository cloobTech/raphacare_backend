from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import (auth, patient, medical_practitioner, appointment, consultation, prescription, event, notification, service, health_center
                           )

app = FastAPI()


origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow sending cookies in cross-origin requests
    # Allow all HTTP methods, you can specify specific methods if needed
    allow_methods=["*"],
    # Allow all headers, you can specify specific headers if needed
    allow_headers=["*"],
)


# MiddleWare
app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(medical_practitioner.router)
app.include_router(appointment.router)
app.include_router(consultation.router)
app.include_router(prescription.router)
app.include_router(event.router)
app.include_router(notification.router)
app.include_router(service.router)
app.include_router(health_center.router)


@app.get("/")
async def read_root():
    """Check server status"""
    return {"server_status": "Server is running fine..."}

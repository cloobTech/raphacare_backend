from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth

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
# app.include_router(study.router)
# app.include_router(screener.router)


@app.get("/")
def read_root():
    """Check server status"""
    return {"server_status": "Server is running fine..."}

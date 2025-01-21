from google.oauth2 import id_token
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from services.users.user_management import get_user_by_email
from services.auth.auth_jwt import create_access_token, create_refresh_token
from settings.pydantic_config import settings
from schemas.default_response import DefaultResponse
from schemas.auth import TokenResponse

# Using the provided client_id, client_secret, and redirect_uri directly
flow = Flow.from_client_config(
    client_config={"web": {"client_id": settings.GOOGLE_CLIENT_ID, "project_id": "alphacare-447806", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token",
                           "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_secret": settings.GOOGLE_CLIENT_SECRET, "redirect_uris": ["http://localhost:8000/api/v1/auth/google/callback"], "javascript_origins": ["http://localhost:3000"]}},

    scopes=['https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'openid'],
    redirect_uri='http://localhost:8000/api/v1/auth/google/callback'
)


def get_auth_url() -> DefaultResponse:
    """Get the Google Auth URL"""

    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return DefaultResponse(
        status="success",
        message="Google auth url generated successfully",
        data={
            "auth_url": auth_url
        }

    )


async def get_user_info(code: str, storage) -> TokenResponse:
    """Get the user info"""
    # Exchange authorization code for an access token
    flow.fetch_token(code=code)

    credentials = flow.credentials

    # Verify the ID token and fetch user info
    request = Request()
    user_info = id_token.verify_oauth2_token(
        credentials.id_token, request, settings.GOOGLE_CLIENT_ID
    )

    email = user_info.get("email")
    user = await get_user_by_email(email, storage)

    data_to_encode = {"user_id": user.id,
                      "user_type": user.user_type,
                      "profile_id": user.user_profile_id}
    token = create_access_token(data_to_encode)
    refresh_token = create_refresh_token(data_to_encode)
    return TokenResponse(access_token=token, refresh_token=refresh_token, token_type="Bearer")
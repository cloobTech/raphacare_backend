from datetime import datetime
import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from errors.custome_errors import UserAlreadyExistsError, UserDisabledError, EmailNotVerifiedError
from storage import DBStorage
from models.user import User
from models.admin import Admin
from models.medical_practitioner import MedicalPractitioner
from models.patient import Patient
from utils.generate_token import generate_token


async def check_user_existence(storage: DBStorage, email: str):
    """Check if a user already exists"""
    user = await storage.find_by(User, email=email)
    if user:
        if not user.email_verified:
            await storage.merge(user)
            await user.delete()
        else:
            raise UserAlreadyExistsError("User already exists")


def create_user(user_auth_details: dict) -> User:
    """Create a new user"""
    new_user = User(**user_auth_details)
    # new_user.reset_token = generate_token()
    new_user.reset_token = "123456"
    new_user.token_created_at = datetime.now()
    return new_user


def create_user_profile(new_user: User, user_profile_details: dict) -> Patient | MedicalPractitioner:
    """Create a new user profile"""
    if new_user.user_type == "patient":
        return Patient(**user_profile_details, user=new_user)
    if new_user.user_type == "admin":
        return Admin(**user_profile_details, user=new_user)
    return MedicalPractitioner(**user_profile_details, user=new_user)


async def get_user_by_email(email: str, storage: DBStorage) -> User:
    """Get a user by email"""
    try:
        user = await storage.find_by(User, email=email)
        if user is None:
            raise NoResultFound("User Not Found!")
        return user
    except NoResultFound as exc:
        raise InvalidRequestError("Invalid Email or Password") from exc


def check_user_status(user: User):
    """Check User Status"""
    if not user.password:
        raise NoResultFound("Password Field Empty!")
    if user.disabled:
        raise UserDisabledError("User is Disabled")
    if not user.email_verified:
        raise EmailNotVerifiedError("Email Not Verified")


def verify_password(user: User, password: str | bytes) -> bool:
    """Verify Password"""
    hashed_password = user.password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

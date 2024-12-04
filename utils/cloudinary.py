import cloudinary
from cloudinary.uploader import upload 
from cloudinary.exceptions import Error as CloudinaryError
from settings.pydantic_config import settings
from errors.custome_errors import InvalidFileError


def cloudinary_config():
    """Configure Cloudinary settings."""
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET
    )


async def upload_file_to_cloudinary(file, **kwargs):
    """
    Upload a file to Cloudinary.
    
    Args:
        file: File object from FastAPI (UploadFile).
        kwargs: Additional upload options for Cloudinary.
        
    Returns:
        dict: The result from Cloudinary.
        
    Raises:
        InvalidFileError: For invalid file types or upload errors.
    """
    cloudinary_config()

    # Define valid file types
    VALID_FILE_TYPES = [
        'image/png', 'image/jpeg', 'image/jpg',
        'video/mp4', 'raw', 'auto', 'image', 'video'
    ]

    try:
        # Read file content
        file_content = await file.read()

        # Validate file type
        if file.content_type not in VALID_FILE_TYPES:
            raise InvalidFileError(
                f"Invalid file type '{file.content_type}'. "
                f"Allowed types: {', '.join(VALID_FILE_TYPES)}."
            )

        # Upload to Cloudinary
        result = upload(file_content, **kwargs)
        return result

    except CloudinaryError as e:
        raise InvalidFileError(f"Cloudinary upload error: {str(e)}") from e

    except Exception as e:
        raise InvalidFileError(f"Unexpected error: {str(e)}") from e

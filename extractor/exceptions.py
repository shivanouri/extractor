class ExtractorExceptions(Exception):
    """
    The base class for all exceptions
    """
    pass


class InvalidCropSizeException(ExtractorExceptions):
    """
    Location input to crop the image is out of range
    """
    pass


class NoImageError(ExtractorExceptions):
    """
    Image not found
    """
    pass

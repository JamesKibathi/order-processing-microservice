import random
import string
import uuid


def get_uuid():
    """Generate UUID
    Returns:
        uuid: UUID Version Four
    """
    return uuid.uuid4()

def generate_category_code():
     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))



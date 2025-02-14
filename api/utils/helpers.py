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


def generate_random_phonenumber():
    # Generate a random 10-digit phone number
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    phone_number = f"+254{random_digits}"  
    return phone_number


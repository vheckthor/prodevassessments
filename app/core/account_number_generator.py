import random

# more logic needed for this in a real life scenario


def generate_random_account(account_type: str):
    if account_type.lower() == "current":
        return str(random.randint(5000000000, 9999999999))
    return str(random.randint(1000000000, 4999999999))

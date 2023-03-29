"""
    transaction operations
"""
import json
import sys
from requests import get
from app.config import settings

LOCATION_UNKNOWN = "UNKNOWN"
REQUEST_TIMEOUT = 10
MAX_AMOUNT = sys.float_info.max
IPIFY_BASE_URL = "https://api.ipify.org"


def perform_credit_or_debit_operations(balance: float, amount: float,
                                       transaction_type: str) -> float:
    """
    perform_credit_or_debit_operations 

    Args:
        balance (float)
        amount (float)
        transaction_type (str)

    Raises:
        ValueError

    Returns:
        float
    """
    if amount >= MAX_AMOUNT:
        raise ValueError(f"Amount {amount} is too large")
    if transaction_type == "credit" and amount > 0:
        return balance + amount
    if amount > balance:
        raise ValueError(
            f"Amount {amount} to withdraw is greater than current balance {balance}")
    return balance - amount


def get_user_ip(request_obj):
    """get ip from third party if available else get from request object"""
    resp = get(IPIFY_BASE_URL, timeout=REQUEST_TIMEOUT)
    if resp.ok:
        ip_address = resp.text
        return ip_address
    return request_obj.client[0]


def get_user_location_from_ip(ip_address: str):
    """Get user location from ip address"""
    api_key = settings.Settings().IPIFY_API_KEY
    if api_key == "":
        return LOCATION_UNKNOWN
    url = f"{IPIFY_BASE_URL}/api/v2/country,city?apiKey={api_key}&ipAddress={ip_address}"
    resp = get(url=url, timeout=REQUEST_TIMEOUT)
    if resp.ok:
        location = resp.json()
        return json.loads(location)
    return LOCATION_UNKNOWN

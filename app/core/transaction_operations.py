"""
    transaction operations
"""
import json
from requests import get
from app.config import settings

LOCATION_UNKNOWN = "UNKNOWN"

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
    if transaction_type == "credit" and amount > 0:
        return  balance + amount
    if amount > balance:
        raise ValueError(f"Amount {amount} to withdraw is greater than current balance {balance}")
    return balance - amount

def get_ip_from_ipify(request_obj):
    """get ip from ipify if available else get from request object"""
    resp = get('https://api.ipify.org')
    if resp.ok:
        ip_address = resp.text
        return ip_address
    return request_obj.client



def get_location_from_ipify(ip_address: str):
    """Get user location from ipify"""
    api_key = settings.Settings().IPIFY_API_KEY
    if api_key == "":
        return LOCATION_UNKNOWN
    url = f"https://geo.ipify.org/api/v2/country,city?apiKey={api_key}&ipAddress={ip_address}"
    resp = get(url=url)
    if resp.ok:
        location = resp.json()
        return json.loads(location)
    return LOCATION_UNKNOWN

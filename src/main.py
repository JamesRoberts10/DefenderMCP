from __future__ import annotations
import os, asyncio, json
import msal, httpx
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Validate required environment variables
required_vars = ["TENANT_ID", "CLIENT_ID", "CLIENT_SECRET"]
missing_vars = [var for var in required_vars if var not in os.environ]
if missing_vars:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

# Configuration
TENANT = os.environ["TENANT_ID"]
CLIENT = os.environ["CLIENT_ID"]
SECRET = os.environ["CLIENT_SECRET"]
BASE = "https://api.security.microsoft.com"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT}"
SCOPE = ["https://api.securitycenter.microsoft.com/.default"]

# Initialize MSAL application
_app = msal.ConfidentialClientApplication(CLIENT, SECRET, authority=AUTHORITY)


async def _token() -> str:
    """Get an authentication token."""
    cache = _app.acquire_token_silent(SCOPE, account=None)
    if not cache:
        cache = _app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" not in cache:
        raise RuntimeError(
            f"Failed to acquire token: {cache.get('error_description', 'Unknown error')}"
        )
    return cache["access_token"]


async def _get(path: str, **params) -> dict:
    """Make a GET request to the Microsoft Defender API."""
    hdrs = {
        "Authorization": f"Bearer {await _token()}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get(f"{BASE}{path}", headers=hdrs, params=params)
        r.raise_for_status()
        return r.json()


async def list_devices() -> dict:
    """List all devices."""
    return await _get("/api/machines")


async def get_alerts(limit: int = 10) -> dict:
    """Get recent alerts.

    Args:
        limit: Maximum number of alerts to return
    """
    return await _get("/api/alerts", **{"$top": limit})


def format_alerts(alerts: dict) -> str:
    """Format alerts data for display."""
    if not alerts.get("value"):
        return "No alerts found"

    result = []
    for alert in alerts["value"][:10]:
        result.append(f"\nAlert: {alert.get('title', 'No title')}")
        result.append(f"Severity: {alert.get('severity', 'Unknown')}")
        result.append(f"Status: {alert.get('status', 'Unknown')}")
        result.append(f"Category: {alert.get('category', 'Unknown')}")
        if alert.get("description"):
            result.append(f"Description: {alert['description']}")
        result.append("-" * 50)

    return "\n".join(result)


def format_devices(devices: dict) -> str:
    """Format devices data for display."""
    if not devices.get("value"):
        return "No devices found"

    result = []
    for device in devices["value"]:
        result.append(f"\nDevice: {device.get('computerDnsName', 'Unknown')}")
        result.append(
            f"OS: {device.get('osPlatform', 'Unknown')} {device.get('osVersion', '')}"
        )
        result.append(f"Health Status: {device.get('healthStatus', 'Unknown')}")
        result.append(f"Last Seen: {device.get('lastSeen', 'Unknown')}")
        result.append("-" * 50)

    return "\n".join(result)


async def main():
    """Main function to demonstrate API usage."""
    # Get and display recent alerts
    alerts = await get_alerts(limit=10)
    print("\nRecent Alerts:")
    print(format_alerts(alerts))

    # Get and display devices
    devices = await list_devices()
    print("\nDevices:")
    print(format_devices(devices))


if __name__ == "__main__":
    # Handle Jupyter/IPython environment
    try:
        import IPython

        if IPython.get_ipython() is not None:
            import nest_asyncio

            nest_asyncio.apply()
    except ImportError:
        pass

    asyncio.run(main())

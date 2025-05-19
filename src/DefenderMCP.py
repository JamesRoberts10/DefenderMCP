from fastmcp import FastMCP
from DefenderAPI import get_alerts, list_devices

mcp = FastMCP(name="defender-alerts")
mcp.version = "0.1.0"


@mcp.tool(
    description="Get Defender alerts with optional filters for date range and device ID."
)
async def mcp_get_alerts(
    limit: int = 100,
    start_date: str | None = None,
    end_date: str | None = None,
    device_id: str | None = None,
):
    # Get alerts from the API and return raw response
    return await get_alerts(
        limit=limit, start_date=start_date, end_date=end_date, device_id=device_id
    )


@mcp.tool(description="List Defender devices.")
async def mcp_list_devices():
    # Get devices from the API and return raw response
    return await list_devices()

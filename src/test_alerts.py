import asyncio
from fastmcp import Client
from fastmcp.client.transports import SSETransport
import json


async def test_alerts():
    server_host = "localhost"
    server_port = 8003
    sse_endpoint_url = f"http://{server_host}:{server_port}/sse"

    print(f"Connecting to {sse_endpoint_url}...")

    try:
        transport = SSETransport(url=sse_endpoint_url)
        async with Client(transport=transport) as client:
            print("Connected successfully!")

            # Test 1: Get alerts
            print("\nCalling mcp_get_alerts...")
            alerts_response = await client.call_tool("mcp_get_alerts", {"limit": 5})
            print(f"Response type: {type(alerts_response)}")

            # Handle response based on what we get back
            if isinstance(alerts_response, list) and len(alerts_response) > 0:
                # Handle TextContent response (from JSON string)
                print("Received list response:")
                for item in alerts_response:
                    if hasattr(item, "text"):
                        try:
                            data = json.loads(item.text)
                            # Print sample of the data
                            data_sample = json.dumps(data, indent=2)
                            print(
                                data_sample[:300] + "..."
                                if len(data_sample) > 300
                                else data_sample
                            )
                        except json.JSONDecodeError:
                            print(f"\nRaw content: {item}")
                    else:
                        print(f"\nRaw item: {item}")
            elif isinstance(alerts_response, dict):
                # Handle direct dictionary response
                print("Received dictionary response for alerts:")
                if "value" in alerts_response:
                    print(f"\nFound {len(alerts_response.get('value', []))} alerts")
                    # Show sample of first alert if available
                    if (
                        alerts_response.get("value")
                        and len(alerts_response["value"]) > 0
                    ):
                        print("\n=== FIRST ALERT SAMPLE ===")
                        print(json.dumps(alerts_response["value"][0], indent=2))
                    else:
                        print("No alerts in the response")
                else:
                    # Just print the whole response if it's small, or truncate if large
                    alerts_sample = json.dumps(alerts_response, indent=2)
                    print(
                        alerts_sample[:300] + "..."
                        if len(alerts_sample) > 300
                        else alerts_sample
                    )
            else:
                print(f"Unexpected response type: {alerts_response}")

            # Test 2: List devices
            print("\n\nCalling mcp_list_devices...")
            devices_response = await client.call_tool("mcp_list_devices", {})

            # Similar handling for devices response
            if isinstance(devices_response, list) and len(devices_response) > 0:
                print("Received list response for devices")
                for item in devices_response:
                    if hasattr(item, "text"):
                        try:
                            data = json.loads(item.text)
                            data_sample = json.dumps(data, indent=2)
                            print(
                                data_sample[:300] + "..."
                                if len(data_sample) > 300
                                else data_sample
                            )
                        except json.JSONDecodeError:
                            print(f"\nRaw content: {item}")
                    else:
                        print(f"\nRaw item: {item}")
            elif isinstance(devices_response, dict):
                print("Received dictionary response for devices:")
                if "value" in devices_response:
                    print(f"\nFound {len(devices_response.get('value', []))} devices")
                    # Show sample of first device if available
                    if (
                        devices_response.get("value")
                        and len(devices_response["value"]) > 0
                    ):
                        print("\n=== FIRST DEVICE SAMPLE ===")
                        print(json.dumps(devices_response["value"][0], indent=2))
                    else:
                        print("No devices in the response")
                else:
                    devices_sample = json.dumps(devices_response, indent=2)
                    print(
                        devices_sample[:300] + "..."
                        if len(devices_sample) > 300
                        else devices_sample
                    )
            else:
                print(f"Unexpected devices response type: {devices_response}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_alerts())

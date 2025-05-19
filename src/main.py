from DefenderMCP import mcp  # FastMCP instance you defined

if __name__ == "__main__":
    # Bind to 0.0.0.0:8003 and expose Server-Sent Events (/sse)
    mcp.run(host="0.0.0.0", port=8003, transport="sse")

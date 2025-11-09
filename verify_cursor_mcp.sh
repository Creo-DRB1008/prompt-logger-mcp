#!/bin/bash
# verify_cursor_mcp.sh
# Quick verification script to check if the MCP server is properly configured

echo "🔍 Verifying MCP Notion Server Setup..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MCP_SERVER_PATH="$SCRIPT_DIR/mcp_notion_server.py"

# Check if mcp.json exists
if [ -f ~/.cursor/mcp.json ]; then
    echo "✅ Found ~/.cursor/mcp.json"
else
    echo "❌ ~/.cursor/mcp.json not found"
    echo "   Please create it with the configuration from README.md"
    exit 1
fi

# Check if notion-chat-logger is configured
if grep -q "notion-chat-logger" ~/.cursor/mcp.json; then
    echo "✅ notion-chat-logger is configured in mcp.json"
else
    echo "❌ notion-chat-logger not found in mcp.json"
    echo "   Please add the configuration from README.md"
    exit 1
fi

# Check if the MCP server file exists
if [ -f "$MCP_SERVER_PATH" ]; then
    echo "✅ MCP server file exists: $MCP_SERVER_PATH"
else
    echo "❌ MCP server file not found: $MCP_SERVER_PATH"
    echo "   Make sure you're running this script from the repository directory"
    exit 1
fi

# Check if the file is executable
if [ -x "$MCP_SERVER_PATH" ]; then
    echo "✅ MCP server file is executable"
else
    echo "⚠️  MCP server file is not executable (not required, but recommended)"
    echo "   Run: chmod +x $MCP_SERVER_PATH"
fi

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python 3 is available: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
    echo "   Please install Python 3.7 or higher"
    exit 1
fi

# Check if requests library is installed
if python3 -c "import requests" 2>/dev/null; then
    echo "✅ Python 'requests' library is installed"
else
    echo "❌ Python 'requests' library not found"
    echo "   Install with: pip3 install -r requirements.txt"
    exit 1
fi

# Check for environment variables
echo ""
echo "🔑 Checking Notion credentials..."

# Set dummy env vars for testing if not set
export NOTION_API_KEY="${NOTION_API_KEY:-test_key}"
export NOTION_DATABASE_ID="${NOTION_DATABASE_ID:-test_db_id}"

# Test the MCP server (it will fail to connect to Notion but should respond to MCP protocol)
echo ""
echo "🧪 Testing MCP server protocol..."
TEST_OUTPUT=$(echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | python3 "$MCP_SERVER_PATH" 2>&1)

if echo "$TEST_OUTPUT" | grep -q '"serverInfo"'; then
    echo "✅ MCP server responds correctly"
else
    echo "❌ MCP server did not respond correctly"
    echo "   Output: $TEST_OUTPUT"
    exit 1
fi

# Check if credentials are configured in mcp.json
if grep -q "NOTION_API_KEY" ~/.cursor/mcp.json; then
    echo "✅ NOTION_API_KEY is configured in mcp.json"
else
    echo "⚠️  NOTION_API_KEY not found in mcp.json"
    echo "   Please add your Notion API key to ~/.cursor/mcp.json"
fi

if grep -q "NOTION_DATABASE_ID" ~/.cursor/mcp.json; then
    echo "✅ NOTION_DATABASE_ID is configured in mcp.json"
else
    echo "⚠️  NOTION_DATABASE_ID not found in mcp.json"
    echo "   Please add your Notion database ID to ~/.cursor/mcp.json"
fi

echo ""
echo "🎉 All checks passed!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure you've set NOTION_API_KEY and NOTION_DATABASE_ID in ~/.cursor/mcp.json"
echo "2. Restart Cursor (⌘Q and reopen)"
echo "3. Go to Cursor Settings → Features → Model Context Protocol"
echo "4. Look for 'notion-chat-logger' in the list"
echo "5. In a chat, type '@' and look for 'store_chat_log' tool"
echo ""
echo "💡 To test the full integration with Notion, run:"
echo "   python3 test_mcp_notion.py"

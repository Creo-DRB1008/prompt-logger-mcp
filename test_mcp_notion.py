#!/usr/bin/env python3
"""
Test script for the MCP Notion server.
This simulates how Cursor will interact with the MCP server.
"""
import subprocess
import json
import sys

def send_mcp_request(process, request):
    """Send a JSON-RPC request to the MCP server and get the response."""
    request_json = json.dumps(request) + "\n"
    process.stdin.write(request_json)
    process.stdin.flush()
    
    response_line = process.stdout.readline()
    return json.loads(response_line)

def main():
    print("🚀 Starting MCP Notion Server test...\n")
    
    # Start the MCP server as a subprocess
    process = subprocess.Popen(
        ["python3", "mcp_notion_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Test 1: Initialize
        print("📋 Test 1: Initialize")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        response = send_mcp_request(process, init_request)
        print(f"✅ Initialize response: {json.dumps(response, indent=2)}\n")
        
        # Test 2: List tools
        print("📋 Test 2: List tools")
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        response = send_mcp_request(process, list_request)
        tools = response.get("result", {}).get("tools", [])
        print(f"✅ Found {len(tools)} tool(s):")
        for tool in tools:
            print(f"   - {tool['name']}: {tool['description']}\n")
        
        # Test 3: Call the store_chat_log tool
        print("📋 Test 3: Call store_chat_log tool")
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "store_chat_log",
                "arguments": {
                    "prompt": "How do I implement a binary search tree in Python?",
                    "response": "Here's how to implement a binary search tree in Python:\n\nclass Node:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None",
                    "user": "dhairya.bhuta@creopsan.com",
                    "context": "file: algorithms.py, function: implement_bst",
                    "timestamp": "2025-11-05T20:00:00Z"
                }
            }
        }
        response = send_mcp_request(process, call_request)
        result = response.get("result", {})
        content = result.get("content", [{}])[0].get("text", "")
        result_data = json.loads(content)
        
        if result_data.get("success"):
            print(f"✅ Successfully stored to Notion!")
            print(f"   Page ID: {result_data.get('page_id')}")
            print(f"   Message: {result_data.get('message')}\n")
        else:
            print(f"❌ Failed to store to Notion: {result_data.get('error')}\n")
        
        print("🎉 All tests passed! The MCP server is working correctly.")
        print("\n📝 Next steps:")
        print("1. Restart Cursor to load the new MCP server configuration")
        print("2. Open Cursor Settings > Features > Model Context Protocol")
        print("3. You should see 'notion-chat-logger' in the list")
        print("4. In a chat, type '@' and you should see the 'store_chat_log' tool")
        print("5. Test it manually by invoking the tool with test data")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    main()




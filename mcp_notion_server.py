#!/usr/bin/env python3
"""
MCP Server for logging Cursor chat interactions to Notion.
This server implements the Model Context Protocol (MCP) specification.
"""
import os
import sys
import json
import logging
from datetime import datetime
from typing import Any
import requests

# Configure logging to stderr (stdout is reserved for MCP protocol)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
log = logging.getLogger("mcp_notion_server")

# Notion Configuration - Load from environment variables
NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
NOTION_VERSION = os.environ.get("NOTION_VERSION", "2022-06-28")
NOTION_PAGES_URL = "https://api.notion.com/v1/pages"

# Validate required environment variables
if not NOTION_API_KEY:
    log.error("NOTION_API_KEY environment variable is required")
    sys.exit(1)

if not DATABASE_ID:
    log.error("NOTION_DATABASE_ID environment variable is required")
    sys.exit(1)


def store_chat_log_to_notion(prompt: str, response: str, user: str, context: str = "", timestamp: str = None) -> dict:
    """
    Store a chat log entry to Notion database.
    
    Args:
        prompt: The user's prompt/question
        response: The assistant's response
        user: User identifier (email or username)
        context: Optional context (file path, function name, etc.)
        timestamp: ISO-8601 timestamp (defaults to current time)
    
    Returns:
        dict with status and page_id if successful
    """
    if not timestamp:
        timestamp = datetime.utcnow().isoformat()
    
    # Truncate to avoid Notion limits
    prompt_safe = prompt[:2000]
    response_safe = response[:4000]
    user_safe = user[:200]
    context_safe = context[:1000]
    
    notion_payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Prompt": {"title": [{"text": {"content": prompt_safe}}]},
            "Response": {"rich_text": [{"text": {"content": response_safe}}]},
            "User": {"rich_text": [{"text": {"content": user_safe}}]},
            "Timestamp": {"date": {"start": timestamp}},
            "Context": {"rich_text": [{"text": {"content": context_safe}}]},
        },
    }
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }
    
    try:
        r = requests.post(NOTION_PAGES_URL, json=notion_payload, headers=headers, timeout=15)
        r.raise_for_status()
        
        resp_json = r.json()
        page_id = resp_json.get("id")
        
        log.info(f"Stored chat log to Notion. page_id={page_id} user={user_safe}")
        
        return {
            "success": True,
            "page_id": page_id,
            "message": f"Successfully logged chat to Notion (page {page_id})"
        }
    
    except requests.RequestException as e:
        log.error(f"Failed to store to Notion: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to log chat to Notion: {e}"
        }


class MCPServer:
    """
    Simple MCP server implementation using stdio transport.
    Follows the Model Context Protocol specification.
    """
    
    def __init__(self):
        self.tools = {
            "store_chat_log": {
                "name": "store_chat_log",
                "description": "Store a chat interaction (prompt and response) to Notion database for logging and analysis",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The user's prompt or question"
                        },
                        "response": {
                            "type": "string",
                            "description": "The assistant's response"
                        },
                        "user": {
                            "type": "string",
                            "description": "User identifier (email or username)"
                        },
                        "context": {
                            "type": "string",
                            "description": "Optional context (file path, function name, etc.)",
                            "default": ""
                        },
                        "timestamp": {
                            "type": "string",
                            "description": "ISO-8601 timestamp (defaults to current time if not provided)",
                            "format": "date-time"
                        }
                    },
                    "required": ["prompt", "response", "user"]
                }
            }
        }
    
    def handle_request(self, request: dict) -> dict:
        """Handle an MCP protocol request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        log.info(f"Received MCP request: method={method}, id={request_id}")
        
        try:
            if method == "initialize":
                result = self.handle_initialize(params)
            elif method == "tools/list":
                result = self.handle_tools_list(params)
            elif method == "tools/call":
                result = self.handle_tools_call(params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        
        except Exception as e:
            log.exception(f"Error handling request: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def handle_initialize(self, params: dict) -> dict:
        """Handle the initialize request."""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "notion-chat-logger",
                "version": "1.0.0"
            }
        }
    
    def handle_tools_list(self, params: dict) -> dict:
        """Handle the tools/list request."""
        return {
            "tools": list(self.tools.values())
        }
    
    def handle_tools_call(self, params: dict) -> dict:
        """Handle the tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name != "store_chat_log":
            raise ValueError(f"Unknown tool: {tool_name}")
        
        # Extract parameters
        prompt = arguments.get("prompt", "")
        response = arguments.get("response", "")
        user = arguments.get("user", "unknown")
        context = arguments.get("context", "")
        timestamp = arguments.get("timestamp")
        
        # Validate required fields
        if not prompt:
            raise ValueError("Missing required field: prompt")
        if not response:
            raise ValueError("Missing required field: response")
        
        # Call the Notion API
        result = store_chat_log_to_notion(
            prompt=prompt,
            response=response,
            user=user,
            context=context,
            timestamp=timestamp
        )
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }
            ]
        }
    
    def run(self):
        """Run the MCP server loop, reading from stdin and writing to stdout."""
        log.info("MCP Notion Server starting...")
        log.info(f"Notion Database ID: {DATABASE_ID}")
        
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                
                # Write response to stdout (MCP protocol channel)
                print(json.dumps(response), flush=True)
            
            except json.JSONDecodeError as e:
                log.error(f"Invalid JSON received: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)
            
            except Exception as e:
                log.exception(f"Unexpected error: {e}")


if __name__ == "__main__":
    server = MCPServer()
    server.run()


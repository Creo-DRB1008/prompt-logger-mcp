# Detailed Setup Guide

This guide walks you through setting up the Cursor Notion MCP Chat Logger step by step.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Notion Setup](#notion-setup)
3. [Installation](#installation)
4. [Cursor Configuration](#cursor-configuration)
5. [Testing](#testing)
6. [Usage](#usage)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have:

- **Python 3.7+** installed
  ```bash
  python3 --version
  ```
- **Cursor IDE** with MCP support
- **Notion account** (free or paid)
- **Git** (optional, for cloning)

## Notion Setup

### Step 1: Create a Notion Integration

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **"+ New integration"**
3. Fill in the details:
   - **Name**: Cursor Chat Logger
   - **Associated workspace**: Select your workspace
   - **Type**: Internal integration
4. Click **"Submit"**
5. Copy the **"Internal Integration Token"** (starts with `secret_`)
   - ⚠️ Keep this secret! Don't share it publicly.

### Step 2: Create a Notion Database

1. Open Notion and create a new page
2. Add a **Database** (Table view recommended)
3. Name it "Cursor Chat Logs" or similar
4. Add the following properties:

| Property Name | Property Type | Description |
|---------------|---------------|-------------|
| Prompt | Title | The user's question (auto-created) |
| Response | Text | The AI's response |
| User | Text | User identifier (email) |
| Context | Text | File path, function name, etc. |
| Timestamp | Date | When the interaction occurred |

5. **Share the database with your integration:**
   - Click **"Share"** in the top right
   - Click **"Invite"**
   - Find your integration ("Cursor Chat Logger")
   - Click **"Invite"**

### Step 3: Get the Database ID

1. Open your database in Notion
2. Look at the URL in your browser:
   ```
   https://www.notion.so/YOUR_WORKSPACE/DATABASE_ID?v=VIEW_ID
   ```
3. Copy the **DATABASE_ID** (32 characters, usually hex)
   - Example: `2a39a9a20f008063bf47f05c286daacf`

## Installation

### Option 1: Clone from GitHub

```bash
cd ~/Documents  # or wherever you want to install
git clone https://github.com/YOUR_USERNAME/cursor-notion-mcp.git
cd cursor-notion-mcp
```

### Option 2: Download ZIP

1. Download the repository as a ZIP file
2. Extract it to a location of your choice
3. Open Terminal/Command Prompt in that directory

### Install Dependencies

```bash
pip3 install -r requirements.txt
```

Or manually:

```bash
pip3 install requests
```

### Make Scripts Executable (Mac/Linux)

```bash
chmod +x mcp_notion_server.py
chmod +x verify_cursor_mcp.sh
```

## Cursor Configuration

### Step 1: Locate Your Cursor Config Directory

- **Mac**: `~/.cursor/`
- **Windows**: `%APPDATA%\Cursor\`
- **Linux**: `~/.config/Cursor/`

### Step 2: Create or Edit `mcp.json`

Create the file `~/.cursor/mcp.json` (or edit if it exists):

```json
{
  "mcpServers": {
    "notion-chat-logger": {
      "command": "python3",
      "args": [
        "/ABSOLUTE/PATH/TO/cursor-notion-mcp/mcp_notion_server.py"
      ],
      "env": {
        "NOTION_API_KEY": "secret_YOUR_INTEGRATION_TOKEN_HERE",
        "NOTION_DATABASE_ID": "YOUR_DATABASE_ID_HERE"
      }
    }
  }
}
```

**Important Replacements:**

1. **`/ABSOLUTE/PATH/TO/cursor-notion-mcp/`**
   - Mac/Linux: `/Users/yourname/Documents/cursor-notion-mcp/`
   - Windows: `C:\\Users\\yourname\\Documents\\cursor-notion-mcp\\`

2. **`secret_YOUR_INTEGRATION_TOKEN_HERE`**
   - Replace with your Notion integration token from Step 1

3. **`YOUR_DATABASE_ID_HERE`**
   - Replace with your database ID from Step 3

### Example (Mac):

```json
{
  "mcpServers": {
    "notion-chat-logger": {
      "command": "python3",
      "args": [
        "/Users/john/Documents/cursor-notion-mcp/mcp_notion_server.py"
      ],
      "env": {
        "NOTION_API_KEY": "secret_abc123xyz789...",
        "NOTION_DATABASE_ID": "2a39a9a20f008063bf47f05c286daacf"
      }
    }
  }
}
```

### Example (Windows):

```json
{
  "mcpServers": {
    "notion-chat-logger": {
      "command": "python",
      "args": [
        "C:\\Users\\john\\Documents\\cursor-notion-mcp\\mcp_notion_server.py"
      ],
      "env": {
        "NOTION_API_KEY": "secret_abc123xyz789...",
        "NOTION_DATABASE_ID": "2a39a9a20f008063bf47f05c286daacf"
      }
    }
  }
}
```

### Step 3: Validate JSON

Make sure your JSON is valid:

```bash
# Mac/Linux
cat ~/.cursor/mcp.json | python3 -m json.tool

# Windows (PowerShell)
Get-Content $env:APPDATA\Cursor\mcp.json | python -m json.tool
```

If you see formatted JSON output, it's valid! If you see an error, fix the syntax.

## Testing

### Step 1: Verify Setup

```bash
cd /path/to/cursor-notion-mcp
./verify_cursor_mcp.sh
```

Expected output:
```
✅ Found ~/.cursor/mcp.json
✅ notion-chat-logger is configured
✅ MCP server file exists
✅ Python 3 is available
✅ Python 'requests' library is installed
✅ MCP server responds correctly
✅ NOTION_API_KEY is configured
✅ NOTION_DATABASE_ID is configured
🎉 All checks passed!
```

### Step 2: Test with Notion API

```bash
python3 test_mcp_notion.py
```

Expected output:
```
🚀 Starting MCP Notion Server test...

📋 Test 1: Initialize
✅ Initialize response: {...}

📋 Test 2: List tools
✅ Found 1 tool(s):
   - store_chat_log: Store a chat interaction...

📋 Test 3: Call store_chat_log tool
✅ Successfully stored to Notion!
   Page ID: 2a39a9a2-0f00-812b-b4fb-...
   Message: Successfully logged chat to Notion

🎉 All tests passed!
```

### Step 3: Check Notion

1. Open your Notion database
2. You should see a new entry with:
   - Prompt: "How do I implement a binary search tree in Python?"
   - Response: "Here's how to implement..."
   - User: Your email
   - Context: "file: algorithms.py, function: implement_bst"
   - Timestamp: Current time

## Cursor Integration

### Step 1: Restart Cursor

**Important**: You MUST restart Cursor completely for it to load the MCP configuration.

- **Mac**: ⌘Q, then reopen
- **Windows/Linux**: Alt+F4, then reopen

### Step 2: Verify in Cursor Settings

1. Open Cursor
2. Go to **Settings** (⌘, or Ctrl+,)
3. Navigate to: **Features** → **Model Context Protocol (MCP)**
4. You should see **"notion-chat-logger"** in the server list
5. Status should show "Running" or "Connected"

### Step 3: Test in Chat

1. Open any chat in Cursor
2. Type `@` to open the tool picker
3. You should see **"store_chat_log"** in the list
4. Click it to test manually

## Usage

### Manual Invocation

After a conversation, say:

```
Log this conversation to Notion
```

Or:

```
Please use the store_chat_log tool to save this chat
```

### Using the Tool Picker

1. Type `@` in chat
2. Select `store_chat_log`
3. Fill in:
   - **Prompt**: The user's question
   - **Response**: The AI's answer
   - **User**: Your email
   - **Context**: File name, function, etc.
   - **Timestamp**: (optional, auto-fills)

### Automatic Context

The AI can automatically extract context:

```
User: "How do I implement OAuth in Python?"
AI: [provides detailed answer]
User: "Log this with context 'auth.py implementation'"
AI: [automatically uses the tool with the conversation]
```

## Troubleshooting

### Issue: Server Not Showing in Cursor

**Symptoms**: "notion-chat-logger" doesn't appear in Cursor Settings → MCP

**Solutions**:
1. Check `~/.cursor/mcp.json` is valid JSON
2. Verify the absolute path to `mcp_notion_server.py` is correct
3. Restart Cursor completely (quit and reopen, not just close window)
4. Check Cursor logs:
   - Mac: `~/Library/Logs/Cursor/main.log`
   - Windows: `%APPDATA%\Cursor\logs\main.log`
   - Linux: `~/.config/Cursor/logs/main.log`

### Issue: Tool Not Appearing in @ Menu

**Symptoms**: Can't find "store_chat_log" when typing `@`

**Solutions**:
1. Verify the server is listed in Settings → Features → MCP
2. Try typing the full name: `@store_chat_log`
3. Check Developer Tools (Help → Toggle Developer Tools) for errors
4. Try restarting Cursor again

### Issue: "NOTION_API_KEY environment variable is required"

**Symptoms**: Server starts but immediately exits

**Solutions**:
1. Check that `NOTION_API_KEY` is set in `~/.cursor/mcp.json`
2. Verify the key starts with `secret_`
3. Make sure there are no extra spaces or quotes
4. Restart Cursor after making changes

### Issue: "Failed to store to Notion"

**Symptoms**: Tool runs but returns an error

**Solutions**:
1. Verify your Notion integration token is valid
2. Check that the database ID is correct (32 hex characters)
3. Ensure the integration has access to the database (Share → Invite)
4. Verify all required properties exist in the database:
   - Prompt (Title)
   - Response (Text)
   - User (Text)
   - Context (Text)
   - Timestamp (Date)

### Issue: Python/requests Not Found

**Symptoms**: "python3: command not found" or "No module named 'requests'"

**Solutions**:
```bash
# Check Python installation
python3 --version

# Install requests
pip3 install requests

# Or install from requirements.txt
pip3 install -r requirements.txt
```

### Issue: Permission Denied

**Symptoms**: "Permission denied" when running scripts

**Solutions**:
```bash
# Make scripts executable
chmod +x mcp_notion_server.py
chmod +x verify_cursor_mcp.sh
chmod +x test_mcp_notion.py
```

## Advanced Configuration

### Using Environment Variables

Instead of hardcoding credentials in `mcp.json`, use a `.env` file:

1. Create `.env` in the repository:
   ```bash
   NOTION_API_KEY=secret_your_token_here
   NOTION_DATABASE_ID=your_database_id_here
   ```

2. Update `mcp.json` to source the `.env` file:
   ```json
   {
     "mcpServers": {
       "notion-chat-logger": {
         "command": "bash",
         "args": [
           "-c",
           "source /path/to/.env && python3 /path/to/mcp_notion_server.py"
         ]
       }
     }
   }
   ```

3. Add `.env` to `.gitignore` (already done)

### Multiple Databases

To log to different databases for different projects, create multiple server entries:

```json
{
  "mcpServers": {
    "notion-chat-logger-work": {
      "command": "python3",
      "args": ["/path/to/mcp_notion_server.py"],
      "env": {
        "NOTION_API_KEY": "secret_work_token",
        "NOTION_DATABASE_ID": "work_database_id"
      }
    },
    "notion-chat-logger-personal": {
      "command": "python3",
      "args": ["/path/to/mcp_notion_server.py"],
      "env": {
        "NOTION_API_KEY": "secret_personal_token",
        "NOTION_DATABASE_ID": "personal_database_id"
      }
    }
  }
}
```

## Next Steps

- ✅ Use it regularly to build a knowledge base
- ✅ Analyze your chat logs to identify patterns
- ✅ Create Notion views to filter by context, user, or date
- ✅ Share your setup with your team
- ✅ Contribute improvements back to the repository

## Support

If you're still having issues:

1. Run `./verify_cursor_mcp.sh` and share the output
2. Run `python3 test_mcp_notion.py` and share the output
3. Check Cursor's logs for errors
4. Open an issue on GitHub with:
   - Your OS and Python version
   - The error message
   - Steps to reproduce

---

**Happy logging!** 🎉


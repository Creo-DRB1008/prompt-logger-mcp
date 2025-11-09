# Cursor Notion MCP - Chat Logger

A Model Context Protocol (MCP) server that logs your Cursor AI chat interactions to Notion for analysis, documentation, and knowledge management.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

- ✅ **Automatic Chat Logging**: Log Cursor AI conversations to Notion with a single command
- ✅ **MCP Protocol**: Implements the official Model Context Protocol specification
- ✅ **Easy Setup**: Simple configuration via environment variables
- ✅ **Rich Context**: Captures prompt, response, user, context, and timestamp
- ✅ **Notion Integration**: Stores data in a structured Notion database
- ✅ **Privacy First**: Self-hosted, no third-party services

## 📋 Prerequisites

- Python 3.7 or higher
- Cursor IDE (with MCP support)
- Notion account with API access
- `requests` library (`pip install requests`)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/cursor-notion-mcp.git
cd cursor-notion-mcp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Notion

#### Create a Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Name it "Cursor Chat Logger"
4. Copy the **Internal Integration Token** (starts with `secret_`)

#### Create a Notion Database

1. Create a new database in Notion
2. Add these properties:
   - **Prompt** (Title) - The user's question
   - **Response** (Text) - The AI's response
   - **User** (Text) - User identifier
   - **Context** (Text) - File/function context
   - **Timestamp** (Date) - When it happened

3. Share the database with your integration:
   - Click "Share" on the database
   - Invite your integration

4. Get the **Database ID** from the URL:
   ```
   https://notion.so/YOUR_WORKSPACE/DATABASE_ID?v=...
                                    ^^^^^^^^^^^^
   ```

### 4. Configure Cursor

Edit `~/.cursor/mcp.json` (create if it doesn't exist):

```json
{
  "mcpServers": {
    "notion-chat-logger": {
      "command": "python3",
      "args": [
        "/ABSOLUTE/PATH/TO/cursor-notion-mcp/mcp_notion_server.py"
      ],
      "env": {
        "NOTION_API_KEY": "secret_YOUR_NOTION_INTEGRATION_TOKEN",
        "NOTION_DATABASE_ID": "YOUR_DATABASE_ID"
      }
    }
  }
}
```

**Important**: Replace:
- `/ABSOLUTE/PATH/TO/` with the actual path to this repository
- `secret_YOUR_NOTION_INTEGRATION_TOKEN` with your Notion integration token
- `YOUR_DATABASE_ID` with your Notion database ID

### 5. Restart Cursor

Quit Cursor completely (⌘Q on Mac, Alt+F4 on Windows/Linux) and reopen it.

### 6. Verify Installation

```bash
# Run the test script
python3 test_mcp_notion.py
```

You should see:
```
✅ Initialize response
✅ Found 1 tool(s)
✅ Successfully stored to Notion!
```

## 💡 Usage

### In Cursor Chat

After having a conversation with Cursor AI, simply say:

```
Log this conversation to Notion
```

Or use the tool picker:
1. Type `@` in the chat
2. Select `store_chat_log`
3. Fill in the details (or let the AI do it)

### Manual Tool Call

You can also invoke the tool explicitly:

```
@store_chat_log
Prompt: "How do I implement OAuth?"
Response: "Here's how to implement OAuth..."
User: "your.email@example.com"
Context: "auth.py"
```

## 🧪 Testing

### Quick Verification

```bash
./verify_cursor_mcp.sh
```

### Full Test Suite

```bash
python3 test_mcp_notion.py
```

### Manual MCP Protocol Test

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python3 mcp_notion_server.py
```

## 📁 Project Structure

```
cursor-notion-mcp/
├── mcp_notion_server.py       # Main MCP server
├── test_mcp_notion.py          # Test suite
├── verify_cursor_mcp.sh        # Quick verification script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── SETUP.md                    # Detailed setup guide
├── ARCHITECTURE.md             # Technical architecture
└── LICENSE                     # MIT License
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NOTION_API_KEY` | Yes | Your Notion integration token |
| `NOTION_DATABASE_ID` | Yes | Your Notion database ID |
| `NOTION_VERSION` | No | Notion API version (default: 2022-06-28) |

### Notion Database Schema

Your Notion database must have these properties:

| Property | Type | Description |
|----------|------|-------------|
| Prompt | Title | The user's question/prompt |
| Response | Text | The assistant's response |
| User | Text | User identifier (email) |
| Context | Text | File path, function name, etc. |
| Timestamp | Date | When the interaction occurred |

## 🐛 Troubleshooting

### Server Not Showing in Cursor

1. Check that `~/.cursor/mcp.json` is valid JSON
2. Verify the absolute path to `mcp_notion_server.py` is correct
3. Restart Cursor completely (quit and reopen)
4. Check Cursor logs: `~/Library/Logs/Cursor/` (Mac) or `%APPDATA%\Cursor\logs\` (Windows)

### Tool Not Appearing

1. Verify the server is listed in Cursor Settings → Features → MCP
2. Try typing the full tool name: `@store_chat_log`
3. Check Developer Tools (Help → Toggle Developer Tools) for errors

### Notion API Errors

1. Verify your `NOTION_API_KEY` is correct (starts with `secret_`)
2. Verify your `NOTION_DATABASE_ID` is correct (32 characters, hex)
3. Ensure the integration has access to the database (Share → Invite integration)
4. Check that all required properties exist in the database

### Python Errors

```bash
# Check Python version
python3 --version  # Should be 3.7+

# Install dependencies
pip3 install -r requirements.txt

# Test the server directly
python3 mcp_notion_server.py
# Then type: {"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
```

## 🔐 Security

**⚠️ Important Security Notes:**

1. **Never commit your Notion API key** to version control
2. **Use environment variables** for sensitive data
3. **Restrict integration permissions** in Notion to only the databases you need
4. **Review logged data** regularly to ensure no sensitive information is stored
5. **Consider encrypting** sensitive fields before logging

### Recommended: Use `.env` File

Instead of hardcoding credentials in `mcp.json`, use a `.env` file:

```bash
# .env
NOTION_API_KEY=secret_YOUR_TOKEN
NOTION_DATABASE_ID=YOUR_DATABASE_ID
```

Then update `mcp.json`:

```json
{
  "mcpServers": {
    "notion-chat-logger": {
      "command": "bash",
      "args": [
        "-c",
        "source .env && python3 /path/to/mcp_notion_server.py"
      ]
    }
  }
}
```

## 📚 Documentation

- [Setup Guide](SETUP.md) - Detailed setup instructions
- [Architecture](ARCHITECTURE.md) - Technical architecture and design
- [MCP Specification](https://spec.modelcontextprotocol.io/) - Official MCP docs
- [Notion API](https://developers.notion.com/) - Notion API documentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) - For the MCP specification
- [Cursor](https://cursor.sh/) - For the amazing AI-powered IDE
- [Notion](https://notion.so/) - For the powerful API and database

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/cursor-notion-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/cursor-notion-mcp/discussions)

## 🗺️ Roadmap

- [ ] Support for multiple Notion databases
- [ ] Filtering/redaction of sensitive data
- [ ] Export to other formats (CSV, JSON)
- [ ] Web dashboard for viewing logs
- [ ] Automatic tagging and categorization
- [ ] Search and analytics features

---

**Made with ❤️ for the Cursor community**

If you find this useful, please ⭐ star the repository!


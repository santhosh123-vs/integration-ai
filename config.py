"""
Configuration for Integration AI
"""
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"

# API Definitions - 30 APIs across different categories
APIS = {
    "gmail_send": {
        "name": "Gmail - Send Email",
        "description": "Send an email to someone with subject and body",
        "keywords": ["email", "send", "mail", "message", "gmail", "write email"],
        "parameters": ["to", "subject", "body"],
        "category": "communication"
    },
    "gmail_read": {
        "name": "Gmail - Read Emails",
        "description": "Read and fetch emails from inbox",
        "keywords": ["read email", "check mail", "inbox", "fetch emails", "get messages"],
        "parameters": ["folder", "limit"],
        "category": "communication"
    },
    "slack_send": {
        "name": "Slack - Send Message",
        "description": "Send a message to a Slack channel or user",
        "keywords": ["slack", "send message", "post", "channel", "notify team"],
        "parameters": ["channel", "message"],
        "category": "communication"
    },
    "slack_read": {
        "name": "Slack - Read Messages",
        "description": "Read messages from a Slack channel",
        "keywords": ["slack", "read messages", "channel history", "get slack"],
        "parameters": ["channel", "limit"],
        "category": "communication"
    },
    "calendar_create": {
        "name": "Google Calendar - Create Event",
        "description": "Create a new calendar event or meeting",
        "keywords": ["calendar", "schedule", "meeting", "event", "appointment", "book"],
        "parameters": ["title", "date", "time", "attendees"],
        "category": "productivity"
    },
    "calendar_list": {
        "name": "Google Calendar - List Events",
        "description": "List upcoming calendar events",
        "keywords": ["calendar", "events", "schedule", "upcoming", "meetings today"],
        "parameters": ["date_range"],
        "category": "productivity"
    },
    "drive_upload": {
        "name": "Google Drive - Upload File",
        "description": "Upload a file to Google Drive",
        "keywords": ["upload", "drive", "file", "save", "store", "backup"],
        "parameters": ["file", "folder"],
        "category": "storage"
    },
    "drive_search": {
        "name": "Google Drive - Search Files",
        "description": "Search for files in Google Drive",
        "keywords": ["search", "find file", "drive", "lookup", "locate document"],
        "parameters": ["query"],
        "category": "storage"
    },
    "sheets_read": {
        "name": "Google Sheets - Read Data",
        "description": "Read data from a Google Sheets spreadsheet",
        "keywords": ["sheets", "spreadsheet", "read data", "get cells", "fetch sheet"],
        "parameters": ["spreadsheet_id", "range"],
        "category": "productivity"
    },
    "sheets_write": {
        "name": "Google Sheets - Write Data",
        "description": "Write data to a Google Sheets spreadsheet",
        "keywords": ["sheets", "spreadsheet", "write", "update cells", "add row"],
        "parameters": ["spreadsheet_id", "range", "data"],
        "category": "productivity"
    },
    "twitter_post": {
        "name": "Twitter - Post Tweet",
        "description": "Post a tweet on Twitter/X",
        "keywords": ["tweet", "twitter", "post", "social media", "x post"],
        "parameters": ["content"],
        "category": "social"
    },
    "twitter_search": {
        "name": "Twitter - Search Tweets",
        "description": "Search for tweets on Twitter/X",
        "keywords": ["search twitter", "find tweets", "twitter search", "trending"],
        "parameters": ["query", "limit"],
        "category": "social"
    },
    "notion_create": {
        "name": "Notion - Create Page",
        "description": "Create a new page in Notion",
        "keywords": ["notion", "create page", "new document", "add note"],
        "parameters": ["title", "content", "database_id"],
        "category": "productivity"
    },
    "notion_search": {
        "name": "Notion - Search Pages",
        "description": "Search for pages in Notion",
        "keywords": ["notion", "search", "find page", "lookup note"],
        "parameters": ["query"],
        "category": "productivity"
    },
    "trello_create": {
        "name": "Trello - Create Card",
        "description": "Create a new card in Trello board",
        "keywords": ["trello", "card", "task", "create task", "add card", "todo"],
        "parameters": ["board", "list", "title", "description"],
        "category": "productivity"
    },
    "trello_move": {
        "name": "Trello - Move Card",
        "description": "Move a card to different list in Trello",
        "keywords": ["trello", "move card", "update status", "change list"],
        "parameters": ["card_id", "target_list"],
        "category": "productivity"
    },
    "github_create_issue": {
        "name": "GitHub - Create Issue",
        "description": "Create a new issue in GitHub repository",
        "keywords": ["github", "issue", "bug", "report", "create issue"],
        "parameters": ["repo", "title", "body"],
        "category": "development"
    },
    "github_create_pr": {
        "name": "GitHub - Create Pull Request",
        "description": "Create a pull request in GitHub",
        "keywords": ["github", "pull request", "PR", "merge", "code review"],
        "parameters": ["repo", "title", "branch"],
        "category": "development"
    },
    "jira_create": {
        "name": "Jira - Create Ticket",
        "description": "Create a new ticket in Jira",
        "keywords": ["jira", "ticket", "issue", "bug", "story", "task"],
        "parameters": ["project", "type", "title", "description"],
        "category": "development"
    },
    "jira_update": {
        "name": "Jira - Update Ticket",
        "description": "Update an existing Jira ticket",
        "keywords": ["jira", "update ticket", "change status", "modify issue"],
        "parameters": ["ticket_id", "status", "comment"],
        "category": "development"
    },
    "weather_get": {
        "name": "Weather - Get Current",
        "description": "Get current weather for a location",
        "keywords": ["weather", "temperature", "forecast", "climate", "rain"],
        "parameters": ["location"],
        "category": "information"
    },
    "news_get": {
        "name": "News - Get Headlines",
        "description": "Get latest news headlines",
        "keywords": ["news", "headlines", "latest", "current events", "articles"],
        "parameters": ["category", "country"],
        "category": "information"
    },
    "translate_text": {
        "name": "Translate - Text Translation",
        "description": "Translate text from one language to another",
        "keywords": ["translate", "language", "convert", "translation"],
        "parameters": ["text", "source_lang", "target_lang"],
        "category": "utility"
    },
    "currency_convert": {
        "name": "Currency - Convert",
        "description": "Convert currency from one to another",
        "keywords": ["currency", "convert", "exchange rate", "money", "forex"],
        "parameters": ["amount", "from_currency", "to_currency"],
        "category": "utility"
    },
    "zoom_create": {
        "name": "Zoom - Create Meeting",
        "description": "Create a new Zoom meeting",
        "keywords": ["zoom", "meeting", "video call", "conference", "schedule zoom"],
        "parameters": ["title", "date", "time", "duration"],
        "category": "communication"
    },
    "spotify_play": {
        "name": "Spotify - Play Music",
        "description": "Play music or playlist on Spotify",
        "keywords": ["spotify", "play", "music", "song", "playlist", "listen"],
        "parameters": ["track", "playlist"],
        "category": "entertainment"
    },
    "dropbox_upload": {
        "name": "Dropbox - Upload File",
        "description": "Upload a file to Dropbox",
        "keywords": ["dropbox", "upload", "file", "backup", "store"],
        "parameters": ["file", "path"],
        "category": "storage"
    },
    "hubspot_create": {
        "name": "HubSpot - Create Contact",
        "description": "Create a new contact in HubSpot CRM",
        "keywords": ["hubspot", "contact", "crm", "lead", "customer"],
        "parameters": ["name", "email", "company"],
        "category": "crm"
    },
    "stripe_charge": {
        "name": "Stripe - Create Charge",
        "description": "Create a payment charge via Stripe",
        "keywords": ["stripe", "payment", "charge", "pay", "transaction"],
        "parameters": ["amount", "currency", "customer"],
        "category": "payment"
    },
    "sendgrid_send": {
        "name": "SendGrid - Send Email",
        "description": "Send transactional email via SendGrid",
        "keywords": ["sendgrid", "email", "send", "transactional", "mail"],
        "parameters": ["to", "subject", "body"],
        "category": "communication"
    }
}

def get_all_apis():
    return APIS

def get_api_by_id(api_id):
    return APIS.get(api_id)

def get_categories():
    categories = set()
    for api in APIS.values():
        categories.add(api["category"])
    return list(categories)

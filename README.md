# LinkedIn MCP Automation

An automated integration tool for LinkedIn using Playwright, designed to interface seamlessly with AI agents and Model Context Protocol (MCP) servers. 

This project provides programmatic access to LinkedIn actions (like creating posts with images, updating profiles, and searching for jobs) while maintaining the ability to include a "Human-in-the-Loop" approval process for safety.

## Features

- **Automated Post Creation**: Create LinkedIn posts automatically. Supports both text-only posts and posts with images.
- **Image Upload Support**: Programmatically intercepts LinkedIn's hidden file choosers to upload media.
- **Profile Updates**: Automates updating the "About" section of your LinkedIn profile.
- **Job Search Navigation**: Automates navigating to LinkedIn's Easy Apply job search pages based on keywords and location.
- **Persistent Sessions**: Uses Playwright's persistent context to save login cookies so you don't have to log in every time.
- **Human-in-the-loop (Optional)**: Can pop up a Tkinter dialog box to ask for user approval before making destructive actions (like clicking the final "Post" button).

## Prerequisites

- Python 3.8+
- [Playwright](https://playwright.dev/python/)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jsomil/linkedin_mcp.git
   cd linkedin_mcp
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. Install requirements and Playwright browsers:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## Usage

### 1. Creating a Post with an Image

You can use the provided script to draft and publish a post with an image:

```bash
python run_post_with_image.py
```

*Note: The first time you run this, a browser window will open and ask you to log in to LinkedIn. It will pause until you log in. Subsequent runs will use the saved session in the `playwright_data` folder.*

### 2. Using the Automation Class Programmatically

You can easily import the `automation` object into your own scripts or MCP Server:

```python
import asyncio
from linkedin_automation import automation

async def main():
    try:
        # Create a text post
        result = await automation.create_post(text="Hello from my AI Agent!")
        
        # Create a post with an image
        result2 = await automation.create_post(text="Look at this chart:", image_path="./chart.png")
        
        # Update Profile About section
        result3 = await automation.update_profile_about("I am a software engineer building AI agents.")
    finally:
        await automation.stop()

asyncio.run(main())
```

## Security & Privacy

**Important:** The `playwright_data` folder is automatically created when you run the script. It contains your live LinkedIn session cookies. **Never commit this folder to a public repository.** (It is excluded via `.gitignore` by default).

## License
MIT License

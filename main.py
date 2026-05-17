from mcp.server.fastmcp import FastMCP
from linkedin_automation import automation

mcp = FastMCP("LinkedIn Server")

@mcp.tool()
async def create_linkedin_post(content: str) -> str:
    """
    Creates a new post on your LinkedIn feed.
    Args:
        content: The text content of the post to create.
    """
    return await automation.create_post(content)

@mcp.tool()
async def update_profile_about(about_text: str) -> str:
    """
    Updates the 'About' section on your LinkedIn profile.
    Args:
        about_text: The new text for your About section.
    """
    return await automation.update_profile_about(about_text)

@mcp.tool()
async def search_and_open_jobs(keywords: str, location: str) -> str:
    """
    Navigates to the LinkedIn Jobs page configured for Easy Apply jobs matching the given keywords and location.
    Args:
        keywords: Job search keywords (e.g. 'Software Engineer').
        location: Job location (e.g. 'Remote' or 'San Francisco').
    """
    return await automation.apply_for_jobs(keywords, location)

if __name__ == "__main__":
    mcp.run(transport='stdio')

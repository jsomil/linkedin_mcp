import os
import asyncio
from playwright.async_api import async_playwright, BrowserContext, Page
import urllib.parse
import tkinter as tk
from tkinter import messagebox

async def async_ask_user_approval(title: str, message: str) -> bool:
    def _ask():
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        result = messagebox.askyesno(title, message)
        root.destroy()
        return result
    return await asyncio.to_thread(_ask)

USER_DATA_DIR = os.path.join(os.getcwd(), 'playwright_data')

class LinkedInAutomation:
    def __init__(self):
        self.playwright = None
        self.browser_context = None
        self._lock = asyncio.Lock()

    async def start(self):
        async with self._lock:
            if self.browser_context is not None:
                return
            self.playwright = await async_playwright().start()
            self.browser_context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,
                channel="chrome",
                args=["--start-maximized"],
                no_viewport=True
            )
            print("Browser context launched.")

    async def stop(self):
        if self.browser_context:
            await self.browser_context.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_page(self) -> Page:
        pages = self.browser_context.pages
        if pages:
            return pages[0]
        return await self.browser_context.new_page()

    async def check_login(self, page: Page):
        await page.goto("https://www.linkedin.com/feed/")
        if "/login" in page.url or "session_key" in await page.content():
            print("User needs to log in manually.")
            # Wait for user to navigate away from login
            while "/login" in page.url or "checkpoint/rm" in page.url:
                await asyncio.sleep(2)

    async def create_post(self, text: str, image_path: str = None) -> str:
        await self.start()
        page = await self.get_page()
        await self.check_login(page)
        
        await page.goto("https://www.linkedin.com/feed/")
        await page.wait_for_load_state("domcontentloaded")
        
        try:
            try:
                post_btn = page.locator("button:has-text('Start a post'), [role='button']:has-text('Start a post'), text='Start a post'").first
                await post_btn.wait_for(state="visible", timeout=15000)
                await post_btn.click()
            except Exception as e:
                # Fallback to URL-based modal opening
                await page.goto("https://www.linkedin.com/feed/?shareActive=true")
            
            editor = page.locator("div[role='textbox'], div.ql-editor").first
            await editor.wait_for(state="visible", timeout=30000)
            
            # If an image path is provided, handle the media upload first
            if image_path:
                try:
                    async with page.expect_file_chooser(timeout=10000) as fc_info:
                        await page.locator("button[aria-label*='Add media'], button[aria-label*='Add a photo']").first.click()
                    file_chooser = await fc_info.value
                    await file_chooser.set_files(image_path)
                    
                    # Wait for media preview to load, then click Next/Done in the modal
                    next_btn = page.locator("div[role='dialog'] button:has-text('Next'), div[role='dialog'] button:has-text('Done')").first
                    await next_btn.wait_for(state="visible", timeout=15000)
                    await next_btn.click()
                    await asyncio.sleep(2) # Buffer for modal to close and return to main editor
                except Exception as media_err:
                    print(f"Warning: Failed to attach media: {str(media_err)}")

            await editor.click()
            # Use Playwright's native fill command to bypass all keyboard/websocket event spam entirely
            await editor.fill(text)
            
            # The user requested to manually click post without being asked
            print("Post drafted successfully. Leaving browser open for 5 minutes so you can manually review and click Post.")
            await asyncio.sleep(300) # Leave open for 5 minutes
            return "Post drafted. Left open for 5 minutes for manual posting."
        except Exception as e:
            return f"Failed to create post. Error: {str(e)}"
            
    async def update_profile_about(self, about_text: str) -> str:
        await self.start()
        page = await self.get_page()
        await self.check_login(page)
        
        await page.goto("https://www.linkedin.com/in/")
        await page.wait_for_load_state("domcontentloaded")
        
        try:
            edit_about_btn = page.locator("button[aria-label='Edit about']").first
            await edit_about_btn.wait_for(state="visible", timeout=10000)
            await edit_about_btn.click()
            
            textarea = page.locator("textarea").first
            await textarea.wait_for(state="visible", timeout=5000)
            await textarea.fill(about_text)
            
            save_btn = page.locator("button:has-text('Save')").first
            
            approved = await async_ask_user_approval(
                "Approve Profile Update", 
                f"Do you want to update your About section to:\n\n{about_text}"
            )
            
            if approved:
                await save_btn.click()
                await asyncio.sleep(3)
                return "Successfully updated profile About section."
            else:
                return "User rejected the profile update action. Profile was not updated."
        except Exception as e:
            return f"Failed to update profile about section. Note: User must have an existing About section to edit. Error: {str(e)}"

    async def apply_for_jobs(self, keywords: str, location: str) -> str:
        await self.start()
        page = await self.get_page()
        await self.check_login(page)
        
        k = urllib.parse.quote(keywords)
        l = urllib.parse.quote(location)
        url = f"https://www.linkedin.com/jobs/search/?keywords={k}&location={l}&f_AL=true"
        await page.goto(url)
        await page.wait_for_load_state("domcontentloaded")
        
        return "Browser has navigated to targeted Easy Apply jobs page. We highly recommend proceeding with applications manually from this page to avoid spam filters and appropriately answer custom recruiter questions."

automation = LinkedInAutomation()

import asyncio
from linkedin_automation import automation

post_text = """Are you applying traditional system design to your AI projects? 

As we shift from single-prompt LLMs to autonomous, multi-agent systems, traditional architecture is getting a massive AI upgrade. I put together this quick cheat sheet on how core distributed system concepts translate to the world of Agentic AI. 

Let me know what you're building below! 👇

#SystemDesign #AgenticAI #MachineLearning #SoftwareArchitecture"""

# Path to the infographic generated earlier
image_path = r"./path/to/your/image.png"

async def main():
    try:
        print("Starting automated post with image...")
        result = await automation.create_post(text=post_text, image_path=image_path)
        print("Result:", result)
    finally:
        await automation.stop()

if __name__ == "__main__":
    asyncio.run(main())

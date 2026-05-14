import os
import discord
from discord.ext import commands
import google.generativeai as genai

# Fetch hidden tokens from Render's Environment settings
genai.configure(api_key=os.environ.get("GOOGLE_AI_KEY"))

# Define your bot's personality here
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are an AI called saturn, you help new players with what they need, if they ask for free kits, tell them to check the #free-kits channel.."
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot successfully launched as {bot.user.name}")

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Respond when someone tags/mentions the bot
    if bot.user.mentioned_in(message):
        clean_prompt = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '')
        
        async with message.channel.typing():
            try:
                response = model.generate_content(clean_prompt)
                await message.reply(response.text)
            except Exception as e:
                await message.reply("My cosmic signals are fading!")
                print(f"Error generating AI content: {e}")

# Retrieve the Discord token safely from the environment
token = os.environ.get("DISCORD_BOT_TOKEN")
if not token:
    print("CRITICAL ERROR: DISCORD_BOT_TOKEN environment variable is missing!")
else:
    bot.run(token)

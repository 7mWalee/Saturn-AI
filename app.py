import os
import discord
from discord.ext import commands
import google.generativeai as genai
from threading import Thread
from flask import Flask

# 1. DUMMY WEB SERVER TO KEEP THE FREE TIER ALIVE
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    # Render passes a PORT variable automatically
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. DISCORD BOT CONFIGURATION
genai.configure(api_key=os.environ.get("GOOGLE_AI_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are a helper for a 6b6t discord server, you help new players and guide them to the #free-kits channel if they ask for free kits."
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot successfully launched as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        clean_prompt = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '')
        async with message.channel.typing():
            try:
                response = model.generate_content(clean_prompt)
                await message.reply(response.text)
            except Exception as e:
                await message.reply("My cosmic signals are fading!")
                print(e)

# 3. RUN BOTH AT THE SAME TIME
if __name__ == "__main__":
    # Start web server in the background so Render free tier is happy
    t = Thread(target=run_web_server)
    t.start()
    
    # Start Discord Bot
    token = os.environ.get("DISCORD_BOT_TOKEN")
    bot.run(token)

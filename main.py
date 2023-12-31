import os
import discord
from discord.ext import commands, tasks
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

bot.load_extension("join")
# YouTube API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Replace 'YOUR_DISCORD_TOKEN' and 'YOUR_YOUTUBE_API_KEY' with your actual tokens
bot_token = os.getenv('DISCORD_TOKEN')
youtube_api_key = os.getenv('YOUTUBE_API_KEY')
channel_id = '1190696344684351498'  # Replace with the actual Discord channel ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    check_new_video.start()

@tasks.loop(minutes=1)
async def check_new_video():
    try:
        youtube = authenticate_youtube_api()
        latest_video = get_latest_video(youtube)

        if latest_video:
            video_title = latest_video['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={latest_video['snippet']['resourceId']['videoId']}"
            channel = bot.get_channel(int(channel_id))
            await channel.send(f"New video uploaded!\nTitle: {video_title}\nURL: {video_url}")

    except Exception as e:
        print(f"Error checking for new video: {e}")

def authenticate_youtube_api():
    credentials = None
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=credentials)

def get_latest_video(youtube):
    response = youtube.search().list(part='snippet', channelId='https://www.youtube.com/@ItsAlphaReturns', type='video', order='date', maxResults=1).execute()

    if 'items' in response:
        return response['items'][0]['snippet']
    else:
        return None

bot.run(bot_token)

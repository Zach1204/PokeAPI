from typing import Final 
import os 
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

#loads token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#pulls message from client
intents: Intents = Intents.default()
intents.message_content = True 
client: Client = Client(intents=intents)

#if message doesn't work with bit it wont pull anything
async def send_message(message: Message, user_message: str) -> None:
    if not user_message: print('empty') 

#if you put "?" before a pokemon name it will DM results
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

#connecting to discord bot
@client.event
async def on_ready() -> None:
    print('ready')

#displays results to a specific person in a specific channel
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user: return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

#runs bot
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()


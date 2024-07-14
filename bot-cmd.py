import discord
import asyncio
import pyfiglet
from pystyle import Center, Colors, Colorate


# Function to read bot tokens from a file
def read_bot_tokens(filename):
    with open(filename, 'r') as file:
        tokens = [line.strip() for line in file.readlines() if line.strip()]
    return tokens

# BOT_TOKENS set to bot tokens in 'bot-tokens.txt'
BOT_TOKENS = read_bot_tokens('bot-tokens.txt')
print(f'Loaded {len(BOT_TOKENS)} Bot Tokens!')

class Client(discord.Client):
    def __init__(self, *args, shared_params, counters, **kwargs):
        super().__init__(*args, **kwargs)
        self.shared_params = shared_params
        self.counters = counters
    
    async def on_ready(self):
        print(f'BOT LOGGED IN AND LOADED AS: {self.user}')
        choice = self.shared_params['choice']

        if choice == 1:
            await self.send_dm()
        elif choice == 2:
            await self.spam_channel_messages()
        elif choice == 3:
            await self.create_channel()
        elif choice == 4:
            await self.delete_all_channels()
        elif choice == 5:
            await self.send_message_all_channels()
        else:
            print("Invalid choice.")
        await self.close()

    async def send_dm(self):
        try:
            USER_ID = self.shared_params['USER_ID']
            MESSAGE = self.shared_params['MESSAGE']
            NUM_MESSAGES = self.shared_params['NUM_MESSAGES']
            PHOTO_URL = self.shared_params['PHOTO_URL']
            DELAY_TIME = self.shared_params['DELAY_TIME']

            user = await self.fetch_user(USER_ID)
            for _ in range(NUM_MESSAGES):
                if PHOTO_URL:
                    embed = discord.Embed(description=MESSAGE)
                    embed.set_image(url=PHOTO_URL)
                    await user.send(embed=embed)
                    print(f'{self.counters["messages"] + 1} Message & Photo sent to "{user}", check their reaction!')
                else:
                    await user.send(MESSAGE)
                    print(f'{self.counters["messages"] + 1} Message sent to "{user}"')
                self.counters["messages"] += 1
                await asyncio.sleep(DELAY_TIME)
        except discord.Forbidden:
            print(f'Cannot perform action due to lack of permissions.')
        except discord.HTTPException as e:
            print(f'Failed to perform action: {e}')

    async def spam_channel_messages(self):
        try:
            CHANNEL_ID = self.shared_params['CHANNEL_ID']
            MESSAGE = self.shared_params['MESSAGE']
            NUM_MESSAGES = self.shared_params['NUM_MESSAGES']
            PHOTO_URL = self.shared_params['PHOTO_URL']
            DELAY_TIME = self.shared_params['DELAY_TIME']

            guild = discord.utils.get(self.guilds, id=self.shared_params['guild_id'])
            if not guild:
                print(f"Guild with ID {self.shared_params['guild_id']} not found.")
                return

            channel = guild.get_channel(CHANNEL_ID)
            if not channel:
                print(f"Channel with ID {CHANNEL_ID} not found in guild.")
                return
            
            for _ in range(NUM_MESSAGES):
                if PHOTO_URL:
                    embed = discord.Embed(description=MESSAGE)
                    embed.set_image(url=PHOTO_URL)
                    await channel.send(embed=embed)
                    print(f'{self.counters["messages"] + 1} Message & Photo sent to channel "{channel.name}"')
                else:
                    await channel.send(MESSAGE)
                    print(f'{self.counters["messages"] + 1} Message sent to channel "{channel.name}"')
                self.counters["messages"] += 1
                await asyncio.sleep(DELAY_TIME)
        except discord.Forbidden:
            print(f'Cannot perform action due to lack of permissions!')
        except discord.HTTPException as e:
            print(f'Failed to perform action: {e}')

    async def create_channel(self):
        try:
            CHANNEL_NAME = self.shared_params['CHANNEL_NAME']
            CHANNEL_TYPE = self.shared_params['CHANNEL_TYPE']
            NUM_CHANNELS = self.shared_params['NUM_CHANNELS']

            guild = discord.utils.get(self.guilds, id=self.shared_params['guild_id'])
            if not guild:
                print(f"Guild with ID {self.shared_params['guild_id']} not found.")
                return
        
            for _ in range(NUM_CHANNELS):
                channel_name = f"{CHANNEL_NAME}" if NUM_CHANNELS > 1 else CHANNEL_NAME
                if CHANNEL_TYPE == "text":
                    await guild.create_text_channel(channel_name)
                    print(f'{self.counters["channels"] + 1} Text channel "{channel_name}" created successfully.')
                elif CHANNEL_TYPE == "voice":
                    await guild.create_voice_channel(channel_name)
                    print(f'{self.counters["channels"] + 1} Voice channel "{channel_name}" created successfully.')
                else:
                    print("Invalid channel type. Please enter 'text' or 'voice'!")
                    return
                self.counters["channels"] += 1
            print("Channel creation completed!")
        except discord.Forbidden:
            print(f'Cannot perform action due to lack of permissions!')
        except discord.HTTPException as e:
            print(f'Failed to perform action: {e}')

    async def delete_all_channels(self):
        try:
            guild = discord.utils.get(self.guilds, id=self.shared_params['guild_id'])
            if not guild:
                print(f"Guild with ID {self.shared_params['guild_id']} not found.")
                return

            channels = guild.channels
            for channel in channels:
                await channel.delete()
                print(f'{self.counters["channels_deleted"] + 1} Channel "{channel.name}" deleted successfully!')
                self.counters["channels_deleted"] += 1
            print("All channels deleted! xd GONE")
        except discord.Forbidden:
            print(f'Cannot perform action due to lack of permissions!')
        except discord.HTTPException as e:
            print(f'Failed to perform action: {e}')

    async def send_message_all_channels(self):
        try:
            guild = discord.utils.get(self.guilds, id=self.shared_params['guild_id'])
            if not guild:
                print(f"Guild with ID {self.shared_params['guild_id']} not found.")
                return

            channels = guild.text_channels
            MESSAGE = self.shared_params['MESSAGE']
            PHOTO_URL = self.shared_params['PHOTO_URL']
            DELAY_TIME = self.shared_params['DELAY_TIME']
            NUM_MESSAGES_PER_CHANNEL = self.shared_params['NUM_MESSAGES_PER_CHANNEL']

            for channel in channels:
                try:
                    for _ in range(NUM_MESSAGES_PER_CHANNEL):
                        if PHOTO_URL:
                            embed = discord.Embed(description=MESSAGE)
                            embed.set_image(url=PHOTO_URL)
                            await channel.send(embed=embed)
                            print(f'{self.counters["messages"] + 1} Message & Photo sent to channel "{channel.name}"')
                        else:
                            await channel.send(MESSAGE)
                            print(f'{self.counters["messages"] + 1} Message sent to channel "{channel.name}"')
                        self.counters["messages"] += 1
                        await asyncio.sleep(DELAY_TIME)
                except discord.Forbidden:
                    print(f'Cannot send message to channel "{channel.name}" due to lack of permissions!')
                except discord.HTTPException as e:
                    print(f'Failed to send message to channel "{channel.name}": {e}')
            print(f"All channels received {NUM_MESSAGES_PER_CHANNEL} messages each!")
        except discord.Forbidden:
            print(f'Cannot perform action due to lack of permissions!')
        except discord.HTTPException as e:
            print(f'Failed to perform action: {e}')
            

async def check_guild_exists(guild_id, bot_token):
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)
        try:
            await client.login(bot_token)
            guild = await client.fetch_guild(guild_id)
            await client.close()
            return guild is not None
        except discord.NotFound:
            await client.close()
            return False
        except Exception as e:
            await client.close()
            print(f"Error: {e}")
            return False

async def main():
        valid_guild = False
        guild_id = None
        while not valid_guild:
            try:
                guild_id = int(input("Enter Discord Server ID: "))
                for token in BOT_TOKENS:
                    valid_guild = await check_guild_exists(guild_id, token)
                    if valid_guild:
                        break   
                if not valid_guild:
                    print("Invalid server ID. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid server ID.")
        shared_params = {'guild_id': guild_id}
        counters = {"messages": 0, "channels": 0, "channels_deleted": 0}

        while True:
            text1 = "SIERRA IS A"
            figlet_text1 = pyfiglet.figlet_format(text1, font="5lineoblique")
            gradient_text1 = Colorate.Color(Colors.blue, figlet_text1, True)
            centered_text1 = Center.XCenter(gradient_text1)
            print(centered_text1)

            text2 = "TERRORIST"
            figlet_text2 = pyfiglet.figlet_format(text2, font="standard")
            gradient_text2 = Colorate.Color(Colors.red, figlet_text2, True)
            centered_text2 = Center.XCenter(gradient_text2)
            print(centered_text2)
            
            print(Center.XCenter("[0 For Exiting]"))
            print(Center.XCenter("[1 For Direct Messages]"))
            print(Center.XCenter("[2 For Text Channel Messages]"))
            print(Center.XCenter("[3 For Create Channels]"))
            print(Center.XCenter("[4 For Deleting All Channels]"))
            print(Center.XCenter("[5 For All Text Channel Messages]"))
            print("")
            print("Note: More Bot Tokens Multiply The Amount You Input!")
            choice = int(input("Choose an action: "))
            shared_params['choice'] = choice

            if choice == 0:
                break
            if choice == 1:
                shared_params['USER_ID'] = int(input("Enter the user ID to send messages to: "))
                shared_params['MESSAGE'] = input("Enter the message you want to send: ")
                shared_params['NUM_MESSAGES'] = int(input("Number of messages: "))
                shared_params['PHOTO_URL'] = input("Enter an Image Address to send (leave empty if no photo): ")
                shared_params['DELAY_TIME'] = float(input("Enter the delay between messages in seconds: "))
            elif choice == 2:
                shared_params['CHANNEL_ID'] = int(input("Enter the channel ID: "))
                shared_params['MESSAGE'] = input("Enter the message you want to spam: ")
                shared_params['NUM_MESSAGES'] = int(input("Number of messages: "))
                shared_params['PHOTO_URL'] = input("Enter an Image Address to send (leave empty if no photo): ").strip()
                shared_params['DELAY_TIME'] = float(input("Enter the delay between messages in seconds: "))
            elif choice == 3:
                shared_params['CHANNEL_NAME'] = input("Enter the new channel name: ")
                shared_params['CHANNEL_TYPE'] = input("Enter the type of the channel (text/voice): ").strip().lower()
                shared_params['NUM_CHANNELS'] = int(input("Number of channels: "))
            elif choice == 4:
                pass
            elif choice == 5:
                shared_params['MESSAGE'] = input("Enter the message you want to send to all text channels: ")
                shared_params['PHOTO_URL'] = input("Enter an Image Address to send (leave empty if no photo): ").strip()
                shared_params['DELAY_TIME'] = float(input("Enter the delay between messages in seconds: "))
                shared_params['NUM_MESSAGES_PER_CHANNEL'] = int(input("Enter number of messages per channel: "))
            else:
                print("Invalid choice.")
                continue

            # Initialize and run all BOT clients
            clients = [Client(intents=discord.Intents.default(), shared_params=shared_params, counters=counters) for _ in BOT_TOKENS]
            await asyncio.gather(*(client.start(token) for client, token in zip(clients, BOT_TOKENS)))

            counters = {"messages": 0, "channels": 0, "channels_deleted": 0}

            continue_choice = input("Continue? (Y/N): ").strip().lower()
            if continue_choice != 'y':
                print("Exiting the program. Goodbye! xD")
                break
    
asyncio.run(main())

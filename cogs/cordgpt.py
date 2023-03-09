import discord
from discord.ext import commands

import config as cfg # This is the config file

# Function to send a message to the chatbot and get a response
def send_message(message_log):
    # We use the OpenAI API to send the message to the chatbot
    response = openai.ChatCompletion.create(
        model=cfg.model,                # The model used to generate the response
        messages=message_log,           # The conversation history
        max_tokens=cfg.max_tokens,      # The maximum number of tokens to generate
        stop=cfg.stop,                  # The token to stop the response generation
        temperature=cfg.temperature,    # The temperature of the response generation
    )

    # We loop through the choices
    for choice in response.choices:
        if "text" in choice:
            # If the response contains text, we return it
            return choice.text

    # If the response doesn't contain text, we return the message content
    return response.choices[0].message.content


# We create a class for the CordGPT cog
class CordGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # When the bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        # We create a variable to store the conversation history
        global message_log
        message_log = []

        # We add the conversation settings to the conversation history
        message_log.append({"role": "system", "content": "You are CordGPT, a chatbot that answers questions from users on Discord."})

    # When a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        # We check if the message is not from the bot and if the channel name is "cordgpt"
        if message.author != self.bot.user and message.channel.name == "cordgpt":
            # We add the message to the conversation history
            message_log.append({"role": "user", "content": message.content})

            # We send the message to the chatbot and get a response
            response = send_message(message_log)

            # We add the response to the conversation history
            message_log.append({"role": "assistant", "content": response})

            # We send the response to the channel
            await message.channel.send(response)


# We add the cog to the bot
def setup(bot):
    bot.add_cog(CordGPT(bot))
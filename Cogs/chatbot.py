import os

from discord.ext import commands
import cohere

class Chatbot(commands.Cog, name = "link fixer"):
    def __init__(self, bot):
        self.api_key = os.getenv("AI_TOKEN")
        self.co = cohere.ClientV2(self.api_key)
        self.bot=bot

    async def ask_bot(self, prompt: str, response_length: int):
        try:
            msgs = [
                    {"role": f"system", "content": f"You are Doabot, a helpful assistant in a Discord channel. Only respond when directly mentioned with \"<@Doabot>\". Provide a response based on the entire conversation, DO NOT MENTION the user you respond to, its already in a reply. Type no more than {response_length} words if possible."},
                    {"role": "user", "content":prompt}
                ]
            output=self.co.chat(
                model = 'command-a-03-2025',
                messages =msgs,
                max_tokens=response_length,
                temperature=1
            )
            print(output)
            return output.message.content[0].text
        except Exception as e:
            print(e)
            return "An error has occurred while generating AI response"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.bot.user in message.mentions and self.bot.chatbot_on==True:
            prompt = """Conversation:"""
            messages = []
            async for msg in message.channel.history(limit=self.bot.bot_read_msg):
                messages.append(msg)
            for msg in reversed(messages):
                content = msg.content # sent message content
                for user_id in msg.raw_mentions: # list of user ids to check with content, raw_mentions works is only userid without <@>
                    member = message.guild.get_member(user_id) or await message.guild.fetch_member(user_id) # caches member based on userid in mentions
                    mention_tag = f"<@{user_id}>" #mention tag for replacement
                    content = content.replace(mention_tag, f"<@{member.name}>") # checks for tag and replaces it with name
                prompt+=f"{msg.author.name}: {content}\n"
            prompt+="Your response: \nDoabot:"
            print(prompt)
            async with message.channel.typing(): # makes bot appear as he is typing a response in chat
                response = await self.ask_bot(prompt, response_length=len(prompt)+self.bot.bot_max_tokens)
                await message.reply(response, mention_author=True)
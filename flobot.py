import discord
import pickle
import sys
import random
TOKEN = pickle.load(open('flo_token.pkl','rb')) #not gonna show my token to ya :)

class FloBot(discord.Client):

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
   
    async def on_message(self, message):
        joe = 803676742639550544

        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        mention = "@"+str(self.user.id)
        if message.author.id == joe and '#terminate' in message.content and mention in message.content:
            await message.reply('Emergency termination.')
            sys.exit()

        if message.content.lower().startswith("!add "):
            print(message.content)
            sentence = message.content.lstrip('!add ')
            with open("sentences.txt",'a') as f:
                f.write(sentence+'\n')
            return await message.reply("Added new line.")
        
        if message.content.lower().startswith('!draw'):
            with open("sentences.txt","r") as f:
                sentences = f.read().split('\n')[:-1]
            repl = "Drawn:\n"+random.choice(sentences)
            return await message.author.send(repl)
        
        if message.content.lower().startswith('!list'):
            with open("sentences.txt","r") as f:
                sentences = f.read().split('\n')[:-1]
            repls = []
            for i,sentence in enumerate(sentences):
                repls.append(f"{i+1}. {sentence}\n")

            msg_l = 0
            msg = ""
            for repl in repls:
                msg_l += len(repl)
                if msg_l > 2000:
                    await message.reply(msg)
                    msg_l = 0
                    msg = repl
                    continue
                msg += repl
            if msg == "":
                return
            
            return await message.reply(msg)
        
        if message.content.lower().startswith('!undo'):
            with open("sentences.txt","r") as f:
                sentences = f.read().split('\n')[:-1]
            sentences.pop(-1)
            with open("sentences.txt","w") as f:
                for s in sentences:
                    f.write(s+'\n')
            return await message.reply("Deleted last line.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = FloBot(intents=intents)
client.run(TOKEN)
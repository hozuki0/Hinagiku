import discord
import random

doseisasnn_user_name = 'doseisann'

class HinagikuClient(discord.Client):
    async def on_ready(self):
        print('Login')
        for n in self.get_all_members():
            if n.name == doseisasnn_user_name:
                self.doseisann = n

    async def on_message(self, message):
        if message.author == self.doseisann:
            if random(1):
                return
        if '下' in message.content or 'した' in message.content:
            await message.channel.send('UD!')


def random(boarder,max = 3):
    return random.randint(0,max) <= boarder

def main():
    token = ''
    # 外部からトークンを読み込む
    with open('token.tk') as f:
        token = f.read().strip()
    client = HinagikuClient()
    client.run(token)


if __name__ == '__main__':
    main()

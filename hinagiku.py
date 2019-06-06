import discord
import random

doseisasnn_user_name = 'doseisann'
debug_room_name = 'yuppibot-debug'


class HinagikuClient(discord.Client):
    async def on_ready(self):
        print('Login')
        for n in self.get_all_members():
            if n.name == doseisasnn_user_name:
                self.doseisann = n
        for channel in self.get_all_channels():
            if channel.name == debug_room_name:
                self.target_channel = channel

    async def on_message(self, message):
        # 発言者がdoseisannの時一定確率で無視する
        if message.author == self.doseisann:
            if random(1):
                return
        # UD機能
        if '下' in message.content or 'した' in message.content or 'sita' in message.content.lower():
            await self.target_channel.send('UD!')


def random(boarder, max=3):
    return random.randint(0, max) <= boarder


def main():
    token = ''
    # 外部からトークンを読み込む
    with open('token.tk') as f:
        token = f.read().strip()
    client = HinagikuClient()
    client.run(token)


if __name__ == '__main__':
    main()

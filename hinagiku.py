import discord
import random
import asyncio
import time

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

        self.said_ecc_opening = False
        self.said_ecc_closing = False
        self.kagisime_ozisann = False
        asyncio.ensure_future(self.schedule_pending())

    async def on_message(self, message):
        # 発言者がdoseisannの時一定確率で無視する
        if message.author == self.doseisann:
            if random(1):
                return
        # UD機能
        if '下' in message.content or 'した' in message.content or 'sita' in message.content.lower():
            await self.target_channel.send('UD!')
        
        if message.content.lower() == 'yukitterの真似して':
            await self.target_channel.send('' ,file=discord.File('./Resource/gone.jpg'))

    async def on_ecc_state_changed(self, message):
        await self.target_channel.send(message)

    async def schedule_pending(self):
        while True:
            # 毎朝05:30と20:45をスケジュールして関数を発行する
            time_formatted_str = time.strftime('%H:%M', time.localtime())
            if not self.said_ecc_opening and time_formatted_str == '05:30':
                await self.target_channel.send('ECCの門が開きだす...')
                self.said_ecc_opening = True
            if not self.said_ecc_closing and time_formatted_str == '20:45':
                await self.target_channel.send('ECCの門が閉まりだす...')
                self.said_ecc_closing = True
            if not self.kagisime_ozisann and time_formatted_str == '19:55':
                await self.target_channel.send('もうここだけやから!もうここだけやから!!')
                self.kagisime_ozisann = True

            if time_formatted_str == '12:00':
                self.said_ecc_opening = False
                self.said_ecc_closing = False
                self.kagisime_ozisann = False
            await asyncio.sleep(10)


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

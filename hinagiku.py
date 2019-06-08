import discord
import random
import asyncio
import time
import date_ext
import datetime

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
        self.is_drinking = False
        self.drinking_time_end = None
        self.gerotter_counter = 0
        self.GERO_LIMIT = 3
        asyncio.ensure_future(self.schedule_pending())

    async def on_message(self, message):
        # 発言者がdoseisannの時一定確率で無視する
        if message.author == self.doseisann:
            if random(1):
                return
        # UD機能
        if '下' in message.content or 'した' in message.content or 'sita' in message.content.lower():
            await self.target_channel.send('UD!')

        # Yukitterモード
        if message.content.lower() == 'yukitterの真似して':
            if self.is_gerotter_mode():
                self.gerotter_counter += 1
                if self.gerotter_counter > self.GERO_LIMIT:
                    self.gerotter_counter = 0
                    await self.target_channel.send('ｺﾞﾒﾝ', file=discord.File('./Resource/gerotter.jpg'))
                else:
                    urtla = ''
                    for n in range(self.gerotter_counter):
                        urtla += 'ﾍｱｯ'
                    await self.target_channel.send(urtla)
            else:
                await self.target_channel.send('', file=discord.File('./Resource/gone.jpg'))

        if self.is_drinking_mode_message(message.content, message.mentions):
            self.is_drinking = True
            self.drinking_time_end = datetime.datetime.now() + datetime.timedelta(minutes=30)
            await self.target_channel.send("debug:泥酔タイム開始")

        if self.is_drinking and self.is_drinking_stop_message(message.content, message.mentions):
            self.is_drinking = False
            self.drinking_time_end = None
            await self.target_channel.send("debug:泥酔タイム終了")

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

            if self.is_drinking and datetime.datetime.now() > self.drinking_time_end:
                self.drinking_time_end = None
                self.is_drinking = False
                await self.target_channel.send("debug:泥酔タイム終了")
            await asyncio.sleep(10)

    def is_gerotter_mode(self):
        return date_ext.is_friday_night() or self.is_drinking

    def is_drinking_mode_message(self, message, mention):
        return ('酒' in message or '飲' in message) and self.user in mention

    def is_drinking_stop_message(self, message, mention):
        return ('ポカリ' in message or 'アクエリ' in message or 'スポドリ' in message or 'スポーツドリンク' in message) and self.user in mention


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

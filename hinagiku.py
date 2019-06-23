import discord
import random
import asyncio
import time
import date_ext
import datetime
import dice_roll
from line_loader import line_loader as ll
import is_xxx

doseisasnn_user_name = 'doseisann'
debug_room_name = 'yuppibot-debug'


class HinagikuClient(discord.Client):
    async def on_ready(self):
        self.line_arch = ll('./line.json')
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
        if message.author == self.doseisann:
            if check_doseisann(3, max=10):
                await self.target_channel.send(
                    self.line_arch.search('4doseisan'))
                # return

        if self.line_arch.search('sita-kanji') in message.content \
                or self.line_arch.search('sita-hiragana') in message.content \
                or self.line_arch.search('sita-kana') in message.content \
                or self.line_arch.search('sita') in message.content:
            await self.target_channel.send('UD!')

        if message.content.lower() == self.line_arch.search('yukitter-mimick'):
            if self.is_gerotter_mode():
                self.gerotter_counter += 1
                if self.gerotter_counter > self.GERO_LIMIT:
                    self.gerotter_counter = 0
                    await self.target_channel.send(
                        self.line_arch.search('sorry'),
                        file=discord.File('./Resource/gerotter.jpg'))
                else:
                    urtla = ''
                    for n in range(self.gerotter_counter):
                        urtla += self.line_arch.search('ultraman')
                    await self.target_channel.send(urtla)
            else:
                await self.target_channel.send('',
                                               file=discord.File(
                                                   './Resource/gone.jpg'))

        if self.is_drinking_mode_message(message.content, message.mentions):
            self.is_drinking = True
            self.drinking_time_end = datetime.datetime.now()
            + datetime.timedelta(minutes=30)
            await self.target_channel.send("debug:start drinking")

        if self.is_drinking and self.is_drinking_stop_message(
                message.content, message.mentions):
            self.is_drinking = False
            self.drinking_time_end = None
            await self.target_channel.send("debug:stop drinking")

        if dice_roll.is_dice_roll(message.content):
            dice_info = dice_roll.parse_dice(message.content)
            parsed_dice = dice_roll.parse_dice_info(dice_info[0])

            dice_result = dice_roll.execute_dice_roll(parsed_dice)
            operator_result = dice_roll.ev_operator(dice_result, dice_info[1])
            comparison_result = dice_roll.ev_comparison_expression(
                operator_result, dice_info[2])

            result_message = dice_roll.create_result_message(
                operator_result, dice_info[2], comparison_result)
            if dice_info[3] != '':
                dice_info[3] += ' '
            await self.target_channel.send(message.author.mention + ' ' +
                                           dice_info[3] + result_message)

        if is_xxx.is_isXXX_format(message.content):
            await self.target_channel.send(message.author.mention + ' ' +
                                           is_xxx.create_reply(
                                               message.content))

    async def on_ecc_state_changed(self, message):
        await self.target_channel.send(message)

    async def schedule_pending(self):
        while True:
            time_formatted_str = time.strftime('%H:%M', time.localtime())
            if not self.said_ecc_opening and time_formatted_str == '05:30':
                await self.target_channel.send(
                    self.line_arch.search('open-ecc'))
                self.said_ecc_opening = True
            if not self.said_ecc_closing and time_formatted_str == '20:45':
                await self.target_channel.send(
                    self.line_arch.search('close-ecc'))
                self.said_ecc_closing = True
            if not self.kagisime_ozisann and time_formatted_str == '19:55':
                await self.target_channel.send(
                    self.line_arch.search('kagisime'))
                self.kagisime_ozisann = True

            if time_formatted_str == '12:00':
                self.said_ecc_opening = False
                self.said_ecc_closing = False
                self.kagisime_ozisann = False

            if self.is_drinking \
                    and datetime.datetime.now() > self.drinking_time_end:
                self.drinking_time_end = None
                self.is_drinking = False
                await self.target_channel.send("debug:stop drinking")
            await asyncio.sleep(10)

    def is_gerotter_mode(self):
        return date_ext.is_friday_night() or self.is_drinking

    def is_drinking_mode_message(self, message, mention):
        return (self.line_arch.search('sake') in message
                or self.line_arch.search('nomu') in message) \
            and self.user in mention

    def is_drinking_stop_message(self, message, mention):
        return (self.line_arch.search('pokari') in message
                or self.line_arch.search('akueri') in message
                or self.line_arch.search('spordori') in message
                or self.line_arch.search('sportdrink') in message) \
            and self.user in mention


def check_doseisann(boarder, max=3):
    return random.randint(0, max) <= boarder


def main():
    token = ''
    with open('token.tk') as f:
        token = f.read().strip()
    client = HinagikuClient()
    client.run(token)


if __name__ == '__main__':
    main()

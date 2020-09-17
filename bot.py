import discord
import asyncio
import json
import aiohttp
import async_timeout
import os

client = discord.Client()
loop = asyncio.get_event_loop()
TOKEN = os.environ['DISCORD_TOKEN']


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="「d.help」でヘルプ", type=1))
    print('ready')


@client.event
async def on_message(message):
    if message.content == 'd.help':
        embed = discord.Embed(title='ヘルプ', color=discord.Color.blue())
        embed.add_field(name='d.status', value="Discordの全サーバーのステータスを表示します。\nSend discord's server status.")
        embed.add_field(name='d.ping', value='Discord(API)の現在のPingを表示します。\nSend discord ping.')
        embed.add_field(name='d.vc', value="このサーバーのVCのPINGを表示します。\nSend this server's region ping.")
        embed.add_field(name='d.invite', value='このBotの招待リンクを送信します。\nSend invite link of this Bot.')
        await message.channel.send(embed=embed)
        return
    elif message.content == 'd.invite':
        await message.channel.send('こちらが招待リンクです。\nInvite link:\n'
                                   'https://discord.com/api/oauth2/authorize?client_id=756102269082271746&permissions=281664&scope=bot')
        return
    elif message.content == 'd.ping':
        r = await request(url='https://discordstatus.com/metrics-display/ztt4777v23lf/day.json')
        request_dict = json.loads(r)
        latency = request_dict['metrics'][0]['data'][-1]['value']
        await message.channel.send('Ping:___**' + str(latency) + 'ms**___')
        return
    elif message.content == 'd.status':
        r = await request(url='https://srhpyqt94yxb.statuspage.io/api/v2/summary.json')
        request_dict = json.loads(r)
        embed = discord.Embed(title='status.discord.com', color=discord.Color.blue())
        for val in request_dict['components']:
            name = val['name']
            status = val['status']
            embed.add_field(name=name, value=status)
        await message.channel.send(embed=embed)
        return
    elif message.content == 'd.vc':
        r = await request(url='https://srhpyqt94yxb.statuspage.io/api/v2/summary.json')
        status = "取得できませんでした\nError: couldn't get the data."
        vc_status = ''
        request_dict = json.loads(r)
        for val in request_dict['components']:
            name = val['name']
            if name.lower() == str(message.guild.region).lower():
                status = val['status']
            elif name == 'Voice':
                vc_status = val['status']
        embed = discord.Embed(title='Region：' + str(message.guild.region), color=discord.Color.blue())
        embed.add_field(name='Status', value=status)
        embed.add_field(name='Voice', value=vc_status)
        await message.channel.send(embed=embed)
        return


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def request(url):
    async with aiohttp.ClientSession() as session:
        body = await fetch(session, url)
        return body

client.run(TOKEN)

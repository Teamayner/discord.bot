import discord
import asyncio
from random import randint
from discord.ext import commands
from discord.ui import Button, button, View
from pymongo import MongoClient

intents = discord.Intents.default()
intents.message_content = True
token = "MTI2NTc4MjE1MzM3NTkxMjAxNg.GpOTeN.hilSDWNq-zoRMA_kqY0xhqldKJ53SxmAR_mE5Y"
bot = commands.Bot(command_prefix='!', intents=intents)
PREFIX = '!'
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} зашел на сервер")


@bot.command()
async def random(ctx):
    embed = discord.Embed(
        title=f"Рандомное число - {randint(0, 100000)}",
    )
    await ctx.send(f"🚨 Число может закачиваться до 100000, удачи вам его выбить :)", embed=embed)


@bot.command()
async def server(ctx):
    embed = discord.Embed(title=f"ℹ️ Информация о {ctx.guild.name}", description=f'🆔 Сервера: {ctx.guild.id}', color=discord.Colour.blue())
    embed.add_field(name='📊 Дата сервера', value=ctx.guild.created_at.strftime("%b %d %Y"), inline=True)
    embed.add_field(name='👑 Король', value='<@981119882206789642>', inline=True)
    embed.add_field(name='👤 Участники:', value=f'Всего: {ctx.guild.member_count}', inline=True)
    embed.set_image(
        url='https://media.discordapp.net/attachments/1113878474223005878/1267569764763566170/2598561.jpg?ex=66a943d6&is=66a7f256&hm=58a25e5389dfbfeb78849236565d240a8a3157655008f3bee6fc69a4673c7ce6&=&format=webp&width=908&height=676')
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1113878474223005878/1267568155291685024/8h13Fi.png?ex=66a94256&is=66a7f0d6&hm=9e67a760891b3160c47b97dba0f85f1ac6f7310b695701d7aefa199a8853f5e5&=&format=webp&quality=lossless&width=676&height=676')
    embed.add_field(name='🔰 Роли', value=f'<@&1266450919243911343> \n <@&1266451891559338004> \n <@&1267530150761861191>', inline=True)
    embed.add_field(name='💬 Каналы', value=f'Всего: 3 \n Текстовые: 2 \n Голосовые: 1', inline=True)
    embed.add_field(name='🔸 Бусты', value=f' Количество: 0', inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None, amount=1):
    await ctx.channel.purge(limit=int(amount))
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} был кикнут по причине {reason}')


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None, amount=1):
    if await ctx.channel.purge(limit=int(amount)):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} был забанен по причине: {reason}')
    else:
        await ctx.send("Вы не можете забанить самого себя", delete_after=2)


@bot.command()
async def clear(ctx):
    await ctx.channel.purge(limit=None)


@bot.command()
async def help(ctx):
    emb = discord.Embed(title='Все команды', color=discord.Colour.blue())
    emb.add_field(name='{}clear'.format(PREFIX), value='Очистка чата')
    emb.add_field(name='/ban', value='Банит участника за какую либо причину')
    emb.add_field(name='/kick', value='Кикает участника из сервера')
    emb.add_field(name='/timeout', value='Замьючен на какое то время')
    emb.add_field(name='{}server'.format(PREFIX), value='Информация о сервере')
    emb.add_field(name='{}random'.format(PREFIX), value='Рандомное число')
    emb.add_field(name='{}user @username'.format(PREFIX), value='Информация об участнике')
    emb.add_field(name='{}avatar @username'.format(PREFIX), value='Аватарка участника')
    await ctx.send(embed=emb)


@bot.command()
async def user(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    roles = [role for role in member.roles]
    embed = discord.Embed(title=f"Информация о {member.name}", color=discord.Colour.blue())
    embed.set_thumbnail(url=member.avatar)
    embed.set_image(url=member.banner)
    embed.add_field(name="ID участника", value=member.id, inline=True)
    embed.add_field(name="Ник", value=member.display_name, inline=True)
    embed.add_field(name="Создал аккаунт", value=member.created_at.strftime(f"%d.%m.%Y \n %H:%M:%S"), inline=True)
    embed.add_field(name="Зашел на сервер", value=member.joined_at.strftime(f"%d.%m.%Y \n %H:%M:%S"), inline=True)
    embed.add_field(name="Роли", value=f"\n".join(role.mention for role in roles), inline=True)
    embed.add_field(name="Статус", value=f'🔰 {member.status}', inline=True)
    await ctx.send(embed=embed)


class Timeout(commands.Cog):
    def __init__(self):
        self.bot = bot


@bot.command()
async def timeout(interaction, member: discord.Member, time: int, reason: str):
    time = datetime.datetime.now() + datetime.timedelta(minutes=time)
    await member.timeout(until=time, reason=reason)
    await interaction.response.send_message(
        f"Пользователь {member.mention} был замьючен до {time.strftime('%H:%M:%S %d.%m.%Y')}",
        ephemeral=True
    )


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f'Аватарка {member.name}', color=discord.Colour.blue())
    embed.set_image(url=member.avatar)
    await ctx.send(embed=embed)
bot.run(token)

import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import random
import time

client = commands.Bot(command_prefix='!')

#initializing all the variables
@client.event
async def on_ready():
    print('Ready')
            
#keeping logs of messages that were deleted
@client.event
async def on_message_delete(message):
    channel = client.get_channel('channel id here')
    serverName = message.author.display_name
    discordName = message.author
    textChannel = message.channel
    if message.author.bot == True:
        return
    else:
        if message.attachments == []:
            embedVar = discord.Embed(description=f'{serverName} ({discordName})' +
                                    f' | #{textChannel}\n{message.content}',
                                     color=0x6699ff)
            embedVar.set_footer(text=message.created_at)
            await channel.send(embed=embedVar)

        elif message.content != '':
            embedVar = discord.Embed(description=f'{serverName} ({discordName})' +
                                    f' | #{textChannel}\n{message.content}' +
                                    f'{message.attachments[0].url}', color=0x6699ff)
            embedVar.set_footer(text=message.created_at)
            await channel.send(embed=embedVar)

        else:
            embedVar = discord.Embed(description=f'{serverName} ({discordName})' +
                                    f' | #{textChannel}\n{message.attachments[0].url}',
                                     color=0x6699ff)
            embedVar.set_footer(text=message.created_at)
            await channel.send(embed=embedVar)
                        
#searches for an anime on myanimelist.net through a google search    
@client.command()
async def mal(ctx, *, args):
    channel = client.get_channel('channel id here')
    query = 'myanimelist {}'.format(args)
    if list(search(query, tld='com', num=1, stop=1, pause=2)) == []:
        embedVar = discord.Embed(description='No results found.',
                                         color=0x6699ff)
        await channel.send(embed=embedVar)

    else:
        for a in search(query, tld='com', num=1, stop=1, pause=2):
            if a[: 30] == 'https://myanimelist.net/anime/':
                await channel.send(a)
            else:
                embedVar = discord.Embed(description='Anime cannot be found.',
                                         color=0x6699ff)
                await channel.send(embed=embedVar)

#takes in a summoner name for an argument and links their op.gg
@client.command()
async def opgg(ctx, *, args):
    channel = client.get_channel('channel id here')
    summonerName = args.replace(' ','+')
    URL = 'https://na.op.gg/summoner/userName={}'.format(summonerName)
    await channel.send(URL)

#links reverse sakura fish image on command
@client.command()
async def sakurafish(ctx):
    channel = client.get_channel('channel id here')
    image = discord.Embed()
    image.set_image(url='https://cdn.discordapp.com/attachments/' +
                    '738140134184058935/738666767366357032/sakurafishreverse.jpg')
    await channel.send(embed=image)

#gives the sauce by pulling a random integer
@client.command()
async def sauce(ctx):
    value = random.randint(1, 322824)
    await ctx.send(value)

#takes in a tag as an argument and searches for images on zerochan. compiles
    #images from the top 3 pages and selects a random one
#i do not own any of these images and all credit goes to their respective artist
@client.command()
async def zerochan(ctx, *, args):
    try:
        tags = args.replace(' ', '+')
        consolidatedList = []
        for page in range(1,4):
            URL = f'https://www.zerochan.net/{tags}?s=fav&p={page}'
            imagePage = requests.get(URL)
            htmlImages = BeautifulSoup(imagePage.content, 'html.parser')
            imageList = htmlImages.find(id='thumbs2')
            for image in imageList.find_all('a', href=True):
                if image['href'][0] == '/':
                    pass
                else:
                    consolidatedList.append(image['href'])

        listLength = len(consolidatedList)
        randomValue = random.randint(0, (listLength - 1))
        imageURL = consolidatedList[randomValue]
        scrapedImage = discord.Embed()
        scrapedImage.set_image(url=imageURL)
        await ctx.send(embed=scrapedImage)
        
    except AttributeError:
        embedVar = discord.Embed(description='Something unexpected occurred.' +
                                 'Try something else.', color=0x6699ff)
        await ctx.send(embed=embedVar)

@client.command()
async def nyanpasu(ctx):
    gif = discord.Embed()
    gif.set_image(url='https://i.imgur.com/orLJSg3.gif')
    await ctx.send(embed=gif)
    
@client.command()
async def happyday(ctx):
    await ctx.send('pls rember when u feel scare or frigten')
    time.sleep(1)
    await ctx.send('never forget ttimes wen u feeled happy')
    time.sleep(1)
    await ctx.send('wen day is dark alway rember happy day')
    image = discord.Embed()
    image.set_image(url='https://i.redd.it/37xklm648v931.png')
    time.sleep(1)
    await ctx.send(embed=image)
    
#insert token here
client.run('Discord Token here')

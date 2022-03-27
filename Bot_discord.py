from gettext import translation
from itertools import count
import discord
from discord.ext import commands
import requests
import random
from googletrans import Translator, constants
from pprint import pprint
bot = commands.Bot(command_prefix="!", description="Bot pour récuperer aléatoirement un anime sur kitsu")
client = discord.Client()
@bot.event
async def on_ready():
    print("The bot is ready !")
kitsu_api = "https://kitsu.io/api/edge/library-entries?fields%5Banime%5D=slug%2CposterImage%2CcanonicalTitle%2Ctitles%2Cdescription%2Csubtype%2CstartDate%2Cstatus%2CaverageRating%2CpopularityRank%2CratingRank%2CepisodeCount&fields%5Busers%5D=id&filter%5Buser_id%5D=     Your user ID here      &filter%5Bkind%5D=anime&filter%5Bstatus%5D=planned&include=anime%2Cuser%2CmediaReaction&page%5Boffset%5D=0&page%5Blimit%5D=500&sort=-progressed_at"
r = requests.get(kitsu_api).json()
@bot.command()
async def kitsu(ctx):
    i = random.randint(1, len(r["included"])-1)
    titre = r["included"][i]["attributes"]["canonicalTitle"]
    ima = r["included"][i]["attributes"]["posterImage"]["original"]
    descr = r["included"][i]["attributes"]["description"]
    nb_episode = r["included"][i]["attributes"]["episodeCount"]
    rating = r["included"][i]["attributes"]["averageRating"]
    popularity = r["included"][i]["attributes"]["popularityRank"]
    status = r["included"][i]["attributes"]["status"]
    date = r["included"][i]["attributes"]["startDate"]
    kilink = "https://kitsu.io/anime/" + r["included"][i]["id"]
    #trad = Translator()
    #translation = trad.translate(descr,scr="en",dest="fr")     
    #You can change the translated description in all language availabel in google translate For exemple change the dest value to "de" to have translation in deutsch
    #print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
    embed = discord.Embed(title=titre, url=kilink ,description=translation.text,color=0xFF5733)
    embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ima)
    embed.add_field(name="Number of episodes :" , value=nb_episode, inline=True)
    embed.add_field(name="Score on 100 :" , value=rating, inline=True)
    embed.add_field(name="Popularity :" , value=popularity, inline=True)
    embed.add_field(name="Status :" , value=status, inline=True)
    embed.add_field(name="Release date :" , value=date, inline=True)
    embed.set_footer(text="Request sent by :  {}".format(ctx.author.display_name))
    await ctx.message.delete()
    await ctx.send(embed=embed)
bot.run("tokken key")
import discord
from discord.ext import commands
import pronotepy
from config import key
from Data.databasehadler import DatabaseHandler
from datetime import *

database_handler = DatabaseHandler("pathfinder_data.db", key)

class Pronote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        bot = self.bot
        for guild in bot.guilds:
            for member in guild.members:
                if member.bot:
                    return
                check_in_data = database_handler.check_data(member.id)
                if check_in_data is False:
                    database_handler.user_init(member.id)
                    print(f"Nouvel utilisateur enregistré {member.name} avec l'id {member.id}")
                else: 
                    print(f"Utilisateur déjà enregistré {member.name} avec l'id {member.id}")
    @discord.slash_command(name="pronote", description="Connectez-vous à Pronote")
    async def connexion_command(self, ctx, utilisateur: str, mdp: str, url: str):
        try:
            client = pronotepy.Client(url, utilisateur, mdp)
            if client.is_logged_in:
                database_handler.add_user(ctx.author.id, utilisateur, mdp, url)
                await ctx.send("Connexion réussie et informations stockées.", ephemeral=True)
            else:
                await ctx.send("Échec de la connexion. Vérifiez vos identifiants.", ephemeral=True)
        except Exception as e:
            await ctx.send(f"Erreur lors de la connexion : {e}", ephemeral=True)

    @discord.slash_command(name="devoir", description="Voir les devoirs des 7 prochains jours")
    async def devoirs_command(self, ctx):
        user_info = database_handler.get_user_info(ctx.author.id)
        if user_info:
            utilisateur, mdp, url = user_info
            client = pronotepy.Client(url, utilisateur, mdp)
            if client.is_logged_in:
                homework = client.homework()
                message = "\n".join([f"{hw.date}: {hw.subject} - {hw.description}" for hw in homework])
                await ctx.send(message, ephemeral=True)
            else:
                await ctx.send("Impossible de se connecter à Pronote.", ephemeral=True)
        else:
            await ctx.send("Vous n'êtes pas connecté. Utilisez /connexion pour vous connecter.", ephemeral=True)

    @discord.slash_command(name="emploie-du-temps", description="Voir le planning de la semaine")
    async def planning_command(self, ctx):
        user_info = database_handler.get_user_info(ctx.author.id)
        if user_info:
            utilisateur, mdp, url = user_info
            client = pronotepy.Client(url, utilisateur, mdp)
            if client.is_logged_in:
                timetable = client.timetable()
                message = "\n".join([f"{lesson.start}: {lesson.subject} avec {lesson.teacher}" for lesson in timetable])
                await ctx.send(message, ephemeral=True)
            else:
                await ctx.send("Impossible de se connecter à Pronote.", ephemeral=True)
        else:
            await ctx.send("Vous n'êtes pas connecté. Utilisez /connexion pour vous connecter.", ephemeral=True)

def setup(bot):
    bot.add_cog(Pronote(bot))

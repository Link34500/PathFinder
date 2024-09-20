import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @discord.slash_command(name="mute", description="Commande pour les modérateurs permettant de mute un utilisateur")
    @has_permissions(moderate_members=True) 
    async def mute(self, ctx, member: discord.Member, duration: int, *, reason=None):
        """
        Rendre muet un utilisateur en utilisant l'exclusion (timeout) native de Discord.
        
        Parameters:
        - member : Le membre à rendre muet.
        - duration : Durée de l'exclusion en minutes.
        - reason : La raison de l'exclusion.
        """

        if member == ctx.author:
            return await ctx.send("Vous ne pouvez pas vous rendre muet vous-même.")
        
        if duration > 60:
            await ctx.respond("Vous ne pouvez pas mute + de 60 minutes")
            return

        mute_duration = timedelta(minutes=duration)
        
      
        await member.timeout_for(mute_duration, reason=reason)
        await ctx.respond(f"{member.mention} a été rendu muet pendant {duration} minutes pour : {reason}")


    @discord.slash_command(name="unmute", description="Commande pour les modérateurs permettant de unmute un utilisateur")
    @has_permissions(moderate_members=True)  
    async def unmute(self, ctx, member: discord.Member):
        """
        Annuler l'exclusion (timeout) d'un utilisateur.
        
        Parameters:
        - member : Le membre à démuter.
        """
        
        await member.timeout(None)
        await ctx.respond(f"{member.mention} a été démuté.")

    # Gestion des erreurs pour la commande mute
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("Vous n'avez pas la permission de rendre muet un membre.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Veuillez fournir un membre et une durée pour l'exclusion.")
        else:
            await ctx.send(f"Une erreur s'est produite : {str(error)}")

    # Gestion des erreurs pour la commande unmute
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("Vous n'avez pas la permission de démuter un membre.")
        else:
            await ctx.send(f"Une erreur s'est produite : {str(error)}")

    @discord.slash_command(name="say", description="Envoyé un Embed dans le salon actuelle")
    @has_permissions(moderate_members=True) 
    async def unmute(self, ctx,tilte_embed,description_embed, url_image):
        await ctx.respond("Vous avez utilisé /say",ephemeral=True)
        embed = discord.Embed(title = tilte_embed, description = description_embed, colour = 0xFFFFFF)
        await ctx.send(embed = embed)
        

def setup(bot):
    bot.add_cog(Moderation(bot))

import discord
from discord.ext import commands

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="profil",description="Commande pour voir son profil d'utilisateur")
    async def profil(self, ctx):
        roles_to_check = ["🟢 6ᵉ Sixième", "🟢 5ᵉ Cinquième", "🟢 4ᵉ Quatrième","🟢 3ᵉ Troisième","🔴 2ᵈᵉ Seconde","🔴 1ʳᵉ Première","🔴Tˡᵉ Terminal","Autre +"]
    
        member = ctx.author
        found_role = None 
        
        
        for role in member.roles:
            if role.name in roles_to_check:
                found_role = role.name
                break
        speciality = None
        if found_role == "Autre +":
            found_role == "Étude supérieur ou Travaille"
        embed = discord.Embed(
            title="Profil",
            description=f"**Cours :**\n---------\nClasse : {found_role}\nSpécialités : {speciality}", 
            color= 0xFFFFFF
        )

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
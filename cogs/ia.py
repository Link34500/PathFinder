import discord
from discord.ext import commands
import cohere
TOKEN = 'MTIwMTMzMzg5MjU4MjQ3MzgwOA.GvoPck.LCeIujtZ-GwrFAgU_6JW5h0L_HF3huu964l4cw'  # C'est le token discord ça permet en gros de se co au client
INTELLIGENCE_CHANNEL = '🧠・intelligence-artificiel'  # Nom du salon où le bot envoie des messages
COHERE_API_KEY = 'Ff9vjkxkJKpHCDBQyg6XGfnK1IyKv5XVUvBcHS7h'  # La clé API de l'ia 

# Initialiser le client Cohere en gros c'est l'api pour le bot
co = cohere.Client(COHERE_API_KEY)

def split_message(message, max_length=2000):
    """Divise un message en plusieurs parties si nécessaire.""" # Pour éviter que le messages fasse plus de 2000 caractères car discord c'est max 2000 donc si son message fait plus de 2000 caractère (Au bot) Il va le diviser en plusieurs
    return [message[i:i + max_length] for i in range(0, len(message), max_length)]

def truncate_message(message, max_length=2000):
    """Tronque le message pour s'assurer qu'il ne dépasse pas max_length.""" # Là il c'est la vérification du truc au dessus
    return message[:max_length]

message_history = {}  # Dictionnaire pour stocker l'historique des messages comme ça le bot a un contexte
class Ia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):  # Ajoute 'self' comme premier argument
        if isinstance(message.channel, discord.DMChannel):
            return  # Ignore les messages privés (DM)
        if message.channel.name == INTELLIGENCE_CHANNEL and not message.author.bot:
            if message.channel.id not in message_history:
                message_history[message.channel.id] = []

            # Ajouter le message actuel à l'historique
            message_history[message.channel.id].append(message.content)

            # Conserver les 10 derniers messages pour le contexte
            context = "\n".join(message_history[message.channel.id][-10:])
            await message.channel.trigger_typing()  # Correction pour utiliser 'await'
            response_text = ""
            try:
                # Demander à l'IA de répondre en tenant compte du contexte et la façon de répondre
                response = co.chat(
                    message=f"Voici les anciens messages de la discussion (Si il n'y en as pas tant pis répond sans tenir compte du contexte): [{context}]Hey, tu es PathFinder, un bot Discord crée par Link qui aide les étudiants avec leurs travaux tu es un bot spécialiser dans toutes les matières du collège à la Terminal. Ne te présente pas sauf si quelqu'un te dit bonjour. Réponds de manière familière, tutoie, et utilise des phrases courtes. Si jamais le message est vulgaire, clash la personne qui t'a envoyé ce message. Voici le message : {message.content}"
                )
                response_text = response.text
                
                # Assurer que la réponse est courte
                response_text = truncate_message(response_text)

                # Diviser la réponse en plusieurs messages si nécessaire
                messages = split_message(response_text)
                
                # Envoyer chaque partie du message si nécessaire  
                for msg in messages:
                    await message.channel.send(msg)
            
            # Gestion d'erreurs
            except Exception as e:
                print(f"Erreur avec l'API Cohere: {e}")
                await message.channel.send('Désolé, il y a eu un problème avec l\'API Cohere.')
        else:
            return


def setup(bot):
    bot.add_cog(Ia(bot))
import discord
from discord.ext import commands
from discord import app_commands
import asyncio


class ValidationCog(commands.Cog):
    """
    A cog that handles role assignment commands and interactions for Discord validation purposes.

    Attributes:
        bot (commands.Bot): The bot instance that this cog is part of.
    """

    def __init__(self, bot):
        """
        Initializes the ValidationCog with the bot instance.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot

    @app_commands.command(name="role")
    async def role_command(
        self,
        interaction: discord.Interaction,
        channel_validation: discord.TextChannel,
        channel_home: discord.TextChannel,
    ):
        """
        A command to initiate role selection and validation process.

        This command asks the user to provide unique roles and a validation role.
        It then sends a message in a specified channel for role selection.

        Args:
            interaction (discord.Interaction): The interaction object containing information about command invocation.
            channel_validation (discord.TextChannel): The channel where validation requests will be sent.
            channel_home (discord.TextChannel): The channel where the role selection message will be sent.

        Raises:
            discord.Forbidden: If the bot lacks the permissions to send messages or perform actions.
            discord.HTTPException: If an error occurs while attempting to send a message.
        """
        try:
            await interaction.response.send_message(
                "Veuillez mentionner les rôles uniques disponibles (par exemple: @role1 @role2 ...)"
                + " puis mentionnez le rôle de validation.",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "Je n'ai pas la permission d'envoyer un message ici.", ephemeral=True
            )
            return
        except discord.HTTPException:
            await interaction.followup.send(
                "Une erreur est survenue lors de l'envoi du message. Veuillez réessayer.",
                ephemeral=True,
            )
            return

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            role_message = await self.bot.wait_for(
                "message", check=check, timeout=120.0
            )
            roles = [role for role in role_message.role_mentions]
            if len(roles) < 2:
                await interaction.followup.send(
                    "Vous devez mentionner au moins deux rôles:"
                    + " les rôles uniques et un rôle de validation.",
                    ephemeral=True,
                )
                return

            unique_roles = roles[:-1]
            validation_role = roles[-1]

            options = [
                discord.SelectOption(label=role.name, value=f"role_{role.id}")
                for role in unique_roles
            ]
            select_menu = discord.ui.Select(
                placeholder="Choisissez votre rôle",
                options=options,
                custom_id="select_unique_role",
            )
            view = discord.ui.View()
            view.add_item(select_menu)
            embed = discord.Embed(
                title="Sélection de rôle",
                description=(
                    f"Rôles uniques: {', '.join([role.mention for role in unique_roles])}\n"
                    f"Rôle de validation: {validation_role.mention}\n"
                    f"Channel de validation: {channel_validation.id}"
                ),
            )

            try:
                await channel_home.send(embed=embed, view=view)
            except discord.Forbidden:
                await interaction.followup.send(
                    "Je n'ai pas la permission d'envoyer le message dans le channel demandé.",
                    ephemeral=True,
                )
            except discord.HTTPException:
                await interaction.followup.send(
                    "Une erreur est survenue lors de l'envoi du message. Veuillez réessayer.",
                    ephemeral=True,
                )

        except asyncio.TimeoutError:
            await interaction.followup.send(
                "Temps écoulé, veuillez recommencer.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "Je n'ai pas la permission de répondre à votre message.", ephemeral=True
            )
        except discord.HTTPException:
            await interaction.followup.send(
                "Une erreur est survenue lors du suivi. Veuillez réessayer.",
                ephemeral=True,
            )


async def setup(bot):
    """
    Sets up the ValidationCog for the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(ValidationCog(bot))

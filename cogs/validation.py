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

        This command asks the user to provide a validation role and unique roles.
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
                "Veuillez mentionner le rôle de validation (par exemple: @role).",
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
            # Get validation role
            validation_message = await self.bot.wait_for(
                "message", check=check, timeout=120.0
            )
            validation_role_mentions = [
                role for role in validation_message.role_mentions
            ]

            if len(validation_role_mentions) != 1:
                await interaction.followup.send(
                    "Vous devez mentionner un seul rôle de validation.",
                    ephemeral=True,
                )
                return

            validation_role = validation_role_mentions[0]

            await interaction.followup.send(
                "Veuillez mentionner les rôles uniques disponibles (par exemple: @role1 @role2 ...).",
                ephemeral=True,
            )

            # Get unique roles
            role_message = await self.bot.wait_for(
                "message", check=check, timeout=120.0
            )
            unique_role_mentions = [role for role in role_message.role_mentions]

            if len(unique_role_mentions) < 1:
                await interaction.followup.send(
                    "Vous devez mentionner au moins un rôle unique.",
                    ephemeral=True,
                )
                return

            options = [
                discord.SelectOption(label=role.name, value=f"role_{role.id}")
                for role in unique_role_mentions
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
                    f"Rôles uniques: {', '.join([role.mention for role in unique_role_mentions])}\n"
                    f"Rôle de validation: {validation_role.mention}\n"
                    f"Channel de validation: {channel_validation.id}"
                ),
            )

            await channel_home.send(embed=embed, view=view)

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

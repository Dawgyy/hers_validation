import discord
from discord.ext import commands
from modals.verification import VerificationModal


class OnInteraction(commands.Cog):
    """
    A Cog to handle user interactions with components (buttons, select menus, etc.) in the Discord bot.
    """

    def __init__(self, bot):
        """
        Initialize the OnInteraction cog with the bot instance.

        Args:
            bot (commands.Bot): The bot instance to interact with Discord.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """
        Event listener to handle user interactions with components.

        Args:
            interaction (discord.Interaction): The interaction object triggered by the user.
        """
        custom_id = interaction.data.get("custom_id")

        if interaction.type == discord.InteractionType.component:
            # Handle role selection interaction
            if custom_id == "select_unique_role":
                original_embed = interaction.message.embeds[0]
                validation_channel_id = int(
                    original_embed.description.split("Channel de validation: ")[
                        1
                    ].split("\n")[0]
                )
                modal = VerificationModal()
                modal.custom_id = f"verification_{validation_channel_id}"
                await interaction.response.send_modal(modal)

            # Handle accept or deny button interaction
            elif custom_id and (
                custom_id.startswith("accept_") or custom_id.startswith("deny_")
            ):
                user_id = int(custom_id.split("_")[1])
                user = interaction.guild.get_member(user_id)

                if user:
                    await interaction.response.defer()
                    if custom_id.startswith("accept_"):
                        original_embed = interaction.message.embeds[0]
                        roles_text = original_embed.description.split(
                            "Rôles uniques: "
                        )[1].split("\n")[0]
                        validation_role_text = original_embed.description.split(
                            "Rôle de validation: "
                        )[1].split("\n")[0]
                        unique_roles = []

                        for role_id in roles_text.replace("@", "").split(">, <"):
                            stripped_role_id = role_id.strip("<>")
                            if stripped_role_id:
                                unique_roles.append(
                                    interaction.guild.get_role(
                                        int(stripped_role_id.replace("&", ""))
                                    )
                                )

                        validation_role = interaction.guild.get_role(
                            int(validation_role_text.strip("<@&>"))
                        )

                        try:
                            await user.add_roles(validation_role)
                        except discord.Forbidden:
                            await interaction.followup.send(
                                f"IJe n'ai pas les droits pour ajouter le rôle de validation à {user.mention}.",
                                ephemeral=True,
                            )
                            return

                        for role in unique_roles:
                            try:
                                await user.add_roles(role)
                            except discord.Forbidden:
                                await interaction.followup.send(
                                    f"Je n'ai pas les droits pour ajouter le rôle {role.name} à {user.mention}.",
                                    ephemeral=True,
                                )
                                return

                        first_name = original_embed.description.split("\n")[0].split(
                            ": "
                        )[1]
                        last_name = original_embed.description.split("\n")[1].split(
                            ": "
                        )[1]
                        if interaction.guild.owner_id == user.id:
                            await interaction.followup.send(
                                f"Je ne peux pas modifier le nom du propriétaire du serveur {user.mention}.",
                                ephemeral=True,
                            )
                            return

                        bot_top_role = interaction.guild.get_member(
                            self.bot.user.id
                        ).top_role
                        user_top_role = user.top_role

                        if bot_top_role <= user_top_role:
                            await interaction.followup.send(
                                f"""Je ne peut pas modifier le nom de {user.mention}
                                parce que le rôle du bot est inférieur ou égal u v^tre.""",
                                ephemeral=True,
                            )
                            return

                        try:
                            await user.edit(nick=f"{first_name} {last_name}")
                        except discord.Forbidden:
                            await interaction.followup.send(
                                f"Je n'ai pas les droits pour modifier le nom de {user.mention}.",
                                ephemeral=True,
                            )
                            return

                        await user.send(
                            "Votre validation a été acceptée, bienvenue!"
                        )

                        original_embed.description += (
                            f"\n\nDemande acceptée par {interaction.user.mention}"
                        )
                        for item in interaction.message.components:
                            for component in item.children:
                                component.disabled = True

                        view = discord.ui.View.from_message(interaction.message)
                        await interaction.message.edit(embed=original_embed, view=view)

                    elif custom_id.startswith("deny_"):
                        await user.send("Votre demande a été refusée.")
                        original_embed.description += (
                            f"\n\nDemande refusée par {interaction.user.mention}"
                        )
                        for item in interaction.message.components:
                            for component in item.children:
                                component.disabled = True

                        view = discord.ui.View.from_message(interaction.message)
                        await interaction.message.edit(embed=original_embed, view=view)

        elif interaction.type == discord.InteractionType.modal_submit:
            if interaction.data["custom_id"].startswith("verification_"):
                validation_channel_id = int(interaction.data["custom_id"].split("_")[1])
                channel_validation = interaction.guild.get_channel(
                    validation_channel_id
                )
                first_name = interaction.data["components"][0]["components"][0]["value"]
                last_name = interaction.data["components"][1]["components"][0]["value"]

                roles_text = (
                    interaction.message.embeds[0]
                    .description.split("Rôles uniques: ")[1]
                    .split("\n")[0]
                )
                validation_role_text = (
                    interaction.message.embeds[0]
                    .description.split("Rôle de validation: ")[1]
                    .split("\n")[0]
                )

                embed = discord.Embed(
                    title="Demande de validation",
                    description=(
                        f"Nom: {first_name}\n"
                        f"Prénom: {last_name}\n"
                        f"Utilisateur: {interaction.user.mention}\n"
                        f"Rôles uniques: {roles_text}\n"
                        f"Rôle de validation: {validation_role_text}"
                    ),
                    color=discord.Color.orange(),
                )

                accept_button = discord.ui.Button(
                    label="Accepter",
                    style=discord.ButtonStyle.success,
                    custom_id=f"accept_{interaction.user.id}_{validation_channel_id}",
                )

                deny_button = discord.ui.Button(
                    label="Refuser",
                    style=discord.ButtonStyle.danger,
                    custom_id=f"deny_{interaction.user.id}_{validation_channel_id}",
                )
                view = discord.ui.View()
                view.add_item(accept_button)
                view.add_item(deny_button)

                await channel_validation.send(embed=embed, view=view)
                await interaction.response.send_message(
                    "Votre demande à été envoyée pour validation.", ephemeral=True
                )
                return


async def setup(bot):
    """
    Setup function to add the OnInteraction cog to the bot.

    Args:
        bot (commands.Bot): The bot instance to add the cog to.
    """
    await bot.add_cog(OnInteraction(bot))

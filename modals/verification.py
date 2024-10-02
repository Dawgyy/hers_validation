import discord


class VerificationModal(discord.ui.Modal):
    """
    A modal for verifying user information as part of the role validation process.

    Attributes:
        first_name (discord.ui.TextInput): Text input for the user's first name.
        last_name (discord.ui.TextInput): Text input for the user's last name.
    """

    first_name = discord.ui.TextInput(label="Prénom", custom_id="first_name")
    last_name = discord.ui.TextInput(label="Nom", custom_id="last_name")

    def __init__(self):
        """
        Initializes the verification modal with the title 'Vérification'.
        """
        super().__init__(title="Vérification")

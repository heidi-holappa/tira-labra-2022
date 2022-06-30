class SupportedCharacters:
    """As the number of supported characters is less than 128, characters can be stored in 7 bits.
    The translation between characters and a seven bit value is done by a dictionary provided by
    this method. The 'characters_as_string' is hard coded to make sure that the order of the
    characters does not change.
    """

    def __init__(self):
        """Constructor for the class.
        """
        self.supported_characters_as_list, \
        self.char_to_index_dict, \
        self.index_to_char_dict = self.init_data_structures()


    def init_data_structures(self) -> tuple:
        """Initializes the data structures of supported characters to be provided
        to other layers of application logic.

        Returns:
            tuple: list and two dictionaries for character-to-index-to-character translations.
        """
        characters_as_string = \
            '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\
                !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        character_list = []
        character_list.append(0)
        for char in characters_as_string:
            character_list.append(ord(char))
        character_list.append(32)
        character_list.append(10)
        character_list.append(228)  # ä
        character_list.append(196)  # Ä
        character_list.append(197)  # Å
        character_list.append(229)  # å
        character_list.append(246)  # ö
        character_list.append(214)  # Ö
        character_to_index_dict = {}
        index_to_character_dict = {}
        for i, value in enumerate(character_list):
            character_to_index_dict[value] = i
            index_to_character_dict[i] = value
        return character_list, character_to_index_dict, index_to_character_dict

    def validate_given_content(self, content: str) -> tuple:
        """Validates that given content only contains supported characters.
        Returns a tuple of a boolean value and a list of possible unsupported characters.

        Args:
            content (str): string to be validated

        Returns:
            tuple: boolean value and a list of unsupported characters
        """
        result = True
        invalid_characters = []
        for char in content:
            if ord(char) not in self.char_to_index_dict:
                result = False
                invalid_characters.append(char)
        return result, invalid_characters

default_supported_characters = SupportedCharacters()
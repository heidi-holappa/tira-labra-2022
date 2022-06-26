class SupportedCharacters:
    """As the number of supported characters is less than 128, characters can be stored in 7 bits.
    The translation between characters and a seven bit value is done by a dictionary provided by this
    method. The 'characters_as_string' is hard coded to make sure that the order of the characters
    does not change. 
    """

    def __init__(self):
        """Constructor for the class. 
        """
        self.supported_characters_as_list, \
        self.char_to_index_dict, \
        self.index_to_char_dict = self.init_data_structures()

    
    def init_data_structures(self):
        characters_as_string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
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
        for i in range(len(character_list)):
            character_to_index_dict[character_list[i]] = i
            index_to_character_dict[i] = character_list[i]
        return character_list, character_to_index_dict, index_to_character_dict

if __name__ == "__main__":
    s = SupportedCharacters()
    d = s.char_to_index_dict
    for key, item in d.items():
        print(key, item)
    l = s.supported_characters_as_list
    print(l)


default_supported_characters = SupportedCharacters()
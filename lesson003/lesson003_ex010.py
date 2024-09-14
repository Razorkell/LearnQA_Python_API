class TestPhrase:

    __phrase = ""
    __expected_len = 15

    def set_phrase(self):
        self.__phrase = input("Set a phrase: ")

    def set_expected_len(self):
        try:
            self.__expected_len = int(input("Set an expected len: "))
        except ValueError:
            print("Expected len should be integer.")

    def get_phrase(self):
        return self.__phrase

    def get_expected_len(self):
        return self.__expected_len

    def test_phrase_len(self):
        TestPhrase.set_phrase(self)
        __phrase_len = len(self.__phrase)
        __temp_len = self.__expected_len
        assert __phrase_len < __temp_len, f"The phrase greater or equal than {__temp_len}"

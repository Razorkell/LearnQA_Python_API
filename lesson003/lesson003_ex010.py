class TestPhrase:

    __phrase = ""
    __expected_len = 15

    def set_phrase(self):
        self.__phrase = input("Set a phrase: ")

    def set_expected_len(self):
        self.__expected_len = input("Set an expected len: ")

    def get_phrase(self):
        return self.__phrase

    def get_expected_len(self):
        return self.__expected_len

    def test_phrase_len(self):
        TestPhrase.set_phrase(self)
        assert len(self.__phrase) < 15, f"The phrase greater or equal than {self.__expected_len}"

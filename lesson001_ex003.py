class Me:
    def __init__(self, name):
        self._name = name

    def print_name(self):
        print("Hello from " + self._name)


man_001 = Me("Vladimir")
man_001.print_name()

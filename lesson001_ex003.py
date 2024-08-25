class Me:
    def __init__(self, name):
        self._name = name

    # print hello from Me
    def hello_from(self):
        print("Hello from " + self._name)


man_001 = Me("Vladimir")
man_001.hello_from()

class God:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.name = kwargs.get('name', 'The Almighty')
        return cls._instance

    def speak(self):
        print(f'I am {self.name}, the one and only.')


god1 = God(name="Zeus")
god2 = God(name="Gholi")

god2.speak()

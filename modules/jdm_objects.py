class Object:    
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        v: float = 0,
    )->None:
        self.x = x
        self.y = y
        self.v = v

class Car(Object):
    def __init__(
        self,
        type: str = "civic",
        len: float = 10,
        width: float = 5,
        *args, 
        **kwargs
    )->None:
        super().__init__(**kwargs)
        self.type = type
        self.len = len
        self.width = width

class Item(Object):
    def __init__(
        self,
        type: str = "money",
        r: float = 5,
        *args,
        **kwargs
    )->None:
        super().__init__(**kwargs)
        self.type = type
        self.r = r

class Obsrtacle(Object):
    def __init__(
            self,
            type: str = ""
    )->None:
        pass
        
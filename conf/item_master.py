
class ItemMaster:
    def __init__(self):
        self.__items = {
                0: ('hey-tea', 380),
                1: ('coca-cola', 400),
                2: ('grapefruit-squash', 400),
                3: ('gogo-tea', 380),
                4: ('pocari', 410),
                5: ('calpis', 410)
                }


    @property
    def items(self):
        return self.__items

class school:
    def __init__(self, name, city, rank):
        self.name = name 
        self.city = city 
        self.rank = rank
    
    def change_name(self, new_name : str):
        self.name = new_name
    
    def get_name(self) -> str:
        return self.name



tamu = school("tamu", "college station", 3)

print(tamu.get_name())

tamu.change_name("UT")

print(tamu.get_name())
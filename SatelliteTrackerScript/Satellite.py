class Satellite:
    def __init__(self,
        satid: id,
        satname: str,
        coordinates: tuple
    ) -> object:
        
        self.satid = satid
        self.satname = satname
        self.coordinates = coordinates

    def get_satid(self) -> id:
        return self.satid
    
    def get_satname(self) -> str:
        return self.satname
    
    def get_coordinates(self) -> tuple:
        return self.coordinates
    
    def set_satid(self, satid: id) -> None:
        self.satid = satid

    def set_satname(self, satname: str) -> None:
        self.satname = satname

    def set_coordinates(self, coordinates: tuple) -> None:
        self.coordinates = coordinates
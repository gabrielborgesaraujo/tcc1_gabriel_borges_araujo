class NiveisWCAG:
    def __init__(self, isAA_Valid, isAAA_Valid):
        self.isAA_Valid = isAA_Valid
        self.isAAA_Valid = isAAA_Valid
    
    def to_dict(self):
        return {
            "isAA_Valid": self.isAA_Valid,
            "isAAA_Valid": self.isAAA_Valid
        }
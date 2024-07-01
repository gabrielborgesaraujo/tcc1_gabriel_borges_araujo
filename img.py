from text_element import TextElement

class Image:
    def __init__(self, path, shape, text_elements, number_of_texts, number_of_valid_texts, contraste_medio_por_imagem):
        self.path = path
        self.text_elements = text_elements
        self.shape = shape
        self.number_of_texts = number_of_texts
        self.number_of_valid_texts = number_of_valid_texts,
        self.contraste_medio_por_imagem = contraste_medio_por_imagem

    
    def to_dict(self):
        return {
            "path": self.path,
            "text_elements": [text_element.to_dict() for text_element in self.text_elements],
            "shape": self.shape,
            "number_of_texts": self.number_of_texts,
            "number_of_valid_texts": self.number_of_valid_texts,
            "contraste_medio_por_imagem": self.contraste_medio_por_imagem
        }


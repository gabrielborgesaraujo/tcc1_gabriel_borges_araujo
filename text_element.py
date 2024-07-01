from niveis_wcag import NiveisWCAG

class TextElement:
    def __init__(self, razao_contraste, cor_clara, cor_escura, niveis_wcag, isValido, posicoes, texto):
        self.razao_contraste = razao_contraste
        self.cor_clara = cor_clara
        self.cor_escura = cor_escura
        self.niveis_wcag = niveis_wcag
        self.isValido = isValido
        self.posicoes = posicoes
        self.texto = texto

    
    def __str__(self):
        return f"Razão de Contraste: {self.razao_contraste}\nLuminosidade Clara: {self.luminosidade_clara}\nLuminosidade Escura: {self.luminosidade_escura}\nNíveis WCAG: {self.niveis_wcag}\nVálido: {self.isValido}\nTamanho da Imagem: {self.tamanho_da_imagem}\nPosições: {self.posicoes}\nTexto: {self.texto}"
    
    def to_dict(self):
        return {
            "razao_contraste": self.razao_contraste,
            "cor_clara": self.cor_clara,
            "cor_escura": self.cor_escura,
            "niveis_wcag": self.niveis_wcag.to_dict(),
            "isValido": self.isValido,
            "posicoes": self.posicoes,
            "texto": self.texto
        }
        
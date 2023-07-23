class token:

    def __init__(self, nome, lexema, linha):
        self.nome = nome
        self.lexema = lexema
        self.linha = linha

    def imprimir(self):
        print("Nome: ", self.nome, "Lexema: ", self.lexema, "Linha: ", self.linha)
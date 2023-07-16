class token:

    def _init_(self, nome, lexema, linha):
        self.nome = nome
        self.lexema = lexema
        self.linha = linha

    def imprimir(self):
        print("Nome: ", self.nome, "Lexema: ", self.lexema, "Linha: ", self.linha)
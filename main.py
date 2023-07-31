from analisadorLexico import analisadorLexico
from analisadorSintatico import analisadorSintatico

arq = open("teste.txt","r")
texto = arq.readlines()
arq.close()

print("*" * 13 + " Analisador lexico " + "*" * 13)
lexer = analisadorLexico(texto)
lexer.tokenizador(texto)
#lexer.imprimir_lista_tokens()
#lexer.imprimir_tabela_simbolos()
print("*" * 26)

print("*" * 13 + " Analisador sintatico " + "*" * 13)
parser = analisadorSintatico(lexer.tokens, lexer.tabela_simbolos)
print("*" * 26)

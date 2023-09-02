from analisadorLexico import analisadorLexico
from analisadorSintatico import analisadorSintatico
from gerador_de_codigo import GeradorCodigoIntermediario

arq = open("teste.txt","r")
texto = arq.readlines()
arq.close()

print("*" * 13 + " Analisador lexico " + "*" * 13)
lexer = analisadorLexico(texto)
lexer.tokenizador(texto)
#lexer.imprimir_lista_tokens()
lexer.imprimir_tabela_simbolos()
print("*" * 45)

print("*" * 13 + " Analisador sintatico " + "*" * 13)
parser = analisadorSintatico(lexer.tokens, lexer.tabela_simbolos)
instrucoes = parser.programa()
print("*" * 48)

gerador = GeradorCodigoIntermediario(instrucoes)
#gerador.imprimirListainstrucoes()
gerador.gerar_codigo()

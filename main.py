from analisadorLexico import analisadorLexico

arq = open("teste.txt","r")
texto = arq.readlines()
arq.close()

print("*" * 26)
lexer = analisadorLexico(texto)
lexer.tokenizador(texto)
lexer.imprimir_lista_tokens()
print("*" * 26)
#lexer.imprimir_tabela_simbolos()
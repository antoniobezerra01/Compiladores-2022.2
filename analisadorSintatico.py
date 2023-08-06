from tokens import token

class analisadorSintatico:

     def __init__(self, lista_tokens, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos
        self.lista_tokens = lista_tokens
        self.look_ahead = 0

     def match(self, token_esperado):
        if self.lista_tokens[self.look_ahead].nome == token_esperado:
            self.look_ahead += 1
        else:
            print("Erro sintatico na linha: ", self.lista_tokens[self.look_ahead].linha, end=" ")
            print("Esperado: ", token_esperado, end=" ")
            print("Encontrado: ", self.lista_tokens[self.look_ahead].nome)
            exit(1)

     def programa(self):
        self.match("<inicio do programa>")
        self.match("<abre chaves>")
        self.bloco()
        self.match("<fecha chaves>")
        self.match("<fim do programa>")

     def bloco(self):
      token_atual = self.lista_tokens[self.look_ahead]
      if token_atual.nome == "<tipo>":
         self.declaracao_variavel()
         self.bloco()
      elif token_atual.nome == "<declaração de função>":
         self.declaracao_funcao()
         self.bloco()
      elif token_atual.nome == "<declaração de procedimento>":
         self.declaracao_procedimento()
         self.bloco()
      elif token_atual.nome == "<chamada de procedimento>":
         self.chamada_procedimento()
         self.bloco()
      elif token_atual.nome == "<chamada de impressão>":
         self.chamada_impressao()
         self.bloco()
      elif token_atual.nome == "<chamada do if>":
         self.condicao()
         self.bloco()
      elif token_atual.nome == "<chamada do while>":
         self.laço()
         self.bloco()
      elif token_atual.nome == "<identificador>":
         self.match("<identificador>")
         self.match("<atribuição>")
         self.atribuicao()
         self.bloco()             
      else:
         return
      
     def declaracao_variavel(self):
        self.match("<tipo>")
        self.match("<identificador>")      
        self.match("<atribuição>")
        self.atribuicao()
        

     def declaracao_procedimento(self):
        self.match("<declaração de procedimento>")
        self.match("<identificador>")
        self.match("<abre parenteses>")
        self.parametros()
        self.match("<fecha parenteses>")
        self.match("<abre chaves>")
        self.bloco()
        self.match("<fecha chaves>")
        self.match("<fim comando>")

     def chamada_procedimento(self):
        self.match("<chamada de procedimento>")
        self.match("<identificador>")
        self.match("<abre parenteses>")
        self.chamada_parametros()
        self.match("<fecha parenteses>")
        self.match("<fim comando>")

     def expressao(self):
        if self.lista_tokens[self.look_ahead].nome == "<valor booleana>":
            self.match("<valor booleana>")
        else:
            if self.lista_tokens[self.look_ahead].nome == "<identificador>":
                self.match("<identificador>")
                self.match("<operador booleano>")
                self.expressao2()
            elif self.lista_tokens[self.look_ahead].nome == "<número>":
                self.match("<número>")
                self.match("<operador booleano>")
                self.expressao2()
            else:
                print("Erro sintático: token esperado: <identificador>" + " ou " + "<número>" + " encontrado: " + self.lista_tokens[self.look_ahead].nome + " na linha: " + str(self.lista_tokens[self.look_ahead].linha))
                exit()
            
     def expressao2(self):
        if self.lista_tokens[self.look_ahead].nome == "<identificador>":
            self.match("<identificador>")
        elif self.lista_tokens[self.look_ahead].nome == "<número>":
            self.match("<número>")
        else:
            print("Erro sintático: token esperado: <identificador>" + " ou " + "<número>" + " encontrado: " + self.lista_tokens[self.look_ahead].nome + " na linha: " + str(self.lista_tokens[self.look_ahead].linha))
            exit()
        
        
     def atribuicao(self):
        if self.lista_tokens[self.look_ahead+1].nome == "<operador aritmético>":
            self.chamada_operador()
            self.match("<fim comando>")
        elif self.lista_tokens[self.look_ahead].nome == "<identificador>":
            self.match("<identificador>")
            self.match("<fim comando>")
        elif self.lista_tokens[self.look_ahead].nome == "<número>":
            self.match("<número>")
            self.match("<fim comando>")
        elif self.lista_tokens[self.look_ahead].nome == "<chamada de função>":
            self.chamada_funcao()
            self.match("<fim comando>")
        elif self.lista_tokens[self.look_ahead].nome == "<valor booleana>":
            self.match("<valor booleana>")
            self.match("<fim comando>")
        else:
            print("Erro sintático: token esperado: <identificador>" + " ou " + "<número>" + " ou " + "<chamada de função>" + " ou " + "<valor booleana>" + " encontrado: " + self.lista_tokens[self.look_ahead].nome + " na linha: " + str(self.lista_tokens[self.look_ahead].linha))
            exit()


     def chamada_operador(self):
        while True:
            if self.lista_tokens[self.look_ahead].nome == "<identificador>":
                self.match("<identificador>")
                self.match("<operador aritmético>")
                self.chamada_operador2()
            elif self.lista_tokens[self.look_ahead].nome == "<número>":
                self.match("<número>")
                self.match("<operador aritmético>")
                self.chamada_operador2()
            elif self.lista_tokens[self.look_ahead].nome == "<operador aritmético>":
                self.match("<operador aritmético>")
                self.chamada_operador2()
            else:
                break

     def chamada_operador2(self):
        if self.lista_tokens[self.look_ahead].nome == "<identificador>":
            self.match("<identificador>")
        elif self.lista_tokens[self.look_ahead].nome == "<número>":
            self.match("<número>")
        else:
            print("Erro sintático: token esperado: <identificador>" + " ou " + "<número>" + " encontrado: " + self.lista_tokens[self.look_ahead].nome + " na linha: " + str(self.lista_tokens[self.look_ahead].linha))
            exit()


     def chamada_retorno(self):
        self.match("<chamada de retorno>")
        self.match("<abre parenteses>")
        if self.lista_tokens[self.look_ahead].nome == "<identificador>":
            self.match("<identificador>")
        elif self.lista_tokens[self.look_ahead].nome == "<número>":
            self.match("<número>")
        elif self.lista_tokens[self.look_ahead].nome == "<valor booleana>":
            self.match("<valor booleana>")
        elif self.lista_tokens[self.look_ahead].nome == "<chamada de função>":
            self.chamada_funcao()
        else:
            print("Erro sintático: token esperado: <identificador>" + " ou " + "<numero>" + " ou " + "<valor booleana>" + " ou " + "<chamada de função>" + " encontrado: " + self.lista_tokens[self.look_ahead].nome + " na linha: " + str(self.lista_tokens[self.look_ahead].linha))
            exit()
        self.match("<fecha parenteses>")
        self.match("<fim comando>")


     def chamada_impressao(self):
        self.match("<chamada de impressão>")
        self.match("<abre parenteses>")
        if (self.lista_tokens[self.look_ahead+1].nome == "<operador aritmético>"):
            self.chamada_operador()
        elif(self.lista_tokens[self.look_ahead].nome == "<identificador>"):
            self.match("<identificador>")
        elif(self.lista_tokens[self.look_ahead].nome == "<numero>"):
            self.match("<numero>")
        elif(self.lista_tokens[self.look_ahead].nome == "<chamada de função>"):
            self.chamada_funcao()
        elif(self.lista_tokens[self.look_ahead].nome == "<valor booleana>"):
            self.match("<valor booleana>")
        else:
            print("Erro sintático: token esperado: <identificador>" + " ou " + "<numero>" + " ou " + "<chamada de função>" + " ou " + "<valor booleana>" + " encontrado: " + self.lista_tokens[self.look_ahead].nome + " na linha: " + str(self.lista_tokens[self.look_ahead].linha))
            exit()
        self.match("<fecha parenteses>")
        self.match("<fim comando>")
            

     def laço(self):
        self.match("<chamada do while>")
        self.match("<abre parenteses>")
        self.expressao()
        self.match("<fecha parenteses>")
        self.match("<abre chaves>")
        self.bloco2()
        if self.lista_tokens[self.look_ahead].nome == "<incondicional>":
            self.match("<incondicional>") 
            self.match("<fim comando>")
        self.match("<fecha chaves>")  
     
     def declaracao_funcao(self):
        self.match("<declaração de função>")
        self.match("<tipo>")
        self.match("<identificador>")
        self.match("<abre parenteses>")
        self.parametros()
        self.match("<fecha parenteses>")
        self.match("<abre chaves>")
        self.bloco4()
        self.chamada_retorno()
        self.match("<fecha chaves>")
        self.match("<fim comando>")

     def chamada_funcao(self):
        self.match("<chamada de função>")
        self.match("<identificador>")
        self.match("<abre parenteses>")
        self.chamada_parametros()
        self.match("<fecha parenteses>")
        #self.match("<fim comando>")
     
     def parametros(self):
        self.match("<tipo>")
        self.match("<identificador>")
        if self.lista_tokens[self.look_ahead].nome == "<virgula>":
            self.match("<virgula>")            
            self.parametros()

     def chamada_parametros(self):
        self.match("<identificador>")
        if self.lista_tokens[self.look_ahead].nome == "<virgula>":
            self.match("<virgula>")
            self.chamada_parametros()

     def condicao(self):
        self.match("<chamada do if>")
        self.match("<abre parenteses>")
        self.expressao()
        self.match("<fecha parenteses>")
        self.match("<abre chaves>")
        self.bloco3()
        self.match("<fecha chaves>")
        if self.lista_tokens[self.look_ahead].nome == "<chamada do else>":
            self.match("<chamada do else>")
            self.match("<abre chaves>")
            self.bloco3()
            self.match("<fecha chaves>")
    


     def bloco2(self):
        if self.lista_tokens[self.look_ahead].nome == "<tipo>":
            self.declaracao_variavel()
            self.bloco2()
        elif self.lista_tokens[self.look_ahead].nome == "<chamada do if>":
            self.condicao2()
            self.bloco2()
        elif self.lista_tokens[self.look_ahead].nome == "<chamada do while>":
            self.laço()
            self.bloco2()
        elif self.lista_tokens[self.look_ahead].nome == "<chamada de impressão>":
            self.chamada_impressao()
            self.bloco2()
        elif self.lista_tokens[self.look_ahead].nome == "<identificador>":
            self.match("<identificador>")
            self.match("<atribuição>")
            self.atribuicao()
            self.bloco2()    
        elif self.lista_tokens[self.look_ahead].nome == "<chamada de procedimento>":
            self.chamada_procedimento()
            self.bloco2()
        elif self.lista_tokens[self.look_ahead].nome == "<incondicional>":
            self.match("<incondicional>")
            self.match("<fim comando>")
            self.bloco2()
                
  
     def condicao2(self):
        self.match("<chamada do if>")
        self.match("<abre parenteses>")
        self.expressao()
        self.match("<fecha parenteses>")
        self.match("<abre chaves>")
        self.bloco2()
        self.match("<fecha chaves>")
        
        if self.lista_tokens[self.look_ahead].nome == "<chamada do else>":
            self.match("<chamada do else>")
            self.match("<abre chaves>")
            self.bloco2()
            self.match("<fecha chaves>")
        
     def bloco3(self):
         if self.lista_tokens[self.look_ahead].nome == "<tipo>":  
            self.declaracao_variavel()
            self.bloco3()
         elif self.lista_tokens[self.look_ahead].nome == "<chamada de procedimento>":
             self.chamada_procedimento()
             self.bloco3()
         elif self.lista_tokens[self.look_ahead].nome == "<identificador>":
            self.match("<identificador>")
            self.match("<atribuição>")
            self.atribuicao()
            self.bloco3()    
         elif self.lista_tokens[self.look_ahead].nome == "<chamada do if>":
            self.condicao()
            self.bloco3()
         elif self.lista_tokens[self.look_ahead].nome == "<chamada do while>":
            self.laço() 
            self.bloco3()   
         elif self.lista_tokens[self.look_ahead].nome == "<chamada de impressão>":
             self.chamada_impressao()
             self.bloco3()
            
     def bloco4(self):
      token_atual = self.lista_tokens[self.look_ahead]
      if token_atual.nome == "<tipo>":
         self.declaracao_variavel()
         self.bloco4()
      elif token_atual.nome == "<declaração de função>":
         self.declaracao_funcao()
         self.bloco4()
      elif token_atual.nome == "<declaração de procedimento>":
         self.declaracao_procedimento()
         self.bloco4()
      elif token_atual.nome == "<chamada de procedimento>":
         self.chamada_procedimento()
         self.bloco4()
      elif token_atual.nome == "<chamada de impressão>":
         self.chamada_impressao()
         self.bloco4()
      elif token_atual.nome == "<chamada do if>":
         self.condicao()
         self.bloco4()
      elif token_atual.nome == "<chamada do while>":
         self.laço()
         self.bloco4()
      elif token_atual.nome == "<identificador>":
         self.match("<identificador>")
         self.match("<atribuição>")
         self.atribuicao()
         self.bloco4()             
      else:
         return
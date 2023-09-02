from tokens import token
from analisadorSemantico import *

class analisadorSintatico:

     def __init__(self, lista_tokens, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos
        self.lista_tokens = lista_tokens
        self.look_ahead = 0
        self.instrucoes = []

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
        return self.instrucoes

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
      elif self.lista_tokens[self.look_ahead].nome == "<identificador>":
            if(self.lista_tokens[self.look_ahead].lexema in self.tabela_simbolos):
                self.match("<identificador>")
                self.match("<atribuição>")
                self.atribuicao()
                self.bloco()            
      else:
         return
      
     def declaracao_variavel(self):
        self.match("<tipo>")
        self.match("<identificador>")
        if (not verificar_declaracao(self.lista_tokens,self.tabela_simbolos,self.look_ahead)):
            exit()     
        self.match("<atribuição>")
        self.atribuicao()
        

     def declaracao_procedimento(self):
        look_ahead_aux = self.look_ahead
        instrucao_aux = []

        while self.lista_tokens[look_ahead_aux].nome != "<abre chaves>":
            instrucao_aux.append(self.lista_tokens[look_ahead_aux])
            look_ahead_aux += 1

        self.instrucoes.append(instrucao_aux)
        self.match("<declaração de procedimento>")
        self.match("<identificador>")
        self.match("<abre parenteses>")
        self.parametros()
        self.match("<fecha parenteses>")
        self.match("<abre chaves>")
        self.bloco()
        self.match("<fecha chaves>")
        self.match("<fim comando>")
        endProc = [token("<end_proc>","<end_proc>",0), token("<end_proc>","endProc",0)]
        self.instrucoes.append(endProc)

     def chamada_procedimento(self):
        look_ahead_aux = self.look_ahead
        instrucao_aux = []

        while self.lista_tokens[look_ahead_aux].nome != "<fim comando>":
            instrucao_aux.append(self.lista_tokens[look_ahead_aux])
            look_ahead_aux += 1

        self.instrucoes.append(instrucao_aux)
        self.match("<chamada de procedimento>")
        
        if(not verificar_parametros_proc(self.lista_tokens,self.tabela_simbolos,self.look_ahead)):
            print("Erro semântico: procedimento ")
            exit()

        self.match("<identificador>")
        self.match("<abre parenteses>")
        self.chamada_parametros()
        self.match("<fecha parenteses>")
        self.match("<fim comando>")

     def expressao(self):
        if self.lista_tokens[self.look_ahead].nome == "<valor booleana>":
            self.match("<valor booleana>")
        else:
            if (not verificar_expressao(self.lista_tokens,self.tabela_simbolos,self.look_ahead)):
                exit()
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
        look_ahead_aux = self.look_ahead - 2  
        instrucao_aux = []
        while self.lista_tokens[look_ahead_aux].nome != "<fim comando>":
            instrucao_aux.append(self.lista_tokens[look_ahead_aux])
            look_ahead_aux += 1
        self.instrucoes.append(instrucao_aux)

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
        if (not verificar_atribuicao(self.lista_tokens,self.tabela_simbolos,self.look_ahead)):
            exit()
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
        instrucao_aux = []

        instrucao_aux.append(self.lista_tokens[self.look_ahead])
        instrucao_aux.append(self.lista_tokens[self.look_ahead + 2])

        self.instrucoes.append(instrucao_aux)

        self.match("<chamada de retorno>")
        if self.lista_tokens[self.look_ahead].nome == "<identificador>":
            self.match("<identificador>")
        elif self.lista_tokens[self.look_ahead].nome == "<número>":
            self.match("<número>")
        elif self.lista_tokens[self.look_ahead].nome == "<valor booleana>":
            self.match("<valor booleana>")
        elif self.lista_tokens[self.look_ahead].nome == "<chamada de função>":
            self.chamada_funcao()
        else:
            print("Erro sintático: token esperado: <identificador>" + " ou " + "<número>" + " ou " + "<valor booleana>" + " ou " + "<chamada de função>" + " encontrado: " + self.lista_tokens[self.look_ahead].nome + " na linha: " + str(self.lista_tokens[self.look_ahead].linha))
            exit()
        self.match("<fim comando>")
        end = [token("<end_func>","<end_func>",0), token("<end_func>","end_func",0)]
        self.instrucoes.append(end)


     def chamada_impressao(self):
        instrucao_aux = []
        look_ahead_aux = self.look_ahead

        while self.lista_tokens[look_ahead_aux].nome != "<fim comando>":
            instrucao_aux.append(self.lista_tokens[look_ahead_aux])
            look_ahead_aux += 1

        self.instrucoes.append(instrucao_aux)
        self.match("<chamada de impressão>")
        self.match("<abre parenteses>")
        if (self.lista_tokens[self.look_ahead+1].nome == "<operador aritmético>"):
            self.chamada_operador()
        elif(self.lista_tokens[self.look_ahead].nome == "<identificador>"):
            self.match("<identificador>")
        elif(self.lista_tokens[self.look_ahead].nome == "<número>"):
            self.match("<número>")
        elif(self.lista_tokens[self.look_ahead].nome == "<chamada de função>"):
            self.chamada_funcao()
        elif(self.lista_tokens[self.look_ahead].nome == "<valor booleana>"):
            self.match("<valor booleana>")
        else:
            print("Erro sintático: token esperado: <identificador>" + " ou " + "<número>" + " ou " + "<chamada de função>" + " ou " + "<valor booleana>" + " encontrado: " + self.lista_tokens[self.look_ahead].nome + " na linha: " + str(self.lista_tokens[self.look_ahead].linha))
            exit()
        self.match("<fecha parenteses>")
        self.match("<fim comando>")
            

     def laço(self):
        look_ahead_aux = self.look_ahead
        instrucao_aux = []
        while self.lista_tokens[look_ahead_aux].nome != "<abre chaves>":
            instrucao_aux.append(self.lista_tokens[look_ahead_aux])
            look_ahead_aux += 1
        self.instrucoes.append(instrucao_aux)

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
        self.instrucoes.append([self.lista_tokens[self.look_ahead],self.lista_tokens[self.look_ahead -1] ])
        
     
     def declaracao_funcao(self):
        look_ahead_aux = self.look_ahead 
        instrucao_aux = []
        while self.lista_tokens[look_ahead_aux].nome != "<abre chaves>":
            instrucao_aux.append(self.lista_tokens[look_ahead_aux])
            look_ahead_aux += 1

        self.instrucoes.append(instrucao_aux)
        self.match("<declaração de função>")
        self.match("<tipo>")
        aux = self.look_ahead
        self.match("<identificador>")
        self.match("<abre parenteses>")
        self.parametros()
        self.match("<fecha parenteses>")
        self.match("<abre chaves>")
        self.bloco4()
        if (not verificar_retorno(self.lista_tokens,self.tabela_simbolos,self.look_ahead,aux)):
            print("Erro semântico: função sem retorno na linha: " + str(self.lista_tokens[self.look_ahead].linha))
            exit()
        self.chamada_retorno()
        self.match("<fecha chaves>")
        self.match("<fim comando>")

     def chamada_funcao(self):
        self.match("<chamada de função>")
        if(not verificar_parametros_funcao(self.lista_tokens,self.tabela_simbolos,self.look_ahead)):
            print("Erro semântico: número de parâmetros inválido na linha: " + str(self.lista_tokens[self.look_ahead].linha))
            exit()
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
        look_ahead_aux = self.look_ahead
        instrucao_aux = []
        while self.lista_tokens[look_ahead_aux].nome != "<abre chaves>":
            instrucao_aux.append(self.lista_tokens[look_ahead_aux])
            look_ahead_aux += 1

        self.instrucoes.append(instrucao_aux)
        self.match("<chamada do if>")
        self.match("<abre parenteses>")
        self.expressao()
        self.match("<fecha parenteses>")
        self.match("<abre chaves>")
        self.bloco3()
        self.match("<fecha chaves>")
        self.instrucoes.append([self.lista_tokens[self.look_ahead],self.lista_tokens[self.look_ahead]])
        if self.lista_tokens[self.look_ahead].nome == "<chamada do else>":
            self.instrucoes.append([self.lista_tokens[self.look_ahead],self.lista_tokens[self.look_ahead]])
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
            if(self.lista_tokens[self.look_ahead].lexema in self.tabela_simbolos):
                self.match("<identificador>")
                self.match("<atribuição>")
                self.atribuicao()
                self.bloco2()
        elif self.lista_tokens[self.look_ahead].nome == "<chamada de procedimento>":
            self.chamada_procedimento()
            self.bloco2()
        elif self.lista_tokens[self.look_ahead].nome == "<incondicional>":
            self.instrucoes.append([self.lista_tokens[self.look_ahead],self.lista_tokens[self.look_ahead]])
            self.match("<incondicional>")
            self.match("<fim comando>")
            self.bloco2()
                
  
     def condicao2(self):
        look_ahead_aux = self.look_ahead
        instrucao_aux = []
        while self.lista_tokens[look_ahead_aux].nome != "<abre chaves>":
            instrucao_aux.append(self.lista_tokens[look_ahead_aux])
            look_ahead_aux += 1

        self.instrucoes.append(instrucao_aux)
        self.match("<chamada do if>")
        self.match("<abre parenteses>")
        self.expressao()
        self.match("<fecha parenteses>")
        self.match("<abre chaves>")
        self.bloco2()
        self.match("<fecha chaves>")
        if not self.lista_tokens[self.look_ahead+1].nome == "<else_part>":
            self.instrucoes.append([self.lista_tokens[self.look_ahead],self.lista_tokens[self.look_ahead]])
        
        if self.lista_tokens[self.look_ahead].nome == "<chamada do else>":
            self.instrucoes.append([self.lista_tokens[self.look_ahead],self.lista_tokens[self.look_ahead]])
            self.match("<chamada do else>")
            self.match("<abre chaves>")
            self.bloco2()
            self.match("<fecha chaves>")
            self.instrucoes.append([self.lista_tokens[self.look_ahead],self.lista_tokens[self.look_ahead]])
        
     def bloco3(self):
         if self.lista_tokens[self.look_ahead].nome == "<tipo>":  
            self.declaracao_variavel()
            self.bloco3()
         elif self.lista_tokens[self.look_ahead].nome == "<chamada de procedimento>":
             self.chamada_procedimento()
             self.bloco3()
         elif self.lista_tokens[self.look_ahead].nome == "<identificador>":
            if(self.lista_tokens[self.look_ahead].lexema in self.tabela_simbolos):
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
      elif self.lista_tokens[self.look_ahead].nome == "<identificador>":
            if(self.lista_tokens[self.look_ahead].lexema in self.tabela_simbolos):
                self.match("<identificador>")
                self.match("<atribuição>")
                self.atribuicao()
                self.bloco4()        
      else:
         return
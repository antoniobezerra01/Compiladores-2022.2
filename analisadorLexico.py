from tokens import token
from simbolos import *

class analisadorLexico:
     
    def __init__(self,texto):
       self.texto = texto
       self.tokens = []
       self.tabela_simbolos = {}

    def tokenizador(self,texto):
       buffer=''
       linha_atual=1
       for linha in texto:
           for i in range(len(linha)):
               if((i + 1) < len(linha)): 
                   buffer += linha[i]
                   if(self.verifica_delimitadores(buffer, linha_atual)):
                       buffer = ""
                   elif(linha[i + 1] == " " or linha[i + 1] == "\n" or linha[i + 1] == "{" or linha[i + 1] == "}" or linha[i + 1] == "(" or linha[i + 1] == ")" or linha[i + 1] == ";" or linha[i + 1] == ","):
                       buffer = buffer.strip()
                       self.palavras_reservadas(buffer, linha_atual, linha, i)
                       buffer = ""
           buffer = ""
           linha_atual += 1

    def palavras_reservadas(self, buffer, linha, texto, i):
       if (buffer == "begin"):
           self.tokens.append(token("<inicio do programa>","begin",linha))
           return True
       elif (buffer == "end"):
           self.tokens.append(token("<fim do programa>","end",linha))
           return True
       elif (buffer == "Integer"):
           self.tokens.append(token("<tipo>","Integer",linha))
           return True
       elif (buffer == "Boolean"):
           self.tokens.append(token("<tipo>","Boolean",linha))
           return True
       elif (buffer == "dfunc"):
           self.tokens.append(token("<declaração de função>","dfunc",linha))
           return True
       elif (buffer == "cfunc"):
           self.tokens.append(token("<chamada de função>","cfunc",linha))
           return True
       elif (buffer == "dproc"):
           self.tokens.append(token("<declaração de procedimento>","dproc",linha))
           return True
       elif (buffer == "cproc"):
           self.tokens.append(token("<chamada de procedimento>","cproc",linha))
           return True
       elif (buffer == "return"):
           self.tokens.append(token("<chamada de retorno>","return",linha))
           return True
       elif (buffer == "if"):
           self.tokens.append(token("<chamada do if>","if",linha))
           return True
       elif (buffer == "else"):
           self.tokens.append(token("<chamada do else>","else",linha))
           return True
       elif (buffer == "while"):
           self.tokens.append(token("<chamada do while>","while",linha))
           return True
       elif (buffer == "break"):
           self.tokens.append(token("<incondicional>","break",linha))
           return True
       elif (buffer == "continue"):
           self.tokens.append(token("<incondicional>","continue",linha))
           return True
       elif (buffer == "println"):
           self.tokens.append(token("<chamada de impressão>","println",linha))
           return True
       elif (buffer == "=="):
           self.tokens.append(token("<operador booleano>","==",linha))
           return True
       elif (buffer == "!="):
           self.tokens.append(token("<operador booleano>","!=",linha))
           return True
       elif (buffer == "<="):
           self.tokens.append(token("<operador booleano>","<=",linha))
           return True
       elif (buffer == ">="):
           self.tokens.append(token("<operador booleano>",">=",linha))
           return True
       elif (buffer == ">"):
           self.tokens.append(token("<operador booleano>",">",linha))
           return True
       elif (buffer == "<"):
           self.tokens.append(token("<operador booleano>","<",linha))
           return True
       elif (buffer == "+"):
           self.tokens.append(token("<operador aritmético>","+",linha))
           return True
       elif (buffer == "-"):
           self.tokens.append(token("<operador aritmético>","-",linha))
           return True
       elif (buffer == "*"):
           self.tokens.append(token("<operador aritmético>","*",linha))
           return True
       elif (buffer == "/"):
           self.tokens.append(token("<operador aritmético>","/",linha))
           return True
       elif (buffer == "="):
           self.tokens.append(token("<atribuição>","=",linha))
           return True
       elif (buffer == ","):
           self.tokens.append(token("<virgula>",",",linha))
           return True
       elif (buffer == "True"):
           self.tokens.append(token("<valor booleana>","True",linha))
           return True
       elif(buffer == "False"):
           self.tokens.append(token("<valor booleana>","False",linha))
           return True
       else:
           self.variavel(buffer, linha , texto, i)

    def verifica_delimitadores(self, p, linha):
       if(p == " "):
           return True
       elif(p == "{"):
           self.tokens.append(token("<abre chaves>","{",linha))
           return True
       elif(p == "}"):
           self.tokens.append(token("<fecha chaves>","}",linha))
           return True
       elif(p == "("):
           self.tokens.append(token("<abre parenteses>","(",linha))
           return True
       elif(p == ")"):
           self.tokens.append(token("<fecha parenteses>",")",linha))
           return True
       elif(p == ";"):
           self.tokens.append(token("<fim comando>",";",linha))
           return True
       else:
           return False
       
    def variavel(self, buffer, linha, texto, i):
        if(buffer[0].isalpha and not buffer[0].isdigit()):
            for i in range(len(buffer)):
                if(buffer[i].isalpha() or buffer[i].isdigit()):
                    continue
                else:
                    print("Erro na linha: ", str(linha))
                    quit()
        
            last_token = self.tokens[len(self.tokens) -1] 
            pre_last_token = self.tokens[len(self.tokens) -2] 
            if(buffer not in self.tabela_simbolos):
                
                if(last_token.nome == "<tipo>" and pre_last_token.nome != '<declaração de função>'): 
                        if(last_token.lexema == "Integer"):
                            self.tabela_simbolos[buffer] = Simbolo("Integer",linha)
                        
                        elif(last_token.lexema == "Boolean"):
                            self.tabela_simbolos[buffer] = Simbolo("Boolean",linha)
                elif(pre_last_token.lexema == 'dfunc'):
                    j = i
                    lista_parametros = []
                    qntd_parametros = 0
                    if(last_token.lexema == "Integer"):
                        while texto[j]!= ")":
                            checkInt = texto[j-6] + texto[j-5] + texto[j-4] + texto[j-3] + texto[j-2] + texto[j-1] + texto[j]
                            checkBoolean = texto[j-6] + texto[j-5] + texto[j-4] + texto[j-3] + texto[j-2] + texto[j-1] + texto[j]

                            if(checkInt == "Integer"):
                                qntd_parametros += 1
                                lista_parametros.append("Integer")
                            elif(checkBoolean == "Boolean"):
                                qntd_parametros += 1
                                lista_parametros.append("Boolean")
                            j += 1
                        self.tabela_simbolos[buffer] = SimboloFuncao("dfunc","Integer",linha,qntd_parametros,lista_parametros)
                    elif(last_token.lexema == "Boolean"):
                        while texto[j]!= ")":
                            checkInt = texto[j-6] + texto[j-5] + texto[j-4] + texto[j-3] + texto[j-2] + texto[j-1] + texto[j]
                            checkBoolean = texto[j-6] + texto[j-5] + texto[j-4] + texto[j-3] + texto[j-2] + texto[j-1] + texto[j]

                            if(checkInt == "Integer"):
                                qntd_parametros += 1
                                lista_parametros.append("Integer")
                            elif(checkBoolean == "Boolean"):
                                qntd_parametros += 1
                                lista_parametros.append("Boolean")
                            j += 1
                        self.tabela_simbolos[buffer] = SimboloFuncao("dfunc","Boolean",linha,qntd_parametros,lista_parametros)

                elif(last_token.lexema == "dproc"):
                    j = i
                    lista_parametros = []
                    qntd_parametros = 0
                    
                    while texto[j]!= ")":
                        checkInt = texto[j-6] + texto[j-5] + texto[j-4] + texto[j-3] + texto[j-2] + texto[j-1] + texto[j]
                        checkBoolean = texto[j-6] + texto[j-5] + texto[j-4] + texto[j-3] + texto[j-2] + texto[j-1] + texto[j]

                        if(checkInt == "Integer"):
                            qntd_parametros += 1
                            lista_parametros.append("Integer")
                        elif(checkBoolean == "Boolean"):
                            qntd_parametros += 1
                            lista_parametros.append("Boolean")
                        j += 1

                    self.tabela_simbolos[buffer] = SimboloCaracteristica("proc",linha,qntd_parametros,lista_parametros)

                elif(self.tokens[len(self.tokens) -1].nome == "<abre_parenteses>" or self.tokens[len(self.tokens) -1].nome == "<virgula>"):
                    print('\033[91m' + "Erro variavel {0} não inicializada ".format(buffer) + '\033[0m')
                    quit()

                self.tokens.append(token("<identificador>",buffer,linha))
            else:
                if(self.tokens[len(self.tokens) -1].nome != "<tipo>" and self.tokens[len(self.tokens) -1].nome != "<declaração de procedimento>" and self.tokens[len(self.tokens) -2].nome != "<declaração de função>") :
                    self.tokens.append(token("<identificador>",buffer,linha))
                else:
                    print('\033[91m' + "Erro variavel {0} já existe ".format(buffer) + '\033[0m')
                    quit()
        else:
            for c in buffer:
                 if(c.isdigit()):
                     continue
                 else:
                    print('\033[91m' + "Erro na linha: " + str(linha) + '\033[0m')
                    quit()
                
            self.tokens.append(token("<número>",buffer,linha))

    def imprimir_lista_tokens(self):
        for t in self.tokens:
            print(t.nome + " " + t.lexema + " " + str(t.linha))
    
    def imprimir_tabela_simbolos(self):
        print("SIMBOLOS")
        for t in self.tabela_simbolos:
            if type(self.tabela_simbolos[t]) is Simbolo:
                print(self.tabela_simbolos[t].tipo + " " + t + " " + str(self.tabela_simbolos[t].linha))
            elif type(self.tabela_simbolos[t]) is SimboloCaracteristica:
                print(self.tabela_simbolos[t].tipo + " " + t + " " + str(self.tabela_simbolos[t].linha) + " " + str(self.tabela_simbolos[t].qtdParam) + " " + str(self.tabela_simbolos[t].listParam))
            elif type(self.tabela_simbolos[t]) is SimboloFuncao:
                print(self.tabela_simbolos[t].tipo + " " +str(self.tabela_simbolos[t].tipoRetorno) + " " + t + " "  + str(self.tabela_simbolos[t].linha) + " " + str(self.tabela_simbolos[t].qtdParam) + " " + str(self.tabela_simbolos[t].listParam))
                    
                
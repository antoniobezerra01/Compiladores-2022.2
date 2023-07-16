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
       elif (buffer == "true"):
           self.tokens.append(token("<valor booleana>","true",linha))
           return True
       elif(buffer == "false"):
           self.tokens.append(token("<valor booleana>","false",linha))
           return True
       else:
           self.identificador(buffer, linha , texto, i)

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
       
    def identificador(buffer, linha , texto, i):     
       if(buffer.isalpha()):
           self.tokens.append(token("<identificador>",buffer,linha))
           return True
       else:
           return False
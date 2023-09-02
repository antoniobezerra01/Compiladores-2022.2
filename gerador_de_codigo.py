from token import *

class GeradorCodigoIntermediario:
    def __init__(self, lista_instrucoes):
        self.lista_instrucoes = lista_instrucoes
        self.rotulos = 0
        self.rotulos_while = []
        self.rotulos_if = []
        
    def imprimirListainstrucoes(self):
        for i in range(len(self.lista_instrucoes)):
            for j in range(len(self.lista_instrucoes[i])):
                print(self.lista_instrucoes[i][j].lexema, end=" ")
            print("")


    def gerar_codigo(self):
        arq = open("output.txt", 'w')

        for i in range(len(self.lista_instrucoes)):
            arq.write("\n")
            if(self.lista_instrucoes[i][1].nome) == "<atribuição>": 
                self.gerador_attr(self.lista_instrucoes[i], arq)
            elif(self.lista_instrucoes[i][0].nome) == "<chamada do if>" or self.lista_instrucoes[i][0].nome == "<chamada do else>": 
                self.gerador_if(self.lista_instrucoes[i], arq)
            elif(self.lista_instrucoes[i][0].nome) == "<chamada do while>" or self.lista_instrucoes[i][1].nome == "<fecha chaves>" or self.lista_instrucoes[i][0].nome == "<incondicional>":
                self.gerador_while(self.lista_instrucoes[i], arq)
            elif(self.lista_instrucoes[i][0].nome) == "<chamada de impressão>":
                 arq.write("print({0})".format(self.lista_instrucoes[i][2].lexema) + "\n")
            elif(self.lista_instrucoes[i][0].nome) == "<chamada de retorno>":
                arq.write("{0} {1}".format(self.lista_instrucoes[i][0].lexema, self.lista_instrucoes[i][1].lexema) + "\n")
            elif(self.lista_instrucoes[i][0].nome == "<declaração de procedimento>"):
                self.gerador_proc(self.lista_instrucoes[i], arq)
            elif(self.lista_instrucoes[i][0].nome) == "<chamada de procedimento>":
                self.gerador_chamada_proc(self.lista_instrucoes[i], arq)
            elif(self.lista_instrucoes[i][0].nome) == "<declaração de função>":
                self.gerador_func(self.lista_instrucoes[i], arq)
            elif(self.lista_instrucoes[i][0].nome) == "<end_func>":
                arq.write("end_func" + "\n")
            elif(self.lista_instrucoes[i][0].nome) == "<end_proc>":
                arq.write("end_proc" + "\n")

    def gerador_chamada_proc(self, instrucao, arq):
        contParam = 0
        i = 2
        if len(instrucao) > 3:
            while(instrucao[i + 1].nome != "<fecha parenteses>"):
                i += 1
            while(instrucao[i].nome != "<abre parenteses>"):
                if instrucao[i].lexema != ",":
                    arq.write("_param = {0} ".format(instrucao[i].lexema) + "\n")
                    contParam += 1
                i -= 1
        arq.write("call {0},{1}".format(instrucao[1].lexema, contParam) + "\n")

    def gerador_attr(self, instrucao, arq):
        if(len(instrucao) == 3):
            
            for item in instrucao:
                arq.write(item.lexema + " ")
            arq.write("\n")
        else:
            
            if(instrucao[4].nome == "<abre parenteses>"): 
                contParam = 0
                i = 4
                if len(instrucao) > 5:
                    while(instrucao[i + 1].nome != "<fecha parenteses>"):
                        i += 1
                    while(instrucao[i].nome != "<abre parenteses>"):
                        if instrucao[i].lexema != ",":
                            arq.write("_param = {0} ".format(instrucao[i].lexema) + "\n")
                            contParam += 1
                        i -= 1
                
                arq.write("{0} = call {1},{2}".format(instrucao[0].lexema, instrucao[3].lexema, contParam) + "\n")

            else:  
                arq.write("_t0 = {0} {1} {2}".format(instrucao[2].lexema, instrucao[3].lexema, instrucao[4].lexema) + "\n")
                anterior = 0
                i = 5
                while(i < len(instrucao)):
                    arq.write("_t{0} = _t{1} {2} {3}".format(anterior + 1,anterior,instrucao[i].lexema,instrucao[i+1].lexema) + "\n")

                    anterior += 1

                    i += 2

                arq.write("{0} = _t{1}".format(instrucao[0].lexema,anterior) + "\n")
    
    def gerador_if(self, instrucao, arq):
        if(instrucao[0].lexema == "if"):
            listAux = []

            for item in instrucao:
                if item.lexema not in ["if","(",")"]:
                    listAux.append(item)
            
            self.rotulos += 1
            arq.write("ifFalse ")

            for item in listAux:
                arq.write(item.lexema + "")

            if len(self.rotulos_while) != 0:
                self.rotulos += 1 
            arq.write(" goto: L{0}".format(self.rotulos) + "\n")
            
            self.rotulos_if.append(self.rotulos)
        elif(instrucao[0].lexema == "else"):
            pop = self.rotulos_if.pop()
            arq.write("goto: L{0}".format(self.rotulos + 1) + "\n")
            arq.write("L{0}:".format(pop) + "\n")
            self.rotulos_if.append(self.rotulos + 1)
        else:
            
            pop = self.rotulos_if.pop()
            arq.write("L{0}:".format(pop) + "\n")


    def gerador_while(self, instrucao, arq):
        if(instrucao[0].lexema == "while"):
            listAux = []
            for item in instrucao:
                if item.lexema not in ["while","(",")"]:
                    listAux.append(item)
            if len(self.rotulos_while) % 2 == 0:
                self.rotulos += 1
            else:
                self.rotulos += 2
            self.rotulos_while.append(self.rotulos)
            arq.write("L{0}:".format(self.rotulos) + "\n")
            arq.write("ifW ")
            for item in listAux: 
                arq.write(item.lexema + "")
            arq.write(" goto: L{0}".format(self.rotulos + 1) + "\n")
        elif(instrucao[0].lexema == "break"):
            pop = self.rotulos_while.pop()
            arq.write("goto: L{0}".format(pop + 1) + "\n")
            self.rotulos_while.append(pop)
        elif(instrucao[0].lexema == "continue"):
            pop = self.rotulos_while.pop()
            arq.write("goto: L{0}".format(pop) + "\n")
            self.rotulos_while.append(pop)
        else:
            pop = self.rotulos_while.pop()
            arq.write("goto: L{0}".format(pop) + "\n")
            arq.write("L{0}:".format(pop + 1) + "\n")
    
    def gerador_func(self, instrucao, arq):
        arq.write("func {0}:\nbegin_func:".format(instrucao[2].lexema) + "\n")

    def gerador_proc(self, instrucao, arq):  
        arq.write("proc {0}:\nbegin_proc:".format(instrucao[1].lexema) + "\n")
# -*- coding: utf-8 -*

import copy, random

def imprime_tabuleiro(s,tabuleiro):

	#descobrindo se eh o usuario ou computador
    player = "Computador"
    if s == "u":
        player = "Usuario"
	
    print("O tabuleiro do " + player + " está assim : \n")

    #printa as linhas horizontais da matriz criada
    print(" ")
    for i in range(10):
        print("  " + str(i+1) + "  ", end=" ") 
    print("\n")

    for i in range(10):
	
    #printa a linha vertical da matriz criada
        if i != 9: 
            print(str(i+1) + "  ", end=" ")
        else:
            print(str(i+1) + " ", end=" ")

    #printa as divisoes da matiz e os simbolos de acerto ou tiro na agua com o tabuleiro criado
        for j in range(10):
            if tabuleiro[i][j] == -1:
                print(' ', end=" ")	
            elif s == "u":
                print(tabuleiro[i][j], end=" ")
            elif s == "c":
                if tabuleiro[i][j] == "*" or tabuleiro[i][j] == "@":
                    print(tabuleiro[i][j], end=" ")
                else:
                    print(" ", end=" ")
			
            if j != 9:
                print(" | ", end=" ")
        print()
		
		#printando a linha horizontal
        if i != 9:
           print("   ----------------------------------------------------------")
        else: 
           print() 


def computador_posiciona_navios(board,ships):

	for ship in ships.keys():
	
		#cira posicoes randomicas e valida para ver se eh possivel
		valid = False
		while(not valid):

			x = random.randint(1,10)-1
			y = random.randint(1,10)-1
			o = random.randint(0,1)
			if o == 0: 
				ori = "v"
			else:
				ori = "h"
			valid = validando(board,ships[ship],x,y,ori)

		#pposiciona os navios com as coordenadas definidas anteriormente
		print("Computador posicionando " + ship)
		tabuleiro = posicionando_navios(board,ships[ship],ship[0],ori,x,y)
	
	return tabuleiro


def posicionando_navios(tabuleiro,ship,s,ori,x,y):

	#posiciona os navios de acordo com as posicoes definidas anteriormente
	if ori == "v":
		for i in range(ship):
			tabuleiro[x+i][y] = s
	elif ori == "h":
		for i in range(ship):
			tabuleiro[x][y+i] = s

	return tabuleiro
	
def validando(tabuleiro,ship,x,y,ori):

	#verifica se a coordenada esta valida para o posicionamento dos navios e que nao esta fora dos parametros
	if ori == "v" and x+ship > 10:
		return False
	elif ori == "h" and y+ship > 10:
		return False
	else:
		if ori == "v":
			for i in range(ship):
				if tabuleiro[x+i][y] != -1:
					return False
		elif ori == "h":
			for i in range(ship):
				if tabuleiro[x][y+i] != -1:
					return False
		
	return True

def criando_coordenadas():
	
	while (True):
		user_input = input("Entre as coordenadas (row,col) ? ")
		try:
			#caso o usuario entre com 2 valores separados por virgula
			coor = user_input.split(",")
			if len(coor) != 2:
				raise Exception("Input inválido , muitas/poucas coordenadas.");

			#checando as coordenadas sao int (inteiras)
			coor[0] = int(coor[0])-1
			coor[1] = int(coor[1])-1

			#checa se ambas as coordenadas estao entre 1 e 10 e sao int tambem
			if coor[0] > 9 or coor[0] < 0 or coor[1] > 9 or coor[1] < 0:
				raise Exception("Input inválido.Por favor utilize valores entre 1 a 10.")

			#se sim retorna as coordenadas
			return coor
		#caso o usuario nao entre com valores numericos nas coordenadas
		except ValueError:
			print("Input inválido.Entre com valores numéricos para as  coordenadas")
		except Exception as e:
			print(e)

def make_move(board,x,y):
	
	#faz um chute no tabuleiro retornando o resultado (acerto , tiro na agua , ou esse tiro ja foi chutado tente outro)
	if board[x][y] == -1:
		return "tiro na água"
	elif board[x][y] == '*' or board[x][y] == '$':
		return "tente novamente"
	else:
		return "acerto"

def user_move(tabuleiro):
	
	#pega a coordenada dado como input do usuario e faz um chutw
	#se o chute for um acerto checa se o navio afundo e a condicao de vitoria
	while(True):
		x,y = criando_coordenadas()
		res = make_move(tabuleiro,x,y)
		if res == "acerto":
			print("Acerto em " + str(x+1) + "," + str(y+1))
			acerto_tiros(tabuleiro,x,y)
			tabuleiro[x][y] = '$'
			if checar_vitoria(tabuleiro):
				return "Vitoria"
		elif res == "tiro na água":
			print("Desculpa, " + str(x+1) + "," + str(y+1) + " é tiro na água.")
			tabuleiro[x][y] = "*"
		elif res == "tente novamente":
			print("Desculpa,mais essa coordenada já foi atingida.Por favor tente novamente")

		if res != "tente novamente":
			return tabuleiro
	
def acerto_tiros(tabuleiro,x,y):

	#Atreves da nomenclatura descobre qual navio foi atingido
	if tabuleiro[x][y] == "P":
		ship = "PortaAviões"
	elif tabuleiro[x][y] == "C":
		ship = "Cruzador"
	elif tabuleiro[x][y] == "S":
		ship = "Submarino"
	elif tabuleiro[x][y] == "D":
		ship = "Destroyer"
	elif tabuleiro[x][y] == "N":
		ship = "NavioGuerra"
	
	#marca a celula que foi atingida e diz qual navio foi afundado para que o mesmo navio nao seja afundado 2 vezes
	tabuleiro[-1][ship] -= 1
	if tabuleiro[-1][ship] == 0:
		print(ship +  "afundado")
		

def checar_vitoria(tabuleiro):
	
	#caso a celula nao retorna um acerto ou tiro na agua com os icones retorna False
	for i in range(10):
		for j in range(10):
			if tabuleiro[i][j] != -1 and tabuleiro[i][j] != '*' and tabuleiro[i][j] != '@':
				return False
	return True

def main():

	#os tipos de navios salvos em um dicionario
	ships = {"PortaAviões":5,
		     "NavioGuerra":4,
 		     "Submarino":3,
		     "Destroyer":3,
		     "Cruzador":2}

	#criando o tabuleiro 10x10
	tabuleiro = []
	for i in range(10):
		tabuleiro_row = []
		for j in range(10):
			tabuleiro_row.append(-1)
		tabuleiro.append(tabuleiro_row)

	#Faz um setup do tabuleiro do PC.(
	comp_tabuleiro= copy.deepcopy(tabuleiro)

	comp_tabuleiro.append(copy.deepcopy(ships))

	comp_tabuleiro =computador_posiciona_navios(comp_tabuleiro,ships)
	print(comp_tabuleiro)

	#Main loop
	while(1):
		comp_tabuleiro = user_move(comp_tabuleiro)

		#checa se o usuario venceu
		if comp_tabuleiro == "vitoria":
			print("Usuario venceu! :)")
			quit()
			
		#mostra o tabulerio no cpu
		imprime_tabuleiro("c",comp_tabuleiro)
	
if __name__=="__main__":
	main()

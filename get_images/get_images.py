#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Gustavo Fernandes dos Santos
# Email: gfdsantos@inf.ufpel.edu.br
# versão 0.72

from datetime import datetime
from subprocess import call
from calendar import monthrange
import os
import sys

INTERVALO = 30
MIN_SUP = 30
MIN_INF = 0

# Função 
def imprimirInfo():
	"""
	Imprime as informaçoes do desenvolvedor
	"""
	call(["clear"])
	print("[*] Downloader de imagens do INMET. v0.72")
	print("[*] Autor: Gustavo Fernandes dos Santos")
	print("[*] Email: gfdsantos@inf.ufpel.edu.br")
	print("    -----------------------------------")
	print("[!] Imagens são produto do GOES - América Latina - Topo das nuvens")
	print("    -----------------------------------")


# 
def print_uso_batch():
	call(["clear"])
	print("""[?] Modo de uso em batch:
    $ ./get_images.py numero_de_imagens intervalo
    *>\tnumero_imagens:  numero de imagens para baixar
    *>\tintervalo:       intervalo de horarios entre as imagens
    	OU
    $ ./get_images.py numero_de_imagens intervalo minuto_superior minuto_inferior
    *>\tnumero_imagens:  numero de imagens para baixar
    *>\tintervalo:       intervalo de horarios entre as imagens
    *>\tminuto_superior: 
    *>\tminuto_inferior: """)


def print_erro():
	print("[-] Erro na inicializaçao.")
	print("[!] Execute novamente utilizando como argumento \"ajuda\".")
	print("[!] Exemplo: $ ./get_imagens.py ajuda")


def testaConexao():
	print("[!] Estabelecendo conexao...")
	programa = """wget -q --spider http://www.inmet.gov.br

					if [ $? -eq 0 ]; then
    					echo "[+] Online"
					else
    					echo "[-] Offline"
					fi"""

	script = open("script.sh", "w")
	script.write(programa)
	script.close()
	res = call(["sh", "script.sh"])
	call(["rm", "script.sh"])
	if res == "[-] Offline":
		sys.exit("[-] Sem conexão.")


def existeImagem(link):
	print("Testando o link:\n   ~>", link)
	programa = []
	programa.append('wget -q --spider ' + link + '\n')
	programa.append('if [ $? -eq 0 ]; then\n')
	programa.append('	echo "[+] Online"\n')
	programa.append('else\n')
	programa.append('	echo "[-] Offline"\n')
	programa.append('fi')

	script = open("script.sh", "w")
	script.writelines(programa)
	script.close()
	res = call(["sh", "script.sh"])
	call(["rm", "script.sh"])
	if res == "[-] Offline":
		print("[-] Sem conexão.")
		return False
	else:
		return True

def existeImagem2(link):
	print("[!] Testando o link:")
	print("    " + link)
	c = call(["wget", "-q", "--spider", link])
	if c != 0:
		print("[-] Não foi possível atingir o alvo.")
		return False
	else:
		print("[+] Link ok.")
		return True


# usa o parâmetro de intervalo INTERVALO
def retrocede(ano, mes, dia, hora, minuto):
	minuto = minuto - INTERVALO
	if minuto < 0:
		hora = hora - 1
		if hora < 0:
			hora = hora + 24
			dia = dia - 1
			if dia <= 0:
				mes = mes - 1
				if mes <= 0:
					mes = 1
					ano = ano - 1

				dia = monthrange(ano, mes)
				
		minuto = MIN_SUP
	else:
		minuto = MIN_INF
	return (ano, mes, dia, hora, minuto)


def gerarLinks(arg):
	hora = datetime.now().hour
	minuto = datetime.now().minute
	dia = datetime.now().day
	mes = datetime.now().month
	ano = datetime.now().year

	if minuto > 0: minuto = INTERVALO
	else: minuto = 0

	if arg == 0:
		qtd = input("[?] Quantidade de imagens\n ~> ")
	else:
		qtd = arg

	if int(qtd) == 0:
		sys.exit("Ok.")
	elif int(qtd) < 0:
		sys.exit("[!] Inválido. A quantidade de imagens deve ser um número inteiro positivo.")

	print("[+] Gerando links...")

	preLink = "http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_TN"

	links = []
	sano = ""
	smes = ""
	sdia = ""
	shora = ""
	sminuto = ""

	i = 0
	t = int(qtd)

	e = 0

	while i < t:
		ano, mes, dia, hora, minuto = retrocede(ano, mes, dia, hora, minuto)

		sano = str(ano)
		if mes < 10: smes = "0" + str(mes)
		else: smes = str(mes)
		if dia < 10: sdia = "0" + str(dia)
		else: sdia = str(dia)
		if hora < 10: shora = "0" + str(hora)
		else: shora = str(hora)
		if minuto < 10: sminuto = "0" + str(minuto)
		else: sminuto = str(minuto)

		link = preLink + sano + smes + sdia + shora + sminuto + ".jpg"

		if existeImagem2(link):
			links.append(link)
			e = 0
		else:
			i = i - 1
			e = e + 1
			if e >= 10: 
				print("[-] Verifique a sua conexão, se o INMET está online e")
				print("    se o programa está gerando os links corretos.")
				sys.exit("[!] Saindo...")

		i = i + 1

	return links



def baixarImagens(links):
	print("[+] Baixando imagens...\n")
	if not os.path.isdir("imagens/"):
		call(["mkdir", "imagens"])

	r = []
	for link in links:
		n = call(["wget", "-q", "--show-progress", link])
		r.append(n)

	return r


def moverImagens():
	print("[!] Tentando criar o diretório \"imagens\"")
	if not os.path.isdir("imagens/"):
		cria_dir = "mkdir imagens"
		script = open("script.sh", "w")
		script.writelines(cria_dir)
		script.close()
		call(["sh", "script.sh"])
		call(["rm", "script.sh"])
	else:
		print("[!] O diretório já existe.")
		print("[!] Movendo imagens...")
		move_imagens = "mv *.jpg imagens/"
		script = open("script.sh", "w")
		script.writelines(move_imagens)
		script.close()
		call(["sh", "script.sh"])
		call(["rm", "script.sh"])
		print("[+] Ok.")

	print("[+] Pronto.")


def modo_batch(arg):
	print('[*] Modo batch')
	imprimirInfo()
	testaConexao()
	links = gerarLinks(arg)
	r = baixarImagens(links)
	for i in r:
		if i != 0:
			print("[-] A imagem referente ao horario requisitado não existe.")
			testaConexao()
			links = gerarLinks(arg)
			r = baixarImagens(links)
	moverImagens()


def modo_iterativo(arg):
	print('[*] Modo iterativo')
	imprimirInfo()
	testaConexao()
	links = gerarLinks(arg)
	r = baixarImagens(links)
	for i in r:
		if i != 0:
			print("[-] A imagem referente ao horario requisitado não existe.")
			d = input("[?] Deseja tentar novamente? [S, n] \n\t> ")
			if d == "S" or d == "s":
				testaConexao()
				links = gerarLinks(arg)
				r = baixarImagens(links)
			else:
				sys.exit("[!] Ok, saindo...")
	moverImagens()


def main():
	argumentos = sys.argv

	if len(argumentos) > 0: # a execuçao possui argumentos
		if argumentos[1] == 'ajuda':
			print_uso_batch()
		elif len(argumentos) == 3: # comando + n_imagens + interv
			if argumentos[1].isdigit() and argumentos[2].isdigit():
				n_imagens = int(argumentos[1])
				INTERVALO = int(argumentos[2])
				if INTERVALO <= 0 or n_imagens <= 0:
					print_erro()
					sys.exit(0)
				else:
					modo_batch(n_imagens)
			else:
				print_erro()
				sys.exit(0)
		elif len(argumentos) == 5: # comando + n_imagens + interv + min_sup + min_inf
			if argumentos[1].isdigit() and argumentos[2].isdigit() and argumentos[3].isdigit() and argumentos[4].isdigit():
				n_imagens = int(argumentos[1])
				INTERVALO = int(argumentos[2])
				MIN_SUP = int(argumentos[3])
				MIN_INF = int(argumentos[4])
				if INTERVALO <= 0 or n_imagens <= 0 or MIN_INF < 0 or MIN_SUP < 0:
					print_erro()
					sys.exit(0)
				else:
					modo_batch(n_imagens)
			else:
				print_erro()
				sys.exit(0)
		else:
			print_erro()
			sys.exit(0)
	else: 
		modo_iterativo(0)


if __name__ == "__main__":
	main()



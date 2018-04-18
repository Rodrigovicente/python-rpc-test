import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')


sair = 0
retorno = "."

while sair != 1:
	entrada = input("Opções: \n \t1 - Adicionar/alterar nota;\n \t2 - Consultar nota;\n \t3 - Consultar notas;\n \t4 - Consultar CR;\n \t5 - Sair.\n\nEntrada: ")

	if entrada == "1":
		print("ADICIONAR/ALTERAR NOTA")
		matricula = input("Matrícula: ")
		disciplina = input("Disciplina: ")
		nota = input("Nota: ")
		retorno = s.cadastrar_nota(int(matricula), disciplina, float(nota))

	elif entrada == "2":
		print("CONSULTAR NOTA")
		matricula = input("Matrícula: ")
		disciplina = input("Disciplina: ")
		retorno = s.consultar_nota(int(matricula), disciplina)

	elif entrada == "3":
		print("CONSULTAR NOTAS")
		matricula = input("Matrícula: ")
		retorno = s.consultar_notas(int(matricula))

	elif entrada == "4":
		print("CONSULTAR CR")
		matricula = input("Matrícula: ")
		retorno = s.consultar_cr(int(matricula))

	elif entrada == "5":
		sair = 1
		retorno = "Tchau."

	print(retorno)



# Print list of available methods
#print(s.system.listMethods())

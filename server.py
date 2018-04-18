from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from pymongo import MongoClient
import numpy as np

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
#with SimpleXMLRPCServer(("localhost", 8000), requestHandler = RequestHandler) as server:
server = SimpleXMLRPCServer(("localhost", 8000), requestHandler = RequestHandler)
server.register_introspection_functions()

mongo_client = MongoClient('localhost', 27017)

banco_notas = mongo_client.boletim_db

boletim_collection = banco_notas.test_collection
boletim_collection = banco_notas.boletim_collection


def cadastrar_nota (mat, cod_disc, nota):
	if boletim_collection.find_one({"matricula": mat, "disciplina": cod_disc}) == None:
		#resgiter new one
		registro_nota = { "matricula": mat, "disciplina": cod_disc, "nota": nota }

		boletim_collection.insert_one(registro_nota)

		return True

	else:
		#update
		boletim_collection.update_one({'matricula': mat, 'disciplina': cod_disc}, {'$set': {'nota': nota}})

		return False

server.register_function(cadastrar_nota, 'cadastrar_nota')


def consultar_nota (mat, cod_disc):
	registro = boletim_collection.find_one({"matricula": mat, "disciplina": cod_disc})
	if registro != None:
		return registro['nota']
	else:
		return "Não há notas cadastradas para este aluno nesta disciplina."

server.register_function(consultar_nota, 'consultar_nota')


def consultar_notas (mat):
	lista_notas = []
	lista_registros = boletim_collection.find({"matricula": mat})
	if lista_registros.count() != 0:
		for registro in lista_registros:
			nota = registro['nota']
			disciplina = registro['disciplina']
			lista_notas.append([nota, disciplina])

		return lista_notas
	else:
		return "Não há notas cadastradas para este aluno."

server.register_function(consultar_notas, 'consultar_notas')

def consultar_cr (mat):
	lista_notas = []
	lista_registros = boletim_collection.find({"matricula": mat})
	if lista_registros.count() != 0:
		for registro in lista_registros:
			lista_notas.append(registro['nota'])

		valor_retorno = np.mean(lista_notas).astype(type('float', (float,), {}))
	else:
		valor_retorno = "Não há notas registradas para este aluno."

	return valor_retorno

server.register_function(consultar_cr, 'consultar_cr')

print("rodando.")

# Run the server's main loop
server.serve_forever()

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from pymongo import MongoClient

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


#def consultar_nota (mat, cod_disc):


def consultar_notas (mat):
	lista_notas = []
	lista_registros = boletim_collection.find({"matricula": mat})
	if lista_registros != None:
		for registro in lista_registros:
			nota = registro['nota']
			disciplina = registro['disciplina']
			lista_notas.append([nota, disciplina])

	return lista_notas

server.register_function(consultar_notas, 'consultar_notas')

#def consultar_cr (mat):

print("rodando.")

# Run the server's main loop
server.serve_forever()

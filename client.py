import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

#retorno = s.cadastrar_nota(4, 'calc', 8.5)
retorno = s.consultar_notas(1)

print(retorno)

# Print list of available methods
#print(s.system.listMethods())

import os
import time
import json
import redis
import datetime
import mysql.connector
from mysql.connector import errorcode
from pymongo import MongoClient, errors

# Funções auxuliares
def clear_screen():
    command = 'cls' if os.name in ('nt', 'dos') else 'clear'
    os.system(command)

def formatar_valor(valor):
    integer_part, decimal_part = f"{valor:.2f}".split(".")
    integer_part_with_dots = ".".join([integer_part[max(i-3, 0):i] for i in range(len(integer_part), 0, -3)][::-1])
    formatted_value = f"R${integer_part_with_dots},{decimal_part}"

    return formatted_value

# Funções do CRUD
def create_cliente(cursor, db, cnx):
    inserir_clientes = "INSERT INTO Cliente (cpf, nome, endereco, cidade, uf, email) VALUES (%(cpf)s, %(nome)s, %(endereco)s, %(cidade)s, %(uf)s, %(email)s)"
    
    cliente = dict()
    cliente['nome'] = input("Digite o nome: ")
    cliente['cpf'] = input("Digite o CPF: ")
    cliente['email'] = input("Digite o e-mail: ")
    cliente_2 = dict()
    cliente_2['endereco'] = input("Digite o endereco: ")
    cliente_2['cidade'] = input("Digite a cidade: ")
    cliente_2['uf'] = input("Digite a UF: ")
    amigo_cpf = input("Digite o CPF do amigo que indicou: ")
    amigo = db.Pessoa.find_one({"cpf": amigo_cpf})
    if amigo:
        amigo['amigos'].append({"cpf": cliente['cpf']})
        db.Pessoa.update_one({"cpf": amigo_cpf}, {"$set": {"amigos": amigo['amigos']}})
        cliente['amigos'] = [amigo_cpf]
    else:
        print("Amigo não encontrado!")
        cliente['amigos'] = []
    db.Pessoa.insert_one(cliente)
    cliente.update(cliente_2)
    cliente.pop('amigos')
    cliente.pop('_id')
    cursor.execute(inserir_clientes, cliente)
    cnx.commit()
    print("Cliente criado!")

    time.sleep(2)
    clear_screen()

def create_compras(cursor, cnx):
    inserir_compras = "INSERT INTO Compra (produto, valor, data, id_cliente) VALUES (%(produto)s, %(valor)s, %(data)s, %(id_cliente)s)"
    
    cpf = input("Digite o CPF do cliente fazendo a compra: ")
    id_cliente_consulta = f"select id from Cliente where cpf = '{cpf}'"
    cursor.execute(id_cliente_consulta)
    id_cliente = cursor.fetchall()[0][0]
    
    compra = dict()
    compra['produto'] = input("Digite o produto: ")
    compra['valor'] = input("Digite o valor: ")
    compra['data'] = datetime.datetime.strptime(input("Digite a data: "), '%d/%m/%Y').date()
    compra['id_cliente'] = id_cliente
    cursor.execute(inserir_compras, compra)
    cnx.commit()
    print("Compra Adicionada!")

    time.sleep(2)
    clear_screen()

def read_cliente(cursor):
    try:
        cpf = input("Escreva o CPF do cliente que você quer encontrar: ")
        consulta_cliente = f"select cpf, nome, endereco, cidade, uf, email from Cliente where cpf = '{cpf}'"
        cursor.execute(consulta_cliente)
        cliente_cursor = cursor.fetchall()[0]

        print("Dados do cliente: ")
        print(f"- Nome: {cliente_cursor[1]}")
        print(f"- CPF: {cliente_cursor[0]}")
        print(f"- E-mail: {cliente_cursor[5]}")
        print(f"- UF: {cliente_cursor[4]}")
        print(f"- Cidade: {cliente_cursor[3]}")
        print(f"- Endereço: {cliente_cursor[2]}")

        time.sleep(4)
        clear_screen()
    except:
        print("Cliente não existe!")
        time.sleep(2)
        clear_screen()

def read_compra(cursor):
    try:
        codigo = input("Escreva o código da compra que você quer encontrar: ")
        consulta_compra = f"select * from Compra where codigo = {codigo}"
        cursor.execute(consulta_compra)
        compra_cursor = cursor.fetchall()[0]

        id_cliente = compra_cursor[4]
        consulta_nome = f"select nome from Cliente where id = {id_cliente}"
        cursor.execute(consulta_nome)
        nome = cursor.fetchall()[0][0]

        data = compra_cursor[3].strftime("%d/%m/%Y")
        print("Dados da compra: ")
        print(f"- Produto: {compra_cursor[1]}")
        print(f"- Valor: {formatar_valor(compra_cursor[2])}")
        print(f"- Data: {data}")
        print(f"- Nome: {nome}")

        time.sleep(4)
        clear_screen()
    except:
        print("Compra não existe!")
        time.sleep(2)
        clear_screen()

def update(cursor, db, cnx):
    try:
        cpf = input("Escreva o CPF do cliente que você quer encontrar: ")

        while True:
            print("Dados que você pode atualizar: ")
            print("1 - Nome")
            print("2 - Endereço")
            print("3 - Cidade")
            print("4 - UF")
            print("5 - E-mail")
            print("6 - Digite qualquer outra tecla para sair")
            dado_atualizado = int(input("Qual dado você quer atualizar: "))
            clear_screen()
            if dado_atualizado == 1:
                dado = input("Digite o nome atualizado: ")
                atualizar = f"UPDATE Cliente SET nome = '{dado}' WHERE cpf = '{cpf}'"
                db.Pessoa.update_one({"cpf": cpf}, {"$set": {"nome": dado}})
            elif dado_atualizado == 2:
                dado = input("Digite o endereço atualizado: ")
                atualizar = f"UPDATE Cliente SET endereco = '{dado}' WHERE cpf = '{cpf}'"
            elif dado_atualizado == 3:
                dado = input("Digite a cidade atualizada: ")
                atualizar = f"UPDATE Cliente SET cidade = '{dado}' WHERE cpf = '{cpf}'"
            elif dado_atualizado == 4:
                dado = input("Digite a UF atualizada: ")
                atualizar = f"UPDATE Cliente SET uf = '{dado}' WHERE cpf = '{cpf}'"
            elif dado_atualizado == 5:
                dado = input("Digite o E-mail atualizado: ")
                atualizar = f"UPDATE Cliente SET email = '{dado}' WHERE cpf = '{cpf}'"
                db.Pessoa.update_one({"cpf": cpf}, {"$set": {"email": dado}})
            else: 
                break
            cursor.execute(atualizar)
            cnx.commit()
            print("Dado atualizado!")
            time.sleep(2)
            clear_screen()
    except:
        print("Cliente não existe!")
        time.sleep(2)
        clear_screen()

def delete(cursor, db, cnx):
    cpf = input("Escreva o CPF do cliente que você quer deletar do banco de dados: ")

    cliente = db.Pessoa.find_one({"cpf": cpf})
    if cliente:
        db.Pessoa.delete_one({"cpf": cpf})

        clientes = db.Pessoa.find()
        for c in clientes:
            amigos = c.get('amigos', [])
            novos_amigos = [amigo for amigo in amigos if amigo['cpf'] != cpf]
            if len(novos_amigos) != len(amigos):
                db.Pessoa.update_one({"cpf": c['cpf']}, {"$set": {"amigos": novos_amigos}})
    
    try:
        id_cliente_consulta = f"SELECT id FROM Cliente WHERE cpf = '{cpf}'"
        cursor.execute(id_cliente_consulta)
        id_cliente = cursor.fetchone()[0]

        deletar_compras = f"DELETE FROM Compra WHERE id_cliente = {id_cliente}"
        cursor.execute(deletar_compras)

        deletar_cliente = f"DELETE FROM Cliente WHERE cpf = '{cpf}'"
        cursor.execute(deletar_cliente)

        cnx.commit()
    except mysql.connector.Error as error:
        print(f"Erro ao deletar o cliente: {error}")

    print(f"Cliente deletado!")
    time.sleep(4)
    clear_screen()

# Funções do REDIS
def verificar_e_buscar_redis(redis_client, chave):
    if redis_client.exists(chave):
        return json.loads(redis_client.get(chave))
    return None

def adicionar_dados_redis(redis_client, chave, dados):
    redis_client.set(chave, json.dumps(dados))

def unir_dados_e_armazenar(cursor, db, redis_client):
    try:
        codigo_compra = input("Digite o código da compra: ")

        consulta_compra = f"SELECT produto, valor, id_cliente FROM Compra WHERE codigo = {codigo_compra}"
        cursor.execute(consulta_compra)
        compra = cursor.fetchone()
        if not compra:
            print("Compra não encontrada no MySQL!")
            return

        produto, valor, id_cliente = compra

        consulta_cliente = f"SELECT cpf, nome FROM Cliente WHERE id = {id_cliente}"
        cursor.execute(consulta_cliente)
        cliente = cursor.fetchone()
        if not cliente:
            print("Cliente não encontrado no MySQL!")
            return

        cpf_cliente, nome_cliente = cliente

        amigo_cpf = None
        while True:
            amigo_cpf = input("Digite o CPF do amigo: ")
            cliente_mongo = db.Pessoa.find_one({"cpf": cpf_cliente})
            if any(a['cpf'] == amigo_cpf for a in cliente_mongo.get('amigos', [])):
                amigo = db.Pessoa.find_one({"cpf": amigo_cpf})
                break
            print("Amigo não encontrado no MongoDB ou não é amigo do cliente! Por favor, digite novamente.")

        amigo = db.Pessoa.find_one({"cpf": amigo_cpf})

        dados = {
            "nome_cliente": nome_cliente,
            "produto": produto,
            "valor": formatar_valor(valor),
            "nome_amigo": amigo['nome']
        }

        redis_chave = f"compra_{codigo_compra}"

        dados_no_redis = verificar_e_buscar_redis(redis_client, redis_chave)
        if dados_no_redis:
            print("Dados já estão no Redis.")
        else:
            adicionar_dados_redis(redis_client, redis_chave, dados)
            print("Dados adicionados ao Redis.")
        time.sleep(4)
    except mysql.connector.Error as error:
        print(f"Erro ao consultar o MySQL: {error}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    clear_screen()

def recuperar_dados_redis(redis_client):
    codigo_compra = input("Digite o código da compra para recuperar os dados: ")
    
    redis_chave = f"compra_{codigo_compra}"
    dados_no_redis = verificar_e_buscar_redis(redis_client, redis_chave)
    if dados_no_redis:
        print("Dados encontrados no Redis:")
        for chave, valor in dados_no_redis.items():
            print(f"{chave}: {valor}")
    else:
        print("Nenhum dado encontrado no Redis.")
    time.sleep(4)
    clear_screen()

# Parte principal
try:
    cnx = mysql.connector.connect(host='localhost', user='root', password='root', database='trabalho3')
    client = MongoClient('localhost', 27017)
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    cursor = cnx.cursor(buffered=True)
    db = client['banco']

    while True:
        print("O que você quer fazer?")
        print("1 - Inserir cliente")
        print("2 - Inserir compra")
        print("3 - Ler cliente")
        print("4 - Ler compra")
        print("5 - Atualizar dados de clientes")
        print("6 - Deletar cliente")
        print("7 - Unir dados e armazenar no Redis")
        print("8 - Recuperar dados do Redis")
        print("9 - Digite qualquer outra tecla para parar")
        opcao = int(input("Digite o número do que você quer fazer aqui: "))
        clear_screen()

        if opcao == 1:
            create_cliente(cursor, db, cnx)
        elif opcao == 2:
            create_compras(cursor, cnx)
        elif opcao == 3:
            read_cliente(cursor)
        elif opcao == 4:
            read_compra(cursor)
        elif opcao == 5:
            update(cursor, db, cnx)
        elif opcao == 6:
            delete(cursor, db, cnx)
        elif opcao == 7:
            unir_dados_e_armazenar(cursor, db, redis_client)
        elif opcao == 8:
            recuperar_dados_redis(redis_client)
        else:
            break

    cursor.close()
    cnx.close()
except mysql.connector.Error as error:
    if error.errno == errorcode.ER_BAD_DB_ERROR:
        print("Banco de dados não existe!")
    elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Nome de usuário ou senha inválidos!")
    else:
        print(error)
except errors.ServerSelectionTimeoutError as error2:
    print("Erro de conexão com o MongoDB: ", error2)
finally:
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()
    if 'client' in locals():
        client.close()

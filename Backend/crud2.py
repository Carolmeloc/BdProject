import asyncpg
from fastapi import Depends, FastAPI, HTTPException, Lifespan
from pydantic import BaseModel
from typing import Optional, List

# Configuração da conexão
DB_NAME = "ProjectBD"
DB_USER = "postgres"
DB_PASSWORD = "Uj78tzyqca"
DB_HOST = "localhost"
DB_PORT = "5432"

# Criando modelo de dados com o Pydantic
class Cliente(BaseModel):
    name: str
    lastName: str
    cpf: str
    phone: str
    cep: str
    numberhome: str
    id: Optional[int] = None

# Criando a FastAPI
app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.post("/clientes/", response_model=Cliente)
async def criar_cliente(cliente: Cliente):
    await inserir_client(cliente)
    return cliente

@app.get("/clientes/", response_model=List[Cliente])
async def listar_clientes():
    return await ler_client()

@app.get("/clientes/{cliente_id}", response_model=Cliente)
async def obter_cliente(cliente_id: int):
    cliente = await pesquisar_um(cliente_id)
    if cliente:
        return cliente
    else:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

async def inserir_client(cliente: Cliente):
    await app.state.db.execute('''
        INSERT INTO clients(name, lastName, cpf, phone, cep, numberhome) VALUES($1, $2, $3, $4, $5, $6)
    ''', cliente.name, cliente.lastName, cliente.cpf, cliente.phone, cliente.cep, cliente.numberhome)

async def ler_client():
    rows = await app.state.db.fetch("SELECT * FROM clients WHERE active = TRUE;")
    return [Cliente(**row) for row in rows]

async def pesquisar_um(client_id: int):
    row = await app.state.db.fetchrow("SELECT * FROM clients WHERE id = $1 AND active = TRUE;", client_id)
    if row:
        return Cliente(**row)
    return None

# # C - Criar
# def inserir_client(name,lastName,cpf,phone,cep,numberhome):
#     query = "INSERT INTO clients (name,lastName,cpf,phone,cep,numberhome) VALUES (%s, %s, %s, %s, %s, %s);"
#     cursor.execute(query, (name,lastName,cpf,phone,cep,numberhome))
#     connection.commit()

# # R - Ler
# def ler_client():
#     cursor.execute("SELECT * FROM clients WHERE active = TRUE;")
#     return cursor.fetchall()

# # Pesquisar um
# def pesquisar_um(client_id):
#     cursor.execute("SELECT * FROM clients WHERE id = %s AND active = TRUE;", (client_id,))
#     return cursor.fetchall()  

# # Pesquisar por nome
# def pesquisar_por_nome(name):
#     cursor.execute("SELECT * FROM clients WHERE name = %s AND active = TRUE;", (name,))
#     return cursor.fetchall()

# # U - Atualizar
# def atualizar_client(id, name,lastName,cpf,phone,cep,numberhome):
#     query = "UPDATE clients SET name = %s, lastname = %s, cpf = %s, phone = %s,cep = %s, numberhome = %s WHERE id = %s;"
#     cursor.execute(query, (name,lastName,cpf,phone,cep,numberhome, id))
#     connection.commit()

# # D - Deletar
# # def deletar_client(id):
# #     query = "DELETE FROM clients WHERE id = %s;"
# #     cursor.execute(query, (id))
# #     connection.commit()

# def desativar_cliente(id):
#     query = "UPDATE clients SET active = FALSE WHERE id = %s;"
#     cursor.execute(query, (id,))
#     connection.commit()

# def venda(client_id, date, product_ids):
#     # Primeiro, inserimos uma nova venda na tabela 'sales' e recuperamos o ID gerado para essa venda
#     cursor.execute("INSERT INTO sales (client_id, date) VALUES (%s, %s) RETURNING id;", (client_id, date))
#     sales_id = cursor.fetchone()[0]

#     # Em seguida, inserimos os IDs dos produtos como um array na tabela 'sales_products'
#     cursor.execute("INSERT INTO sales_products (sales_id, product_ids) VALUES (%s, %s);", (sales_id, product_ids))

#     connection.commit()


# # Relatório de Vendas    ---- > ajeitar as tabelas sales e stok no BD
def relatorio_vendas():
    cursor.execute("SELECT COUNT(*) FROM sales;")
    total_sales = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(price) FROM sales_products sp JOIN products p ON p.id = ANY(sp.product_ids);")
    total_value = cursor.fetchone()[0]
    print("----- Relatório de Vendas -----")
    print(f"Total de Vendas Realizadas: {total_sales}")
    print(f"Valor Total das Vendas: R$ {total_value:.2f}")

# # Relatório de Estoque
def relatorio_estoque():
    cursor.execute("SELECT COUNT(*) FROM products WHERE in_stock = true;")
    total_items = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(price) FROM products WHERE in_stock = true;")
    total_value = cursor.fetchone()[0]
    print("----- Relatório de Estoque -----")
    print(f"Total de Produtos em Estoque: {total_items}")
    print(f"Valor Total em Estoque: R$ {total_value:.2f}")

# # Relatório de Clientes
def relatorio_clientes():
    cursor.execute("SELECT COUNT(*) FROM clients;")
    total_clients = cursor.fetchone()[0]
    print("----- Relatório de Clientes -----")
    print(f"Total de Clientes Cadastrados: {total_clients}")


# Função para exibir o menu e obter a escolha do usuário
def mostrar_menu():
    print("Menu:")
    print("1 - Inserir Cliente")
    print("2 - Ler Clientes")
    print("3 - Pesquisar Cliente por ID")
    print("4 - Pesquisar Cliente por Nome")
    print("5 - Atualizar Cliente")
    print("6 - Excluir Cliente")
    print("7 - Gerar Relatórios")
    print("8 - Sair")
    return input("Escolha uma opção: ")

while True:
    
    opcao = mostrar_menu()

    # C - Criar
    if opcao == "1":
        name = input("Nome: ")
        lastName = input("Sobrenome: ")
        cpf = input("CPF: ")
        phone = input("Telefone: ")
        cep = input("CEP: ")
        numberhome = input("Número da casa: ")
        inserir_client(name, lastName, cpf, phone, cep, numberhome)

    # R - Ler
    elif opcao == "2":
        clientes = ler_client()
        for cliente in clientes:
            print(cliente)

    # Pesquisar um
    elif opcao == "3":
        client_id = input("ID do Cliente: ")
        cliente = pesquisar_um(client_id)
        if cliente:
            print(cliente)
        else:
            print("O cliente não foi encontrado ou está inativo.")

    # Pesquisar por nome
    elif opcao == "4":
        name = input("Nome do Cliente: ")
        clientes = pesquisar_por_nome(name)
        if clientes:
            for cliente in clientes:
                print(cliente)
        else:
            print("O cliente não foi encontrado ou está inativo.")

    # U - Atualizar
    elif opcao == "5":
        client_id = input("ID do Cliente a ser atualizado: ")
        name = input("Novo Nome: ")
        lastName = input("Novo Sobrenome: ")
        cpf = input("Novo CPF: ")
        phone = input("Novo Telefone: ")
        cep = input("Novo CEP: ")
        numberhome = input("Novo Número da casa: ")
        atualizar_client(client_id, name, lastName, cpf, phone, cep, numberhome)

    # D - Deletar
    elif opcao == "6":
        client_id = input("ID do Cliente a ser desativado: ")
        desativar_cliente(client_id)
    
    elif opcao == "7":
      relatorio_vendas()
      relatorio_estoque()
      relatorio_clientes()
    
    elif opcao == "8":
        # Sair do programa
        break

    else:
        print("Opção inválida.")

# Exemplo de uso:

# Considerando que você já está conectado ao banco de dados e tem um cursor disponível...
# Criar uma nova compra para o cliente de ID 1, na data '20231001', para os produtos de IDs 2, 3 e 4



# Testando as funções:
# inserir_client('Flor','Mendes','55555555555','839999999997','58312020','555');
# print(ler_client())
# atualizar_client(5, "Maria",'Flor', '55555555555','839999999997','58312020','555');
# print(ler_client())
# deletar_client(5)
# print(ler_client())
# print(pesquisar_um(1))

# print(pesquisar_por_nome("Flor"))
venda(1, '20231001', [2, 3])


# # Testando os relatórios
# relatorio_vendas()
# relatorio_estoque()
# relatorio_clientes()

# Fechar a conexão
cursor.close()
connection.close()
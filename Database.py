from Usuario import Usuario
from Pedido_Estoque import Estoque, Pedido, Produto
import os, csv

class ManipuladorCSV:
    def Adicionar_Dados(self, dados, arquivo):
        """
        Adiciona um dicionário em um arquivo CSV usando a função ler_csv para 
        pegar as informações atuais, juntar com as novas informações e usa a 
        funação escrever_csv para escrever os dados de volta no arquivo.

        Args:
        dados (list): Um dicionário a ser adicionado no arquivo CSV.
        arquivo (str): O caminho para o arquivo CSV a ser adicionado.
        """

        #verifica se o arquivo existe no diretório, cria um novo se não existir.
        if not os.path.exists(f'data/{arquivo}'):
            with open(f'data/{arquivo}', 'w') as filecsv:
                filecsv.close()
        else:
            pass


        if not dados:#Dá um return caso não existam dados a serem adicionados
            return
        
        #Cria uma lista com todas as informações atuais do arquivo csv 
        dados_novos = self.ler_csv(arquivo)
        #Adiciona os novos dados na lista
        dados_novos.extend(dados)
        #Escreve todos os dados em um novo arquivo csv de mesmo nome
        self.escrever_csv(dados_novos, arquivo)


    def ler_csv(self, arquivo):
        """
        Lê um arquivo CSV e retorna os dados como uma lista de dicionários.

        Args:
        arquivo (str): O caminho para o arquivo CSV a ser lido.

        Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma linha do arquivo CSV.
        """

        #Verifica se o arquivo exite no diretório. Se existir, lê os dados e retorna, se não, cria um arquivo
        if os.path.exists(f'data/{arquivo}'):
            dados = []
            with open(f'data/{arquivo}', mode='r', encoding='utf-8') as arquivo_csv:#Abre o arquivo em modo de leitura
                leitor_csv = csv.DictReader(arquivo_csv,delimiter=',')#Lê os dados do arquivo csv
                for linha in leitor_csv:
                    dados.append(linha)
            return dados
        else:
            with open(f'data/{arquivo}', 'w') as filecsv:#Cria um arquivo caso não exista
                filecsv.close()

    def escrever_csv(self, dados, arquivo):
        """
        Escreve uma lista de dicionários em um arquivo CSV.

        Args:
        dados (list): Uma lista de dicionários a serem escritos no arquivo CSV.
        arquivo (str): O caminho para o arquivo CSV a ser escrito.
        """
        if not dados:
            return

        cabecalhos = dados[0].keys()#Define os Cabeçalhos
        with open(f'data/{arquivo}', mode='w', encoding='utf-8', newline='') as arquivo_csv:#Abre o arquivo em modo de escrita(todos os dados serão excluídos)
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=cabecalhos,delimiter=',')
            escritor_csv.writeheader()#escreve a primeira linha do arquivo csv usando os fieldnames pré-especificados
            for linha in dados:
                escritor_csv.writerow(linha)#Escreve os itens de cada linha separado por vígula

manipuladorcsv = ManipuladorCSV()

class Database:
    def Carregar_Usuarios(self):
        """
        Chama a função ler_csv() e retorna uma lista de ojetos da classe Usuario

        Returns:
        Retorna uma lista de instancias do tipo da classe Usuário
        """
        dict_Usuarios = manipuladorcsv.ler_csv('usuarios.csv')
        usuarios = []
        #Itera sobre dict_usuarios
        for list in dict_Usuarios:
            usuario = Usuario(list['Nome'],list['CPF_CNPJ'], list['E-mail'], list['Login'], list['Senha'])
            usuarios.append(usuario)
        return usuarios
    
    def Carregar_Estoque(self):
        """
        Chama a função ler_csv() e retorna uma lista de instancias do tipo Produto

        Returns:
        Retorna uma lista de instancias do tipo Produto
        """
        #Armazena os dados do arquivo csv em dict_Estoque
        dict_Estoque = manipuladorcsv.ler_csv('estoque.csv')
        lista_produtos_estoque = []
        #Itera sobre dict_Estoque
        for list in dict_Estoque:
            #Instancia um produto e adiciona à lista
            produto = Produto(str(list['ID_Produto']),list['Nome_Produto'],float(list['Preco']),float(list['Preco_Custo']),int(list['Quantidade']))
            lista_produtos_estoque.append(produto)
            
        #retorna a lista de produtos
        return lista_produtos_estoque


    def Carregar_Pedidos(self):
        """
        Carrega os Pedidos salvos no arquivo CSV

        Returns: 
        Retorna uma lista com instancias do tipo da classe Pedido

        """
        dict_Pedidos = manipuladorcsv.ler_csv('pedidos.csv')
        pedidos = []
        idlinha = []

        for id in dict_Pedidos:
            idlinha.append(int(id['ID_Pedido']))

        idpedidoDes = list(set(idlinha))#Remove os IDs duplicados
        idpedidordenado = sorted(idpedidoDes)


        for id in idpedidordenado:
            pedido = Pedido()
            pedido.set_IDPedido(id)
            for linha in dict_Pedidos:
                if linha['ID_Pedido'] == str(id):
                    pedido.set_DataPedido(linha['Data_Pedido'])
                    pedido.set_valorTotal(linha['Valor_Total'])
                    pedido.Adicionar_Item(linha['ID_Produto'],linha['Nome_Produto'],float(linha['Preco']), float(linha['Preco_Custo']), int(linha['Quantidade'])) 
            pedidos.append(pedido)#Adiciona o Pedido a Lista de Pedidos
        return pedidos
    

    def Database_Adicionar_Novo_Usuario(self, nome, cpf_cnpj, email, login, senha):#Adicionar docstrings

        """
        Instancia um objeto do tipo Usuário e salva no arquivo csv

        Retuern:
        Retorna uma Instancia do tipo da classe Usuario
        """

        usuario = Usuario(nome, cpf_cnpj, email, login, senha)
        dados = [
            {'Nome': usuario.get_nome(), 'CPF_CNPJ': usuario.get_cpf_cnpj(), 'E-mail': usuario.get_email(), 'Login': usuario.get_login(), 'Senha': usuario.get_senha()}
        ]
        manipuladorcsv.Adicionar_Dados(dados, 'usuarios.csv')
        return usuario
    


    def Database_Salvar_Dados_Estoque(self, estoque):
        """
        Reescreve o arquivo csv atualizando dados do estoque

        Args: 
        estoque(Estoque): Instancia da classe estoque 
        """
        produtos = estoque.get_produtosEstoque()

        with open('data/estoque.csv', 'w') as file:#Apaga totos os dados salvos em estoque.csv
            file.close()

        for produto in produtos:#Salva os dados da classe alterada após a conlusão do pedido
            dados = [
                {'ID_Produto': produto.get_id(), 'Nome_Produto': produto.get_nomeProduto(), 'Preco': produto.get_preco(),'Preco_Custo': produto.get_precoCusto(),  'Quantidade': produto.get_quantidade()}
            ]
            manipuladorcsv.Adicionar_Dados(dados, 'estoque.csv')


    def Database_Salvar_Dados_Pedido(self, pedidos):
        """
        Reescreve o arquivo csv atualizando dados do pedido

        Args: 
        pedidos(list): lista de pedidos do sistema
        """
        with open('data/pedidos.csv', 'w') as file:#Apaga totos os dados salvos em estoque.csv
            file.close()

        for pedido in pedidos:#Salva os dados da classe alterada após a conlusão do pedido
            for produto in pedido.get_produtos():
                dados = [
                    {'ID_Pedido': pedido.get_IDPedido(),'ID_Produto': produto.get_id(), 'Nome_Produto': produto.get_nomeProduto(), 'Preco': produto.get_preco(),'Preco_Custo': produto.get_precoCusto(), 'Quantidade': produto.get_quantidade(), 'Valor_Total': pedido.get_valorTotal(), 'Data_Pedido': pedido.get_DataPedido()}
                ]
                manipuladorcsv.Adicionar_Dados(dados, 'pedidos.csv')
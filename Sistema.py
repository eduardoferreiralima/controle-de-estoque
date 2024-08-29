from Usuario import *
from Database import Database
from Pedido_Estoque import *
import datetime
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode
database = Database()

class Sistema(MixInAutenticavel):#Herança
    def __init__(self) -> None:
        produtos_estoque = database.Carregar_Estoque()
        self.__estoque = Estoque()  #Objeto da Classe Estoque              (Composição)     Método da classe Database
        self.__estoque.set_produtos_Estoque(produtos_estoque)
        
        self.__usuarios = database.Carregar_Usuarios() #Lista de instancias do tipo Usuário  (agregação)     Método da classe Database
        self.__pedidos = database.Carregar_Pedidos() #Lista de instancias do tipo Pedido     (agregação)     Método da classe Database

    def get_estoque(self):
        return self.__estoque
    def get_usuarios(self):
        return self.__usuarios
    def get_pedidos(self):
        return self.__pedidos
    

    def Autenticar_Usuario(self, loginDigitado, senhaDigitada):
        """
        Faz a autenticação do usuário

        Args: 
            loginDigitado(str): Login digitado pelo usuário
            senhaDigitada(str): Senha digitada pelo usuário

        Returns:
            Retorna True se as informações estiverem corretas
            Retorna False se não estiverem corretas.
        """
        return super().Autenticar_Usuario(self.__usuarios, loginDigitado, senhaDigitada)


    def Escanear_Codigo_Barras(self, image):
        """
        Converte uma imagem de Código de barras em string

        Args:
        image: Imagem (png, jpg ou jpeg)

        Returns: 
        Retorna False se não for encontrado,
        Retorna o código se for encontrado

        Mais informações: 
        https://acervolima.com/como-fazer-um-leitor-de-codigo-de-barras-em-python/#google_vignette
        """
        img = Image.open(image)
        # Converte a imagem para uma matriz NumPy
        img_array = np.array(img)
        # Decodifica os códigos de barras na imagem 
        detectedBarcodes = decode(img_array)
        # Verifica se foram detectados códigos de barras
        if not detectedBarcodes:
            return False
        else:
            # Itera sobre cada código de barras detectado
            for barcode in detectedBarcodes:
                byte_barcode = barcode.data
                id_produto = byte_barcode.decode()
                return id_produto


    def Adicionar_Novo_Usuario(self, nome, cpf_cnpj, email, login, senha):#Adicionar docstrings
        """
        chama o Método da classe Database e cria um novo objeto usuário
        """
        usuario = database.Database_Adicionar_Novo_Usuario(nome, cpf_cnpj, email, login, senha)     #Método da classe Database
        self.__usuarios.append(usuario)
        return True

        
    def Remover_Usuario(self, usuario):
        """
        Remove um Usuário da Lista de Usuários

        Args:
        usuario(class:Usuário): Objeto da classe usuário
        """
        self.__usuarios.remove(usuario)
    


    def Salvar_Dados_Estoque(self):
        """
        chama o Método da classe Database e Reescreve o arquivo csv atualizando dados do estoque 
        """
        database.Database_Salvar_Dados_Estoque(self.__estoque) #Método da classe Database



    def Adicionar_Novo_Produto_Estoque(self,id,nome_Produto, preco, preco_custo, quantidade):
        
        """
        Adiciona um item ao estoque.

        Args:
        id (str): O Produto a ser adicionado ao estoque.
        Nome_produto (str): Nome do produto
        preco (float): Preço do produto
        quantidade(int): Quantidade do produto a ser adicionado ao estoque

        Returns:
        Retorna o Objeto Produto
        Retorna False se o ID já existir no estoque
        """
        produto_existe = False
        produtos = self.__estoque.get_produtosEstoque()
        for produto in produtos:#Verifica se o produto existe no estoque
            if produto.get_id() == id:
                produto_existe = True

        if not produto_existe:
            produto = self.__estoque.Adicionar_Item(id, nome_Produto, preco, preco_custo, quantidade)
            database.Database_Salvar_Dados_Estoque(self.__estoque)
            return produto
        
        else:
            return produto_existe


    def Repor_Remover_Produto_Estoque(self, id_produto,  quantidade, preco = None, preco_custo = None):
        """
        Remove ou Repõe um produto no estoque

        Args:
        id_produto(str): O id do produto a ser modificado
        quantidade(int): A quantidade do produto a ser modificado
        preco(float): O Novo preço do produto(Quanndo o Preço não for definido, significa que a função chamada é para remover um produto do estoque)

        Returns: 
        Retorna True Se o Produto for encontrado no estoque
        Retorna False se Não for encontrado
        """
        produtos = self.__estoque.get_produtosEstoque()
        encontrado = False
        for produto in produtos:
            if id_produto == produto.get_id():
                encontrado = True
                if preco == None and preco_custo == None:#Quanndo o Preço e o Preço de custo não for definido, significa que a função chamada é para remover um produto do estoque
                    if quantidade > produto.get_quantidade():#Se a quantidade digitada for maior que a quantidade em estoque, remove apenas o que está no estoque
                        produto.set_quantidade(-produto.get_quantidade())
                    else:
                        produto.set_quantidade(-quantidade)
                else:#Quando o preço for atribuído,  significa que a função chamada é para repor um produto ao estoque
                    produto.set_preco(preco)
                    produto.set_precoCusto(preco_custo)
                    produto.set_quantidade(quantidade)
                
        if encontrado:
            database.Database_Salvar_Dados_Estoque(self.__estoque)
            return True
        else:
            return False
        
    def Excluir_Produto_Estoque(self, id_produto):
        """
        Exclui um produto do estoque

        Args:
        id_produto(str): O id do produto a ser Excluído

        Returns: 
        Retorna True Se o Produto for encontrado no estoque
        Retorna False se Não for encontrado
        """
        if self.__estoque.Excluir_Item(id_produto):
            database.Database_Salvar_Dados_Estoque(self.__estoque)
            return True
        else:
            return False



    def Criar_Novo_Pedido(self):
        """
        Cria um Objeto da classe Pedido

        Return: 
            Retorna o objeto Pedido
        """
        pedido = Pedido()
        return pedido

    def Adicionar_Item_Pedido(self,pedido, id_produto, quantidade):
        """Adiciona um Item ao Pedido.
           
           Args:
                id_produto(int): id do produto a ser adicionado no pedido
                quantidade(int): quantidade do produto a ser adicionado no pedido
            
        """
        encontrado = False
        for produto_estoque in self.__estoque.get_produtosEstoque():#itera sobre os Produtos no estoque
            if produto_estoque.get_id() == str(id_produto):#Compara o id de cada produto com o id digitado, se for igual vai para o próximo if
                encontrado = True
                if int(produto_estoque.get_quantidade()) >= quantidade:#verifica se há itens suficientes no estoque       
                    pedido.Adicionar_Item(produto_estoque.get_id(), produto_estoque.get_nomeProduto(), produto_estoque.get_preco(), produto_estoque.get_precoCusto(), quantidade)
                    produto_estoque.set_quantidade(-quantidade)#Remove a quantidade de produtos do pedido no estoque
                    return True
                else:
                    return False, '2'#Não há Produtos suficiente no Estoque!
        if not encontrado:
            return False, '3'#Produto Não Encontrado no Estoque!

    def Finalizar_Pedido(self, pedido):
        """
        Calcula o valor total do Pedido,
        Atribui uma data ao pedido
        Define o ID do pedido com base no ID do Último pedido

        Args:
            Objeto da classe Pedido

        
        Returns: 
            Retorna o objeto da classe Pedido
        """  

        Valor_Total = 0.0
        for produto in pedido.get_produtos():
            preco = produto.get_preco()
            Valor_Total += float(preco)*produto.get_quantidade()

        pedido.set_valorTotal(Valor_Total)
        pedido.set_DataPedido(datetime.datetime.today())

        indice = len(self.__pedidos) - 1
        if indice < 0:
            id_pedido = 1
        else:
            utmo_pedido = self.__pedidos[indice]
            id_pedido = utmo_pedido.get_IDPedido() + 1
        pedido.set_IDPedido(id_pedido)

        self.__pedidos.append(pedido)#adiciona o pedido a lista de pedidos

        database.Database_Salvar_Dados_Estoque(self.__estoque)
        database.Database_Salvar_Dados_Pedido(self.__pedidos)

        return pedido

    def Salvar_Dados_Pedido(self):
        """
        Reescreve o arquivo csv atualizando dados do pedido 
        """
        database.Database_Salvar_Dados_Pedido(self.__pedidos)

    def Cancelar_Pedido(self, id_pedido):
        """
        Cancela um Pedido 

        Args:
            id_pedido: O id do pedido a ser cancelado

        Returns: 
            Retorna True se o pedido for encontrado
            Retorna False se o Pedido não for encontrado
        """
        encontrado = False
        produtos_estoque = self.__estoque.get_produtosEstoque()#Pega a lista de produtos em estoque
        for pedido in self.__pedidos:#Itera sobre os pedidos 
            if pedido.get_IDPedido() == id_pedido:#Compara o id de cada pedido com o id fornecido
                pedido_encontrado = pedido
                encontrado = True
                break

        if encontrado:
            produtos = pedido_encontrado.get_produtos()#pega a lista de produtos desse pedido
            for produto in produtos:#itera sobre a lista de produtos do pedido
                quantidade = produto.get_quantidade()#pega a quantidade de cada produto
                for produto_estoque in produtos_estoque:#Itera sobre a lista de produtos em estoque
                    if produto_estoque.get_id() == produto.get_id():#compara o id do produto do estoque com o produto do pedido
                        produto_estoque.set_quantidade(int(quantidade))#Se for igual, Adiciona a quantidade de produtos do pedido no estoque
            database.Database_Salvar_Dados_Estoque(self.__estoque)#reescreve o arquivo estoque.csv 
            self.__pedidos.remove(pedido_encontrado)#remove o pedido da lista de pedidos
            database.Database_Salvar_Dados_Pedido(self.__pedidos)#reescreve o arquivo pedidos.csv 

        return encontrado


    def Modificar_Pedido(self, pedido, remover_produto, id_produto, quantidade = None):#Não Finalizado
        """
        Remove um Produto se remover_produto for True, Modifica a Quantidade de um produto se for False

        Args:
            id_produto: O id do produto a ser modificado
        """

        if remover_produto:
            if pedido.Excluir_Item(id_produto):
                return pedido
            else:
                return False
            

        else:
            if quantidade != None:
                if pedido.Modificar_Item(id_produto, quantidade):
                    return pedido
                else:
                    return False
            else:
                return False



    def Gerar_Dados_De_Produtos_Vendidos(self):#Usado para as tabelas de pedidos da pagina inicial
        """
        Cria um Dicionário com as informações dos pedidos 

        Returns:
            Retorna um Dicionário com as informações dos pedidos
        """
        lista_dados = []
        for pedido in reversed(self.__pedidos):#itera sobre os pedidos começando do final da lista de pedidos
            lista_IDpedidos = []
            lista_ValorTotalpedidos = []
            lista_nomeProduto = []
            lista_valor_produto = []
            lista_quantidadeprodutos = []
            lista_Datapedidos = []

            lista_IDpedidos.append(pedido.get_IDPedido())
            lista_ValorTotalpedidos.append(pedido.get_valorTotal())
            lista_Datapedidos.append(pedido.get_DataPedido())
            lista_nomeProduto.append('-')
            lista_valor_produto.append('-')
            lista_quantidadeprodutos.append('-')

            produtos = pedido.get_produtos()#pega a lista de produtos do pedido

            for produto in produtos:
                lista_IDpedidos.append('-')
                lista_ValorTotalpedidos.append('-')
                lista_Datapedidos.append('-')
                lista_nomeProduto.append(produto.get_nomeProduto())
                preco = produto.get_preco()
                preco_formatado = round(float(preco), 2)
                lista_valor_produto.append(preco_formatado)
                lista_quantidadeprodutos.append(produto.get_quantidade())

            dados = {
                'ID do Pedido': lista_IDpedidos,
                'Valor Do Pedido': lista_ValorTotalpedidos,
                'Nome do Produto': lista_nomeProduto,
                'Valor do Produto': lista_valor_produto,
                'Quantidade de Produtos': lista_quantidadeprodutos,
                'Data e Hora do Pedido': lista_Datapedidos
            }
            lista_dados.append(dados)
        return lista_dados
    


    def Gerar_Dados_De_Pedidos(self):
        """
        Cria um Dicionário com as informações dos pedidos 

        Returns:
            Retorna um Dicionário com as informações dos pedidos
        """
        lista_IDpedidos = []
        lista_ValorTotalpedidos = []
        lista_quantidadeprodutos = []
        lista_Datapedidos = []
        quantidade = 0
        for pedido in reversed(self.__pedidos):#itera sobre os pedidos partindo do final da lista de pedidos
            lista_IDpedidos.append(pedido.get_IDPedido())
            lista_ValorTotalpedidos.append(pedido.get_valorTotal())
            lista_Datapedidos.append(pedido.get_DataPedido())
            quantidade = 0
            produtos = pedido.get_produtos()
            for produto in produtos:
                quantidade += int(produto.get_quantidade())
            lista_quantidadeprodutos.append(quantidade)
        dados = {
            'ID do Pedido': lista_IDpedidos,
            'Quantidade de Produtos': lista_quantidadeprodutos,
            'Data e Hora do Pedido': lista_Datapedidos,
            'Valor Do Pedido': lista_ValorTotalpedidos
        }
        return dados

    def Gerar_Dados_De_Estoque(self):
        """
        Cria um Dicionário com as informações dos produtos em estoque

        Returns:
            Retorna um Dicionário com as informações dos produtos em estoque
        """
        produtos = self.__estoque.get_produtosEstoque()
        lista_IDProdutos = []
        lista_NomeProdutos = []
        lista_PrecoProdutos = []
        lista_QuantidadeProdutos = []
        lista_ValorDeCustoDosProdutos = []
        lista_ValorDosProdutosFornecedor = []
        lista_ValorDosProdutos = []
        

        for produto in produtos:
            lista_IDProdutos.append(produto.get_id())
            lista_NomeProdutos.append(produto.get_nomeProduto())
            lista_PrecoProdutos.append(produto.get_preco())
            lista_QuantidadeProdutos.append(produto.get_quantidade())
            lista_ValorDeCustoDosProdutos.append(produto.get_precoCusto())
            lista_ValorDosProdutosFornecedor.append(produto.get_precoCusto()*produto.get_quantidade())
            lista_ValorDosProdutos.append(produto.get_preco()*produto.get_quantidade())

        data = {
            'Código do Produto': lista_IDProdutos,
            'Produto': lista_NomeProdutos,
            'Quantidade': lista_QuantidadeProdutos,
            'Preço Unitário': lista_PrecoProdutos,
            'Preço Unitário Pago ao Fornecedor': lista_ValorDeCustoDosProdutos,
            'Valor Total Pago ao Fornecedor': lista_ValorDosProdutosFornecedor,
            'Valor Total dos Produtos': lista_ValorDosProdutos
        }
        return data
    

    def Gerar_Dados_De_Faturamento(self):#Não Finalizado

        """
        Cria uma lista com o faturamento bruto, valor pago aos fornecedores e o lucro bruto



        Returns:
            Retorna uma lista com as informações citadas acima
        """

        lista_Faturamento = []
        faturamento_Bruto = 0.0
        pago_fornecedores = 0.0
        for pedido in self.__pedidos:
            faturamento_Bruto += float(pedido.get_valorTotal())
            produtos_pedido = pedido.get_produtos()
            
            for produto_pedido in produtos_pedido:
                pago_fornecedores += produto_pedido.get_precoCusto() * produto_pedido.get_quantidade() 

        lucro_Bruto = faturamento_Bruto - pago_fornecedores

        lista_Faturamento.append(faturamento_Bruto)
        lista_Faturamento.append(pago_fornecedores)
        lista_Faturamento.append(lucro_Bruto)
    
        return lista_Faturamento
    

    def Gerar_Dados_Pedido(self, pedido):
        produtos = pedido.get_produtos()

        lista_IDProdutos = []
        lista_NomeProdutos = []
        lista_PrecoProdutos = []
        lista_QuantidadeProdutos = []
        valor_total = 0.0

        for produto in produtos:
            valor_total += produto.get_preco()*produto.get_quantidade()
            lista_IDProdutos.append(produto.get_id())
            lista_NomeProdutos.append(produto.get_nomeProduto())
            lista_PrecoProdutos.append(produto.get_preco())
            lista_QuantidadeProdutos.append(produto.get_quantidade())
            data = {
            'Cód Produto': lista_IDProdutos,
            'Nome': lista_NomeProdutos,
            'Quantidade': lista_QuantidadeProdutos,
            'Preço': lista_PrecoProdutos,
            }
        return data, valor_total
from abc import ABC, abstractmethod

class Produto:#Abstração
    def __init__(self, id, nomeProduto, preco, preco_custo = None, quantidade = None) -> None:
        self.__id = id
        self.__nomeProduto = nomeProduto
        self.__preco = preco
        self.__precoCusto = preco_custo
        self.__quantidade = quantidade

    def __str__(self) -> str:
        dados = f"""
        Id: {self.__id}
        Nome do Produto: {self.__nomeProduto}
        Preço: {self.__preco}
        Preço de Custo: {self.__precoCusto}
        Quantidade: {self.__quantidade} 
        """
        return dados

    def set_id(self, id):
        self.__id = id
    def set_nomeProduto(self, nome):
        self.__nomeProduto = nome
    def set_preco(self, preco):
        self.__preco = preco
    def set_precoCusto(self, preco_custo):
        self.__precoCusto = preco_custo
    def set_quantidade(self, quantidade):
        self.__quantidade += quantidade


    def get_id(self):
        return self.__id
    def get_nomeProduto(self):
        return self.__nomeProduto
    def get_preco(self):
        return self.__preco
    def get_precoCusto(self):
        return self.__precoCusto
    def get_quantidade(self):
        return self.__quantidade





class OperacoesInterface(ABC):
    @abstractmethod
    def Adicionar_Item(self):
        pass
    @abstractmethod
    def Excluir_Item(self):
        pass
    @abstractmethod
    def Modificar_Item(self):
        pass



class Estoque(OperacoesInterface):#Herança
    def __init__(self) -> None:
        self.__produtos_Estoque = []

    def get_produtosEstoque(self):
        return self.__produtos_Estoque
    
    def set_produtos_Estoque(self, estoque):
        self.__produtos_Estoque = estoque

    def Adicionar_Item(self, id_produto,nome_produto,preco,preco_custo,quantidade):
        """
        Cria um objeto Produto e Adiciona ao Estoque

        Args:
            id_produto(str): ID do produto
            nome_produto(str): Nome do produto
            preco(float): Preço Final do produto
            preco_custo(float): Preço pago ao fornecedor
            quantidade(int): Quantidade do produto

        Returns:
            Retorna um objeto Produto
        """
        produto = Produto(id_produto,nome_produto,preco,preco_custo,quantidade)
        self.__produtos_Estoque.append(produto)
        return produto



    def Excluir_Item(self, id_produto):
        """
        Remove um produto do estoque de produtos

        Args:
        id_produto(str): O id do produto a ser removido do estoque

        Returns:
        Retorna True se o Produto for encontrado, False se não.
        """
        encontrado = False
        for produto in self.__produtos_Estoque:
            if produto.get_id() == id_produto:
                self.__produtos_Estoque.remove(produto)
                encontrado = True
        return encontrado



    def Modificar_Item(self, id_produto, quantidade):
        pass


class Pedido(OperacoesInterface):#Herança
    def __init__(self) -> None:
        self.__idpedido = None
        self.__Produtos = []#Associação com a classe produto(lista de produtos)
        self.__valorTotal = 0.0
        self.__dataPedido = None


    def __str__(self) -> str:

        dados = f"""
            ID do Pedido: {self.__idpedido}
            Valor Total: {self.__valorTotal}
            Data do Pedido: {self.__dataPedido}
        """
        return dados

    def set_produtos(self, produto):
        self.__Produtos.append(produto)
    def set_valorTotal(self, total):
        self.__valorTotal = total
    def set_DataPedido(self, data):
        self.__dataPedido = data
    def set_IDPedido(self, id):
        self.__idpedido = id

    def get_produtos(self):
        return self.__Produtos
    def get_valorTotal(self):
        return self.__valorTotal
    def get_DataPedido(self):
        return self.__dataPedido
    def get_IDPedido(self):
        return self.__idpedido

    def Adicionar_Item(self, id_produto,nome_produto,preco,preco_custo,quantidade):
        """
        Cria um objeto Produto e Adiciona ao Pedido

        Args:
            id_produto(str): ID do produto
            nome_produto(str): Nome do produto
            preco(float): Preço do produto
            quantidade(int): Quantidade do produto
        """
        produto = Produto(id_produto,nome_produto,preco,preco_custo,quantidade)
        self.__Produtos.append(produto)

    def Excluir_Item(self, id_produto):
        for produto in self.__Produtos:
            if produto.get_id() == id_produto:
                self.__Produtos.remove(produto)
                return True
        return False
        
        
    def Modificar_Item(self, id_produto, quantidade):
        for produto in self.__Produtos:
            if produto.get_id() == id_produto:
                if quantidade > 0:
                    produto.set_quantidade(quantidade)
                    return True
                
                else:
                    if (produto.get_quantidade() + quantidade) > 0:
                        produto.set_quantidade(quantidade)
                        return True
                    else:
                        return False
        return False
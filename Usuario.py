class Usuario:
    def __init__(self, nome, cpf_cnpj, email, login, senha) -> None:
        self.__nome = nome
        self.__cpf_cnpj = cpf_cnpj
        self.__email = email
        self.__login = login
        self.__senha = senha

    def __str__(self) -> str:
        return f'''
        Nome: {self.__nome}
        CPF_CNPJ: {self.__cpf_cnpj}
        E-mail: {self.__email}
        Login: {self.__login}
        Senha: {self.__senha}
        '''

    def set_nome(self, nome):
        self.__nome = nome
    def set_cpf_cnpj(self, cpf_cnpj):
        self.__cpf_cnpj = cpf_cnpj
    def set_email(self, email):
        self.__email = email
    def set_login(self, login):
        self.__login = login
    def set_senha(self, senha):
        self.__senha = senha

    def get_nome(self):
        return self.__nome
    def get_cpf_cnpj(self):
        return self.__cpf_cnpj
    def get_email(self):
        return self.__email
    def get_login(self):
        return self.__login
    def get_senha(self):
        return self.__senha

class MixInAutenticavel:
    def Autenticar_Usuario(self, usuarios, loginDigitado, senhaDigitada):

        """
        Faz a autenticação do usuário

        Args: 
            usuarios(list): Lista de usuários cadastrados
            loginDigitado(str): Login digitado pelo usuário
            senhaDigitada(str): Senha digitada pelo usuário

        Returns:
            Retorna True se as informações estiverem corretas
            Retorna False se não estiverem corretas.
        """
        
        for usuario in usuarios:
            if usuario.get_login() == loginDigitado and usuario.get_senha() == senhaDigitada:
                return True, usuario.get_nome()
            elif usuario.get_cpf_cnpj() == loginDigitado and usuario.get_senha() == senhaDigitada:
                return True, usuario.get_nome()
            elif usuario.get_email() == loginDigitado and usuario.get_senha() == senhaDigitada:
                return True, usuario.get_nome()
        return False
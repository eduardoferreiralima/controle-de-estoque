import re
from Sistema import Sistema
sistema = Sistema()


def Validar_Nome(nome):
    """
    Usa Regex para Verificar se o Nome digitado é Válido.

    Args:
        nome(str): Nome digitado pelo usuário

    Returns:
        Retorna True se for um nome válido, False se não.
    """
    return bool (re.match(r'^[a-zA-Z ]+$', nome))
    
def Validar_CPF_CNPJ(cpf_cnpj):#incompleto
    """
    Usa Regex para Verificar se o CPF ou CNPJ digitado é Válido.

    Args:
        cpf_cnpj(str): cpf ou cnpj digitado pelo usuário

    Returns:
        Retorna True se for um cpf ou cnpj válido, False se não.
    """
    if bool (re.match(r'^(\d{3}\.?){2}\d{3}\-?\d{2}$', cpf_cnpj)):
        return True
    #return bool (re.match(r'', cpf_cnpj))

def Validar_Email(email):
    """
    Usa Regex para Verificar se o E-mail digitado é Válido.

    Args:
        email(str): E-mail digitado pelo usuário

    Returns:
        Retorna True se for um email válido, False se não.
    """
    return bool (re.match(r'^\S+@\S+\.\S+$', email))

def Validar_Senha(senha):
    """
    Usa Regex para Verificar se a senha digitada é forte.

    Args:
        senha(str): Senha digitada pelo usuário

    Returns:
        Retorna True se a Senha for forte o suficiente, False se não.
    """
    regex = (
        r'^(?=.*[A-Z])'         # Pelo menos uma letra maiúscula
        r'(?=.*[a-z])'          # Pelo menos uma letra minúscula
        r'(?=.*\d)'             # Pelo menos um número
        r'(?=.*[@$!%*?+&_])'      # Pelo menos um caractere especial
        r'[A-Za-z\d@$!%*?+&_]{8,}$'  # Pelo menos 8 caracteres no total
    )
    return bool (re.match(regex, senha))

def Validar_Usuario(nome_usuario):
    """
    Verifica se o nome de usuário digitado já existe.

    Args:
        nome_usuario(str): nome de usuario digitado pelo usuário

    Returns:
        Retorna True se não existir, False se existir.
    """
    usuarios = sistema.get_usuarios()
    for usuario in usuarios:
        if nome_usuario == usuario.get_login():
            return False
    return True
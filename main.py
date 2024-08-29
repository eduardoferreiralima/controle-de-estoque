import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import time
from Sistema import Sistema
import Validadores as vl

# Instância do sistema
if 'sistema' not in st.session_state:
    st.session_state.sistema = Sistema()

def Escanear_Codigo_Barras():
    image = st.file_uploader('Faça o upload da imagem do Código de Barras', type=['jpg', 'jpeg', 'png'])
    if image != None:
        id_produto = st.session_state.sistema.Escanear_Codigo_Barras(image)
        if id_produto == False:
            st.error("Código de barras não detectado ou o código está em branco/corrompido!")
            return id_produto
        else:
            st.success(f'Código Identificado: {id_produto}')
            return id_produto

def Pagina_Inicial(usuario):
    with st.sidebar:
        # Uso do streamlit_option_menu para criar um menu com ícones
        selected = option_menu("Menu", ["Vendas", 'Pedidos', 'Estoque', 'Estatísticas'],
                               icons=['coin', 'cart', 'box2-fill', 'bar-chart'], menu_icon="cast", default_index=0)

    if selected == 'Vendas':
        st.title('Vendas')


        container = st.empty()
        pagina = container.radio('Selecione uma Opção', ['Tabela','Gráfico de Barras'], horizontal=True)

        if pagina == 'Tabela':
            st.subheader("Últimas Vendas")
            
            dados_total = st.session_state.sistema.Gerar_Dados_De_Produtos_Vendidos()
            
            for dados in dados_total:
                pedido = pd.DataFrame(dados)
                st.write(pedido)

        elif pagina == 'Gráfico de Barras':

            dadospedidos = st.session_state.sistema.Gerar_Dados_De_Pedidos()
            df = pd.DataFrame(dadospedidos)
            # Exibir gráfico de barras para a quantidade de produtos
            fig_qtd = px.bar(df, x='Data e Hora do Pedido', y='Valor Do Pedido', title='Faturamento Diario')
            st.plotly_chart(fig_qtd, use_container_width=True)

    elif selected == 'Pedidos':
        st.title('Pedidos')
        # Inicializa o estado da sessão
        if 'pedido' not in st.session_state:
            st.session_state.pedido = None

        def Novo_Pedido():
            # Se o pedido ainda não foi criado, cria um novo
            if st.session_state.pedido is None:
                st.session_state.pedido = st.session_state.sistema.Criar_Novo_Pedido()#armazena o pedido de maneira persistente entre as interações do usuário em uma única sessão

            caixa = st.empty()
            opcao = caixa.radio('Selecione:', ["Digitar Código", "Escanear Código"], horizontal=True)

            if opcao == "Digitar Código":              
                id_produto = str(st.text_input("Código do Produto", placeholder='Digite aqui o Código do Produto...'))
                quantidade = st.number_input("Quantidade", placeholder='Digite aqui a Quantidade...', min_value=1, max_value=10000)

            if opcao == "Escanear Código":
                    id_produto = Escanear_Codigo_Barras()
                    if id_produto == False: pass 
                    else: 
                        quantidade = st.number_input("Quantidade", placeholder='Digite aqui a Quantidade...', min_value=1, max_value=10000)

            col1, col2 = st.columns(2)
            mensagem_resultado = st.empty()

            if col1.button('Adicionar Produto'):
                try:
                    result = st.session_state.sistema.Adicionar_Item_Pedido(st.session_state.pedido, id_produto, quantidade)
                    if result == True:
                        mensagem_resultado.success('Produto Adicionado ao Pedido!')
                    else:
                        if result[1] == '2':
                            mensagem_resultado.error('Não há Produtos suficientes no Estoque!')
                        elif result[1] == '3':
                            mensagem_resultado.error('Produto Não Encontrado no Estoque!')
                except UnboundLocalError:
                    st.error('Escaneie o Código de Um Produto Primeiro!')

            if col2.button('Finalizar Pedido'):
                if st.session_state.pedido.get_produtos() != []:
                    pedidofinalizado = st.session_state.sistema.Finalizar_Pedido(st.session_state.pedido)
                    st.session_state.pedido = None
                    mensagem_resultado.success("Pedido finalizado com sucesso!")
                    st.write(pedidofinalizado)
                    st.rerun()
                else: 
                    mensagem_resultado.error("Adicione um Produto!")


        def Modificar_Pedido():
            container = st.empty()
            opcao = container.radio('Escolha uma Opção:', ['Remover Produto', 'Modificar Quantidade de um Produto'], horizontal=True)
            if opcao == 'Remover Produto':
                if st.session_state.pedido.get_produtos() != []:
                    id_produto = str(st.text_input("Código do Produto", placeholder='Digite aqui o Código do Produto...'))

                    if st.button('Remover Produto'):
                        pedido = st.session_state.sistema.Modificar_Pedido(st.session_state.pedido, True, id_produto)
                        if pedido == False:
                            st.error('Produto Não Encontrado no Pedido!')
                        else:
                            st.session_state.pedido = pedido
                else:
                    st.error("Não Há Itens no Pedido!")


            if opcao == 'Modificar Quantidade de um Produto':
                if st.session_state.pedido.get_produtos() != []:
                    container2 = st.empty()
                    opcao2 = container2.radio('Escolha uma opção:', ['Adicionar', 'Remover'], horizontal=True)

                    id_produto = str(st.text_input("Código do Produto", placeholder='Digite aqui o Código do Produto...'))
                    quantidade = st.number_input("Quantidade", placeholder='Digite aqui a Quantidade...', min_value=1, max_value=10000)

                    
                    if opcao2 == 'Adicionar':
                        if st.button('Adicionar Item'):
                            pedido = st.session_state.sistema.Modificar_Pedido(st.session_state.pedido, False, id_produto, quantidade)
                            if pedido == False:
                                st.error('Produto Não Encontrado no Pedido!')
                            else:
                                st.session_state.pedido = pedido


                    elif opcao2 == 'Remover':
                        if st.button('Remover Item'):
                            pedido = st.session_state.sistema.Modificar_Pedido(st.session_state.pedido, False, id_produto, -quantidade)
                            if pedido == False:
                                st.error('Produto Não Encontrado no Pedido ou quantidade Inválida!')
                            else:
                                st.session_state.pedido = pedido
                else:
                    st.error("Não Há Itens no Pedido!")             

        def Cancelar_Pedido():

            container = st.empty()
            opcao = container.radio('Selecione uma Opção:',['Pedido Atual', 'Outro Pedido'],horizontal=True)

            if opcao == 'Pedido Atual':
                if st.button('Cancelar Pedido Atual'):
                    st.session_state.pedido = None
                    if st.session_state.pedido == None:
                        st.success('Pedido Atual Cancelado!')
                        st.session_state.pedido = st.session_state.sistema.Criar_Novo_Pedido()
            if opcao == 'Outro Pedido':
                id_pedido= st.number_input("ID do Pedido", placeholder='Digite aqui o ID do Pedido.', min_value=0)
                mensagem_resultado = st.empty()
                if st.button('Cancelar Pedido'):
                    result = st.session_state.sistema.Cancelar_Pedido(id_pedido)
                    if result == False:
                        mensagem_resultado.error('Pedido Não Encontrado!')
                    else: 
                        mensagem_resultado.success('Pedido Cancelado!')

        pagina = st.empty()
        opcao_selecionada = pagina.radio("Selecione uma Opção", ['Novo Pedido', 'Modificar Pedido', 'Cancelar Pedido'], horizontal=True)

        if opcao_selecionada == 'Novo Pedido':
            Novo_Pedido()
        elif opcao_selecionada == 'Modificar Pedido':
            Modificar_Pedido()
        elif opcao_selecionada == 'Cancelar Pedido':
            Cancelar_Pedido()


        try:
            dados = st.session_state.sistema.Gerar_Dados_Pedido(st.session_state.pedido)
            dados_tabela = dados[0]
            valor_total = round(dados[1], 2)
            st.title(f"Valor Total: {valor_total}")
            st.subheader('Pedido Atual')
            st.table(dados_tabela)
        except UnboundLocalError:
            st.table(None)

        dados = st.session_state.sistema.Gerar_Dados_De_Pedidos()
        df = pd.DataFrame(dados)
        # Exibe a tabela de estoque
        st.subheader("Últimos Pedidos:")
        st.table(df)

                

    elif selected == 'Estoque':
        st.title('Estoque')
        # Dados de estoque

        def Novo_Produto():
            caixa = st.empty()
            opcao = caixa.radio('Selecione:', ["Digitar Código", "Escanear Código"], horizontal=True)

            if opcao == "Digitar Código":              
                id_produto = str(st.text_input("Código do Produto", placeholder='Digite aqui o Código do Produto.'))
                nome_produto = str(st.text_input("Nome do Produto", placeholder='Digite aqui o Nome do Produto.'))
                preco = st.number_input("Valor Pago pelo Cliente", placeholder='Preço de Venda do Produto')
                preco_custo = st.number_input("Valor Pago aos Fornecedores do Produto", placeholder='Preço de Custo do Produto')
                quantidade = st.number_input("Quantidade", placeholder='Digite aqui a Quantidade.', min_value=1)
                preco = round(preco, 2)
                preco_custo = round(preco_custo, 2)

                if id_produto == '' or nome_produto == '' or preco_custo == 0.0 or preco == 0.0:
                    st.error('Dados Atuais Inválidos')
                    return

            if opcao == "Escanear Código":
                id_produto = Escanear_Codigo_Barras()
                if id_produto == False: pass 
                else: 
                    nome_produto = str(st.text_input("Nome do Produto", placeholder='Digite aqui o Nome do Produto.'))
                    preco = st.number_input("Valor Pago pelo Cliente", placeholder='Preço de Venda do Produto')
                    preco_custo = st.number_input("Valor Pago aos Fornecedores do Produto", placeholder='Preço de Custo do Produto')
                    quantidade = st.number_input("Quantidade", placeholder='Digite aqui a Quantidade.', min_value=1)
                    preco = round(preco, 2)
                    preco_custo = round(preco_custo, 2)
                if id_produto == '' or nome_produto == '' or preco_custo == 0.0 or preco == 0.0:
                    st.error('Dados Atuais Inválidos')
                    return

            mensagem_resultado = st.empty()
            if st.button('Adicionar Produto ao Estoque'):
                produto = st.session_state.sistema.Adicionar_Novo_Produto_Estoque(id_produto, nome_produto, preco, preco_custo, quantidade)
                if produto == False:
                    mensagem_resultado.error('O Produto já Existe No Estoque!')
                else:
                    mensagem_resultado.success('Produto Adicionado ao Estoque!')
                    time.sleep(2)
                    mensagem_resultado.write(produto)

        def Repor_Produto():
            caixa = st.empty()
            opcao = caixa.radio('Selecione:', ["Digitar Código", "Escanear Código"], horizontal=True)

            if opcao == "Digitar Código":              
                id_produto = str(st.text_input("Código do Produto", placeholder='Digite aqui o Código do Produto.'))
                preco = st.number_input("Valor Pago pelo Cliente", placeholder='Preço de Venda do Produto')
                preco_custo = st.number_input("Valor Pago aos Fornecedores do Produto", placeholder='Preço de Custo do Produto')
                quantidade = st.number_input("Quantidade", placeholder='Digite aqui a Quantidade.', min_value=1)

            if opcao == "Escanear Código":
                id_produto = Escanear_Codigo_Barras()
                if id_produto == False: pass 
                else:    
                    preco = st.number_input("Valor Pago pelo Cliente", placeholder='Preço de Venda do Produto')
                    preco_custo = st.number_input("Valor Pago aos Fornecedores do Produto", placeholder='Preço de Custo do Produto')
                    quantidade = st.number_input("Quantidade", placeholder='Digite aqui a Quantidade.', min_value=1)

            if st.button('Salvar Alteração'):
                mensagem_resultado = st.empty()
                if st.session_state.sistema.Repor_Remover_Produto_Estoque(id_produto,quantidade, preco, preco_custo):
                    mensagem_resultado.success('Alteração Salva')
                else:
                    mensagem_resultado.error('Produto Não Encontrado No Estoque!')

        def Remover_Produto():
            caixa = st.empty()
            opcao = caixa.radio('Selecione:', ["Digitar Código", "Escanear Código"], horizontal=True)

            if opcao == "Digitar Código":              
                id_produto = str(st.text_input("Código do Produto", placeholder='Digite aqui o Código do Produto.'))
                quantidade = st.number_input("Quantidade", placeholder='Digite aqui a Quantidade.', min_value=1)
            if opcao == "Escanear Código":
                id_produto = Escanear_Codigo_Barras()
                if id_produto == False: pass 
                else: 
                    quantidade = st.number_input("Quantidade", placeholder='Digite aqui a Quantidade...', min_value=1, max_value=10000)    

            if st.button('Salvar Alteração'):
                
                mensagem_resultado = st.empty()
                if st.session_state.sistema.Repor_Remover_Produto_Estoque(id_produto, quantidade):
                    mensagem_resultado.success('Alteração Salva')
                else:
                    mensagem_resultado.error('Produto Não Encontrado No Estoque!')

        def Excluir_Produto():
            caixa = st.empty()
            opcao = caixa.radio('Selecione:', ["Digitar Código", "Escanear Código"], horizontal=True)

            if opcao == "Digitar Código":              
                id_produto = str(st.text_input("Código do Produto", placeholder='Digite aqui o Código do Produto.'))
            if opcao == "Escanear Código":
                    id_produto = Escanear_Codigo_Barras()
                    
            if st.button('Excluir Produto'):
                mensagem_resultado = st.empty()
                if st.session_state.sistema.Excluir_Produto_Estoque(id_produto):
                    mensagem_resultado.success('Produto Excluído do Estoque!')
                else:
                    mensagem_resultado.error('Produto Não Encontrado No Estoque!')


        pagina = st.empty()
        opcao_selecionada = pagina.radio("Selecione uma Opção", ['Novo Produto', 'Repor Produto', 'Remover Produto', 'Excluir Produto'], horizontal=True)

        if opcao_selecionada == 'Novo Produto':
            Novo_Produto()
        elif opcao_selecionada == 'Repor Produto':
            Repor_Produto()
        elif opcao_selecionada == 'Remover Produto':
            Remover_Produto()
        elif opcao_selecionada == 'Excluir Produto':
            Excluir_Produto()

        dados = st.session_state.sistema.Gerar_Dados_De_Estoque()
        df = pd.DataFrame(dados)
        # Exibe a tabela de estoque
        st.subheader("Estoque Atual:")
        st.table(df)



    elif selected == 'Estatísticas':
        st.title('Estatísticas')
        #gráfico de pizza para a distribuição de preços
        listadados = st.session_state.sistema.Gerar_Dados_De_Faturamento()
        faturamento_Bruto = listadados[0]
        pago_fornecedores = listadados[1]
        lucro_Bruto = listadados[2]
        dados = {
            'Categoria': ['Faturamento Bruto','Pago aos Fornecedores', 'Lucro Bruto'],
            'Valor': [faturamento_Bruto, pago_fornecedores,lucro_Bruto], 
        }

        #DataFrame com os dados
        df = pd.DataFrame(dados)

        #gráfico de pizza usando Plotly Express
        fig = px.pie(df,
                    title='Faturamento Bruto vs Pago aos Fornecedores vs Lucro Bruto',
                    names='Categoria',
                    values='Valor',
                    color_discrete_map={'Faturamento Bruto': 'blue', 'Lucro Bruto': 'green'})

        st.write(fig)





def login():
    st.title("Página de Login")
    username = st.text_input("Login:", placeholder='Usuário, CPF/CNPJ ou E-mail')
    password = st.text_input("Senha:", type="password", placeholder='Digite a Senha')

    if st.button("Login"):
        if st.session_state.sistema.Autenticar_Usuario(username, password):
            nome_usuario = st.session_state.sistema.Autenticar_Usuario(username, password)[1]
            st.success("Login bem-sucedido! Bem-vindo, {}".format(nome_usuario))
            # Salva o nome do usuário em um Session State
            time.sleep(2)
            st.session_state.nome_usuario = nome_usuario
            st.rerun()
        else:
            st.error("Credenciais inválidas. Tente novamente.")

def register():
    st.title("Página de Cadastro")
    
    nome = st.text_input("Nome Completo:", placeholder='Digite seu Nome completo')
    mensagem_nome = st.empty()
    email = st.text_input("E-mail:", placeholder='Digite um Endereço de E-mail Válido')
    mensagem_email = st.empty()
    cpf_cnpj = st.text_input("CPF ou CNPJ:", placeholder='Digite seu CPF ou CNPJ')
    mensagem_cpf_cnpj = st.empty()
    usuario = st.text_input("Nome de Usuário:", placeholder='Usuário...')
    mensagem_usuario = st.empty()
    senha = st.text_input("Senha:", type="password", placeholder='Digite a Senha')
    mensagem_senha = st.empty()
    confirma_senha = st.text_input("Confirme a Senha:", type="password", placeholder='Confirme a Senha')
    confirmar_senha = st.empty()

    
    if st.button("Cadastrar"):
        if not vl.Validar_Nome(nome):
            mensagem_nome.error('Nome Inválido!')
        elif not vl.Validar_Email(email):
            mensagem_email.error('E-mail Inválido!')
        elif not vl.Validar_CPF_CNPJ(cpf_cnpj):
            mensagem_cpf_cnpj.error('CPF Inválido!')
        elif not vl.Validar_Usuario(usuario):
            mensagem_usuario.error('O Nome de Usuário já Existe!')
        elif not vl.Validar_Senha(senha):
            mensagem_senha.error('Digite uma senha mais Forte!')
        elif senha != confirma_senha:
            confirmar_senha.error('As Senhas Digitadas Diferem!')
        else:
            st.session_state.sistema.Adicionar_Novo_Usuario(nome, cpf_cnpj, email, usuario, senha)
            st.success("Cadastro bem-sucedido! Bem-vindo, {}".format(usuario))
            # Salva o nome do usuário em um Session State
            st.session_state.nome_usuario = usuario
            time.sleep(1)
            st.rerun()

def main():
    # Exibe a página inicial se o nome do usuário estiver no Session State
    if hasattr(st.session_state, 'nome_usuario'):
        Pagina_Inicial(st.session_state.nome_usuario)
    else:
        pagina = st.empty()
        page = pagina.radio("Selecione uma Opção", ["Login", "Cadastro"], horizontal=True)

        if page == "Login":
            login()
        elif page == "Cadastro":
            register()

if __name__ == "__main__":
    # Esta chamada deve ser a última linha do script, após todas as definições de funções
    st.set_page_config(page_title='CEV - Controle de Estoque e Vendas', layout='centered', initial_sidebar_state='auto')
    main()
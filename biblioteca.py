"""
1. Sistema de gerenciamento de biblioteca: desenvolva um sistema de gerenciamento de uma biblioteca em Python, utilizando estruturas de dados apropriadas para armazenar informações sobre os livros, usuários, empréstimos, etc. Implemente, no mínimo, as funcionalidades de cadastro de livros e usuários, empréstimos, devoluções, pesquisa e relatórios.
"""

import sys

class Biblioteca:
    def __init__(self):
        self._usuarios = []
        self._livros = []
        self._prateleiras = []
        self._historico_emprestimos = []

        #mockando usuarios para testar busca
        usuario1 = Usuario("Joice", "joice@email.com", "12345678910", "Rua 1")
        self._usuarios.append(usuario1)
        usuario2 = Usuario("Lucas", "lucas@email.com", "10987654321", "Av 5")
        self._usuarios.append(usuario2)
        usuario3 = Usuario("Molly", "molly@email.com", "16051605910", "Rua 3")
        self._usuarios.append(usuario3)
        #mockando livros para testar busca
        livro1 = Livro("Sobre os ossos dos mortos", "Olga Tokarczuk", "Aventura,Suspense,Mistério", 246)
        self._livros.append(livro1)
        livro2 = Livro("Crepúsculo", "Stephenie Meyer", "Romance,Fantasia", 478)
        self._livros.append(livro2)
        livro3 = Livro("Cloud Atlas", "David Mitchell", "Ficção Científica,Ficção Histórica", 530)
        self._livros.append(livro3)

    def exec(self):
        while True:
            print("Selecione uma opção:")
            print("1 - Cadastrar usuário")
            print("2 - Cadastrar livro")
            print("3 - Cadastrar empréstimo")
            print("4 - Pesquisar livro")
            print("5 - Pesquisar usuário")
            print("6 - Gerar relatório")
            print("7 - Sair")
            selecionado = input("")
            if selecionado == "7":
                sys.exit()
            self.seleciona_funcao(selecionado)
            
    def getUsuarios(self):
        return self._usuarios
    
    def getLivros(self):
        return self._livros
    
    def getPrateleiras(self):
        return self._prateleiras
    
    def seleciona_funcao(self, opcao):
        if opcao == '1':
            return self.cadastra_usuario()
        elif opcao == '2':
            return self.cadastra_livro()
        elif opcao == '3':
            return self.cadastra_emprestimo()
        elif opcao == '4':
            return self.pesquisa_livro()
        elif opcao == '5':
            return self.pesquisa_usuario()
        elif opcao == '6':
            return self.gera_relatorio()
        else:
            print("Essa opção não é válida. Tente novamente.")
            return

        
    def cadastra_usuario(self):
        print("Cadastro de Usuário")
        nome = input("Nome do usuário: ")
        email = input("Email do usuário ")
        telefone = input("Telefone do usuário: ")
        endereco = input("Endereço do usuário: ")
        usuario = Usuario(nome, email, telefone, endereco)
        self._usuarios.append(usuario)
        
    def cadastra_livro(self):
        print("Cadastro de Livro")
        nome = input("Nome do livro: ")
        autor = input("Email do livro ")
        generos = input("Insira os gêneros do livro, separados por vírgula (,): ")
        generos = generos.split(",")
        disponibilidade = True
        qt_pagina = input("Quantidade de páginas: ")
        livro = Livro(nome, autor, generos, disponibilidade, qt_pagina)
        self._livros.append(livro)
        
    def cadastra_emprestimo(self):
        print("Cadastro de Empréstimo")
        print("Primeiro, selecione o usuário que está realizando o empréstimo.")
        
        usuario = self.pesquisa_usuario()
        livro = self.pesquisa_livro()
        dt_emprestimo = ""
        dt_devolucao = ""
        emprestimo = Emprestimo(dt_emprestimo, dt_devolucao, usuario, livro)
        self._historico_emprestimos.append(emprestimo)
        
    def pesquisa_livro(self):
        if len(self._livros) > 0:
            opt_ok = False
            while not opt_ok:
                print("Procurar o livro por:")
                tipos = ["Nome", "Autor", "Generos", "Disponibilidade"]
                opcoes = ['1', '2', '3', '4']
                for i in range(len(opcoes)):
                    print("{n} - {opcao}".format(n = opcoes[i], opcao = tipos[i]))
                tipo_filtro = input("")
                if tipo_filtro in opcoes:
                    tipo = tipos[opcoes.index(tipo_filtro)]
                    func_escolhida = "get" + tipo
                    livro = self.filtrarLivros(func_escolhida, tipo)
                    if livro is not None:
                        opt_ok = True
                        return livro
                    else:
                        print("Nenhum livro selecionado, tentar novamente.")
                else:
                    print("Opção inválida. Tente novamente.")
        else:
            print("Não há livros na base de dados. Antes de buscar livro, cadastre algum.")

    def filtrarLivros(self, func_name, tipo):
        filtrarPor = self.configurarFuncaoFiltrarParaLivros(func_name, tipo)
        filtrados = list(filter(filtrarPor, self._livros))
        qt_filtrados = len(filtrados)
        if qt_filtrados == 1:
            livro = filtrados[0]
            print("1 usuário encontrado")
            return self.validarEscolha(livro)
        elif qt_filtrados > 1:
            print("{n} usuários encontrados".format(n=qt_filtrados))
            livro = self.escolheUsuario(filtrados, qt_filtrados)
            return livro
        
    def configurarFuncaoFiltrarParaLivros(self, func_name, tipo):
        filtro = ""
        filtrarPor = lambda usuario : filtro.lower() in getattr(usuario, func_name)().lower()
        if func_name == "getDisponibilidade":
            disponibilidade_ok = False
            while not disponibilidade_ok:
                print("Escolha a disponibilidade a ser buscada: ")
                opcoes = ["1", "2"]
                tipos = ["Disponível", "Indisponível"]
                tipos_boolean = [True, False]
                for i in opcoes:
                    print("{m} - {opcao}".format(n=opcoes[i], opcao = tipos[i]))
                filtro = input("")
                if filtro in opcoes:
                    filtrarPor = lambda usuario : getattr(usuario, func_name)() == tipos_boolean[opcoes.index(filtro)]
                    disponibilidade_ok = True
                else:
                    print("Opção inválida. Tente novamente.")
        elif func_name == "getGeneros":
            filtro = input("Digite o gênero a ser buscado: ".format(v=tipo))
        else:
            filtro = input("Digite o {v} a ser buscado: ".format(v=tipo))
        return filtrarPor
        
    def pesquisa_usuario(self):
        if len(self._usuarios) > 0:
            opt_ok = False
            while not opt_ok:
                print("Procurar o usuário por:")
                tipos = ["Nome", "Email", "Telefone"]
                opcoes = ['1', '2', '3']
                for i in range(len(opcoes)):
                    print("{n} - {opcao}".format(n = opcoes[i], opcao = tipos[i]))
                tipo_filtro = input("")
                if tipo_filtro in opcoes:
                    tipo = tipos[opcoes.index(tipo_filtro)]
                    func_escolhida = "get" + tipo
                    usuario = self.filtrarUsuarios(func_escolhida, input("Digite o {v} a ser buscado: ".format(v=tipo)))
                    if usuario is not None:
                        opt_ok = True
                        return usuario
                    else:
                        print("Nenhum usuário selecionado, tentar novamente.")
                else:
                    print("Opção inválida. Tente novamente.")
        else:
            print("Não há usuários na base de dados. Antes de buscar usuário, cadastre algum.")

    def filtrarUsuarios(self, func_name, filtro):
        filtrarPor = lambda usuario : filtro.lower() in getattr(usuario, func_name)().lower()
        filtrados = list(filter(filtrarPor, self._usuarios))
        qt_filtrados = len(filtrados)
        if qt_filtrados == 1:
            usuario = filtrados[0]
            print("1 usuário encontrado")
            return self.validarEscolha(usuario)
        elif qt_filtrados > 1:
            print("{n} usuários encontrados".format(n=qt_filtrados))
            usuario = self.escolheUsuario(filtrados, qt_filtrados)
            return usuario

    def escolheUsuario(self, lista, qt):
        opcao_ok = False
        while not opcao_ok:
            print("Dados dos usuários encontrados")
            for i in range(qt):
                usuario = lista[i]
                print("Usuário #{n}".format(n=i+1))
                print("Nome: {n}".format(n=usuario.getNome()))
                print("Email: {e}".format(e=usuario.getEmail()))
                print("Telefone: {t}".format(t=usuario.getTelefone()))
                if i < qt - 1:
                    print("--------------")
            opcoes = [str(i) for i in range(1, qt + 1)]
            escolhido = input("Selecione o usuário desejado: ")
            if escolhido in opcoes:
                usuarioEscolhido = lista[int(escolhido) - 1]
                if self.validarEscolha(usuarioEscolhido):
                    return usuarioEscolhido
                else:
                    return None
            else:
                print("Opção inválida.")

    def validarEscolha(self, escolha):
        print("Dados do usuário:")
        escolha.exibeDados()
        escolha_ok = False
        while not escolha_ok:
            validaEscolha = input("Confirmar escolha? (Y/n) ")
            if validaEscolha.lower() == "y" or validaEscolha == "":
                return True
            elif validaEscolha.lower() == "n":
                print("Realizar a busca novamente.")
                return False
            else:
                print("Opção inválida. Tente novamente:")
        
    def gera_relatorio(self):
        pass
        

class Usuario:
    def __init__(self, nome, email, telefone, endereco):
        self._nome = nome
        self._email = email
        self._telefone = telefone
        self._endereco = endereco

    def getNome(self):
        return self._nome

    def getEmail(self):
        return self._email

    def getTelefone(self):
        return self._telefone

    def getEndereco(self):
        return self._endereco
    
    def exibeDados(self):
        print("Nome: {n}".format(n=self.getNome()))
        print("Email: {e}".format(e=self.getEmail()))
        print("Telefone: {t}".format(t=self.getTelefone()))
        print("Endereço: {t}".format(t=self.getEndereco()))

class Livro:
    def __init__(self, nome: str, autor: str, generos: str, qt_pagina: int, disponibilidade: bool = True):
        self._nome = nome
        self._autor = autor
        self._generos = generos.split(",")
        self._qt_pagina = qt_pagina
        self._disponibilidade = disponibilidade

    def getNome(self):
        return self._nome
    
    def getAutor(self):
        return self._autor
    
    def getGeneros(self):
        return self._generos
    
    def getDisponibilidade(self):
        return self._disponibilidade
    
    def setDisponibilidade(self, valor):
        if isinstance(valor, bool):
            self._disponibilidade = valor
        else:
            print("Erro ao setar novo valor de disponibilidade, valor anterior inalterado para o livro {n}. Valor atual = {v}.".format(n = self._nome, v = self._disponibilidade))

    def getQuantidadeDePaginas(self):
        return self._qt_pagina
    
    def exibeDados(self):
        generos = self.getGeneros()
        generosToString = ' '.join(map(str, generos))
        disponibilidade = "Disponível" if self.getDisponibilidade() else "Indisponível"
        print("Nome: {n}".format(n=self.getNome()))
        print("Autor: {e}".format(e=self.getAutor()))
        print("Generos: {t}".format(t=generosToString))
        print("Disponibilidade: {t}".format(t=disponibilidade))
        print("Endereço: {t}".format(t=str(self.getQuantidadeDePaginas())))

class Prateleira:
    def __init__(self, identificador, livros, max_capacidade):
        self._identificador = identificador
        self._livros = livros
        self._max_capacidade = max_capacidade

class Emprestimo:
    def __init__(self, dt_emprestimo, dt_devolucao, usuario, livro):
        self._dt_emprestimo = dt_emprestimo
        self._dt_devolucao = dt_devolucao
        self._usuario = usuario
        self._livro = livro

biblioteca = Biblioteca()
biblioteca.exec()
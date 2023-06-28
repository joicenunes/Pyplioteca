"""
1. Sistema de gerenciamento de biblioteca: desenvolva um sistema de gerenciamento de uma biblioteca em Python, utilizando estruturas de dados apropriadas para armazenar informações sobre os livros, usuários, empréstimos, etc. Implemente, no mínimo, as funcionalidades de cadastro de livros e usuários, empréstimos, devoluções, pesquisa e relatórios.
"""

import sys
import datetime

class Biblioteca:
    def __init__(self):
        self._usuarios = []
        self._livros = []
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
            acoes = ["Cadastrar usuário", "Cadastrar livro", "Cadastrar empréstimo", "Cadastrar devolução", "Pesquisar livro", "Pesquisar usuário", "Gerar relatório"]
            opcoes = [str(i) for i in range(1, len(acoes))]
            for i in range(len(acoes)):
                print("{n} - {opcao}".format(n = i + 1, opcao = acoes[i]))
            print("0 - Sair")
            selecionado = input("")
            if selecionado == "0":
                sys.exit()
            self.seleciona_funcao(selecionado, opcoes)
            
    def getUsuarios(self):
        return self._usuarios
    
    def getLivros(self):
        return self._livros
    
    def seleciona_funcao(self, opcao):
        if opcao == '1':
            return self.cadastra_usuario()
        elif opcao == '2':
            return self.cadastra_livro()
        elif opcao == '3':
            return self.cadastra_emprestimo()
        elif opcao == '4':
            return self.cadastra_devolucao()
        elif opcao == '5':
            return self.pesquisa_livro()
        elif opcao == '6':
            return self.pesquisa_usuario()
        elif opcao == '7':
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
        autor = input("Autor do livro ")
        generos = input("Insira os gêneros do livro, separados por vírgula (,): ")
        generos = generos.split(",")
        disponibilidade = True
        qt_pagina_valida = False
        while not qt_pagina_valida:
            qt_pagina = input("Quantidade de páginas: ")
            try:
                qt_pagina = int(qt_pagina)
                qt_pagina_valida = True
            except Exception as e:
                print("Quantidade de páginas não é um valor válido. Tente novamente. Valor esperado: inteiro.")
        livro = Livro(nome, autor, generos, disponibilidade, qt_pagina)
        self._livros.append(livro)
        
    def cadastra_emprestimo(self):
        print("Cadastro de Empréstimo")
        print("Passo 1: Selecione o usuário que está realizando o empréstimo.")
        usuario = self.pesquisa_usuario()
        
        print("Passo 2: Selecione o livro que está sendo emprestado.")
        livro = Livro()
        livro_disponibilidade_ok = False
        while not livro_disponibilidade_ok:
            livro = self.pesquisa_livro()
            if livro.getDisponibilidade():
                livro_disponibilidade_ok = True
            else:
                print("Livro selecionado não está disponível. Por favor, selecione outro livro.")
        
        dt_emprestimo = datetime.datetime.now()

        duracao_emprestimo = datetime.timedelta(weeks=2)
        dt_devolucao = dt_emprestimo + duracao_emprestimo

        emprestimo = Emprestimo(dt_emprestimo, dt_devolucao, usuario, livro, True)
        self._historico_emprestimos.append(emprestimo)

        print("O empréstimo foi cadastrado com sucesso. Devolução prevista para {d}".format(d=dt_devolucao))
    
    def cadastra_devolucao(self):
        if len(self._historico_emprestimos) > 0:
            opcoes = ["1", "2"]
            tipos = ["Usuário", "Livro"]
            fns = ["pesquisa_usuario", "pesquisa_livro"]

            tipo_filtro = ""
            filtro = ""
            opcao_ok = False
            while not opcao_ok:
                print("Pesquisar empréstimo por:")
                for i in range(len(opcoes)):
                    print("{n} - {opcao}".format(n = opcoes[i], opcao = tipos[i]))
                selecionado = input("")
                if selecionado in opcoes:
                    tipo_filtro = opcoes.index(selecionado)
                    filtro = getattr(self, fns[tipo_filtro])()
                else:
                    print("Opção inválida. Tente novamente.")
                    continue
                emprestimos_em_aberto = list(filter(lambda emprestimo : emprestimo.getStatus(), self._historico_emprestimos))
                emprestimo = self.filtrarEmprestimo(filtro, emprestimos_em_aberto)
                if emprestimo is not None:
                    emprestimo.realizarDevolucao()
                else:
                    print("Nenhum empréstimo selecionado. Tente novamente.")
        else:
            print("Não há empréstimos da base de dados. Para que uma devolução possa ocorrer, é preciso existir um empréstimo.")

    def filtrarEmprestimo(self, filtro, lista_emprestimo):
        if not lista_emprestimo:
            lista_emprestimo = self._historico_emprestimos
        if len(self._historico_emprestimos) > 0:
            filtrados = []
            if isinstance(filtro, Usuario):
                filtrados = list(filter(lambda emprestimo : emprestimo.getUsuario() == filtro, lista_emprestimo))
            elif isinstance(filtro, Livro):
                filtrados = list(filter(lambda emprestimo : emprestimo.getLivro() == filtro, lista_emprestimo))
            qt_filtrados = len(filtrados)
            if qt_filtrados == 1:
                emprestimo = filtrados[0]
                print("1 empréstimo encontrado com o filtro")
                return self.validarEscolha(emprestimo)
            elif qt_filtrados > 1:
                print("{qt} de empréstimos encontrados para esse filtro".format(qt = qt_filtrados))
                emprestimo = self.escolheObjeto(filtrados, qt_filtrados, "empréstimo")
                return emprestimo
        print("Não há empréstimos da base de dados. Antes de pesquisar um empréstimo, cadastre algum.")

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
            print("1 livro encontrado")
            return self.validarEscolha(livro)
        elif qt_filtrados > 1:
            print("{qt} livros encontrados".format(qt = qt_filtrados))
            livro = self.escolheObjeto(filtrados, qt_filtrados, "livro")
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
            filtro = input("Digite o gênero a ser buscado: ")
            lowerStr = lambda a : a.lower()
            filtrarPor = lambda usuario : filtro.lower() in list(map(lowerStr, getattr(usuario, func_name)()))
        else:
            filtro = input("Digite o {t} a ser buscado: ".format(t = tipo))
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
                    usuario = self.filtrarUsuarios(func_escolhida, input("Digite o {t} a ser buscado: ".format(t = tipo)))
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
            print("{qt} usuários encontrados".format(qt = qt_filtrados))
            usuario = self.escolheObjeto(filtrados, qt_filtrados, "usuário")
            return usuario

    def escolheObjeto(self, lista, qt, tipo_dado):
        opcao_ok = False
        while not opcao_ok:
            print("Dados dos(as) {t}s encontrados(as)".format(t = tipo_dado))
            for i in range(qt):
                objeto = lista[i]
                print("{t} #{n}".format(t=tipo_dado.capitalize(),n=i+1))
                objeto.exibeDados()
                if i < qt - 1:
                    print("--------------")
            opcoes = [str(i) for i in range(1, qt + 1)]
            escolhido = input("Selecione o(a) {t} desejado(a): ".format(t = tipo_dado))
            if escolhido in opcoes:
                objetoEscolhido = lista[int(escolhido) - 1]
                if self.validarEscolha(objetoEscolhido):
                    return objetoEscolhido
                else:
                    return None
            else:
                print("Opção inválida.")

    def validarEscolha(self, escolha):
        print("Dados da opção escolhida:")
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
    
    def setDisponibilidade(self, valor: bool):
        if isinstance(valor, bool):
            self._disponibilidade = valor
        else:
            print("Erro ao setar novo valor de disponibilidade {nv}, valor anterior inalterado para o livro {n}. Valor atual = {v}.".format(nv = valor, n = self._nome, v = self._disponibilidade))

    def getQuantidadeDePaginas(self):
        return self._qt_pagina
    
    def exibeDados(self):
        generos = self.getGeneros()
        generosToString = ' '.join(map(str, generos))
        disponibilidade = "Disponível" if self.getDisponibilidade() else "Indisponível"
        print("Nome: {n}".format(n=self.getNome()))
        print("Autor: {e}".format(e=self.getAutor()))
        print("Generos: {g}".format(g = generosToString))
        print("Disponibilidade: {d}".format(d = disponibilidade))
        print("Endereço: {t}".format(t=str(self.getQuantidadeDePaginas())))

class Emprestimo:
    def __init__(self, dt_emprestimo, dt_devolucao, usuario: Usuario, livro: Livro, status: bool):
        self._dt_emprestimo = dt_emprestimo
        self._dt_devolucao = dt_devolucao
        self._usuario = usuario
        self._livro = livro
        self._status = status
        self._livro.setDisponibilidade(False)

    def getDataEmprestimo(self):
        return self._dt_emprestimo

    def getDataDevolucao(self):
        return self._dt_devolucao

    def getUsuario(self):
        return self._usuario

    def getLivro(self):
        return self._livro

    def getStatus(self):
        return self._status

    def verificarAtraso(self):
        return self._status == True and datetime.datetime.now() > self.getDataDevolucao()

    def realizarDevolucao(self):
        self._status = False
        self._livro.setDisponibilidade(True)
    
    def exibeDados(self):
        status = "Finalizada" if self._status == False else ("Em Atraso" if self.verificaAtraso() else "Em Aberto")
        data_emprestimo_formatada = self.getDataEmprestimo().strftime("%m/%d/%Y")
        data_devolucao_formatada = self.getDataDevolucao().strftime("%m/%d/%Y")
        print("Usuario: {n}".format(n = self.getUsuario().exibeDados()))
        print("Livro: {e}".format(e = self.getLivro().exibeDados()))
        print("Data de empréstimo: {dt_e}".format(dt_e = data_emprestimo_formatada))
        print("Data de devolução: {dt_d}".format(dt_d = data_devolucao_formatada))
        print("Status: {s}".format(s = status))

biblioteca = Biblioteca()
biblioteca.exec()
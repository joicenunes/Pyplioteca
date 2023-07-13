"""
1. Sistema de gerenciamento de biblioteca: desenvolva um sistema de gerenciamento de uma biblioteca em Python, utilizando estruturas de dados apropriadas para armazenar informações sobre os livros, usuários, empréstimos, etc. Implemente, no mínimo, as funcionalidades de cadastro de livros e usuários, empréstimos, devoluções, pesquisa e relatórios.
"""

import sys
import datetime

from emprestimo import Emprestimo
from livro import Livro
from usuario import Usuario

from helper import maximiza_caracteres_ou_corta_string

class Biblioteca:
    def __init__(self):
        self._usuarios = []
        self._livros = []
        self._historico_emprestimos = []

        #mockando usuarios para testar busca
        usuariosMockados = [
            ("João Silva", "joao.silva@gmail.com", "(11) 98765-4321", "Rua A, 123"),
            ("Maria Santos", "maria.santos@yahoo.com", "(22) 99999-8888", "Avenida B, 456"),
            ("Pedro Almeida", "pedro.almeida@hotmail.com", "(33) 55555-4444", "Rua C, 789"),
            ("Ana Oliveira", "ana.oliveira@gmail.com", "(44) 12345-6789", "Avenida D, 012"),
            ("Lucas Pereira", "lucas.pereira@yahoo.com", "(55) 77777-6666", "Rua E, 345"),
            ("Mariana Costa", "mariana.costa@hotmail.com", "(66) 22222-1111", "Avenida F, 678"),
            ("Carlos Santos", "carlos.santos@gmail.com", "(77) 44444-3333", "Rua G, 901"),
            ("Camila Rodrigues", "camila.rodrigues@yahoo.com", "(88) 88888-9999", "Avenida H, 234"),
            ("Rafaela Fernandes", "rafaela.fernandes@hotmail.com", "(99) 33333-2222", "Rua I, 567"),
            ("Bruno Oliveira", "bruno.oliveira@gmail.com", "(00) 11111-0000", "Avenida J, 890")
        ]
        """ Obrigada chatGPT pelos dados fictícios """
        for info in usuariosMockados:
            nome, email, telefone, endereco = info
            usuario = Usuario(nome, email, telefone, endereco)
            self._usuarios.append(usuario)

        #mockando livros para testar busca
        livrosMockados = [
            ("Sobre os ossos dos mortos", "Olga Tokarczuk", "Aventura,Suspense,Mistério", 246),
            ("Crepúsculo", "Stephenie Meyer", "Romance,Fantasia", 478),
            ("Cloud Atlas", "David Mitchell", "Ficção Científica,Ficção Histórica", 530),
            ("Dom Quixote", "Miguel de Cervantes", "Romance, Clássico", 863),
            ("1984", "George Orwell", "Distopia, Ficção Científica", 328),
            ("Orgulho e Preconceito", "Jane Austen", "Romance, Clássico", 432),
            ("Crime e Castigo", "Fyodor Dostoevsky", "Romance, Clássico", 671),
            ("O Senhor dos Anéis", "J.R.R. Tolkien", "Fantasia, Aventura", 1178),
            ("A Revolução dos Bichos", "George Orwell", "Sátira, Ficção Política", 144),
            ("Cem Anos de Solidão", "Gabriel García Márquez", "Realismo Mágico, Romance", 417),
            ("O Grande Gatsby", "F. Scott Fitzgerald", "Romance, Drama", 180),
            ("As Crônicas de Nárnia", "C.S. Lewis", "Fantasia, Aventura", 767),
            ("A Metamorfose", "Franz Kafka", "Ficção Absurda, Clássico", 55),
            ("Moby Dick", "Herman Melville", "Romance, Aventura", 585),
            ("O Conde de Monte Cristo", "Alexandre Dumas", "Aventura, Drama", 1312),
            ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", "Fantasia, Filosófico", 96),
            ("Ulisses", "James Joyce", "Modernismo, Romance", 783)
        ]
        """ Obrigada chatGPT pelos dados fictícios """
        for info in livrosMockados:
            nome, autor, generos, paginas = info
            livro = Livro(nome, autor, generos, paginas)
            self._livros.append(livro)

        hoje = datetime.datetime.now()
        duas_semanas = datetime.timedelta(weeks=2)
        dt_devolucao = hoje + duas_semanas

        """ aqui sao os emprestimos mockados bonitinhos pra testar os relatórios de empréstimo
        emprestimosMockados = [
            (self._usuarios[0], self._livros[0], hoje, dt_devolucao),
            (self._usuarios[3], self._livros[3], hoje, dt_devolucao),
            (self._usuarios[6], self._livros[6], hoje, dt_devolucao),
        ]"""

        """ aqui vao os emprestimos atrasados para testar o relatorio de emprestimo em atraso """
        emprestimosMockados = [
            (self._usuarios[0], self._livros[0], hoje, hoje + duas_semanas),
            (self._usuarios[3], self._livros[3], hoje - duas_semanas, hoje - datetime.timedelta(days=2)),
            (self._usuarios[6], self._livros[6], hoje - duas_semanas, hoje - datetime.timedelta(days=5)),
        ]

        for info in emprestimosMockados:
            usuario, livro, dt_emp, dt_dev = info
            emprestimo = Emprestimo(dt_emp, dt_dev, usuario, livro)
            self._historico_emprestimos.append(emprestimo)

    def exec(self):
        while True:
            print("Selecione uma opção:")
            acoes = ["Cadastrar usuário", "Cadastrar livro", "Cadastrar empréstimo", "Cadastrar devolução", "Pesquisar livro", "Pesquisar usuário", "Gerar relatório"]
            opcoes = [str(i) for i in range(1, len(acoes) + 1)]
            for i in range(len(acoes)):
                print("{n} - {opcao}".format(n = opcoes[i], opcao = acoes[i]))
            print("0 - Sair")
            selecionado = input("")
            if selecionado == "0":
                sys.exit()
            self.seleciona_funcao(selecionado, opcoes)
            
    def getUsuarios(self):
        return self._usuarios
    
    def getLivros(self):
        return self._livros
    
    def seleciona_funcao(self, opcao, opcoes):
        funcs = ["cadastra_usuario", "cadastra_livro", "cadastra_emprestimo", "cadastra_devolucao", "pesquisa_livro", "pesquisa_usuario", "gera_relatorio"]
        if opcao in opcoes:
            return getattr(self, funcs[opcoes.index(opcao)])()
        else:
            print("Essa opção não é válida. Tente novamente.")
            return

    def exibe_opcoes(self, opcoes, tipos):
        for i in range(len(opcoes)):
            print("{n} - {opcao}".format(n = opcoes[i], opcao = tipos[i]))
        
    def cadastra_usuario(self):
        print("Cadastro de Usuário")
        nome = input("(1/4) Nome do usuário: ")
        email = input("(2/4) Email do usuário ")
        telefone = input("(3/4) Telefone do usuário: ")
        endereco = input("(4/4) Endereço do usuário: ")
        usuario = Usuario(nome, email, telefone, endereco)
        usuario.exibeDados()
        usuario = self.loop_confirmacao_binaria(usuario, "Confirmar criação desse usuário? (Y/n)", "Usuário criado.", "Criação de usuário cancelada.")
        if usuario:
            self._usuarios.append(usuario)
        
    def cadastra_livro(self):
        print("Cadastro de Livro")
        nome = input("(1/4) Nome do livro: ")
        autor = input("(2/4) Autor do livro: ")
        generosStr = input("(3/4) Insira os gêneros do livro, separados por vírgula (,): ")
        disponibilidade = True
        qt_pagina_valida = False
        while not qt_pagina_valida:
            qt_pagina = input("(4/4) Quantidade de páginas: ")
            try:
                qt_pagina = int(qt_pagina)
                qt_pagina_valida = True
            except Exception as e:
                print("Quantidade de páginas não é um valor válido. Tente novamente. Valor esperado: inteiro.")
        livro = Livro(nome, autor, generosStr, disponibilidade, qt_pagina)
        livro.exibeDados()
        livro = self.loop_confirmacao_binaria(livro, "Confirmar criação desse livro? (Y/n)", "Livro criado.", "Criação de livro cancelada.")
        if livro:
            self._livros.append(livro)

    def cadastra_emprestimo(self):
        print("Cadastro de Empréstimo")
        print("(1/2) Selecione o usuário que está realizando o empréstimo.")
        usuario = self.pesquisa_usuario()
        
        print("(2/2) Selecione o livro que está sendo emprestado.")
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

        emprestimo = Emprestimo(dt_emprestimo, dt_devolucao, usuario, livro)
        self._historico_emprestimos.append(emprestimo)

        print("O empréstimo foi cadastrado com sucesso. Devolução prevista para {d}".format(d=dt_devolucao.strftime("%d/%m/%Y")))
    
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
                self.exibe_opcoes(opcoes, tipos)
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
                self.exibe_opcoes(opcoes, tipos)
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
        if func_name == "getDisponibilidade":
            disponibilidade_ok = False
            while not disponibilidade_ok:
                print("Escolha a disponibilidade a ser buscada: ")
                opcoes = ["1", "2"]
                tipos = ["Disponível", "Indisponível"]
                tipos_boolean = [True, False]
                self.exibe_opcoes(opcoes, tipos)
                filtro = input("")
                if filtro in opcoes:
                    return lambda usuario : getattr(usuario, func_name)() == tipos_boolean[opcoes.index(filtro)]
                else:
                    print("Opção inválida. Tente novamente.")
        elif func_name == "getGeneros":
            filtro = input("Digite o gênero a ser buscado: ")
            lowerStr = lambda a : a.lower()
            return lambda usuario : filtro.lower() in list(map(lowerStr, getattr(usuario, func_name)()))
        else:
            filtro = input("Digite o {t} a ser buscado: ".format(t = tipo))
            return lambda usuario : filtro.lower() in getattr(usuario, func_name)().lower()
        
    def pesquisa_usuario(self):
        if len(self._usuarios) > 0:
            opt_ok = False
            while not opt_ok:
                print("Procurar o usuário por:")
                tipos = ["Nome", "Email", "Telefone"]
                opcoes = ['1', '2', '3']
                self.exibe_opcoes(opcoes, tipos)
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
        print("Dados da opção")
        escolha.exibeDados()
        return self.loop_confirmacao_binaria(escolha, "Confirmar escolha? (Y/n) ", "", "Realizar a busca novamente.")
    
    def loop_confirmacao_binaria(self, objeto, pergunta, mensagem_sucesso, mensagem_erro):
        confirmado = False
        while not confirmado:
            validacao = input(pergunta)
            if validacao.lower() == "y" or validacao == "":
                fim = "" if mensagem_sucesso == "" else "\n"
                print(mensagem_sucesso, end = fim)
                return objeto
            elif validacao.lower() == "n":
                print(mensagem_erro)
                return False
            else:
                print("Opção inválida. Tente novamente:")
        
    def gera_relatorio(self):
        opcoes = ["1", "2", "3", "4", "5"]
        tipos = ["Histórico de empréstimo por usuário", "Histórico de empréstimo por livro", "Livros disponíveis", "Livros indisponíveis", "Empréstimos em atraso"]
        criterios = ["usuario", "livro", True, False, "atraso"]
        print("Selecione o tipo de relatório:")
        self.exibe_opcoes(opcoes, tipos)
        selecionado = input("")
        if selecionado in ["1", "2", "5"]:
            self.gera_relatorio_emprestimo(criterios[opcoes.index(selecionado)])
        elif selecionado in ["3", "4"]:
            self.gera_relatorio_livros(criterios[opcoes.index(selecionado)])
        else:
            print("Essa opção não é válida.")

    def gera_relatorio_emprestimo(self, criterio):
        filtrados = []

        opcoes = ["usuario", "livro", "atraso"]
        filtro_fns = ["pesquisa_usuario", "pesquisa_livro"]
        lambdas = ["getUsuario", "getLivro", "verificarAtraso"]
        
        filtro = True
        criterio_idx = opcoes.index(criterio)

        if criterio_idx < 2:
            filtro = getattr(self, filtro_fns[criterio_idx])()

        filtrados = list(filter(lambda emprestimo : getattr(emprestimo, lambdas[criterio_idx])() == filtro, self._historico_emprestimos))

        if len(filtrados) > 0:
            print("Imprimindo relatório de empréstimo. Critério: {c}".format(c = criterio))
            print("{nome} | {titulo} | {dt_emp} | {dt_dev} | {status}".format(nome = maximiza_caracteres_ou_corta_string("Nome do Usuário", 50), titulo = maximiza_caracteres_ou_corta_string("Título do Livro", 50), dt_emp = maximiza_caracteres_ou_corta_string("Empréstimo", 10), dt_dev = maximiza_caracteres_ou_corta_string("Devolução", 10), status = maximiza_caracteres_ou_corta_string("Status", 10)))
            for i in range(len(filtrados)):
                filtrados[i].exibeDadosTabelado()
        else:
            print("Não foram encontrados dados para o relatório.")

    def gera_relatorio_livros(self, disponibilidade):
        """
        Foi removida a ideia de filtragem por data dinâmica pois para essa ideia funcionar eu teria que ter desenvolvido um sistema de reserva e eu só pensei isso muito em cima da entrega
        """
        filtrados = list(filter(lambda livro : livro.getDisponibilidade() == disponibilidade, self._livros))
        if len(filtrados) > 0:
            print("Imprimindo relatório de livros. Critério: {c}".format(c = "Disponível" if disponibilidade else "Indisponível"))
            print("{titulo} | {autor} | {generos} | {qt_paginas}".format(titulo = maximiza_caracteres_ou_corta_string("Título do Livro", 50), autor = maximiza_caracteres_ou_corta_string("Nome do Autor", 50), generos = maximiza_caracteres_ou_corta_string("Gêneros", 50), qt_paginas = maximiza_caracteres_ou_corta_string("Qt. Páginas", 11)))
            for i in range(len(filtrados)):
                filtrados[i].exibeDadosTabelado()
        else:
            print("Não foram encontrados dados para o relatório.")

biblioteca = Biblioteca()
biblioteca.exec()
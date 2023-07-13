from helper import maximiza_caracteres_ou_corta_string

class Livro:
    def __init__(self, nome: str = None, autor: str = None, generos: str = None, qt_pagina: int = None, disponibilidade: bool = True):
        self._nome = nome
        self._autor = autor
        if generos is not None:
            self._generos = [genero.strip() for genero in generos.split(",")]
        else:
            self._generos = generos
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
        generosToString = ', '.join(generos)
        disponibilidade = "Disponível" if self.getDisponibilidade() else "Indisponível"
        print("Nome: {n}".format(n=self.getNome()))
        print("Autor: {e}".format(e=self.getAutor()))
        print("Generos: {g}".format(g = generosToString))
        print("Disponibilidade: {d}".format(d = disponibilidade))
        print("Quantidade de páginas: {t}".format(t=str(self.getQuantidadeDePaginas())))

    def exibeDadosTabelado(self, max_nomes = 50):
        titulo_livro = maximiza_caracteres_ou_corta_string(self.getNome(), max_nomes)
        nome_autor = maximiza_caracteres_ou_corta_string(self.getAutor(), max_nomes)
        generosToString = maximiza_caracteres_ou_corta_string(', '.join(self.getGeneros()), max_nomes)
        qt_paginas_maximizada = maximiza_caracteres_ou_corta_string(str(self.getQuantidadeDePaginas()), 4)
        print("{lTitulo} | {lAutor} | {generos} | {qt_paginas}".format(lTitulo = titulo_livro, lAutor = nome_autor, generos = generosToString, qt_paginas = qt_paginas_maximizada))

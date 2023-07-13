import datetime
from helper import maximiza_caracteres_ou_corta_string

from livro import Livro
from usuario import Usuario

class Emprestimo:
    def __init__(self, dt_emprestimo, dt_devolucao, usuario: Usuario, livro: Livro):
        self._dt_emprestimo = dt_emprestimo
        self._dt_devolucao = dt_devolucao
        self._usuario = usuario
        self._livro = livro
        self._status = True
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

    def descreveStatus(self):
        return "Finalizada" if self._status == False else ("Em Atraso" if self.verificarAtraso() else "Em Aberto")
    
    def formataData(self, data):
        return data.strftime("%d/%m/%Y")
    
    def exibeDados(self):
        data_emprestimo_formatada = self.formataData(self.getDataEmprestimo())
        data_devolucao_formatada = self.formataData(self.getDataDevolucao())
        print("Usuario: {n}".format(n = self.getUsuario().exibeDados()))
        print("Livro: {e}".format(e = self.getLivro().exibeDados()))
        print("Data de empréstimo: {dt_e}".format(dt_e = data_emprestimo_formatada))
        print("Data de devolução: {dt_d}".format(dt_d = data_devolucao_formatada))
        print("Status: {s}".format(s = self.descreveStatus()))

    def exibeDadosTabelado(self, max_nomes = 50):
        data_emprestimo_formatada = self.formataData(self.getDataEmprestimo())
        data_devolucao_formatada = self.formataData(self.getDataDevolucao())
        nome_usuario = maximiza_caracteres_ou_corta_string(self.getUsuario().getNome(), max_nomes)
        titulo_livro = maximiza_caracteres_ou_corta_string(self.getLivro().getNome(), max_nomes)
        print("{uNome} | {lTitulo} | {dEmprestimo} | {dDevolucao} | {s}".format(uNome = nome_usuario, lTitulo = titulo_livro, dEmprestimo = data_emprestimo_formatada, dDevolucao = data_devolucao_formatada, s = self.descreveStatus()))
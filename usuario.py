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

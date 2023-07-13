def maximiza_caracteres_ou_corta_string(string, tamanho):
    if len(string) <= tamanho:
        string += ' ' * (tamanho - len(string))
    else:
        string = string[0:tamanho - 3] + "..."
    return string
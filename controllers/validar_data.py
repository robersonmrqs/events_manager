import re

# Função para validar formato de data brasileiro (DD/MM/AAAA)
def validar_data(data):
    padrao = r"^([0-2][0-9]|3[0-1])/(0[1-9]|1[0-2])/\d{4}$"
    return re.match(padrao, data) is not None
def calcular_frete(cep):
    if cep.startswith("01"):
        return 12.90
    elif cep.startswith("20"):
        return 18.50
    else:
        return 25.00
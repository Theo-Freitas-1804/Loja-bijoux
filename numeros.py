import random

numeros = {
  "positivos": [ 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12] ,
  "negativos": [-1 , -2 , -3 , -4 , -5 , -6 , -7 , -8 , -10 ,-11 , -12] ,
  "pares": [2 , 4 , 6 , 8 , 10 , 12] ,
  "impares": [1 , 3 , 5 , 7 , 9 , 11]
}

for n in numeros:
  par = random.choice(numeros["pares"])
  impar = random.choice(numeros["impares"])
  positivo = random.choice(numeros["positivos"])
  negativo = random.choice(numeros["negativos"])
  
  print(f" os números escolhidos são: {par} , {impar} , {positivo} ,{negativo}")
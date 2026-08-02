from sklearn.linear_model import LinearRegression

X = [
    [10],
    [20],
    [30],
    [40],
    [50]
]

y = [
    1000,
    1500,
    2100,
    2600,
    3200
]

modelo = LinearRegression()

modelo.fit(X, y)

valor = int(input("Quanto quer prever? "))

resultado = modelo.predict([[valor]])

print(f"A previsão é {resultado[0]:.0f}")

print(modelo.coef_)
print(modelo.intercept_)
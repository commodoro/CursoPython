# S2E2: Raíces de un polinomio.

Una raiz de un polinomio es un valor x tal que P(x) = 0.

1. Realiza un programa que encuentre raices reales de un polinomio de grado 3 por métodos iterativos (se recomienda el método de newton).

2. Mejora el programa para que encuentre raices reales de un polinomio de **cualquier grado** por métodos iterativos (se recomienda el método de newton).

3. [**Extra - No oblig.**] Encuentra TODAS las raices reales de un polinomio.

**Pista**: una forma eficiente de tratar los polinomio es guardando solo los coeficientes. Por ejemplo el polinomio x**2 + 3x - 1 puede ser codificado como 1 3 -1. En Python esto lo podemos traducir en:

    polinomio = input("Introduce coeficientes separados por comas.")
    grado = polinomio.count(' ')
    i = 0
    for coeff in polinomio.split(' '):
        print(coeff)
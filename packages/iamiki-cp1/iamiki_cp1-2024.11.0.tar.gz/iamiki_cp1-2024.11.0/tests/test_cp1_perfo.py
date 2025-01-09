
import pandas as pd
import numpy as np
import timeit

def test_performance():
    # Générer un DataFrame d'exemple
    np.random.seed(0)
    dfin = pd.DataFrame({'v2': np.random.rand(1000000)})

    # Méthode 1: Utilisation de lambda
    def apply_lambda():
        dfin['v2'] = dfin['v2'].apply(lambda x: 0.5 if x < 0.5 else x)

    # Méthode 2: Utilisation de loc
    def apply_loc():
        dfin.loc[dfin['v2'] < 0.5, 'v2'] = 0.5

    # Mesurer le temps de calcul pour chaque méthode
    time_lambda = timeit.timeit(apply_lambda, number=10)
    time_loc = timeit.timeit(apply_loc, number=10)

    # Assertion pour vérifier que time_loc est inférieur à time_lambda
    assert time_loc < time_lambda, f"Expected time_loc < time_lambda, but got {time_loc} >= {time_lambda}"

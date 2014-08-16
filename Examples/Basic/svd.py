#python imports
import time

#3rd party imports
import numpy as np
import pandas as pd

def pd_svd(pd_dataframe):
    np_dataframe = pd_dataframe.values
    return np.linalg.svd(pd_dataframe)

if __name__ == '__main__':
    for i in range(1, 20):
        pd_dataframe = pd.DataFrame(np.random.random((3000, 252 * i)))
        pd_svd(pd_dataframe)
    

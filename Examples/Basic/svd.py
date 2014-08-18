#python imports
import time

#3rd party imports
import numpy as np
import pandas as pd


def pd_svd(pd_dataframe):
    np_dataframe = pd_dataframe.values
    return np.linalg.svd(pd_dataframe)

if __name__ == '__main__':
    li_times = []
    for i in range(1, 3):
        pd_dataframe = pd.DataFrame(np.random.random((3000, 252 * i)))
        start = time.time()
        pd_svd(pd_dataframe)
        li_times.append(str(time.time() - start))
    
    print li_times
    with open(sys.argv[1], 'a') as f:
        writer = csv.writer(f)
        writer.writerow(li_times)

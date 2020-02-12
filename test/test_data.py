import os

import numpy as np
import pandas as pd

from core.data import Data


def test_data_from_csv():
    test_file_path = str(os.path.dirname(__file__))
    file = 'data/test_dataset.csv'
    df = pd.read_csv(os.path.join(test_file_path, file))
    data_array = np.array(df).T
    features = data_array[1:-1].T
    target = data_array[-1]
    idx = data_array[0]
    assert Data.from_csv(os.path.join(test_file_path, file)).features.all() == Data(
        features=features, target=target, idx=idx).features.all()

__version__ = '0.0.10'

import os
import pandas as pd # type: ignore

def load_dataset(file_name):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, f'../Data/{file_name}')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_name}' does not exist in the Data directory.")
    return pd.read_csv(file_path, encoding='utf-8')


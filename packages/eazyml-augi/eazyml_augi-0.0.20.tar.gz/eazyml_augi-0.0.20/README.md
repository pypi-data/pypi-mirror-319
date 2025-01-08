## Eazyml Augmented Intelligence
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.20-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

EazyML Augmented Intelligence extract insights from Dataset with certain insights
score which is calculated using coverage of that insights.

### Features
- Builds a predictive model based on the input training data, mode, and options. 
    Supports classification and regression tasks.
### APIs
It provides following apis :

1. scikit_feature_selection
    ```python
    ez_augi(mode='classification',
            outcome='target',
            train_file_path='train.csv')

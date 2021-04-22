import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import metrics
from sklearn.dummy import DummyRegressor


def r2_adj(r2, n, k):
  return 1 - ((1 - r2) * (n-1) / (n-k-1))

def linear_regression(X, y, log_transform_y=False):
  X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=27)
  lr = LinearRegression()
  train_csv = cross_val_score(lr, X_train, y_train, cv=5)
  test_csv = cross_val_score(lr, X_test, y_test)
  # fit the model and score
  lr.fit(X_train, y_train)
  train_r2 = lr.score(X_train, y_train)
  train_r2_adj = r2_adj(train_r2, len(y_train.index), len(X_train.columns))
  test_r2 = lr.score(X_test, y_test)
  test_r2_adj = r2_adj(test_r2, len(y_test.index), len(X_test.columns))
  # make predictions and get rmse
  preds = lr.predict(X_test)
  if log_transform_y:
    rmse = metrics.mean_squared_error(np.exp(y_test), np.exp(preds), squared=False)
  else:
    rmse = metrics.mean_squared_error(y_test, preds, squared=False)
  # Dummy model to see if our model makes things better
  dm = DummyRegressor()
  dm.fit(X_train, y_train)
  dm_train_r2 = dm.score(X_train, y_train)
  dm_train_r2_adj = r2_adj(dm_train_r2, len(y_train.index), len(X_train.columns))
  dm_test_r2 = dm.score(X_test, y_test)
  dm_test_r2_adj = r2_adj(dm_test_r2, len(y_test.index), len(X_test.columns))
  dm_preds = dm.predict(X_test)
  if log_transform_y:
    dm_rmse = metrics.mean_squared_error(np.exp(y_test), np.exp(dm_preds), squared=False)
  else:
    dm_rmse = metrics.mean_squared_error(y_test, dm_preds, squared=False)

    results = {
    
            'cross_val_score': {
            'train': train_csv.mean(),
            'test': test_csv.mean()
            },
            'R2': {
            'train': train_r2,
            'test': test_r2,
            'dm_train': dm_train_r2,
            'dm_test': dm_test_r2
            },
            'R2_adj': {
            'train': train_r2_adj,
            'test': test_r2_adj,
            'dm_train': dm_train_r2_adj,
            'dm_test': dm_test_r2_adj
            },
            'rmse': {
            'model': rmse,
            'dm': dm_rmse
            }
        }

    return pd.DataFrame(results)
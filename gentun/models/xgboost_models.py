#!/usr/bin/env python
"""
Machine Learning models compatible with the Genetic Algorithm implemented using xgboost
"""

import xgboost as xgb

from .generic_models import GentunModel


class XgboostModel(GentunModel):

    def __init__(self, x_train, y_train, hyperparameters, booster='gbtree', objective='reg:linear',
                 eval_metric='rmse', kfold=5, num_boost_round=5000, early_stopping_rounds=100, folds=None, verbose_eval=False):
        super(XgboostModel, self).__init__(x_train, y_train)
        self.params = {
            'booster': booster,
            'objective': objective,
            'eval_metric': eval_metric,
            'silent': 1
        }
        self.params.update(hyperparameters)
        self.eval_metric = eval_metric
        self.kfold = kfold
        self.num_boost_round = num_boost_round
        self.early_stopping_rounds = early_stopping_rounds
        self.folds = folds
        self.verbose_eval = verbose_eval

    def cross_validate(self):
        """Train model using k-fold cross validation and
        return mean value of validation metric.
        """
        d_train = xgb.DMatrix(self.x_train, label=self.y_train)
        # xgb calls its k-fold cross-validation parameter 'nfold'
        cv_result = xgb.cv(
            self.params, d_train, num_boost_round=self.num_boost_round,
            early_stopping_rounds=self.early_stopping_rounds, nfold=self.kfold,
            stratified=True, folds=self.folds, verbose_eval=self.verbose_eval,
            as_pandas=True
            # seed=0
        )
        # return the negative mean auc of the trained model
        return cv_result[f"test-{self.eval_metric}-mean"].iloc[-1]

from lightgbm import LGBMRegressor
from sklearn.model_selection import GridSearchCV
from __init___ import X,y


def LGBM(X=X,y=y,cv=5,random_state=42):
    lgbm_clf = LGBMRegressor(random_state=random_state)
    lgbm_params = {'learning_rate': [.01, 0.03, .05, 0.1],
                    "max_depth": [3,4,5]}
    
    grid_lgbm = GridSearchCV(lgbm_clf, 
                             param_grid=lgbm_params, 
                             cv=cv, 
                             refit=True)
    grid_lgbm.fit(X, y)
    pred_grid_lgbm = grid_lgbm.predict(X)
    
    return pred_grid_lgbm
    
    
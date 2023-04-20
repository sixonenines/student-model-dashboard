import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from patsy import dmatrices
from sklearn.metrics import f1_score, precision_score, recall_score, brier_score_loss
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

def deviance(X,y,model):
    return 2*log_loss(y, model.predict_proba(X), normalize=False)

    
def feature_engineering(df):
    df.loc[ df['First Attempt'] == 'incorrect', 'First Attempt'] = 0
    df.loc[ df['First Attempt'] == 'hint', 'First Attempt'] = 0
    df.loc[ df['First Attempt'] == 'correct', 'First Attempt'] = 1
    df = df[(df['First Attempt']==0) | (df['First Attempt']==1)]

    df=df.dropna()
    df.insert(22,'Outcome',df['First Attempt'])

    df.rename(columns={'KC (Default)': 'KCModel', 'Opportunity': 'OpportunityModel'}, inplace=True)

    df.rename(columns={'Corrects': 'CorrectModel', 'Incorrects': 'IncorrectModel'}, inplace=True)

    df.rename(columns={'Hints': 'TellsModel'}, inplace=True)
    return df

def getX(df,modeltype):
    if modeltype=="AFM":
        y, X = dmatrices('Outcome ~ AnonStudentId + KCModel+ KCModel:OpportunityModel', df,return_type="dataframe")
    elif modeltype=="PFM":
        y, X = dmatrices('Outcome ~ AnonStudentId + KCModel+ KCModel:(CorrectModel+IncorrectModel)', df,return_type="dataframe")
    elif modeltype=="IFM":
        y, X = dmatrices('Outcome ~ AnonStudentId + KCModel+ KCModel:(CorrectModel+IncorrectModel+TellsModel)', df,return_type="dataframe")
    return X

def trainModels(df,modeltype,X,uuid):

    y = df['Outcome']
    y= y.astype('int')

    TrainingModel=LogisticRegression(max_iter=1000)
    TrainingModel=TrainingModel.fit(X,y)

    k=10
    kf = KFold(n_splits=k, random_state=None)
    ACCcv = cross_val_score(TrainingModel , X, y, cv = kf).mean()


    predictedProb=TrainingModel.predict_proba(X)
    predictedClass=TrainingModel.predict(X)
    predictedProb=np.max(predictedProb,axis=1)
    predictionResultsdf=df
    predictionResultsdf=predictionResultsdf.assign(predProb=predictedProb,predClass=predictedClass)
    predictionResultsdf['predClass'].astype(int)
    predictionResultsdf['predProb']=predictionResultsdf['predProb'].round(2)
    predictionResultsdf.rename(columns={'predProb': "Py_{}_predictedProbabilities".format(modeltype), 'predClass': "Py_{}prediction".format(modeltype)}, inplace=True)


    X_train,X_test,y_train,y_test=train_test_split(X, y, test_size=0.2, random_state=0)
    TrainTestSplitModel=LogisticRegression(max_iter=1000)
    TrainTestSplitModel=TrainTestSplitModel.fit(X_train,y_train)


    y_pred=TrainTestSplitModel.predict(X_test)
    RMSE=np.sqrt(np.mean((y_test-y_pred)**2))
    f1=f1_score(y_test, y_pred, average="macro")
    precision=precision_score(y_test, y_pred, average="macro")
    recall=recall_score(y_test, y_pred, average="macro")
    likelihood=-deviance(X,y,TrainingModel)/2
    y_pred_proba=TrainingModel.predict_proba(X)[:,1]
    logloss=log_loss(y,y_pred_proba)
    loglikelihood=-logloss*len(y)
    K=len(TrainingModel.coef_[0])
    AIC = -2*loglikelihood+2*K
    n=len(df)
    AICc= -2*(loglikelihood)+2*K+(2*K*(K+1)/(n-K-1))
    BIC= AIC+K*(np.log(n)-2)
    brierscoreloss= brier_score_loss(y, y_pred_proba)




    exports= pd.DataFrame(columns=["Model_type","Models_AIC",\
                               "AICc","Models_BIC","NumParameters",\
                               "Likelihood","BrierScore","LogLoss",
                               "RMSE","ACCcv","Precision","Recall","F1"])
    exports.loc[len(exports.index)] = ["Py_{modeltype}".format(modeltype=modeltype),AIC,AICc,BIC,K,likelihood,brierscoreloss,logloss,RMSE,ACCcv,precision,recall,f1]


    exports=exports.round(2)
    coefs=np.transpose(TrainingModel.coef_).round(2)
    coefficients=pd.DataFrame(zip(X.columns, coefs))
    coefficients.columns=["Features","coef"]
    return exports, coefficients, predictionResultsdf
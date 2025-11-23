import os
from rpy2 import robjects
from rpy2.robjects import r, globalenv, default_converter, pandas2ri
from rpy2.robjects.conversion import localconverter
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
import matplotlib.pyplot as plt
import subprocess
import uuid
import io
import zipfile
from PythonModelScripts import feature_engineering,getX,trainModels
import traceback

if "submit_state" not in st.session_state:
            st.session_state.submit_state=False
            st.session_state.error=False
            st.session_state.uniqueid=str(uuid.uuid4())
            st.session_state.datapath=False
            st.session_state.pystats=[]
            st.session_state.rstats=[]
            st.session_state.coefDic={}
            st.session_state.extendedDfList=[]


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def dfcombiner(dflist):
    newdf=pd.DataFrame()
    for df in dflist:
        newdf=pd.concat([newdf,df])
    return newdf


@st.cache_data
def dfappender(cleanedDf,dflist):
    newdf=cleanedDf.copy()
    combined_results=pd.concat(dflist)
    combined_df=pd.concat([newdf,combined_results])
    final_df=combined_df[["Row"]].drop_duplicates()
    final_df=pd.merge(final_df,newdf,on='Row',how="left")
    for df in dflist:
        final_df=pd.merge(final_df,df, on="Row",how="left")
    return final_df

@st.cache_data
def read_excel(uploaded_file):       
    df=pd.read_excel(uploaded_file)
    return df

@st.cache_data
def save_excel(df):
    st.session_state.datapath=f'./data/{st.session_state.uniqueid}.xlsx' #Trying to fix this
    df.to_excel(st.session_state.datapath)
    return 1
@st.cache_data
def createPythonModels(df,modeltype,uniqueid):
        X=getX(df,modeltype)
        results=trainModels(df,modeltype,X,uniqueid)
        stats=results[0]
        coef=results[1]
        extendedDf=results[2]
        csv=convert_df(coef)
        st.session_state.coefDic[f"PY_{modeltype}_Coefficients"]=csv
        st.session_state.pystats.append(stats)
        st.session_state.extendedDfList.append(extendedDf)
        return {"stats":stats,"coef":coef}


@st.cache_data
def createRModels(modeltype,uuid):
    if modeltype=="AFM":
        process = subprocess.run(["Rscript","AFM_Script.R"] + [f'./data/{uuid}.xlsx',uuid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    elif modeltype=="PFM":
        process = subprocess.run(["Rscript","PFM_Script.R"] + [f'./data/{uuid}.xlsx',uuid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    elif modeltype=="IFM":
        process = subprocess.run(["Rscript","IFM_Script.R"] + [f'./data/{uuid}.xlsx',uuid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if process.returncode!=0:
        raise Exception(process.returncode)
    statspath=f"./output/{modeltype}_Rstats_{uuid}.csv"
    coefpath=f"./output/{modeltype}_Rcoef_{uuid}.csv"
    predpath=f"./output/{modeltype}_Pred_{uuid}.csv"
    stats=pd.read_csv(statspath).round(2)
    st.session_state.rstats.append(stats)
    coef=pd.read_csv(coefpath).round(2)
    preds=pd.read_csv(predpath)
    extendedDf=pd.DataFrame()
    extendedDf["Row"]=preds["Row"]
    extendedDf[f"R_{modeltype}predictedProbabilities"]=preds.iloc[:,1].round(2)
    extendedDf[f"R_{modeltype}prediction"]=preds.iloc[:,2]
    st.session_state.extendedDfList.append(extendedDf)
    csv=convert_df(coef)
    st.session_state.coefDic[f"R_{modeltype}_Coefficients"]=csv
    return {"stats":stats,"coef":coef}
                    
@st.cache_data
def create_plot(allstatsdf,chosen_metric):
    splitPoint=len(allstatsdf["Model_type"])//2
    pythonModels=allstatsdf["Model_type"].iloc[:splitPoint].values
    rModels=allstatsdf["Model_type"].iloc[splitPoint:].values
    colors=["green","blue"]
    for metric in chosen_metric:
        plt.clf()
        values=allstatsdf[metric].values
        pythonValues=values[:splitPoint]
        rValues=values[splitPoint:]
        plt.bar(pythonModels,pythonValues, color=colors[0])
        plt.bar(rModels,rValues, color=colors[1])
        plt.title(f"{metric}")
        plt.xlabel("Model_type")
        plt.ylabel(metric)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left',handles=[plt.Line2D([0], [0], color='green', label='Python'),plt.Line2D([0], [0], color='blue', label='R')])
        st.pyplot(plt)

st.title('IRT Student Models Dashboard')

uploaded_file = st.file_uploader("Choose a file",type=["xlsx"])
if uploaded_file is not None:
    originaldf=read_excel(uploaded_file)
    expected_column_names=['AnonStudentId','First Attempt','Corrects','Incorrects','Opportunity','Hints','KC (Default)']
    expected_data_types={'AnonStudentId':object,'First Attempt':object,'Corrects':"int64",'Incorrects':"int64",'Opportunity':["float64","int64"],'Hints':"int64",'KC (Default)':object}
    if not set(expected_column_names).issubset(originaldf.columns):
        uploaded_file=None
        st.error("Error: Please make sure to use the right columns")
    for col in originaldf.columns:
        if col in expected_data_types:
            if isinstance(expected_data_types[col],list):
                if not originaldf[col].dtype in expected_data_types[col]:
                    uploaded_file=None
                    st.error(f"Error: Please make sure to use the right datatype for {col} -> Panda {expected_data_types[col]}")
            else:
                if not originaldf[col].dtype==expected_data_types[col]:
                    uploaded_file=None
                    st.error(f"Error: Please make sure to use the right datatype for {col} -> Panda {expected_data_types[col]}")
else:
    st.warning("""Upload a XLSX file with an "AnonStudentId",  "KC (Default)", "First Attempt", "Incorrects", "Corrects" and "Hints" column""")

with open('./data/example_template.xlsx', 'rb') as xlsx_template:
    excel_bytes = xlsx_template.read()

st.download_button("Example xlsx file taken from DataShop @CMU",data=excel_bytes,file_name="example_template.xlsx",mime="text/csv")
with st.expander("XLSX structure"):
    st.write("""
        \nAnonStudentId: text
        \nFirst Attempt: correct, incorrect, hint, unknown
        \nCorrects: Positive number
        \nIncorrects: Positive number
        \nHints: Positive number
        \nOpportunity: Positive number
        \nKC (Default): text
    """)

if uploaded_file is not None:
    with st.form('my_form'):
        df=originaldf.copy()
        st.write('Choose Trainingmodels')
        selectedModels=st.multiselect('Models to select',['AFM','PFM','IFM'])
        submitted = st.form_submit_button('Submit')

    if submitted or st.session_state.submit_state:
        st.session_state.submit_state=True
        if st.session_state.datapath==False:
            st.session_state.datapath=f'./data/{st.session_state.uniqueid}.xlsx' # Trying to fix this
            df.to_excel(st.session_state.datapath)
        tab1, tab2, tab3,tab4 = st.tabs(["Python", "R","Evaluation Metrics","Predicted Outcomes and Downloads"])
        with tab1:
            cleanedDf=feature_engineering(df)
            st.header("Python Implementation")
            for modeltype in selectedModels:
                try:
                    st.subheader(f"{modeltype}")
                    results=createPythonModels(cleanedDf,modeltype,st.session_state.uniqueid)
                    st.dataframe(results["stats"].style.format(thousands="",precision=2))
                    st.dataframe(results["coef"])
                except:
                    st.error('Error creating Python models, might need more input data', icon="🚨") 
        with tab2:
            st.header("R Implementation")
            for modeltype in selectedModels:
                try:
                    st.subheader(f"{modeltype}")
                    results=createRModels(modeltype,st.session_state.uniqueid)
                    st.dataframe(results["stats"].style.format(thousands="",precision=2))    
                    st.dataframe(results["coef"].style.format(precision=2))
                except Exception as e:
                    st.error(e)
                    st.session_state.error="True"
                    st.error('Error creating R models, might need more input data', icon="🚨")       
        with tab3:
            if not st.session_state.error:
                st.header("Evaluation Metrics")
                pystatsdf=dfcombiner(st.session_state["pystats"])
                rstatsdf=dfcombiner(st.session_state["rstats"])
                st.session_state.allstatsdf=pd.concat([pystatsdf,rstatsdf])
                st.write(st.session_state.allstatsdf)
                all_metrics= st.session_state.allstatsdf.drop('Model_type',axis=1).columns
                with st.expander("Metric explanation"):
                    st.write("""\n
                    \nPrecision: Proportion of true positives to the amount of positive predictions. Should be intrepreted as a probability,
                     where 1 is the highest value which means that the model is not making any false positive predictions.
                    \nRecall: Proportion of true positives to the amount of positive outcomes. Should be interpreted as a probability,
                     where 1 is the highest value which means that the model has no false negatives
                    \nF1: Harmonic mean of precision and recall. Useful in cases where you want to take both the amount of false positives and false negatives
                      into account. F1 value ranges between 0 and 1, where a lower value means that the model is making too many
                      false positives or false negative predictions.
                    \nRoot mean squared error: Measures the average distance between predicted values and the actual values
                    \nAccuracy with cross-validation: Useful to evaluate the models ability to generalize to new data. The value ranges between 0 and 1, where 1 means
                      that the model was able to correctly classify all data entries.
                    \nLikelihood: Measure of how well a model fits the data
                    \nLog-likelihood: Natural logarithm of the likelihood function
                    \nNumParameters: Number of Parameters the model has
                    \nAIC (Akaike Information Criterion): Useful for comparing goodness of fit between different models, the lower the better 
                    \nAICc (Corrected Akaike Information Criterion): Like AIC, but with a correction term that accounts for the number of parameters in relation to the sample size
                    \nBIC (Bayesian Information Criterion): Like AIC, but with a stronger penaly on overly complex models
                    \nBrier Score Loss: Measures the accuracy of probabilistic predictions. A low score means that the model is able to predict
                      the correct outcome with high confidence.
                    """)
                st.session_state["chosen_metric"]=st.multiselect("Which statistic do you want to compare?",all_metrics,default=all_metrics[0])
                create_plot(st.session_state.allstatsdf,st.session_state["chosen_metric"])
        with tab4:
            if not st.session_state.error:
                predDf=dfappender(cleanedDf,st.session_state.extendedDfList)
                st.write("""Here is the predicted Outcome (1 or 0) of each data entry used
                        to build the model and the confidence (predicted probability)
                            in that predicted Outcome""")
                st.write(predDf)
                buffer=io.BytesIO()
                with zipfile.ZipFile(buffer,"w") as z:
                    z.writestr('PredictedOutcomes.csv',convert_df(predDf))
                    z.writestr('AllStats.csv',convert_df(st.session_state.allstatsdf))
                    for model,coefcsv in st.session_state.coefDic.items():
                        z.writestr(f"{model}.csv",coefcsv)
                zip_bytes=buffer.getvalue()
                st.download_button("Download Results", zip_bytes, "results.zip")
                
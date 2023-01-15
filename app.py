import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
import matplotlib.pyplot as plt
import subprocess
from PythonModelScripts import feature_engineering,getX,trainModels
import uuid
import streamlit_ext as ste




@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def dfcombiner(dflist):
    newdf=pd.DataFrame()

    for df in dflist:
        newdf=pd.concat([newdf,df])
    return newdf



st.title('IRT Student Models Dashboard')

uploaded_file = st.file_uploader("Choose a file",type=["xlsx"])
if uploaded_file is not None:
    df=pd.read_excel(uploaded_file)
else:
    st.warning("""Upload a XLXS file with an "AnonStudentId",  "KC (Default)", "First Attempt", "Incorrects", "Corrects" and "Hints" column""")

submitted=""

if uploaded_file is not None:
    with st.form('my_form'):
        st.write('Choose Trainingmodels')
        selectedModels=st.multiselect('Models to select',['AFM','PFM','IFM']) 
        submitted = st.form_submit_button('Submit')

    if submitted:
        pystats=[]
        rstats=[]
        uniqueid=str(uuid.uuid4())
        datapath=f'./data/{uniqueid}.xlsx'
        writer = pd.ExcelWriter(datapath, engine='xlsxwriter')
        df.to_excel(writer,sheet_name="data")
        writer.save()
        tab1, tab2 = st.tabs(["Python", "R"])
        with tab1:
            df=feature_engineering(df)
            st.header("Python Implementation")
            for modeltype in selectedModels:
                st.subheader(f"{modeltype}")
                X=getX(df,modeltype)
                results=trainModels(df,modeltype,X,uniqueid)
                stats=results[0]
                coef=results[1]
                stats
                pystats.append(stats)
                coef
                csv=convert_df(coef)
                ste.download_button(f"Export {modeltype} Coefficients",csv,f'{modeltype}_Pycoef_{uniqueid}.csv')
                

        with tab2:
            st.header("R Implementation")
            for modeltype in selectedModels:
                try:
                    st.subheader(f"{modeltype}")
                    if modeltype=="AFM":
                        process = subprocess.run(["Rscript","AFM_Script.R"] + [f'./data/{uniqueid}.xlsx',uniqueid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                    elif modeltype=="PFM":
                        process = subprocess.run(["Rscript","PFM_Script.R"] + [f'./data/{uniqueid}.xlsx',uniqueid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                    elif modeltype=="IFM":
                        process = subprocess.run(["Rscript","IFM_Script.R"] + [f'./data/{uniqueid}.xlsx',uniqueid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                    if process.returncode!=0:
                        raise Exception(process.returncode)
                    statspath=f"./output/{modeltype}_Rstats_{uniqueid}.csv"
                    coefpath=f"./output/{modeltype}_Rcoef_{uniqueid}.csv"
                    predpath=f"./output/{modeltype}_Pred_{uniqueid}.csv"
                    stats=pd.read_csv(statspath)
                    os.remove(statspath)
                    stats
                    rstats.append(stats)
                    coef=pd.read_csv(coefpath)
                    os.remove(coefpath)
                    coef
                    preds=pd.read_csv(predpath)
                    os.remove(predpath)
                    df[f"R_{modeltype}predictedProbabilities"]=preds.iloc[:,0]
                    df[f"R_{modeltype}prediction"]=preds.iloc[:,1]
                    csv=convert_df(coef)
                    ste.download_button(f"Export {modeltype} Coefficients",csv,f'{modeltype}_Rcoef_{uniqueid}.csv')
                except:
                    st.write("Error creating R Model")                
            os.remove(datapath)
        
        
        col1, col2, col3 = st.columns(3)
        pystatsdf=dfcombiner(pystats)
        rstatsdf=dfcombiner(rstats)
        allstatsdf=pd.concat([pystatsdf,rstatsdf])
        pystatscsv=convert_df(pystatsdf)
        rstatscsv=convert_df(rstatsdf)
        allstatscsv=convert_df(allstatsdf)
            
        with col1:
            ste.download_button(f"Download Python Model Stats",pystatscsv,f'Py_ModelStats_{uniqueid}.csv')  
        with col2:
            ste.download_button(f"Download R Model Stats",rstatscsv,f'R_ModelStats_{uniqueid}.csv')     
        with col3:
            ste.download_button(f"Download Python and R Stats",allstatscsv,f'All_ModelStats_{uniqueid}.csv')      
        with st.container():
            df
            csv=convert_df(df)
            ste.download_button("Download predicted outcomes of each student model",csv,'PredictedOutcomes.csv')
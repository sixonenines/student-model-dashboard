import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
import matplotlib.pyplot as plt
import subprocess
import streamlit_ext as ste
import uuid
import io
import zipfile
from PythonModelScripts import feature_engineering,getX,trainModels




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
        coefDic={}
        uniqueid=str(uuid.uuid4())
        datapath=f'./data/{uniqueid}.xlsx'
        writer = pd.ExcelWriter(datapath, engine='xlsxwriter')
        df.to_excel(writer,sheet_name="data")
        writer.save()
        tab1, tab2,tab3,tab4 = st.tabs(["Python", "R","Comparison","Predicted Outcomes"])
        with tab1:
            df=feature_engineering(df)
            st.header("Python Implementation")
            for modeltype in selectedModels:
                st.subheader(f"{modeltype}")
                X=getX(df,modeltype)
                results=trainModels(df,modeltype,X,uniqueid)
                stats=results[0]
                coef=results[1]
                df=results[2]
                st.dataframe(stats.style.format(thousands="",precision=2))
                pystats.append(stats)
                st.dataframe(coef)
                csv=convert_df(coef)
                coefDic[f"PY_{modeltype}_Coefficients"]=csv
                ste.download_button(f"Export {modeltype} Coefficients",csv,f'{modeltype}_Pycoef_{uniqueid}.csv')
            pystatsdf=dfcombiner(pystats)
            pystatscsv=convert_df(pystatsdf)
            ste.download_button(f"Download Python Model Stats",pystatscsv,f'Py_ModelStats_{uniqueid}.csv') 

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
                    stats=pd.read_csv(statspath).round(2)
                    os.remove(statspath)
                    st.dataframe(stats.style.format(thousands="",precision=2))
                    rstats.append(stats)
                    coef=pd.read_csv(coefpath).round(2)
                    os.remove(coefpath)
                    st.dataframe(coef.style.format(precision=2))
                    preds=pd.read_csv(predpath)
                    os.remove(predpath)
                    df[f"R_{modeltype}predictedProbabilities"]=preds.iloc[:,0].round(2)
                    df[f"R_{modeltype}prediction"]=preds.iloc[:,1]
                    csv=convert_df(coef)
                    coefDic[f"R_{modeltype}_Coefficients"]=csv
                    ste.download_button(f"Export {modeltype} Coefficients",csv,f'{modeltype}_Rcoef_{uniqueid}.csv')
                except:
                    st.write("Error creating R Model")
            rstatsdf=dfcombiner(rstats)
            rstatscsv=convert_df(rstatsdf)
            ste.download_button(f"Download R Model Stats",rstatscsv,f'R_ModelStats_{uniqueid}.csv')             
            os.remove(datapath)
        
        
        col1, col2, col3 = st.columns(3)
        allstatsdf=pd.concat([pystatsdf,rstatsdf])
        allstatscsv=convert_df(allstatsdf)
        print(allstatsdf)
        with tab3:
            st.header("Comparison")
            ste.download_button(f"Download Python and R Stats",allstatscsv,f'All_ModelStats_{uniqueid}.csv')  
            column_names= allstatsdf.columns[1:]
            splitPoint=len(allstatsdf["Model_type"])//2
            pythonModels=allstatsdf["Model_type"].iloc[:splitPoint].values
            rModels=allstatsdf["Model_type"].iloc[splitPoint:].values
            colors=["green","blue"]
            for column in column_names:
                plt.clf()
                values= allstatsdf[column].values
                pythonValues=values[:splitPoint]
                rValues=values[splitPoint:]
                plt.bar(pythonModels,pythonValues, color=colors[0])
                plt.bar(rModels,rValues, color=colors[1])
                #cmap=plt.get_cmap("viridis")
                #plt.bar(allstatsdf["Model_type"],values,color=cmap(values))
                plt.title(f"{column}")
                plt.xlabel("Model_type")
                plt.ylabel(column)
                st.pyplot(plt)    
        with tab4:
            st.header("Predicted outcomes and predicted probabilities of each step")
            st.dataframe(df)
            csv=convert_df(df)
            ste.download_button("Download predicted outcomes of each student model",csv,'PredictedOutcomes.csv')
            buffer= io.BytesIO()
            with zipfile.ZipFile(buffer,"w") as z:
                z.writestr('PredictedOutcomes.csv',csv)
                z.writestr('AllStats.csv',allstatscsv)
                for model,coefcsv in coefDic.items():
                    z.writestr(f"{model}.csv",coefcsv)
            zip_bytes=buffer.getvalue()
            ste.download_button("Download everything in zip",zip_bytes,"fullmodels.zip")
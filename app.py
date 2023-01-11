import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
import matplotlib.pyplot as plt
import subprocess
from PythonModelScripts import feature_engineering,getX,trainModels
import uuid
import streamlit_ext as ste



#
# Add packages.txt and stuff
#
# Rename helloworld.R and make it a pdf
#  
# Add comments
# 
# Upload it to github
#
# Change Path




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

uploaded_file = st.file_uploader("Choose a file")
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
        #writer = pd.ExcelWriter(f'./data/{uniqueid}.xlsx', engine='xlsxwriter')
        writer = pd.ExcelWriter(f'./{uniqueid}.xlsx', engine='xlsxwriter')
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
                #st.download_button(
                #label=f"Export {modeltype} Coefficients",
                #data=csv,
                #file_name=f'{modeltype}_Pycoef_{uniqueid}.csv',
                #mime='text/csv',
                #)
                

        with tab2:
            st.header("R Implementation")
            for modeltype in selectedModels:
                st.subheader(f"{modeltype}")
                if modeltype=="AFM":
                    #process = subprocess.run(["Rscript","AFM_Script.R"] + [f'./data/{uniqueid}.xlsx',uniqueid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                    process = subprocess.run(["Rscript","AFM_Script.R"] + [f'./{uniqueid}.xlsx',uniqueid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                elif modeltype=="PFM":
                    #process = subprocess.run(["Rscript","PFM_Script.R"] + [f'./data/{uniqueid}.xlsx',uniqueid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                    process = subprocess.run(["Rscript","PFM_Script.R"] + [f'./{uniqueid}.xlsx',uniqueid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                elif modeltype=="IFM":
                    #process = subprocess.run(["Rscript","IFM_Script.R"] + [f'./data/{uniqueid}.xlsx',uniqueid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True
                    process = subprocess.run(["Rscript","IFM_Script.R"] + [f'./{uniqueid}.xlsx',uniqueid], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)            
                paths=process.stdout
                pathlist=paths.rsplit(sep="!")
                stats=pd.read_csv(pathlist[0])
                stats
                rstats.append(stats)
                coef=pd.read_csv(pathlist[1])
                coef
                preds=pd.read_csv(pathlist[2])
                df[f"R_{modeltype}predictedProbabilities"]=preds.iloc[:,0]
                df[f"R_{modeltype}prediction"]=preds.iloc[:,1]
                csv=convert_df(coef)
                ste.download_button(f"Export {modeltype} Coefficients",csv,f'{modeltype}_Rcoef_{uniqueid}.csv')
                #st.download_button(
                #label=f"Export {modeltype} Coefficients",
                #data=csv,
                #file_name=f'{modeltype}_Rcoef_{uniqueid}.csv',
                #mime='text/csv',
                #)
        
        
        col1, col2, col3 = st.columns(3)
        pystatsdf=dfcombiner(pystats)
        rstatsdf=dfcombiner(rstats)
        allstatsdf=pd.concat([pystatsdf,rstatsdf])
        pystatscsv=convert_df(pystatsdf)
        rstatscsv=convert_df(rstatsdf)
        allstatscsv=convert_df(allstatsdf)
            

        with col1:
            ste.download_button(f"Download Python Model Stats",pystatscsv,f'Py_ModelStats_{uniqueid}.csv')
            #st.download_button(
            #label=f"Download Python Model Stats",
            #data=pystatscsv,
            #file_name=f'Py_ModelStats_{uniqueid}.csv',
            #mime='text/csv',
            #)
        with col2:
            ste.download_button(f"Download R Model Stats",rstatscsv,f'R_ModelStats_{uniqueid}.csv')
            #st.download_button(
            #label=f"Download R Script Model Stats",
            #data=rstatscsv,
            #file_name=f'R_ModelStats_{uniqueid}.csv',
            #mime='text/csv',
            #)
        with col3:
            ste.download_button(f"Download Python and R Stats",allstatscsv,f'All_ModelStats_{uniqueid}.csv')
            #st.download_button(
            #label=f"Download both Python and R Stats",
            #data=allstatscsv,
            #file_name=f'All_ModelStats_{uniqueid}.csv',
            #mime='text/csv',
            #)

        with st.container():
            df
            csv=convert_df(df)
            ste.download_button("Download predicted outcomes of each student model",csv,'PredictedOutcomes.csv')
            #st.download_button(
            #label="Download predicted outcomes of each student model",
            #data=csv,
            #file_name='PredictedOutcomes.csv',
            #mime='text/csv',
            #)

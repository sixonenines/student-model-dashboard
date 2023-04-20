FROM rocker/tidyverse

ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev libpng16-16 python3.9 python3-pip python3-setuptools python3-dev
RUN pip3 install --upgrade pip
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY . /app
WORKDIR /app

# installing python libraries
RUN pip3 install streamlit==1.16.0
RUN pip3 install -r requirements.txt

# installing r libraries
#RUN Rscript requirements.r
RUN Rscript -e "install.packages('tidyverse',version='1.3.2')"
RUN Rscript -e "install.packages('DAAG',version='1.25.4')"
RUN Rscript -e "install.packages('boot',version='1.3.28')"
RUN Rscript -e "install.packages('lme4',version='1.1.31')"
RUN Rscript -e "install.packages('caret',version='6.0.93')"
RUN Rscript -e "install.packages('plyr',version='1.8.8')"
RUN Rscript -e "install.packages('car',version='3.1.1')"
RUN Rscript -e "install.packages('pROC',version='1.18.0')"
RUN Rscript -e "install.packages('readxl',version='1.4.1')"
RUN Rscript -e "install.packages('glmnet',version='4.1.6')"
RUN Rscript -e "install.packages('glmnetUtils',version='1.1.8')"
RUN Rscript -e "install.packages('optimx',version='2022.4.30')"



EXPOSE 8501
ENTRYPOINT [ "streamlit","run"]
CMD ["app.py"]
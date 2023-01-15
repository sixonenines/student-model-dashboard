FROM rocker/tidyverse

ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev libpng16-16 python3.9 python3-pip python3-setuptools python3-dev
RUN pip3 install --upgrade pip
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY . /app
WORKDIR /app

# installing python libraries
RUN pip3 install streamlit
RUN pip3 install -r requirements.txt

# installing r libraries
#RUN Rscript requirements.r
RUN Rscript -e "install.packages('tidyverse')"
RUN Rscript -e "install.packages('DAAG')"
RUN Rscript -e "install.packages('boot')"
RUN Rscript -e "install.packages('lme4')"
RUN Rscript -e "install.packages('caret')"
RUN Rscript -e "install.packages('plyr')"
RUN Rscript -e "install.packages('car')"
RUN Rscript -e "install.packages('pROC')"
RUN Rscript -e "install.packages('readxl')"
RUN Rscript -e "install.packages('glmnet')"
RUN Rscript -e "install.packages('glmnetUtils')"
RUN Rscript -e "install.packages('optimx')"



EXPOSE 8501
ENTRYPOINT [ "streamlit","run"]
CMD ["app.py"]
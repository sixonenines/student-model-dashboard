FROM rocker/tidyverse:4.5.1

# avoid interactive apt prompts
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install Python and tools (create venv later). Keep packages minimal.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      python3 python3-venv python3-pip build-essential libpq-dev libpng16-16 \
 && rm -rf /var/lib/apt/lists/*

# Create an isolated virtualenv and upgrade pip inside it
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/python -m pip install --upgrade pip setuptools wheel

# Ensure venv's python/pip are used in subsequent steps
ENV PATH="/opt/venv/bin:${PATH}"

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

# Install python packages into venv (no system pip changes)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app sources
COPY . /app

# installing r libraries

#RUN Rscript requirements.r
RUN Rscript -e "install.packages('tidyverse',version='1.3.2')"
RUN Rscript -e "install.packages('DAAG',version='1.25.4')"
RUN Rscript -e "install.packages('boot',version='1.3.28')"
#RUN Rscript -e "install.packages('lme4',version='1.1.31')"
RUN Rscript -e "install.packages('caret',version='6.0.93')"
RUN Rscript -e "install.packages('plyr',version='1.8.8')"
RUN Rscript -e "install.packages('car',version='3.1.1')"
RUN Rscript -e "install.packages('pROC',version='1.18.0')"
RUN Rscript -e "install.packages('readxl',version='1.4.1')"
RUN Rscript -e "install.packages('glmnet',version='4.1.6')"
RUN Rscript -e "install.packages('glmnetUtils',version='1.1.8')"
RUN Rscript -e "install.packages('optimx',version='2022.4.30')"

EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]

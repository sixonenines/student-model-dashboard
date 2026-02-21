FROM rocker/r-ver:4.3.2

RUN apt-get update && apt-get install -y --no-install-recommends \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libsodium-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY install_packages.R .
RUN Rscript install_packages.R

COPY plumber.R .
COPY train_model.R .

EXPOSE 8001

RUN useradd -r -s /bin/false -u 9741 -M studentmodeldashboarduser && chown -R studentmodeldashboarduser:studentmodeldashboarduser /app
USER studentmodeldashboarduser

CMD ["R", "-e", "plumber::pr_run(plumber::pr('plumber.R'), host='0.0.0.0', port=8001)"]

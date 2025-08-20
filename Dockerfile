# Base Quarto image (includes Quarto and Pandoc)
FROM ghcr.io/quarto-dev/quarto:latest

# Set noninteractive mode to prevent timezone prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install R, LaTeX, Python, and pip
RUN apt-get update && apt-get install -y \
    tzdata \
    r-base \
    r-base-dev \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-xetex \
    libfontconfig1-dev \
    libfreetype6-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    pkg-config \
    libharfbuzz-dev \
    libfribidi-dev \
    libpng-dev \
    python3 \
    python3-pip \
    python3-venv \
    python3-distutils \
    git \
    ttf-mscorefonts-installer \
    fontconfig \
 && fc-cache -f -v \
 && ln -s /usr/bin/python3 /usr/bin/python \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Python venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt \
    gunicorn

# Install R packages
RUN Rscript -e "install.packages(c('dplyr','ggplot2','lubridate','readr','yaml','janitor','tidyr','forcats','rmarkdown','knitr','reticulate','viridis','scales','showtext','kableExtra','svglite','systemfonts','textshaping','xml2'), repos='https://cran.r-project.org')"

# Set environment variables for Flask
ENV FLASK_APP=api/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "300", "api.app:app"]
FROM rocker/tidyverse:latest

WORKDIR /home/app

RUN R -e "library(devtools)" && \
    R -e "devtools::install_github('FantasyFootballAnalytics/ffanalytics')" && \
    R -e "library(ffanalytics)" && \
    R -e "install.packages('readr')" && \
    R -e "library('readr')"
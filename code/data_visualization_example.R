if (!require(ggplot2)) install.packages('ggplot2')
if (!require(showtext)) install.packages('showtext')
if (!require(tidyverse)) install.packages('tidyverse')
if (!require(readxl)) install.packages('readxl')
if (!require(lubridate)) install.packages('lubridate')
library(ggplot2)
library(showtext)
library(tidyverse)
library(readxl)
library(lubridate)

rm(list=ls())
path <- "/home/dashaa/wildfire_politics/data"

###visualizing data on two 2020 wildfire complexes in North California
###the code produces graphs average_aerial_comparison.png and news_citations.png
#load the data
sitreps <- read.csv(paste0(path,
                           "/build_wildfire_reports/input/raw/new_ics209plus/ics209plus-wildfire/ics209-plus-wf_sitreps_1999to2020.csv"))
complexes <- filter(sitreps,INCIDENT_NAME %in% c("North Complex","LNU LIGHTNING COMPLEX"))

#add average aerial values for each day
complexes <- complexes %>%
  mutate(
    REPORT_FROM_DATE = ymd_hms(REPORT_FROM_DATE),
    REPORT_TO_DATE = ymd_hms(REPORT_TO_DATE),
    REPORT_MID_DATE = date(REPORT_FROM_DATE + (REPORT_TO_DATE - REPORT_FROM_DATE) / 2)
  ) %>%
  group_by(REPORT_MID_DATE) %>%
  summarize(
    AVERAGE_AERIAL = mean(TOTAL_AERIAL, na.rm = TRUE),
  ) %>%
  rename(Complex = INCIDENT_NAME) %>%
  filter(REPORT_MID_DATE<max(lnu_complex$REPORT_MID_DATE))

#make a graph
font_add_google("IBM Plex Sans", "ibm plex sans")
font_add_google("IBM Plex Serif", "ibm plex serif")
the_font <- "ibm plex sans"









#news data
news <- read_excel(paste0(path,"/data_analysis/input/built/fire_citations.xlsx"))
news <- news%>%
  mutate(Date=mdy(Date)) %>%
  dplyr::select(-c("Claremont Fire","Meyers Fire", "Walbridge Fire"))
news <- melt(news, id.vars = "Date") %>%
  rename(Fire=variable)

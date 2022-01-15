library(ffanalytics)
library(readr)

# running FFA scrape function
my_scrape <- ffanalytics::scrape_data(pos = c("QB", "RB", "WR", "TE"), season = 2021, week = 15)

my_projections <- ffanalytics::projections_table(my_scrape) %>% add_ecr() %>% add_risk() %>% add_aav()

#f_name <- paste("S21W15")

write.table(my_projections, file = "./db/S21W15.csv", append = FALSE, na = "NAN")
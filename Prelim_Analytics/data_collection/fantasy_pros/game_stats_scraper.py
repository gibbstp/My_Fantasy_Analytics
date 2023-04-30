import pandas as pd
from sqlalchemy import create_engine
import time


def create_urls():
    positions = ["qb", "rb", "wr", "te", "k", "dst", "dl", "lb", "db"]
    years = list(range(2002, 2023))
    weeks = list(range(1, 19))

    url_info = []

    for position in positions:
        for year in years:
            for week in weeks:
                url = f"https://www.fantasypros.com/nfl/stats/{position}.php?year={year}&week={week}&range=week"

                url_info.append([url, position, year, week])

    return url_info


def scrape_site(url):
    
    scraped_data = pd.read_html(url)[0]

    return scraped_data


def clean_dataframe(data, position, year, week):
    
    mutli_index_frames = ['qb', 'rb', 'wr', 'te']
    
    if position in mutli_index_frames:
        
        # removing milti-indexing and adding the additional index to the column names
        data.columns = ["_".join(col) for col in data.columns.values]

        # renaming column names to removed the "Unnamed:..." that is a result of the html
        columns_renames = {data.columns[0]: "RANK", data.columns[1]: "PLAYER"}

        data.rename(columns=columns_renames, inplace=True)

    if position not in mutli_index_frames:
        
        data.columns = data.columns.str.upper()
        
    # splitting the Team abbreviations from the Player name, adding Team to a new column and dropping the parenthesis from team name
    player_team = data.PLAYER.str.rsplit(" ", n=1, expand=True)
    data.PLAYER = player_team[0]
    data["TEAM"] = player_team[1].str.replace("\(|\)", "", regex=True)

    # adding year, position, and week to dataframe for query purposes
    data["POS"] = position
    data["YEAR"] = year
    data["WEEK"] = week
    
    return data


def write_to_db(dataframe, position):
    
    engine = create_engine('sqlite://../data/historic_data.db')

    sqlite_connection = engine.connect()

    sqlite_table = f"game_stats_{position}"

    dataframe.to_sql(sqlite_table, sqlite_connection, if_exists="append")

    sqlite_connection.close()


def main():
    url_info_list = create_urls()

    for url_info in url_info_list:
        url, position, year, week = url_info

        print(f'Scraping {position}, {year}, week {week}')
        print(url)
        scraped_data = scrape_site(url)

        cleaned_data = clean_dataframe(scraped_data, position, year, week)

        write_to_db(cleaned_data, position)

        # waiting 6 seconds to abide by sites robots.txt
        # see https://www.fantasypros.com/robots.txt
        time.sleep(5.25)


if __name__ == '__main__':
    main()
from bs4 import BeautifulSoup
import pandas as pd
import cloudscraper
import time
from io import StringIO

all_teams = []  # Store all team stats

scraper = cloudscraper.create_scraper()  # bypass Cloudflare

# Get the main Premier League stats page
html = scraper.get('https://fbref.com/en/comps/9/Premier-League-Stats').text
print("Length of main page HTML:", len(html))

soup = BeautifulSoup(html, 'lxml')
tables = soup.find_all('table', class_='stats_table')
print("Number of tables found on main page:", len(tables))

if not tables:
    raise ValueError("No tables found on main page.")

table = tables[0]

# Extract team links
links = [l.get("href") for l in table.find_all('a') if l.get("href") and '/squads/' in l.get("href")]
print("Number of team links found:", len(links))

if not links:
    raise ValueError("No team links found.")

team_urls = [f"https://fbref.com{l}" for l in links]

# Scrape each team
for team_url in team_urls:
    print("Scraping team URL:", team_url)
    team_name = team_url.split("/")[-1].replace("-Stats", "")
    data = scraper.get(team_url).text

    if len(data) < 1000:
        print("Team page too short, skipping:", team_url)
        continue

    soup_team = BeautifulSoup(data, 'lxml')
    tables_team = soup_team.find_all('table', class_='stats_table')
    if not tables_team:
        print(f"No stats table found for team: {team_name}")
        continue

    # PICK ONLY THE STANDARD PLAYER STATS TABLE
    stats_table = None
    for t in tables_team:
        if t.get("id") and "stats_standard" in t.get("id"):
            stats_table = t
            break
    if not stats_table:
        print(f"No standard stats table found for team: {team_name}")
        continue

    # Convert to DataFrame
    team_data = pd.read_html(StringIO(str(stats_table)))[0]

    # Drop multi-level columns
    if isinstance(team_data.columns, pd.MultiIndex):
        team_data.columns = team_data.columns.droplevel(0)

    # CLEAN AGE COLUMN (extract just the number)
    if "Age" in team_data.columns:
        team_data["Age"] = team_data["Age"].astype(str).str.extract(r"(\d+)")[0]
        team_data["Age"] = pd.to_numeric(team_data["Age"], errors="coerce")

    # REMOVE NON-PLAYER ROWS
    team_data = team_data[team_data["Player"].notnull()]  # remove empty player names
    team_data = team_data[~team_data["Player"].str.contains(
        "Team Total|Squad Total|Opponent Total|Reserves|Sub", na=False
    )]

    # Add team name column
    team_data["Team"] = team_name
    all_teams.append(team_data)
    print(f"Added data for team: {team_name}, rows: {len(team_data)}")

    time.sleep(5)  # avoid being blocked

# Combine all teams into one DataFrame
if all_teams:
    stat_df = pd.concat(all_teams, ignore_index=True)
    stat_df.to_csv("Prem_Stats.csv", index=False)
    print("Scraping complete! CSV saved as Prem_Stats.csv")
else:
    print("No data collected. Exiting.")

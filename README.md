<h1 align="center">⚽ Premier League Data Scraper</h1>

## 📖 Overview

This project scrapes Premier League team statistics directly from FBref
 and consolidates them into a single, clean CSV dataset. It bypasses Cloudflare protection using Cloudscraper and leverages BeautifulSoup + Pandas to transform raw HTML tables into analysis-ready data.


## 🚀 Features

Scrapes every Premier League squad page automatically

Cleans & merges all stats into a single CSV output

Handles multi-level HTML tables and normalizes columns

Resilient scraping with request throttling to avoid blocks

Flexible, modular code for future extensions (e.g., match stats, player stats)


## 💻 Tech Stack

Languages:
![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white) 

Developer Tools:
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)


## 📂 Output Example

Prem_Stats.csv (sample structure):

| Player  | Nation | Pos | Age | Min  | Gls | Ast | Team    |
|---------|--------|-----|-----|------|-----|-----|---------|
| J. Doe  | ENG    | FW  | 25  | 1800 | 10  | 5   | Arsenal |


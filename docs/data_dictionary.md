# Data Dictionary

## Production Table

| Column | Description | Source | Example |
|---|---|---|---|
| production_id | Unique IBDB production identifier | URL | 1285 |
| title | Production title | h3.title-label | Oklahoma! |
| opening_date | Broadway opening date | metadata card | Mar 31, 1943 |
| closing_date | Broadway closing date | metadata card | May 29, 1948 |
| performances | Number of performances | metadata card | 2212 |
| production_type | Musical, Play, etc. | page title metadata | Musical |
| production_status | Original or Revival | page title metadata | Original |
| revival_year | Year of revival if applicable | page title metadata | 2016 |

## Cast Table

| Column | Description | Source | Example |
|---|---|---|---|
| production_id | Links cast to production | Production table | 1285 |
| performer_id | Unique IBDB performer identifier | cast URL | 4031 |
| performer_name | Performer name | cast section | Alfred Drake |
| role | Character/role played | cast section | Curly |
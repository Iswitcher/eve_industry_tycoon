# What it is about

If you ever tried to play EvE online as a trader or a manufacturer - you might have even heard about people making spreadsheets or using side projects to track expenses, calculate profits, etc.
I tried to use some of these services, set up my own data sheets, but alas - did not get the experience I wanted.

This is a simple pet project, where my goal it to:
* track my assets, blueprints included
* analyze the supply of manufacturing materials on the main markets (Jita, Amarr, citadel hubs)
* search for the most lucrative production chains: highest margin/hour with large throughput

# How will it work

There would be main body of all services and logic on Python, database to store static data (blueprints, items, etc) and ESI API connector to track my ingame assets directly

# Roadmap

1. SDE downloader and unpacker into SQLite db
2. Additional game logic: production chains, expense formulas, etc
3. ESI connector and secure storage for personal assets
4. Profit search: look for the assets and bp I have, calculate margins
5. FIFO accounting
6. New suggesions: look for the stuff I don't have, calculate break-even ETA
7. Turnover statistics, market spy: track demand spikes and supply drops


P.S. See you in 10 years, because this project is also for me to learn Python /s

⚽ Soccer League Simulation

A data-driven soccer league simulator that models teams, players, fixtures, and match outcomes using probabilistic methods.

✨ Features

JSON-based player and team datasets

Round-robin fixture generation with home/away balancing

Week-by-week simulation with persistent season state

Beta distribution–based match modeling for realistic randomness

Live league table updates via Streamlit

🧠 Simulation Model

Possession & scoring probabilities are sampled using Beta distributions, allowing:

Controlled randomness

More realistic match variance than uniform or fixed values

Team strength is derived from aggregated player attributes

Beta distributions are commonly used in sports analytics to model probabilities constrained between 0 and 1.

🗂 Data Design

players.json: Individual player attributes (position-specific stats supported)

teams.json: Team metadata and roster mapping

JSON enables:

Easy dataset swapping (realistic vs fictional teams)

Future database integration

🖥 UI

Interactive Streamlit app

Run matches one week at a time

Reset season at any point

Live league standings sorted by:

Points

Goal difference

Goals scored

🧩 Tech Stack

Python

NumPy (probability & distributions)

Pandas (table management)

Streamlit (UI)

JSON (data storage)

🚀 Future Improvements

Transfer market & player development

Injury and fatigue modeling

Elo-based or xG-based match engine

Mobile deployment (Flutter / React Native frontend)

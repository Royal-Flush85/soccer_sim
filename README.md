# ⚽ Soccer League Simulation

A **data-driven soccer league simulator** that models teams, players, fixtures, and match outcomes using probabilistic methods.

---

## ✨ Features

- JSON-based **player and team datasets**
- **Round-robin fixture generation** with home/away balancing
- **Week-by-week simulation** with persistent season state
- **Beta distribution–based match modeling** for realistic randomness
- **Live league table updates** via Streamlit

---

## 🧠 Simulation Model

Possession and scoring probabilities are sampled using **Beta distributions**, enabling:

- **Controlled randomness**
- **More realistic match variance** than uniform or fixed values
- Team strength derived from **aggregated player attributes**

> Beta distributions are commonly used in sports analytics to model probabilities constrained between 0 and 1.

---

## 🗂 Data Design

- `players.json`: Individual player attributes (supports position-specific stats)
- `teams.json`: Team metadata and roster mapping

**Benefits of JSON design:**

- Easy dataset swapping (realistic vs fictional teams)
- Supports **future database integration**

---

## 🖥 User Interface

- Interactive **Streamlit app**
- Run matches **one week at a time**
- **Reset season** at any point
- Live league standings sorted by:
  - Points
  - Goal difference
  - Goals scored

---

## 🧩 Tech Stack

- **Python**
- **NumPy** – probability & distributions
- **Pandas** – table management
- **Streamlit** – UI
- **JSON** – data stor

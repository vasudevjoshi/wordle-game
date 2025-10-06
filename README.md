# Wordle Game Web App (Django)

A simple **5-letter word guessing game** built with Django. Players can guess words, get visual feedback, and track their game history. Admins can view daily and per-user reports.

---

## Features

### Player Features
- User registration & login
- Password validation (letters, numbers, special chars `$%*@`)
- 5-letter word guessing game
- Up to **3 words/day** per player
- Maximum **5 guesses per word**
- Visual feedback:
  - Green → correct letter & correct position
  - Orange → correct letter & wrong position
  - Grey → letter not in word
- Game history saved in database
- Alert messages for wins and losses

### Admin Features
- Daily report:
  - Number of users who played
  - Number of correct guesses
- User report:
  - Words tried
  - Correct guesses per day
- Access restricted to staff users (`is_staff=True`)

---

## Tech Stack
- Python 3.x
- Django 4.x
- SQLite (default, can use PostgreSQL or MySQL)
- HTML/CSS/Bootstrap for frontend

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/wordle_game.git
cd wordle_game

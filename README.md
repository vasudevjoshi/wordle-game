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
```
2. **Create a virtual environment**

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Apply migrations**
```bash
python manage.py migrate
```



5. **Create superuser (for admin access)**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```
7. **Access the app**
Player pages: http://127.0.0.1:8000/
Admin reports: http://127.0.0.1:8000/admin/daily-report/

 **Usage**
  Register as a player or login.
  Start guessing words.
  Admins can view reports using their staff account.

**Database Models**
  User → username, password, is_staff
  Word → word (5-letter, uppercase)
  Game → user, word, attempts_used, completed, won, date
  Guess → game, guess_word, attempt_number, result (green/orange/grey)

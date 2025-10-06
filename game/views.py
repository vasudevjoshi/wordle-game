from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date
import random

from .forms import RegistrationForm
from .models import Word, Game, Guess


# ========== AUTH VIEWS ==========

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'game/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'game/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ========== GAME VIEWS ==========

@login_required
def home(request):
    today = date.today()
    games_today = Game.objects.filter(user=request.user, date=today)
    return render(request, 'game/home.html', {'games_today': games_today})


@login_required
def start_game(request):
    today = date.today()
    if Game.objects.filter(user=request.user, date=today).count() >= 3:
        messages.error(request, 'You have already played 3 games today.')
        return redirect('home')

    word = random.choice(list(Word.objects.all()))
    game = Game.objects.create(user=request.user, word=word)
    return redirect('play_game', game.id)


def evaluate_guess(secret, guess):
    secret = list(secret)
    guess = list(guess)
    result = ['grey'] * 5
    unmatched = []

    # First pass: correct positions
    for i in range(5):
        if guess[i] == secret[i]:
            result[i] = 'green'
        else:
            unmatched.append(secret[i])

    # Second pass: correct letters wrong position
    for i in range(5):
        if result[i] == 'grey' and guess[i] in unmatched:
            result[i] = 'orange'
            unmatched.remove(guess[i])

    return result


# Main game view
@login_required
def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id, user=request.user)

    # If game already completed
    if game.completed:
        messages.info(request, 'This game is already completed.')
        return redirect('home')

    # Handle guesses
    if request.method == 'POST':
        guess_word = request.POST.get('guess', '').upper()

        # Validate guess
        if len(guess_word) != 5 or not guess_word.isalpha():
            messages.error(request, 'Guess must be exactly 5 uppercase letters.')
            return redirect('play_game', game.id)

        # Check guess limit
        if game.attempts_used >= 5:
            game.completed = True
            game.save()
            messages.error(request, 'Maximum 5 guesses reached.')
            return redirect('home')

        # Evaluate result
        result = evaluate_guess(game.word.word, guess_word)

        # Save the guess
        Guess.objects.create(
            game=game,
            guess_word=guess_word,
            attempt_number=game.attempts_used + 1,
            result=','.join(result)
        )

        # Increase attempt count
        game.attempts_used += 1

        # Check if correct
        if guess_word == game.word.word:
            game.won = True
            game.completed = True
            game.save()
            guesses = game.guesses.all()
            for g in guesses:
                g.result_list = g.result.split(',') if g.result else []
            return render(request, 'game/game.html', {
                'game': game,
                'guesses': guesses,
                'message': f'🎉 Congratulations! The word was {game.word.word}.'
            })

        # If 5 attempts done but not guessed
        if game.attempts_used == 5:
            game.completed = True
            game.save()
            guesses = game.guesses.all()
            for g in guesses:
                g.result_list = g.result.split(',') if g.result else []
            return render(request, 'game/game.html', {
                'game': game,
                'guesses': guesses,
                'message': f'❌ Better luck next time! The word was {game.word.word}.'
            })

        game.save()
        return redirect('play_game', game.id)

    # GET request → just show game
    guesses = game.guesses.all()
    for g in guesses:
        g.result_list = g.result.split(',') if g.result else []

    return render(request, 'game/game.html', {
        'game': game,
        'guesses': guesses
    })

@user_passes_test(lambda u: u.is_staff)
def admin_daily_report(request):
    qdate = request.GET.get('date')
    qdate = date.fromisoformat(qdate) if qdate else date.today()
    games = Game.objects.filter(date=qdate)
    users_played = games.values('user').distinct().count()
    correct_guesses = games.filter(won=True).count()
    return render(request, 'game/admin_daily_report.html', {
        'qdate': qdate,
        'users_played': users_played,
        'correct_guesses': correct_guesses,
    })


@user_passes_test(lambda u: u.is_staff)
def admin_user_report(request):
    username = request.GET.get('username')
    report = []
    if username:
        report = (
            Game.objects.filter(user__username=username)
            .values('date')
            .annotate(words_tried=Count('id'),
                      correct=Count('id', filter=Q(won=True)))
            .order_by('-date')
        )
    return render(request, 'game/admin_user_report.html', {'report': report, 'username': username})

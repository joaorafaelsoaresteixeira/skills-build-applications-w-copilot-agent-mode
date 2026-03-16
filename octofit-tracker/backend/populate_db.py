import django
import os
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard

def create_users():
    users = []
    for i in range(5):
        user, _ = User.objects.get_or_create(username=f'user{i}', defaults={
            'email': f'user{i}@example.com',
            'first_name': f'First{i}',
            'last_name': f'Last{i}',
        })
        user.set_password('password')
        user.save()
        users.append(user)
    return users

def create_teams(users):
    teams = []
    for i in range(2):
        team = Team.objects.create(name=f'Team {i}')
        for user in users[i*2:(i+1)*2+1]:
            team.members.add(user)
        teams.append(team)
    return teams

def create_activities(users):
    activities = []
    for user in users:
        for j in range(3):
            activity = Activity.objects.create(
                user=user,
                activity_type=random.choice(['run', 'walk', 'cycle']),
                duration=random.randint(20, 60),
                calories_burned=random.uniform(100, 500),
                date=date.today() - timedelta(days=j)
            )
            activities.append(activity)
    return activities

def create_workouts(users):
    workouts = []
    for user in users:
        for j in range(2):
            workout = Workout.objects.create(
                user=user,
                name=f'Workout {j}',
                description='Sample workout',
                date=date.today() - timedelta(days=j)
            )
            workouts.append(workout)
    return workouts

def create_leaderboards(teams):
    for team in teams:
        Leaderboard.objects.create(team=team, total_points=random.randint(100, 500))

def main():
    users = create_users()
    teams = create_teams(users)
    create_activities(users)
    create_workouts(users)
    create_leaderboards(teams)
    print('Test data created successfully.')

if __name__ == '__main__':
    main()

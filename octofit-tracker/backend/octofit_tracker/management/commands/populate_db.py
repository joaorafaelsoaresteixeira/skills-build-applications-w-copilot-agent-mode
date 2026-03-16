from django.core.management.base import BaseCommand
import random
from datetime import date, timedelta
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard

class Command(BaseCommand):
    help = 'Populate the database with test data.'

    def handle(self, *args, **kwargs):
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

        teams = []
        for i in range(2):
            team = Team.objects.create(name=f'Team {i}')
            for user in users[i*2:(i+1)*2+1]:
                team.members.add(user)
            teams.append(team)

        for user in users:
            for j in range(3):
                Activity.objects.create(
                    user=user,
                    activity_type=random.choice(['run', 'walk', 'cycle']),
                    duration=random.randint(20, 60),
                    calories_burned=random.uniform(100, 500),
                    date=date.today() - timedelta(days=j)
                )

        for user in users:
            for j in range(2):
                Workout.objects.create(
                    user=user,
                    name=f'Workout {j}',
                    description='Sample workout',
                    date=date.today() - timedelta(days=j)
                )

        for team in teams:
            Leaderboard.objects.create(team=team, total_points=random.randint(100, 500))

        self.stdout.write(self.style.SUCCESS('Test data created successfully.'))

"""
Seed the database with demo users, habits, check-ins, streaks and a partnership.

Usage:
    python manage.py seed_demo

Creates two users (idempotent — safe to re-run):
    - Damodar_Josh  (password: demo12345)
    - Unisha_Gautam (password: demo12345)
"""
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import CheckIn, Habit, Partnership, Streak

PASSWORD = "demo12345"


class Command(BaseCommand):
    help = "Seed demo users Damodar_Josh and Unisha_Gautam with demo data."

    def handle(self, *args, **options):
        damodar = self._get_or_create_user("Damodar_Josh")
        unisha = self._get_or_create_user("Unisha_Gautam")

        today = date.today()

        # ---- Damodar_Josh ----
        workout = self._make_habit(
            damodar,
            "Morning Workout",
            "30 minutes of strength or cardio every morning to start the day strong.",
            "daily",
        )
        self._seed_checkins(workout, days=12, notes={0: "Felt amazing! 💪", 2: "Tough but done."})
        self._seed_streak(workout, current=12, longest=21, last=today)

        reading = self._make_habit(
            damodar,
            "Read 20 Pages",
            "Read at least 20 pages of a book before bed.",
            "daily",
        )
        self._seed_checkins(reading, days=5, notes={0: "Great chapter on habit formation."})
        self._seed_streak(reading, current=5, longest=5, last=today)

        # A habit with no check-ins yet — showcases the "No check-ins yet" card state.
        self._make_habit(
            damodar,
            "Meditate",
            "10 minutes of mindfulness right after waking up.",
            "daily",
        )

        # ---- Unisha_Gautam ----
        yoga = self._make_habit(
            unisha,
            "Morning Yoga",
            "45-minute vinyasa flow to energise the whole day.",
            "daily",
        )
        self._seed_checkins(yoga, days=18, notes={0: "Sun salutations under the sunrise 🌅", 6: "Deep stretch day."})
        self._seed_streak(yoga, current=18, longest=18, last=today)

        journal = self._make_habit(
            unisha,
            "Weekly Journaling",
            "A reflective journal entry every Sunday evening.",
            "weekly",
        )
        # Most recent 6 Sundays before today.
        sundays = []
        d = today
        while len(sundays) < 6:
            if d.weekday() == 6:  # Sunday
                sundays.append(d)
            d -= timedelta(days=1)
        for dt in sundays:
            CheckIn.objects.get_or_create(habit=journal, date=dt, defaults={"note": "Weekly reflection 📓"})
        self._seed_streak(journal, current=6, longest=10, last=sundays[0])

        # ---- Partnership ----
        partnership, created = Partnership.objects.get_or_create(user=damodar, partner=unisha)
        if created:
            self.stdout.write(self.style.SUCCESS("Partnership created: Damodar_Josh <-> Unisha_Gautam"))

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
        self.stdout.write(self.style.SUCCESS("Login with Damodar_Josh or Unisha_Gautam / demo12345"))

    def _get_or_create_user(self, username):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(PASSWORD)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"User created: {username}"))
        else:
            self.stdout.write(f"User already exists: {username}")
        return user

    def _make_habit(self, user, name, description, frequency):
        habit, created = Habit.objects.get_or_create(
            user=user,
            name=name,
            defaults={"description": description, "frequency": frequency},
        )
        return habit

    def _seed_checkins(self, habit, days, notes=None):
        notes = notes or {}
        today = date.today()
        for offset in range(days):
            dt = today - timedelta(days=offset)
            CheckIn.objects.get_or_create(
                habit=habit,
                date=dt,
                defaults={"note": notes.get(offset, "")},
            )

    def _seed_streak(self, habit, current, longest, last):
        streak, created = Streak.objects.get_or_create(
            habit=habit,
            defaults={
                "current_streak": current,
                "longest_streak": longest,
                "last_check_in": last,
            },
        )
        return streak

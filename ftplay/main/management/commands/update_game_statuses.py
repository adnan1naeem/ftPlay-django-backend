from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Game


class Command(BaseCommand):
    help = 'Update game statuses based on current time (ongoing/completed)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        verbose = options['verbose']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting game status update at {timezone.now()}')
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        # Get all non-canceled games
        games = Game.objects.exclude(status='CANCELED')
        
        if verbose:
            self.stdout.write(f'Found {games.count()} games to check')
        
        updated_games = []
        
        for game in games:
            current_status = game.status
            should_be_ongoing = game.should_be_ongoing()
            should_be_completed = game.should_be_completed()
            
            if verbose:
                game_datetime = game.get_game_datetime()
                game_end = game.get_game_end_datetime()
                self.stdout.write(
                    f'Game: {game.title} (ID: {game.id})'
                )
                self.stdout.write(
                    f'  Current Status: {current_status}'
                )
                self.stdout.write(
                    f'  Game Start: {game_datetime}'
                )
                self.stdout.write(
                    f'  Game End: {game_end}'
                )
                self.stdout.write(
                    f'  Should be ongoing: {should_be_ongoing}'
                )
                self.stdout.write(
                    f'  Should be completed: {should_be_completed}'
                )
            
            if not dry_run:
                if game.update_status():
                    updated_games.append(game)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated game "{game.title}" from {current_status} to {game.status}'
                        )
                    )
            else:
                # Dry run - just show what would happen
                if should_be_completed and current_status != 'COMPLETED':
                    updated_games.append(game)
                    self.stdout.write(
                        self.style.WARNING(
                            f'Would update game "{game.title}" from {current_status} to COMPLETED'
                        )
                    )
                elif should_be_ongoing and current_status != 'ONGOING':
                    updated_games.append(game)
                    self.stdout.write(
                        self.style.WARNING(
                            f'Would update game "{game.title}" from {current_status} to ONGOING'
                        )
                    )
        
        if updated_games:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated {len(updated_games)} games'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No games needed status updates')
            )
        
        # Show summary by status
        status_counts = {}
        for game in Game.objects.all():
            status_counts[game.status] = status_counts.get(game.status, 0) + 1
        
        self.stdout.write('\nCurrent game status summary:')
        for status, count in status_counts.items():
            self.stdout.write(f'  {status}: {count} games') 
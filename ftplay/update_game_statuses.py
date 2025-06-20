#!/usr/bin/env python
"""
Standalone script to update game statuses automatically.
This can be run by cron or a task scheduler.

Usage:
    python update_game_statuses.py
    python update_game_statuses.py --dry-run
    python update_game_statuses.py --verbose
"""

import os
import sys
import django
import argparse
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ftplay.settings')
django.setup()

from main.models import Game


def update_game_statuses(dry_run=False, verbose=False):
    """Update game statuses based on current time"""
    print(f"[{datetime.now()}] Starting game status update...")
    
    if dry_run:
        print("DRY RUN MODE - No changes will be made")
    
    # Get all non-canceled games
    games = Game.objects.exclude(status='CANCELED')
    
    if verbose:
        print(f"Found {games.count()} games to check")
    
    updated_games = []
    
    for game in games:
        current_status = game.status
        should_be_ongoing = game.should_be_ongoing()
        should_be_completed = game.should_be_completed()
        
        if verbose:
            game_datetime = game.get_game_datetime()
            game_end = game.get_game_end_datetime()
            print(f"Game: {game.title} (ID: {game.id})")
            print(f"  Current Status: {current_status}")
            print(f"  Game Start: {game_datetime}")
            print(f"  Game End: {game_end}")
            print(f"  Should be ongoing: {should_be_ongoing}")
            print(f"  Should be completed: {should_be_completed}")
        
        if not dry_run:
            if game.update_status():
                updated_games.append(game)
                print(f"✓ Updated game '{game.title}' from {current_status} to {game.status}")
        else:
            # Dry run - just show what would happen
            if should_be_completed and current_status != 'COMPLETED':
                updated_games.append(game)
                print(f"Would update game '{game.title}' from {current_status} to COMPLETED")
            elif should_be_ongoing and current_status != 'ONGOING':
                updated_games.append(game)
                print(f"Would update game '{game.title}' from {current_status} to ONGOING")
    
    if updated_games:
        print(f"Successfully updated {len(updated_games)} games")
    else:
        print("No games needed status updates")
    
    # Show summary by status
    status_counts = {}
    for game in Game.objects.all():
        status_counts[game.status] = status_counts.get(game.status, 0) + 1
    
    print('\nCurrent game status summary:')
    for status, count in status_counts.items():
        print(f"  {status}: {count} games")
    
    return len(updated_games)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update game statuses based on current time')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be updated without making changes')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    try:
        updated_count = update_game_statuses(dry_run=args.dry_run, verbose=args.verbose)
        sys.exit(0 if updated_count >= 0 else 1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 
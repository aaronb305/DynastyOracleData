#!/usr/bin/env python3
"""
Season Recap Generator for Sleeper Dynasty Fantasy Football Leagues

Generates a self-contained HTML recap including:
- League standings and champion
- All-Busts team (players who underperformed expectations)
- All-Sleeper team (players who overperformed expectations)
- Top waiver wire additions
- Notable drops
- Best and worst trades

Usage:
    python scripts/season_recap_generator.py [league_id]
    python scripts/season_recap_generator.py --demo    # Generate with sample data

If no league_id is provided, defaults to GAH Dynasty league.
"""

import requests
import json
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any, Optional, Tuple
import html
import sys
import argparse

# Default to GAH Dynasty league
DEFAULT_LEAGUE_ID = "1228781964740268032"

# 2024 NFL Season weeks (17 regular season weeks + playoffs)
REGULAR_SEASON_WEEKS = 17
PLAYOFF_WEEKS = 4


def get_demo_data() -> Tuple[Dict, List, List, Dict, Dict, Dict]:
    """Generate sample demo data for preview purposes."""
    league_info = {
        "name": "GAH Dynasty",
        "season": "2024",
        "total_rosters": 12,
        "league_id": DEFAULT_LEAGUE_ID,
    }

    users = [
        {"user_id": "1", "display_name": "ChampionMike"},
        {"user_id": "2", "display_name": "DynastyKing"},
        {"user_id": "3", "display_name": "TradeHawk"},
        {"user_id": "4", "display_name": "WaiverWire_Warrior"},
        {"user_id": "5", "display_name": "RookieHunter"},
        {"user_id": "6", "display_name": "VetCollector"},
        {"user_id": "7", "display_name": "PointsKing"},
        {"user_id": "8", "display_name": "TankCommander"},
        {"user_id": "9", "display_name": "BoomOrBust"},
        {"user_id": "10", "display_name": "SleepyDrafter"},
        {"user_id": "11", "display_name": "PickTrader"},
        {"user_id": "12", "display_name": "LastPlace_Larry"},
    ]

    rosters = [
        {"roster_id": 1, "owner_id": "1", "settings": {"wins": 11, "losses": 6, "ties": 0, "fpts": 2145, "fpts_decimal": 50, "fpts_against": 1890, "fpts_against_decimal": 30}, "playoff_seed": 1, "players": []},
        {"roster_id": 2, "owner_id": "2", "settings": {"wins": 10, "losses": 7, "ties": 0, "fpts": 2089, "fpts_decimal": 20, "fpts_against": 1920, "fpts_against_decimal": 10}, "playoff_seed": 2, "players": []},
        {"roster_id": 3, "owner_id": "3", "settings": {"wins": 9, "losses": 8, "ties": 0, "fpts": 1987, "fpts_decimal": 80, "fpts_against": 1950, "fpts_against_decimal": 60}, "playoff_seed": 3, "players": []},
        {"roster_id": 4, "owner_id": "4", "settings": {"wins": 9, "losses": 8, "ties": 0, "fpts": 1965, "fpts_decimal": 40, "fpts_against": 1980, "fpts_against_decimal": 20}, "playoff_seed": 4, "players": []},
        {"roster_id": 5, "owner_id": "5", "settings": {"wins": 8, "losses": 9, "ties": 0, "fpts": 1920, "fpts_decimal": 10, "fpts_against": 1945, "fpts_against_decimal": 80}, "playoff_seed": 5, "players": []},
        {"roster_id": 6, "owner_id": "6", "settings": {"wins": 8, "losses": 9, "ties": 0, "fpts": 1898, "fpts_decimal": 70, "fpts_against": 1910, "fpts_against_decimal": 40}, "playoff_seed": 6, "players": []},
        {"roster_id": 7, "owner_id": "7", "settings": {"wins": 7, "losses": 10, "ties": 0, "fpts": 2201, "fpts_decimal": 30, "fpts_against": 2250, "fpts_against_decimal": 10}, "playoff_seed": 7, "players": []},
        {"roster_id": 8, "owner_id": "8", "settings": {"wins": 6, "losses": 11, "ties": 0, "fpts": 1654, "fpts_decimal": 90, "fpts_against": 1870, "fpts_against_decimal": 50}, "playoff_seed": 8, "players": []},
        {"roster_id": 9, "owner_id": "9", "settings": {"wins": 6, "losses": 11, "ties": 0, "fpts": 1876, "fpts_decimal": 20, "fpts_against": 1920, "fpts_against_decimal": 70}, "playoff_seed": 9, "players": []},
        {"roster_id": 10, "owner_id": "10", "settings": {"wins": 5, "losses": 12, "ties": 0, "fpts": 1756, "fpts_decimal": 60, "fpts_against": 1890, "fpts_against_decimal": 20}, "playoff_seed": 10, "players": []},
        {"roster_id": 11, "owner_id": "11", "settings": {"wins": 5, "losses": 12, "ties": 0, "fpts": 1723, "fpts_decimal": 40, "fpts_against": 1845, "fpts_against_decimal": 90}, "playoff_seed": 11, "players": []},
        {"roster_id": 12, "owner_id": "12", "settings": {"wins": 4, "losses": 13, "ties": 0, "fpts": 1589, "fpts_decimal": 10, "fpts_against": 1820, "fpts_against_decimal": 60}, "playoff_seed": 12, "players": []},
    ]

    # Sample matchups for championship week
    matchups = {
        18: [
            {"roster_id": 1, "matchup_id": 1, "points": 156.8, "starters": [], "starters_points": [], "players_points": {}},
            {"roster_id": 2, "matchup_id": 1, "points": 142.3, "starters": [], "starters_points": [], "players_points": {}},
        ]
    }

    # Sample transactions
    transactions = {
        1: [
            {"type": "waiver", "status": "complete", "roster_ids": [4], "adds": {"player_1": 4}, "drops": {}},
        ],
        5: [
            {"type": "trade", "status": "complete", "roster_ids": [3, 5], "adds": {"player_10": 3, "player_11": 5}, "drops": {}, "draft_picks": []},
        ],
        8: [
            {"type": "waiver", "status": "complete", "roster_ids": [7], "adds": {"player_20": 7}, "drops": {"player_21": 7}},
        ],
    }

    # Sample players database
    players = {
        "player_1": {"full_name": "Bucky Irving", "position": "RB", "team": "TB"},
        "player_10": {"full_name": "Davante Adams", "position": "WR", "team": "NYJ"},
        "player_11": {"full_name": "2025 1st Round Pick", "position": "PICK", "team": ""},
        "player_20": {"full_name": "Rico Dowdle", "position": "RB", "team": "DAL"},
        "player_21": {"full_name": "Ezekiel Elliott", "position": "RB", "team": "DAL"},
    }

    return league_info, users, rosters, matchups, transactions, players


def get_demo_analyzed_data():
    """Get pre-analyzed demo data for HTML generation."""
    standings = [
        {"owner": "ChampionMike", "wins": 11, "losses": 6, "ties": 0, "points_for": 2145.5, "points_against": 1890.3},
        {"owner": "DynastyKing", "wins": 10, "losses": 7, "ties": 0, "points_for": 2089.2, "points_against": 1920.1},
        {"owner": "TradeHawk", "wins": 9, "losses": 8, "ties": 0, "points_for": 1987.8, "points_against": 1950.6},
        {"owner": "WaiverWire_Warrior", "wins": 9, "losses": 8, "ties": 0, "points_for": 1965.4, "points_against": 1980.2},
        {"owner": "RookieHunter", "wins": 8, "losses": 9, "ties": 0, "points_for": 1920.1, "points_against": 1945.8},
        {"owner": "VetCollector", "wins": 8, "losses": 9, "ties": 0, "points_for": 1898.7, "points_against": 1910.4},
        {"owner": "PointsKing", "wins": 7, "losses": 10, "ties": 0, "points_for": 2201.3, "points_against": 2250.1},
        {"owner": "TankCommander", "wins": 6, "losses": 11, "ties": 0, "points_for": 1654.9, "points_against": 1870.5},
        {"owner": "BoomOrBust", "wins": 6, "losses": 11, "ties": 0, "points_for": 1876.2, "points_against": 1920.7},
        {"owner": "SleepyDrafter", "wins": 5, "losses": 12, "ties": 0, "points_for": 1756.6, "points_against": 1890.2},
        {"owner": "PickTrader", "wins": 5, "losses": 12, "ties": 0, "points_for": 1723.4, "points_against": 1845.9},
        {"owner": "LastPlace_Larry", "wins": 4, "losses": 13, "ties": 0, "points_for": 1589.1, "points_against": 1820.6},
    ]

    champion = {"owner": "ChampionMike", "points": 156.8}

    busts = [
        {"name": "Jonathan Taylor", "position": "RB", "team": "IND", "points": 98.4, "games": 12, "ppg": 8.2},
        {"name": "Travis Kelce", "position": "TE", "team": "KC", "points": 112.6, "games": 15, "ppg": 7.5},
        {"name": "Davante Adams", "position": "WR", "team": "NYJ", "points": 89.3, "games": 10, "ppg": 8.9},
        {"name": "Stefon Diggs", "position": "WR", "team": "HOU", "points": 45.2, "games": 7, "ppg": 6.5},
        {"name": "Joe Burrow", "position": "QB", "team": "CIN", "points": 156.8, "games": 10, "ppg": 15.7},
        {"name": "Isiah Pacheco", "position": "RB", "team": "KC", "points": 52.1, "games": 6, "ppg": 8.7},
        {"name": "Dalton Kincaid", "position": "TE", "team": "BUF", "points": 78.4, "games": 14, "ppg": 5.6},
        {"name": "Chris Olave", "position": "WR", "team": "NO", "points": 95.6, "games": 11, "ppg": 8.7},
        {"name": "DeVonta Smith", "position": "WR", "team": "PHI", "points": 102.3, "games": 14, "ppg": 7.3},
        {"name": "Rhamondre Stevenson", "position": "RB", "team": "NE", "points": 88.9, "games": 13, "ppg": 6.8},
        {"name": "Trey McBride", "position": "TE", "team": "ARI", "points": 105.2, "games": 15, "ppg": 7.0},
        {"name": "Nick Chubb", "position": "RB", "team": "CLE", "points": 35.6, "games": 7, "ppg": 5.1},
    ]

    sleepers = [
        {"name": "Lamar Jackson", "position": "QB", "team": "BAL", "points": 412.5, "games": 16, "ppg": 25.8},
        {"name": "Jahmyr Gibbs", "position": "RB", "team": "DET", "points": 298.4, "games": 17, "ppg": 17.6},
        {"name": "Ja'Marr Chase", "position": "WR", "team": "CIN", "points": 342.1, "games": 17, "ppg": 20.1},
        {"name": "Bucky Irving", "position": "RB", "team": "TB", "points": 198.7, "games": 15, "ppg": 13.2},
        {"name": "Brock Bowers", "position": "TE", "team": "LV", "points": 212.4, "games": 17, "ppg": 12.5},
        {"name": "Jayden Daniels", "position": "QB", "team": "WAS", "points": 356.8, "games": 16, "ppg": 22.3},
        {"name": "Brian Thomas Jr", "position": "WR", "team": "JAX", "points": 198.5, "games": 16, "ppg": 12.4},
        {"name": "Chuba Hubbard", "position": "RB", "team": "CAR", "points": 245.6, "games": 17, "ppg": 14.4},
        {"name": "Rico Dowdle", "position": "RB", "team": "DAL", "points": 178.9, "games": 14, "ppg": 12.8},
        {"name": "Malik Nabers", "position": "WR", "team": "NYG", "points": 187.3, "games": 14, "ppg": 13.4},
        {"name": "Trey Benson", "position": "RB", "team": "ARI", "points": 156.7, "games": 12, "ppg": 13.1},
        {"name": "Sam Darnold", "position": "QB", "team": "MIN", "points": 298.4, "games": 16, "ppg": 18.7},
    ]

    waiver_adds = [
        {"player": "Bucky Irving", "position": "RB", "team": "TB", "week": 3, "owner": "WaiverWire_Warrior"},
        {"player": "Rico Dowdle", "position": "RB", "team": "DAL", "week": 8, "owner": "TradeHawk"},
        {"player": "Trey Benson", "position": "RB", "team": "ARI", "week": 4, "owner": "RookieHunter"},
        {"player": "Taysom Hill", "position": "TE", "team": "NO", "week": 6, "owner": "BoomOrBust"},
        {"player": "Chase Brown", "position": "RB", "team": "CIN", "week": 5, "owner": "DynastyKing"},
        {"player": "Audric Estime", "position": "RB", "team": "DEN", "week": 10, "owner": "TankCommander"},
        {"player": "Jaleel McLaughlin", "position": "RB", "team": "DEN", "week": 2, "owner": "PointsKing"},
        {"player": "Ray Davis", "position": "RB", "team": "BUF", "week": 7, "owner": "VetCollector"},
        {"player": "Tyrone Tracy Jr", "position": "RB", "team": "NYG", "week": 9, "owner": "SleepyDrafter"},
        {"player": "Jalen Coker", "position": "WR", "team": "CAR", "week": 11, "owner": "PickTrader"},
    ]

    waiver_drops = [
        {"player": "Ezekiel Elliott", "position": "RB", "team": "DAL", "week": 6, "owner": "WaiverWire_Warrior"},
        {"player": "Devin Singletary", "position": "RB", "team": "NYG", "week": 4, "owner": "TradeHawk"},
        {"player": "Antonio Gibson", "position": "RB", "team": "NE", "week": 8, "owner": "RookieHunter"},
        {"player": "Tyler Allgeier", "position": "RB", "team": "ATL", "week": 10, "owner": "ChampionMike"},
        {"player": "Diontae Johnson", "position": "WR", "team": "BAL", "week": 12, "owner": "DynastyKing"},
        {"player": "Jerry Jeudy", "position": "WR", "team": "CLE", "week": 7, "owner": "BoomOrBust"},
        {"player": "Michael Pittman Jr", "position": "WR", "team": "IND", "week": 9, "owner": "PointsKing"},
        {"player": "Courtland Sutton", "position": "WR", "team": "DEN", "week": 11, "owner": "VetCollector"},
    ]

    trades = [
        {
            "week": 2,
            "sides": [
                {"owner": "DynastyKing", "receives": {"players": [{"name": "Ja'Marr Chase", "position": "WR"}], "picks": []}},
                {"owner": "TankCommander", "receives": {"players": [{"name": "Jaylen Waddle", "position": "WR"}, {"name": "Tony Pollard", "position": "RB"}], "picks": [{"season": "2025", "round": "1"}]}},
            ],
        },
        {
            "week": 5,
            "sides": [
                {"owner": "TradeHawk", "receives": {"players": [{"name": "Davante Adams", "position": "WR"}], "picks": []}},
                {"owner": "RookieHunter", "receives": {"players": [], "picks": [{"season": "2025", "round": "2"}, {"season": "2026", "round": "2"}]}},
            ],
        },
        {
            "week": 7,
            "sides": [
                {"owner": "ChampionMike", "receives": {"players": [{"name": "Jahmyr Gibbs", "position": "RB"}], "picks": []}},
                {"owner": "PickTrader", "receives": {"players": [{"name": "Breece Hall", "position": "RB"}], "picks": [{"season": "2025", "round": "1"}]}},
            ],
        },
        {
            "week": 9,
            "sides": [
                {"owner": "VetCollector", "receives": {"players": [{"name": "Travis Kelce", "position": "TE"}], "picks": []}},
                {"owner": "LastPlace_Larry", "receives": {"players": [], "picks": [{"season": "2025", "round": "3"}, {"season": "2026", "round": "3"}]}},
            ],
        },
        {
            "week": 11,
            "sides": [
                {"owner": "BoomOrBust", "receives": {"players": [{"name": "DK Metcalf", "position": "WR"}], "picks": []}},
                {"owner": "SleepyDrafter", "receives": {"players": [{"name": "George Pickens", "position": "WR"}, {"name": "Keon Coleman", "position": "WR"}], "picks": []}},
            ],
        },
    ]

    return standings, champion, busts, sleepers, waiver_adds, waiver_drops, trades


def fetch_json(url: str) -> Optional[Any]:
    """Fetch JSON data from a URL with error handling."""
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def fetch_league_data(league_id: str) -> Dict[str, Any]:
    """Fetch all league data from Sleeper API."""
    base_url = "https://api.sleeper.app/v1"

    data = {
        "league": fetch_json(f"{base_url}/league/{league_id}"),
        "users": fetch_json(f"{base_url}/league/{league_id}/users"),
        "rosters": fetch_json(f"{base_url}/league/{league_id}/rosters"),
        "matchups": {},
        "transactions": {},
    }

    if not data["league"]:
        raise ValueError(f"Could not fetch league data for ID: {league_id}")

    # Fetch matchups for all weeks
    season = data["league"].get("season", "2024")
    total_weeks = REGULAR_SEASON_WEEKS + PLAYOFF_WEEKS

    print(f"Fetching matchups for {total_weeks} weeks...")
    for week in range(1, total_weeks + 1):
        matchups = fetch_json(f"{base_url}/league/{league_id}/matchups/{week}")
        if matchups:
            data["matchups"][week] = matchups

    # Fetch transactions for all weeks
    print(f"Fetching transactions for {total_weeks} weeks...")
    for week in range(1, total_weeks + 1):
        transactions = fetch_json(f"{base_url}/league/{league_id}/transactions/{week}")
        if transactions:
            data["transactions"][week] = transactions

    return data


def fetch_players() -> Dict[str, Any]:
    """Fetch all NFL players from Sleeper API."""
    print("Fetching NFL player database (this may take a moment)...")
    players = fetch_json("https://api.sleeper.app/v1/players/nfl")
    return players or {}


def fetch_projections_and_stats() -> Tuple[Dict, Dict]:
    """
    Fetch projected vs actual fantasy points.
    Note: Sleeper deprecated their stats endpoint, so we'll use alternative methods.
    """
    # We'll calculate performance based on matchup points and use position-based expectations
    return {}, {}


def get_user_display_names(users: List[Dict]) -> Dict[str, str]:
    """Create mapping of user_id to display name."""
    return {
        user["user_id"]: user.get("display_name", user.get("user_id", "Unknown"))
        for user in users
    } if users else {}


def get_roster_owner_mapping(rosters: List[Dict], users_map: Dict[str, str]) -> Dict[int, str]:
    """Create mapping of roster_id to owner display name."""
    return {
        roster["roster_id"]: users_map.get(roster.get("owner_id", ""), "Unknown Owner")
        for roster in rosters
    } if rosters else {}


def calculate_standings(rosters: List[Dict], users_map: Dict[str, str]) -> List[Dict]:
    """Calculate final standings from roster data."""
    standings = []
    for roster in rosters:
        owner_id = roster.get("owner_id", "")
        settings = roster.get("settings", {})
        standings.append({
            "owner": users_map.get(owner_id, "Unknown"),
            "owner_id": owner_id,
            "roster_id": roster["roster_id"],
            "wins": settings.get("wins", 0),
            "losses": settings.get("losses", 0),
            "ties": settings.get("ties", 0),
            "points_for": settings.get("fpts", 0) + settings.get("fpts_decimal", 0) / 100,
            "points_against": settings.get("fpts_against", 0) + settings.get("fpts_against_decimal", 0) / 100,
            "playoff_seed": roster.get("playoff_seed"),
        })

    # Sort by wins, then points for
    standings.sort(key=lambda x: (x["wins"], x["points_for"]), reverse=True)
    return standings


def analyze_player_performance(matchups: Dict, rosters: List[Dict], players: Dict) -> Tuple[List[Dict], List[Dict]]:
    """
    Analyze player performance vs expectations to find busts and sleepers.
    Uses aggregate season points and position-based expectations.
    """
    # Track total points per player
    player_points = defaultdict(float)
    player_starts = defaultdict(int)

    # Collect all player IDs on rosters
    rostered_players = set()
    for roster in rosters:
        rostered_players.update(roster.get("players", []) or [])

    # Sum up points from all matchups
    for week, week_matchups in matchups.items():
        if not week_matchups:
            continue
        for matchup in week_matchups:
            starters = matchup.get("starters", []) or []
            starters_points = matchup.get("starters_points", []) or []
            players_points = matchup.get("players_points", {}) or {}

            # Count points from starters_points
            for i, player_id in enumerate(starters):
                if player_id and i < len(starters_points) and starters_points[i]:
                    player_points[player_id] += starters_points[i]
                    player_starts[player_id] += 1

            # Also use players_points if available
            for player_id, pts in players_points.items():
                if pts and player_id not in starters:
                    player_points[player_id] += pts

    # Position-based expectations (approximate ADP-based expectations for 2024)
    position_expectations = {
        "QB": {"high": 350, "avg": 280, "low": 200},
        "RB": {"high": 250, "avg": 150, "low": 80},
        "WR": {"high": 250, "avg": 160, "low": 90},
        "TE": {"high": 200, "avg": 120, "low": 60},
    }

    # Categorize players
    busts = []
    sleepers = []

    for player_id, total_pts in player_points.items():
        if player_id not in players:
            continue

        player_info = players[player_id]
        position = player_info.get("position", "")
        name = player_info.get("full_name", player_info.get("first_name", "") + " " + player_info.get("last_name", ""))
        team = player_info.get("team", "FA")

        if position not in position_expectations:
            continue

        exp = position_expectations[position]
        starts = player_starts.get(player_id, 0)

        # Only consider players who started at least 5 games
        if starts < 5:
            continue

        # Normalize to 17-game expectation
        ppg = total_pts / max(starts, 1)
        projected_season = ppg * 17

        # Bust: High expectation players who significantly underperformed
        # Look for players in top-tier positions who scored below average
        if projected_season < exp["low"] and starts >= 8:
            busts.append({
                "name": name,
                "position": position,
                "team": team,
                "points": round(total_pts, 1),
                "games": starts,
                "ppg": round(ppg, 1),
                "player_id": player_id,
            })

        # Sleeper: Lower expectation players who significantly overperformed
        if projected_season > exp["high"]:
            sleepers.append({
                "name": name,
                "position": position,
                "team": team,
                "points": round(total_pts, 1),
                "games": starts,
                "ppg": round(ppg, 1),
                "player_id": player_id,
            })

    # Sort by PPG (descending for sleepers, ascending for busts)
    sleepers.sort(key=lambda x: x["ppg"], reverse=True)
    busts.sort(key=lambda x: x["ppg"])

    return busts[:12], sleepers[:12]  # Top 12 each (enough for a starting lineup)


def analyze_waiver_activity(transactions: Dict, players: Dict, roster_owners: Dict[int, str]) -> Tuple[List[Dict], List[Dict]]:
    """Analyze waiver wire additions and drops."""
    additions = []
    drops = []

    for week, week_transactions in transactions.items():
        if not week_transactions:
            continue
        for tx in week_transactions:
            tx_type = tx.get("type", "")
            status = tx.get("status", "")

            if status != "complete":
                continue

            if tx_type in ["waiver", "free_agent"]:
                adds = tx.get("adds", {}) or {}
                drops_dict = tx.get("drops", {}) or {}
                roster_ids = tx.get("roster_ids", [])

                owner = "Unknown"
                if roster_ids:
                    owner = roster_owners.get(roster_ids[0], "Unknown")

                for player_id, roster_id in adds.items():
                    if player_id in players:
                        player_info = players[player_id]
                        additions.append({
                            "player": player_info.get("full_name", "Unknown"),
                            "position": player_info.get("position", ""),
                            "team": player_info.get("team", "FA"),
                            "week": week,
                            "owner": roster_owners.get(roster_id, owner),
                            "player_id": player_id,
                        })

                for player_id, roster_id in drops_dict.items():
                    if player_id in players:
                        player_info = players[player_id]
                        drops.append({
                            "player": player_info.get("full_name", "Unknown"),
                            "position": player_info.get("position", ""),
                            "team": player_info.get("team", "FA"),
                            "week": week,
                            "owner": roster_owners.get(roster_id, owner),
                            "player_id": player_id,
                        })

    return additions, drops


def analyze_trades(transactions: Dict, players: Dict, roster_owners: Dict[int, str]) -> List[Dict]:
    """Analyze all trades in the league."""
    trades = []

    for week, week_transactions in transactions.items():
        if not week_transactions:
            continue
        for tx in week_transactions:
            if tx.get("type") != "trade" or tx.get("status") != "complete":
                continue

            adds = tx.get("adds", {}) or {}
            drops = tx.get("drops", {}) or {}
            draft_picks = tx.get("draft_picks", []) or []
            roster_ids = tx.get("roster_ids", []) or []

            # Group by roster_id
            sides = defaultdict(lambda: {"players": [], "picks": []})

            for player_id, roster_id in adds.items():
                if player_id in players:
                    player_info = players[player_id]
                    sides[roster_id]["players"].append({
                        "name": player_info.get("full_name", "Unknown"),
                        "position": player_info.get("position", ""),
                        "team": player_info.get("team", "FA"),
                    })

            for pick in draft_picks:
                owner_id = pick.get("owner_id")
                if owner_id:
                    # Find roster_id for this owner
                    for rid in roster_ids:
                        if roster_owners.get(rid) and str(pick.get("owner_id")) in str(rid):
                            sides[rid]["picks"].append({
                                "season": pick.get("season", ""),
                                "round": pick.get("round", ""),
                            })
                            break

            if len(roster_ids) >= 2:
                trade_info = {
                    "week": week,
                    "sides": [],
                }
                for roster_id in roster_ids[:2]:  # Get first two sides
                    owner = roster_owners.get(roster_id, "Unknown")
                    side = sides.get(roster_id, {"players": [], "picks": []})
                    trade_info["sides"].append({
                        "owner": owner,
                        "receives": side,
                    })

                # Determine what each side gave up
                if len(trade_info["sides"]) >= 2:
                    # Side 0 receives what side 1 gave up
                    # Need to recalculate based on drops
                    trades.append(trade_info)

    return trades


def determine_champion(rosters: List[Dict], matchups: Dict, users_map: Dict[str, str]) -> Optional[Dict]:
    """Determine the league champion based on playoff matchups."""
    # Check last week of playoffs (championship week)
    championship_week = max(matchups.keys()) if matchups else REGULAR_SEASON_WEEKS + 3

    if championship_week in matchups:
        week_matchups = matchups[championship_week]
        if week_matchups:
            # Find the highest scoring team in the championship matchup
            champion_matchup = None
            max_points = 0

            for matchup in week_matchups:
                pts = matchup.get("points", 0) or 0
                if pts > max_points:
                    max_points = pts
                    champion_matchup = matchup

            if champion_matchup:
                roster_id = champion_matchup.get("roster_id")
                for roster in rosters:
                    if roster["roster_id"] == roster_id:
                        owner_id = roster.get("owner_id", "")
                        return {
                            "owner": users_map.get(owner_id, "Unknown"),
                            "points": max_points,
                            "roster_id": roster_id,
                        }

    # Fallback: use the team with most wins and best playoff seed
    for roster in rosters:
        if roster.get("playoff_seed") == 1:
            settings = roster.get("settings", {})
            owner_id = roster.get("owner_id", "")
            return {
                "owner": users_map.get(owner_id, "Unknown"),
                "points": settings.get("fpts", 0),
                "roster_id": roster["roster_id"],
            }

    return None


def generate_html(
    league_info: Dict,
    standings: List[Dict],
    champion: Optional[Dict],
    busts: List[Dict],
    sleepers: List[Dict],
    waiver_adds: List[Dict],
    waiver_drops: List[Dict],
    trades: List[Dict],
) -> str:
    """Generate the complete HTML recap."""

    league_name = html.escape(league_info.get("name", "Dynasty Fantasy Football League"))
    season = league_info.get("season", "2024")

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{league_name} - {season} Season Recap</title>
    <style>
        :root {{
            --primary-color: #1a1a2e;
            --secondary-color: #16213e;
            --accent-color: #e94560;
            --accent-secondary: #0f3460;
            --gold: #ffd700;
            --silver: #c0c0c0;
            --bronze: #cd7f32;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --success: #4caf50;
            --danger: #f44336;
            --warning: #ff9800;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--primary-color) 100%);
            border-bottom: 4px solid var(--accent-color);
            margin-bottom: 40px;
        }}

        header h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}

        header .season {{
            font-size: 1.5rem;
            color: var(--accent-color);
            font-weight: bold;
        }}

        .section {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }}

        .section h2 {{
            color: var(--accent-color);
            margin-bottom: 20px;
            font-size: 1.8rem;
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .champion-card {{
            background: linear-gradient(135deg, var(--gold) 0%, #b8860b 100%);
            color: #1a1a1a;
            text-align: center;
            padding: 40px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(255,215,0,0.3);
        }}

        .champion-card h2 {{
            color: #1a1a1a;
            border-bottom-color: #1a1a1a;
        }}

        .champion-card .trophy {{
            font-size: 4rem;
            margin-bottom: 20px;
        }}

        .champion-card .name {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .standings-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .standings-table th,
        .standings-table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}

        .standings-table th {{
            background: rgba(233,69,96,0.2);
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9rem;
        }}

        .standings-table tr:hover {{
            background: rgba(255,255,255,0.05);
        }}

        .standings-table .rank-1 td:first-child {{ color: var(--gold); font-weight: bold; }}
        .standings-table .rank-2 td:first-child {{ color: var(--silver); font-weight: bold; }}
        .standings-table .rank-3 td:first-child {{ color: var(--bronze); font-weight: bold; }}

        .team-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
        }}

        .player-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .player-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }}

        .player-card.bust {{
            border-left: 4px solid var(--danger);
        }}

        .player-card.sleeper {{
            border-left: 4px solid var(--success);
        }}

        .player-card .position {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9rem;
        }}

        .player-card .position.QB {{ background: #e91e63; }}
        .player-card .position.RB {{ background: #4caf50; }}
        .player-card .position.WR {{ background: #2196f3; }}
        .player-card .position.TE {{ background: #ff9800; }}

        .player-card .info {{
            flex: 1;
        }}

        .player-card .name {{
            font-weight: bold;
            font-size: 1.1rem;
        }}

        .player-card .team {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .player-card .stats {{
            text-align: right;
        }}

        .player-card .points {{
            font-size: 1.3rem;
            font-weight: bold;
        }}

        .player-card .ppg {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .transaction-list {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .transaction-item {{
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .transaction-item .week {{
            background: var(--accent-secondary);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
        }}

        .transaction-item .player {{
            flex: 1;
            font-weight: bold;
        }}

        .transaction-item .owner {{
            color: var(--text-secondary);
        }}

        .transaction-item.add {{ border-left: 4px solid var(--success); }}
        .transaction-item.drop {{ border-left: 4px solid var(--danger); }}

        .trade-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid var(--warning);
        }}

        .trade-card .week-badge {{
            background: var(--warning);
            color: #1a1a1a;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 15px;
        }}

        .trade-sides {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 20px;
            align-items: center;
        }}

        .trade-side {{
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 15px;
        }}

        .trade-side .owner {{
            font-weight: bold;
            color: var(--accent-color);
            margin-bottom: 10px;
        }}

        .trade-arrow {{
            font-size: 2rem;
            color: var(--warning);
        }}

        .trade-player {{
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}

        .trade-player:last-child {{
            border-bottom: none;
        }}

        .trade-pick {{
            color: var(--text-secondary);
            font-style: italic;
        }}

        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .badge-best {{ background: var(--success); color: white; }}
        .badge-worst {{ background: var(--danger); color: white; }}

        footer {{
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
            border-top: 1px solid rgba(255,255,255,0.1);
            margin-top: 40px;
        }}

        .empty-state {{
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
        }}

        @media (max-width: 768px) {{
            header h1 {{
                font-size: 2rem;
            }}

            .trade-sides {{
                grid-template-columns: 1fr;
            }}

            .trade-arrow {{
                transform: rotate(90deg);
                text-align: center;
            }}

            .team-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>{league_name}</h1>
        <div class="season">{season} Season Recap</div>
    </header>

    <div class="container">
'''

    # Champion Section
    if champion:
        html_content += f'''
        <div class="champion-card">
            <div class="trophy">🏆</div>
            <h2>League Champion</h2>
            <div class="name">{html.escape(champion["owner"])}</div>
            <div>Championship Points: {champion.get("points", "N/A")}</div>
        </div>
'''

    # Standings Section
    html_content += '''
        <div class="section">
            <h2>📊 Final Standings</h2>
            <table class="standings-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Team</th>
                        <th>Record</th>
                        <th>Points For</th>
                        <th>Points Against</th>
                    </tr>
                </thead>
                <tbody>
'''

    for i, team in enumerate(standings, 1):
        rank_class = f"rank-{i}" if i <= 3 else ""
        record = f"{team['wins']}-{team['losses']}"
        if team.get('ties', 0) > 0:
            record += f"-{team['ties']}"

        html_content += f'''
                    <tr class="{rank_class}">
                        <td>{i}</td>
                        <td>{html.escape(team["owner"])}</td>
                        <td>{record}</td>
                        <td>{team["points_for"]:.1f}</td>
                        <td>{team["points_against"]:.1f}</td>
                    </tr>
'''

    html_content += '''
                </tbody>
            </table>
        </div>
'''

    # All-Busts Team Section
    html_content += '''
        <div class="section">
            <h2>💔 All-Busts Team</h2>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">Players who dramatically underperformed expectations this season</p>
'''

    if busts:
        html_content += '<div class="team-grid">'
        for player in busts:
            html_content += f'''
                <div class="player-card bust">
                    <div class="position {player["position"]}">{player["position"]}</div>
                    <div class="info">
                        <div class="name">{html.escape(player["name"])}</div>
                        <div class="team">{player["team"] or "FA"}</div>
                    </div>
                    <div class="stats">
                        <div class="points">{player["points"]}</div>
                        <div class="ppg">{player["ppg"]} PPG</div>
                    </div>
                </div>
'''
        html_content += '</div>'
    else:
        html_content += '<div class="empty-state">No significant busts identified</div>'

    html_content += '</div>'

    # All-Sleeper Team Section
    html_content += '''
        <div class="section">
            <h2>🌟 All-Sleeper Team</h2>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">Players who dramatically overperformed expectations this season</p>
'''

    if sleepers:
        html_content += '<div class="team-grid">'
        for player in sleepers:
            html_content += f'''
                <div class="player-card sleeper">
                    <div class="position {player["position"]}">{player["position"]}</div>
                    <div class="info">
                        <div class="name">{html.escape(player["name"])}</div>
                        <div class="team">{player["team"] or "FA"}</div>
                    </div>
                    <div class="stats">
                        <div class="points">{player["points"]}</div>
                        <div class="ppg">{player["ppg"]} PPG</div>
                    </div>
                </div>
'''
        html_content += '</div>'
    else:
        html_content += '<div class="empty-state">No significant sleepers identified</div>'

    html_content += '</div>'

    # Top Waiver Wire Additions
    html_content += '''
        <div class="section">
            <h2>📈 Top Waiver Wire Additions</h2>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">Notable pickups throughout the season</p>
'''

    if waiver_adds:
        html_content += '<div class="transaction-list">'
        for tx in waiver_adds[:15]:  # Top 15
            html_content += f'''
                <div class="transaction-item add">
                    <span class="week">Week {tx["week"]}</span>
                    <span class="player">{html.escape(tx["player"])} ({tx["position"]} - {tx["team"] or "FA"})</span>
                    <span class="owner">Added by {html.escape(tx["owner"])}</span>
                </div>
'''
        html_content += '</div>'
    else:
        html_content += '<div class="empty-state">No waiver additions recorded</div>'

    html_content += '</div>'

    # Notable Drops
    html_content += '''
        <div class="section">
            <h2>📉 Notable Drops</h2>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">Players released throughout the season</p>
'''

    if waiver_drops:
        html_content += '<div class="transaction-list">'
        for tx in waiver_drops[:15]:  # Top 15
            html_content += f'''
                <div class="transaction-item drop">
                    <span class="week">Week {tx["week"]}</span>
                    <span class="player">{html.escape(tx["player"])} ({tx["position"]} - {tx["team"] or "FA"})</span>
                    <span class="owner">Dropped by {html.escape(tx["owner"])}</span>
                </div>
'''
        html_content += '</div>'
    else:
        html_content += '<div class="empty-state">No drops recorded</div>'

    html_content += '</div>'

    # Trades Section
    html_content += '''
        <div class="section">
            <h2>🔄 Season Trades</h2>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">All trades that went down this season</p>
'''

    if trades:
        for i, trade in enumerate(trades):
            badge = ""
            if i == 0:
                badge = '<span class="badge badge-best">Best Trade</span>'
            elif i == len(trades) - 1 and len(trades) > 1:
                badge = '<span class="badge badge-worst">Worst Trade</span>'

            html_content += f'''
            <div class="trade-card">
                <span class="week-badge">Week {trade["week"]}</span>
                {badge}
                <div class="trade-sides">
'''

            if len(trade["sides"]) >= 2:
                # Side 1
                side1 = trade["sides"][0]
                html_content += f'''
                    <div class="trade-side">
                        <div class="owner">{html.escape(side1["owner"])} receives:</div>
'''
                receives = side1.get("receives", {})
                for player in receives.get("players", []):
                    html_content += f'<div class="trade-player">{html.escape(player["name"])} ({player["position"]})</div>'
                for pick in receives.get("picks", []):
                    html_content += f'<div class="trade-pick">{pick["season"]} Round {pick["round"]} Pick</div>'
                if not receives.get("players") and not receives.get("picks"):
                    html_content += '<div class="trade-player">Unknown assets</div>'
                html_content += '</div>'

                html_content += '<div class="trade-arrow">⇄</div>'

                # Side 2
                side2 = trade["sides"][1]
                html_content += f'''
                    <div class="trade-side">
                        <div class="owner">{html.escape(side2["owner"])} receives:</div>
'''
                receives = side2.get("receives", {})
                for player in receives.get("players", []):
                    html_content += f'<div class="trade-player">{html.escape(player["name"])} ({player["position"]})</div>'
                for pick in receives.get("picks", []):
                    html_content += f'<div class="trade-pick">{pick["season"]} Round {pick["round"]} Pick</div>'
                if not receives.get("players") and not receives.get("picks"):
                    html_content += '<div class="trade-player">Unknown assets</div>'
                html_content += '</div>'

            html_content += '''
                </div>
            </div>
'''
    else:
        html_content += '<div class="empty-state">No trades recorded this season</div>'

    html_content += '</div>'

    # Footer
    html_content += f'''
    </div>

    <footer>
        <p>Generated on {datetime.now().strftime("%B %d, %Y")}</p>
        <p>Powered by Dynasty Oracle | Data from Sleeper API</p>
    </footer>
</body>
</html>
'''

    return html_content


def main():
    """Main function to generate the season recap."""
    parser = argparse.ArgumentParser(
        description="Generate a season recap for a Sleeper dynasty fantasy football league"
    )
    parser.add_argument(
        "league_id",
        nargs="?",
        default=DEFAULT_LEAGUE_ID,
        help=f"Sleeper league ID (default: {DEFAULT_LEAGUE_ID})"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate recap with sample demo data (for preview)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Custom output file path"
    )

    args = parser.parse_args()
    import os

    print(f"\n🏈 Dynasty Fantasy Football Season Recap Generator")
    print(f"=" * 50)

    if args.demo:
        print("Running in DEMO mode with sample data...\n")

        # Get demo analyzed data
        standings, champion, busts, sleepers, waiver_adds, waiver_drops, trades = get_demo_analyzed_data()
        league_info = {
            "name": "GAH Dynasty",
            "season": "2024",
        }

        print(f"League: {league_info['name']} (Demo)")
        print(f"Season: {league_info['season']}")
        print(f"  - {len(standings)} teams in standings")
        print(f"  - {len(busts)} busts and {len(sleepers)} sleepers")
        print(f"  - {len(waiver_adds)} waiver additions and {len(waiver_drops)} drops")
        print(f"  - {len(trades)} trades")

    else:
        league_id = args.league_id
        print(f"League ID: {league_id}\n")

        # Fetch all data
        print("Fetching league data from Sleeper API...")
        league_data = fetch_league_data(league_id)

        players = fetch_players()
        if not players:
            print("Warning: Could not fetch player database. Some features may be limited.")

        # Extract data
        league_info = league_data["league"]
        users = league_data["users"] or []
        rosters = league_data["rosters"] or []
        matchups = league_data["matchups"]
        transactions = league_data["transactions"]

        print(f"\nLeague: {league_info.get('name', 'Unknown')}")
        print(f"Season: {league_info.get('season', 'Unknown')}")
        print(f"Teams: {len(rosters)}")
        print(f"Matchup weeks fetched: {len(matchups)}")
        print(f"Transaction weeks fetched: {len(transactions)}")

        # Create mappings
        users_map = get_user_display_names(users)
        roster_owners = get_roster_owner_mapping(rosters, users_map)

        # Analyze data
        print("\nAnalyzing data...")

        standings = calculate_standings(rosters, users_map)
        champion = determine_champion(rosters, matchups, users_map)

        busts, sleepers = analyze_player_performance(matchups, rosters, players)
        print(f"  - Found {len(busts)} busts and {len(sleepers)} sleepers")

        waiver_adds, waiver_drops = analyze_waiver_activity(transactions, players, roster_owners)
        print(f"  - Found {len(waiver_adds)} waiver additions and {len(waiver_drops)} drops")

        trades = analyze_trades(transactions, players, roster_owners)
        print(f"  - Found {len(trades)} trades")

    # Generate HTML
    print("\nGenerating HTML recap...")
    html_content = generate_html(
        league_info,
        standings,
        champion,
        busts,
        sleepers,
        waiver_adds,
        waiver_drops,
        trades,
    )

    # Save to file
    output_dir = "data_outputs"
    os.makedirs(output_dir, exist_ok=True)

    if args.output:
        output_file = args.output
    else:
        league_name_safe = "".join(c for c in league_info.get("name", "league") if c.isalnum() or c in " -_").strip()
        season = league_info.get("season", "2024")
        suffix = "_Demo" if args.demo else ""
        output_file = f"{output_dir}/{league_name_safe}_{season}_Recap{suffix}.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n✅ Recap generated successfully!")
    print(f"📄 Output file: {output_file}")
    print(f"\nOpen this file in your browser to view the recap!")


if __name__ == "__main__":
    main()

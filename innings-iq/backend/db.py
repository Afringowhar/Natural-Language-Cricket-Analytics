import os
import sqlite3
import pandas as pd
import json
from datetime import datetime

DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'ipl_data')
DB_PATH = os.path.join(os.path.dirname(__file__), 'ipl.db')

def create_tables(conn):
    """Create all required tables in the database."""
    cursor = conn.cursor()
    
    # Season table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS season (
        season_id INTEGER PRIMARY KEY AUTOINCREMENT,
        year TEXT NOT NULL,
        UNIQUE(year)
    )
    """)
    
    # Venue table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venue (
        venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT,
        UNIQUE(name, city)
    )
    """)
    
    # Team table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS team (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        team_type TEXT
    )
    """)
    
    # Player table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        identifier TEXT UNIQUE,
        UNIQUE(name, identifier)
    )
    """)
    
    # Official type table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS official_type (
        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL UNIQUE
    )
    """)
    
    # Official table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS official (
        official_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        identifier TEXT UNIQUE,
        UNIQUE(name, identifier)
    )
    """)
    
    # Match table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS match (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        season_id INTEGER,
        venue_id INTEGER,
        match_number INTEGER,
        gender TEXT,
        match_type TEXT,
        event_name TEXT,
        balls_per_over INTEGER,
        dates TEXT,
        created_date TEXT,
        revision INTEGER,
        data_version TEXT,
        FOREIGN KEY (season_id) REFERENCES season(season_id),
        FOREIGN KEY (venue_id) REFERENCES venue(venue_id)
    )
    """)
    
    # Toss table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS toss (
        toss_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        winner_team_id INTEGER,
        decision TEXT,
        FOREIGN KEY (match_id) REFERENCES match(match_id),
        FOREIGN KEY (winner_team_id) REFERENCES team(team_id)
    )
    """)
    
    # Outcome table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS outcome (
        outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        winner_team_id INTEGER,
        by_runs INTEGER,
        by_wickets INTEGER,
        method TEXT,
        eliminated_team_id INTEGER,
        result TEXT,
        FOREIGN KEY (match_id) REFERENCES match(match_id),
        FOREIGN KEY (winner_team_id) REFERENCES team(team_id),
        FOREIGN KEY (eliminated_team_id) REFERENCES team(team_id)
    )
    """)
    
    # Match official table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS match_official (
        match_official_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        official_id INTEGER,
        type_id INTEGER,
        FOREIGN KEY (match_id) REFERENCES match(match_id),
        FOREIGN KEY (official_id) REFERENCES official(official_id),
        FOREIGN KEY (type_id) REFERENCES official_type(type_id)
    )
    """)
    
    # Match team table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS match_team (
        match_team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        team_id INTEGER,
        is_playing BOOLEAN,
        FOREIGN KEY (match_id) REFERENCES match(match_id),
        FOREIGN KEY (team_id) REFERENCES team(team_id),
        UNIQUE(match_id, team_id)
    )
    """)
    
    # Match player table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS match_player (
        match_player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        team_id INTEGER,
        player_id INTEGER,
        is_playing BOOLEAN,
        FOREIGN KEY (match_id) REFERENCES match(match_id),
        FOREIGN KEY (team_id) REFERENCES team(team_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id),
        UNIQUE(match_id, player_id)
    )
    """)
    
    # Player of match table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_of_match (
        pom_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        player_id INTEGER,
        FOREIGN KEY (match_id) REFERENCES match(match_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id),
        UNIQUE(match_id, player_id)
    )
    """)
    
    # Innings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS innings (
        innings_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        team_id INTEGER,
        innings_number INTEGER,
        target_runs INTEGER,
        target_overs INTEGER,
        FOREIGN KEY (match_id) REFERENCES match(match_id),
        FOREIGN KEY (team_id) REFERENCES team(team_id)
    )
    """)
    
    # Powerplay table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS powerplay (
        powerplay_id INTEGER PRIMARY KEY AUTOINCREMENT,
        innings_id INTEGER,
        start_over REAL,
        end_over REAL,
        type TEXT,
        FOREIGN KEY (innings_id) REFERENCES innings(innings_id)
    )
    """)
    
    # Over table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS over (
        over_id INTEGER PRIMARY KEY AUTOINCREMENT,
        innings_id INTEGER,
        over_number INTEGER,
        FOREIGN KEY (innings_id) REFERENCES innings(innings_id),
        UNIQUE(innings_id, over_number)
    )
    """)
    
    # Delivery table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS delivery (
        delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
        over_id INTEGER,
        innings_id INTEGER,
        delivery_number INTEGER,
        batter_id INTEGER,
        bowler_id INTEGER,
        non_striker_id INTEGER,
        runs_batter INTEGER,
        runs_extras INTEGER,
        runs_total INTEGER,
        extras_type TEXT,
        extras_value INTEGER,
        FOREIGN KEY (over_id) REFERENCES over(over_id),
        FOREIGN KEY (innings_id) REFERENCES innings(innings_id),
        FOREIGN KEY (batter_id) REFERENCES player(player_id),
        FOREIGN KEY (bowler_id) REFERENCES player(player_id),
        FOREIGN KEY (non_striker_id) REFERENCES player(player_id)
    )
    """)
    
    # Wicket table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wicket (
        wicket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        delivery_id INTEGER,
        player_out_id INTEGER,
        kind TEXT,
        fielder_id INTEGER,
        FOREIGN KEY (delivery_id) REFERENCES delivery(delivery_id),
        FOREIGN KEY (player_out_id) REFERENCES player(player_id),
        FOREIGN KEY (fielder_id) REFERENCES player(player_id)
    )
    """)
    
    # Replacement table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS replacement (
        replacement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        team_id INTEGER,
        player_out_id INTEGER,
        player_in_id INTEGER,
        reason TEXT,
        FOREIGN KEY (match_id) REFERENCES match(match_id),
        FOREIGN KEY (team_id) REFERENCES team(team_id),
        FOREIGN KEY (player_out_id) REFERENCES player(player_id),
        FOREIGN KEY (player_in_id) REFERENCES player(player_id)
    )
    """)
    
    # Review table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS review (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        delivery_id INTEGER,
        reviewed_by TEXT,
        umpire TEXT,
        batter_id INTEGER,
        decision TEXT,
        type TEXT,
        is_umpires_call BOOLEAN,
        FOREIGN KEY (delivery_id) REFERENCES delivery(delivery_id),
        FOREIGN KEY (batter_id) REFERENCES player(player_id)
    )
    """)
    
    conn.commit()

def get_or_create(conn, table, columns, values, id_column=None):
    """
    Helper function to get or create a record in a table.
    Returns the ID of the existing or newly created record.
    """
    cursor = conn.cursor()
    
    # Determine the primary key column if not provided
    if id_column is None:
        # Map tables to their primary key columns
        pk_columns = {
            'season': 'season_id',
            'venue': 'venue_id',
            'team': 'team_id',
            'player': 'player_id',
            'official_type': 'type_id',
            'official': 'official_id',
            'match': 'match_id',
            'toss': 'toss_id',
            'outcome': 'outcome_id',
            'match_official': 'match_official_id',
            'match_team': 'match_team_id',
            'match_player': 'match_player_id',
            'player_of_match': 'pom_id',
            'innings': 'innings_id',
            'powerplay': 'powerplay_id',
            'over': 'over_id',
            'delivery': 'delivery_id',
            'wicket': 'wicket_id',
            'replacement': 'replacement_id',
            'review': 'review_id'
        }
        id_column = pk_columns.get(table, 'id')  # Default to 'id' if not found
    
    # Build WHERE clause for checking existence
    where_clause = ' AND '.join([f"{col} = ?" for col in columns])
    
    # Check if record exists
    cursor.execute(f"SELECT {id_column} FROM {table} WHERE {where_clause}", values)
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        # Insert new record
        placeholders = ', '.join(['?'] * len(values))
        col_names = ', '.join(columns)
        cursor.execute(f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})", values)
        conn.commit()
        return cursor.lastrowid

def process_match_data(conn, data):
    """Process a single match JSON data and insert into database."""
    try:
        # Extract basic info
        meta = data.get('meta', {})
        info = data.get('info', {})
        innings = data.get('innings', [])
        
        # Insert season
        season_year = info.get('season', '')
        season_id = get_or_create(conn, 'season', ['year'], [season_year])
        
        # Insert venue
        venue_name = info.get('venue', '')
        city = info.get('city', '')
        venue_id = get_or_create(conn, 'venue', ['name', 'city'], [venue_name, city])
        
        # Insert teams
        teams = info.get('teams', [])
        team_ids = {}
        for team_name in teams:
            team_type = info.get('team_type', '')
            team_id = get_or_create(conn, 'team', ['name', 'team_type'], [team_name, team_type])
            team_ids[team_name] = team_id
        
        # Insert players
        players = info.get('players', {})
        registry = info.get('registry', {}).get('people', {})
        player_ids = {}
        
        for team_name, team_players in players.items():
            for player_name in team_players:
                player_identifier = registry.get(player_name, '')
                player_id = get_or_create(
                    conn, 'player', ['name', 'identifier'], [player_name, player_identifier])
                player_ids[player_name] = player_id
        
        # Insert officials and their types
        officials = info.get('officials', {})
        official_types = {
            'match_referees': 'match_referee',
            'umpires': 'umpire',
            'tv_umpires': 'tv_umpire',
            'reserve_umpires': 'reserve_umpire'
        }
        
        # First ensure all official types exist
        for role in official_types.values():
            get_or_create(conn, 'official_type', ['role'], [role])
        
        # Then process officials
        for official_group, role in official_types.items():
            if official_group in officials:
                type_id = get_or_create(conn, 'official_type', ['role'], [role])
                
                for official_name in officials[official_group]:
                    official_identifier = registry.get(official_name, '')
                    official_id = get_or_create(
                        conn, 'official', ['name', 'identifier'], [official_name, official_identifier])
        
        # Insert match
        match_values = [
            season_id,
            venue_id,
            info.get('event', {}).get('match_number'),
            info.get('gender'),
            info.get('match_type'),
            info.get('event', {}).get('name'),
            info.get('balls_per_over'),
            json.dumps(info.get('dates', [])),
            meta.get('created'),
            meta.get('revision'),
            meta.get('data_version')
        ]
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO match (
                season_id, venue_id, match_number, gender, match_type, event_name, 
                balls_per_over, dates, created_date, revision, data_version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, match_values)
        match_id = cursor.lastrowid
        conn.commit()
        
        # Insert toss
        toss_winner = info.get('toss', {}).get('winner')
        if toss_winner and toss_winner in team_ids:
            cursor.execute("""
                INSERT INTO toss (match_id, winner_team_id, decision)
                VALUES (?, ?, ?)
            """, [match_id, team_ids[toss_winner], info.get('toss', {}).get('decision')])
            conn.commit()
        
        # Insert outcome
        outcome = info.get('outcome', {})
        winner = outcome.get('winner')
        if winner and winner in team_ids:
            by_data = outcome.get('by', {})
            cursor.execute("""
                INSERT INTO outcome (
                    match_id, winner_team_id, by_runs, by_wickets, method, result
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, [
                match_id,
                team_ids[winner],
                by_data.get('runs'),
                by_data.get('wickets'),
                outcome.get('method'),
                outcome.get('result')
            ])
            conn.commit()
        
        # Insert match officials
        for official_group, role in official_types.items():
            if official_group in officials:
                type_id = get_or_create(conn, 'official_type', ['role'], [role])
                
                for official_name in officials[official_group]:
                    official_identifier = registry.get(official_name, '')
                    official_id = get_or_create(
                        conn, 'official', ['name', 'identifier'], [official_name, official_identifier])
                    
                    cursor.execute("""
                        INSERT INTO match_official (match_id, official_id, type_id)
                        VALUES (?, ?, ?)
                    """, [match_id, official_id, type_id])
        conn.commit()
        
        # Insert match teams
        for team_name, team_id in team_ids.items():
            cursor.execute("""
                INSERT INTO match_team (match_id, team_id, is_playing)
                VALUES (?, ?, ?)
            """, [match_id, team_id, True])
        conn.commit()
        
        # Insert match players
        for team_name, team_players in players.items():
            team_id = team_ids[team_name]
            for player_name in team_players:
                player_id = player_ids[player_name]
                cursor.execute("""
                    INSERT INTO match_player (match_id, team_id, player_id, is_playing)
                    VALUES (?, ?, ?, ?)
                """, [match_id, team_id, player_id, True])
        conn.commit()
        
        # Insert player of match
        player_of_match = info.get('player_of_match', [])
        for player_name in player_of_match:
            player_id = player_ids.get(player_name)
            if player_id:
                cursor.execute("""
                    INSERT INTO player_of_match (match_id, player_id)
                    VALUES (?, ?)
                """, [match_id, player_id])
        conn.commit()
        
        # Process innings
        for innings_num, innings_data in enumerate(innings, 1):
            team_name = innings_data.get('team')
            team_id = team_ids.get(team_name)
            
            # Insert innings
            target = innings_data.get('target', {})
            cursor.execute("""
                INSERT INTO innings (
                    match_id, team_id, innings_number, target_runs, target_overs
                ) VALUES (?, ?, ?, ?, ?)
            """, [
                match_id,
                team_id,
                innings_num,
                target.get('runs'),
                target.get('overs')
            ])
            innings_id = cursor.lastrowid
            conn.commit()
            
            # Insert powerplays
            powerplays = innings_data.get('powerplays', [])
            for pp in powerplays:
                cursor.execute("""
                    INSERT INTO powerplay (
                        innings_id, start_over, end_over, type
                    ) VALUES (?, ?, ?, ?)
                """, [
                    innings_id,
                    pp.get('from'),
                    pp.get('to'),
                    pp.get('type')
                ])
            conn.commit()
            
            # Process overs
            overs = innings_data.get('overs', [])
            for over_data in overs:
                over_number = over_data.get('over')
                
                # Insert over
                cursor.execute("""
                    INSERT INTO over (innings_id, over_number)
                    VALUES (?, ?)
                """, [innings_id, over_number])
                over_id = cursor.lastrowid
                conn.commit()
                
                # Process deliveries
                deliveries = over_data.get('deliveries', [])
                for delivery_num, delivery_data in enumerate(deliveries, 1):
                    batter_name = delivery_data.get('batter')
                    bowler_name = delivery_data.get('bowler')
                    non_striker_name = delivery_data.get('non_striker')
                    
                    batter_id = player_ids.get(batter_name)
                    bowler_id = player_ids.get(bowler_name)
                    non_striker_id = player_ids.get(non_striker_name)
                    
                    runs = delivery_data.get('runs', {})
                    extras = delivery_data.get('extras', {})
                    
                    # Get first extra type and value if exists
                    extra_type = None
                    extra_value = None
                    if extras:
                        extra_type = next(iter(extras.keys()), None)
                        extra_value = extras.get(extra_type)
                    
                    # Insert delivery
                    cursor.execute("""
                        INSERT INTO delivery (
                            over_id, innings_id, delivery_number, batter_id, bowler_id, 
                            non_striker_id, runs_batter, runs_extras, runs_total, 
                            extras_type, extras_value
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, [
                        over_id,
                        innings_id,
                        delivery_num,
                        batter_id,
                        bowler_id,
                        non_striker_id,
                        runs.get('batter'),
                        runs.get('extras'),
                        runs.get('total'),
                        extra_type,
                        extra_value
                    ])
                    delivery_id = cursor.lastrowid
                    conn.commit()
                    
                    # Process wickets
                    wickets = delivery_data.get('wickets', [])
                    for wicket in wickets:
                        player_out_name = wicket.get('player_out')
                        player_out_id = player_ids.get(player_out_name)
                        
                        fielders = wicket.get('fielders', [])
                        fielder_id = None
                        if fielders:
                            fielder_name = fielders[0].get('name')
                            fielder_id = player_ids.get(fielder_name)
                        
                        cursor.execute("""
                            INSERT INTO wicket (
                                delivery_id, player_out_id, kind, fielder_id
                            ) VALUES (?, ?, ?, ?)
                        """, [
                            delivery_id,
                            player_out_id,
                            wicket.get('kind'),
                            fielder_id
                        ])
                    conn.commit()
                    
                    # Process replacements
                    replacements = delivery_data.get('replacements', {}).get('match', [])
                    for replacement in replacements:
                        player_in_name = replacement.get('in')
                        player_out_name = replacement.get('out')
                        team_name = replacement.get('team')
                        
                        player_in_id = player_ids.get(player_in_name)
                        player_out_id = player_ids.get(player_out_name)
                        team_id = team_ids.get(team_name)
                        
                        if player_in_id and player_out_id and team_id:
                            cursor.execute("""
                                INSERT INTO replacement (
                                    match_id, team_id, player_out_id, player_in_id, reason
                                ) VALUES (?, ?, ?, ?, ?)
                            """, [
                                match_id,
                                team_id,
                                player_out_id,
                                player_in_id,
                                replacement.get('reason')
                            ])
                    conn.commit()
                    
                    # Process reviews
                    review_data = delivery_data.get('review')
                    if review_data:
                        reviewed_by = review_data.get('by')
                        umpire = review_data.get('umpire')
                        batter_name = review_data.get('batter')
                        batter_id = player_ids.get(batter_name)
                        
                        cursor.execute("""
                            INSERT INTO review (
                                delivery_id, reviewed_by, umpire, batter_id, 
                                decision, type, is_umpires_call
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, [
                            delivery_id,
                            reviewed_by,
                            umpire,
                            batter_id,
                            review_data.get('decision'),
                            review_data.get('type'),
                            review_data.get('umpires_call', False)
                        ])
                    conn.commit()
        
        return True
    
    except Exception as e:
        print(f"Error processing match data: {e}")
        conn.rollback()
        return False

def ingest_json_file(conn, file_path):
    """Ingest a single JSON file into the database."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        success = process_match_data(conn, data)
        if success:
            print(f"Successfully ingested {os.path.basename(file_path)}")
            return True
        else:
            print(f"Failed to ingest {os.path.basename(file_path)}")
            return False
    
    except Exception as e:
        print(f"Error ingesting {file_path}: {e}")
        return False

def create_db():
    """Create the database and ingest all JSON files in the data folder."""
    # Create database and tables
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    
    # Ingest all JSON files in the data folder
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith('.json'):
            file_path = os.path.join(DATA_FOLDER, filename)
            ingest_json_file(conn, file_path)
    
    conn.close()
    print(f"Database created successfully at {DB_PATH}")

def update_db_with_new_files(conn, new_files_folder):
    """Update the database with new JSON files from a folder."""
    if not os.path.exists(new_files_folder):
        print(f"Folder {new_files_folder} does not exist")
        return
    
    # Get list of already processed files (from match table)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT created_date FROM match")
    existing_dates = {row[0] for row in cursor.fetchall()}
    
    # Process new files
    for filename in os.listdir(new_files_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(new_files_folder, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check if this match already exists (based on created date)
                created_date = data.get('meta', {}).get('created')
                if created_date and created_date in existing_dates:
                    print(f"Skipping {filename} (already in database)")
                    continue
                
                # Process new file
                success = ingest_json_file(conn, file_path)
                if success:
                    print(f"Added new match from {filename}")
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    conn.commit()

if __name__ == "__main__":
    # Create the database if it doesn't exist
    if not os.path.exists(DB_PATH):
        create_db()
    
    # Connect to the database for potential updates
    conn = sqlite3.connect(DB_PATH)
    
    # Example of how to update with new files (provide the folder path)
    # new_files_folder = "path/to/new/files"
    # update_db_with_new_files(conn, new_files_folder)
    
    conn.close()
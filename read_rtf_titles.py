from striprtf.striprtf import rtf_to_text
import os
import sqlite3
from datetime import datetime

def init_database():
    """Initialize SQLite database and create table if not exists"""
    conn = sqlite3.connect('rtf_titles.db')
    cursor = conn.cursor()
    
    # Drop existing table if it exists (to update schema)
    cursor.execute('DROP TABLE IF EXISTS rtf_files')
    
    cursor.execute('''
        CREATE TABLE rtf_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            title TEXT,
            path TEXT NOT NULL,
            file_created_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(path, filename, title)
        )
    ''')
    conn.commit()
    return conn

def read_repository_file(repo_file="repository.txt"):
    """Read the list of RTF file paths from repository.txt"""
    with open(repo_file, 'r') as f:
        return [line.strip() for line in f.readlines()]

def get_file_timestamp(file_path):
    """Get file's last modification time as a formatted timestamp"""
    try:
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except OSError:
        return None

def extract_title_from_rtf(rtf_path):
    """Extract title from RTF file"""
    try:
        with open(rtf_path, 'r', encoding='utf-8') as file:
            rtf_content = file.read()
            # Convert RTF to plain text
            plain_text = rtf_to_text(rtf_content)
            
            # Get the first non-empty line as title
            lines = plain_text.split('\n')
            title = next((line.strip() for line in lines if line.strip()), "No title found")
            
            return title
    except FileNotFoundError:
        return f"Error: File not found - {rtf_path}"
    except Exception as e:
        return f"Error processing {rtf_path}: {str(e)}"

def save_to_database(conn, filename, title, path, file_created_at):
    """Save file and title information to database"""
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO rtf_files (filename, title, path, file_created_at)
            VALUES (?, ?, ?, ?)
        ''', (filename, title, path, file_created_at))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Skipping duplicate entry for file: {filename}")
        return False

def display_database_contents(conn):
    """Display all records from the database"""
    cursor = conn.cursor()
    cursor.execute('SELECT filename, title, path, file_created_at, created_at FROM rtf_files')
    rows = cursor.fetchall()
    
    print("\nDatabase Contents:")
    print("-" * 50)
    for row in rows:
        print(f"\nFilename: {row[0]}")
        print(f"Title: {row[1]}")
        print(f"Path: {row[2]}")
        print(f"File Last Modified: {row[3]}")
        print(f"Record Created at: {row[4]}")

def main():
    # Initialize database
    conn = init_database()
    
    # Read RTF file paths from repository.txt
    rtf_files = read_repository_file()
    
    print("Extracting titles from RTF files and saving to database:")
    print("-" * 50)
    
    for rtf_path in rtf_files:
        title = extract_title_from_rtf(rtf_path)
        filename = os.path.basename(rtf_path)
        path = os.path.dirname(rtf_path)
        file_created_at = get_file_timestamp(rtf_path)
        
        print(f"\nProcessing: {filename}")
        print(f"Path: {path}")
        print(f"Title: {title}")
        print(f"File Last Modified: {file_created_at}")
        
        # Save to database
        if save_to_database(conn, filename, title, path, file_created_at):
            print("Successfully saved to database")
    
    # Display all records from database
    display_database_contents(conn)
    
    # Close database connection
    conn.close()

if __name__ == "__main__":
    main() 
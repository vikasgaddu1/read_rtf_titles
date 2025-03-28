import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import io

def connect_to_db():
    """Create a connection to the SQLite database"""
    return sqlite3.connect('rtf_titles.db')

def search_database(conn, search_term, search_by):
    """Search the database based on the search term and field"""
    cursor = conn.cursor()
    
    # Create the WHERE clause based on search_by
    if search_by == "All Fields":
        query = '''
            SELECT filename, title, path, file_created_at, created_at 
            FROM rtf_files 
            WHERE filename LIKE ? 
            OR title LIKE ? 
            OR path LIKE ?
        '''
        params = [f"%{search_term}%"] * 3
    else:
        field_map = {
            "Filename": "filename",
            "Title": "title",
            "Path": "path"
        }
        query = f'''
            SELECT filename, title, path, file_created_at, created_at 
            FROM rtf_files 
            WHERE {field_map[search_by]} LIKE ?
        '''
        params = [f"%{search_term}%"]
    
    cursor.execute(query, params)
    return cursor.fetchall()

def create_results_dataframe(results):
    """Convert results to a pandas DataFrame with formatted columns"""
    df = pd.DataFrame(
        results,
        columns=['Filename', 'Title', 'Path', 'Last Modified', 'Record Created']
    )
    return df

def main():
    st.title("RTF Files Database Search")
    st.write("Search through the database of RTF files and their titles")
    
    # Create a connection to the database
    conn = connect_to_db()
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("Enter search term")
    
    with col2:
        search_by = st.selectbox(
            "Search by",
            ["All Fields", "Filename", "Title", "Path"]
        )
    
    # Add a search button
    if st.button("Search"):
        if search_term:
            results = search_database(conn, search_term, search_by)
            
            if results:
                st.write(f"Found {len(results)} results:")
                
                # Convert results to DataFrame and display as table
                df = create_results_dataframe(results)
                
                # Add styling and display the dataframe
                st.dataframe(
                    df,
                    column_config={
                        "Filename": st.column_config.TextColumn(
                            "Filename",
                            width="medium",
                            help="Name of the RTF file",
                            max_chars=50  # Show first 50 chars with ellipsis
                        ),
                        "Title": st.column_config.TextColumn(
                            "Title",
                            width="large",
                            help="Title extracted from the RTF file",
                            max_chars=None  # Allow full text with wrapping
                        ),
                        "Path": st.column_config.TextColumn(
                            "Path",
                            width="medium",
                            help="File location",
                            max_chars=50  # Show first 50 chars with ellipsis
                        ),
                        "Last Modified": st.column_config.DatetimeColumn(
                            "Last Modified",
                            format="DD-MM-YYYY HH:mm:ss"
                        ),
                        "Record Created": st.column_config.DatetimeColumn(
                            "Record Created",
                            format="DD-MM-YYYY HH:mm:ss"
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    height=400  # Fixed height with scrolling
                )
                
                # Add export buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "Download as CSV",
                        df.to_csv(index=False).encode('utf-8'),
                        "rtf_search_results.csv",
                        "text/csv",
                        key='download-csv'
                    )
                with col2:
                    # Fix for Excel export
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    st.download_button(
                        "Download as Excel",
                        buffer.getvalue(),
                        "rtf_search_results.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key='download-excel'
                    )
            else:
                st.warning("No results found")
        else:
            st.warning("Please enter a search term")
    
    # Display all records option
    if st.button("Show All Records"):
        cursor = conn.cursor()
        cursor.execute('SELECT filename, title, path, file_created_at, created_at FROM rtf_files')
        results = cursor.fetchall()
        
        if results:
            st.write(f"Total Records: {len(results)}")
            
            # Convert results to DataFrame and display as table
            df = create_results_dataframe(results)
            
            # Add styling and display the dataframe
            st.dataframe(
                df,
                column_config={
                    "Filename": st.column_config.TextColumn(
                        "Filename",
                        width="medium",
                        help="Name of the RTF file",
                        max_chars=50  # Show first 50 chars with ellipsis
                    ),
                    "Title": st.column_config.TextColumn(
                        "Title",
                        width="large",
                        help="Title extracted from the RTF file",
                        max_chars=None  # Allow full text with wrapping
                    ),
                    "Path": st.column_config.TextColumn(
                        "Path",
                        width="medium",
                        help="File location",
                        max_chars=50  # Show first 50 chars with ellipsis
                    ),
                    "Last Modified": st.column_config.DatetimeColumn(
                        "Last Modified",
                        format="DD-MM-YYYY HH:mm:ss"
                    ),
                    "Record Created": st.column_config.DatetimeColumn(
                        "Record Created",
                        format="DD-MM-YYYY HH:mm:ss"
                    )
                },
                hide_index=True,
                use_container_width=True,
                height=400  # Fixed height with scrolling
            )
        else:
            st.warning("No records found in the database")
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main() 
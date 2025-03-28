# RTF Titles Database

A Python application that extracts titles from RTF files, stores them in a SQLite database, and provides a Streamlit web interface for searching and viewing the data.

## Features

- Extracts titles from RTF files
- Stores file information in SQLite database including:
  - Filename
  - Title
  - File path
  - File last modified date
  - Record creation date
- Streamlit web interface for:
  - Searching files by filename, title, or path
  - Viewing all records in a table format
  - Exporting results to CSV or Excel

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd rtf-titles
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Add RTF file paths to `repository.txt`, one path per line:
```
C:\path\to\your\file1.rtf
C:\path\to\your\file2.rtf
```

2. Run the title extraction script:
```bash
python read_rtf_titles.py
```

3. Launch the Streamlit web interface:
```bash
streamlit run streamlit_app.py
```

## Project Structure

- `read_rtf_titles.py`: Main script for extracting titles and populating database
- `streamlit_app.py`: Web interface for searching and viewing database
- `repository.txt`: List of RTF file paths to process
- `requirements.txt`: Python package dependencies
- `.gitignore`: Git ignore configuration

## Dependencies

- Python 3.x
- striprtf==0.0.26
- streamlit==1.32.0
- pandas==2.2.0
- openpyxl==3.1.2

## Database Schema

The SQLite database (`rtf_titles.db`) contains a single table with the following structure:

```sql
CREATE TABLE rtf_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    title TEXT,
    path TEXT NOT NULL,
    file_created_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(path, filename, title)
)
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
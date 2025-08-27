# Risk Stratification Project - SQLite3 Database Setup

This project has been configured to use SQLite3 as the database backend, which is lightweight, serverless, and perfect for development and small to medium-scale applications.

## Database Configuration

The project uses SQLite3 with the following configuration:
- **Database URL**: `sqlite:///risk_data.db`
- **Database File**: `risk_data.db` (created automatically in the project root)
- **ORM**: SQLAlchemy

## Setup Instructions

### 1. Install Dependencies

Make sure you have all required dependencies installed:

```bash
pip install -r requirements.txt
```

### 2. Set Up the Database

Run the database setup script to create tables from your CSV data:

```bash
python setup_database.py
```

This script will:
- Look for CSV files in the `data/` directory
- Create SQLite tables from each CSV file
- Verify the database setup

### 3. Verify Database Setup

You can check the database status anytime:

```python
from risk.db import get_engine
import pandas as pd

engine = get_engine()
# List all tables
with engine.connect() as conn:
    result = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in result.fetchall()]
    print(f"Tables: {tables}")
```

## Database Functions

The following functions are available in `risk/db.py`:

### Core Functions
- `load_data_from_db(table_name)`: Load data from a specific table
- `load_patient_data()`: Load patient data with fallback to CSV
- `update_predictions_in_db(df, table_name)`: Update predictions for individual records
- `update_predictions_in_db_bulk(df, table_name)`: Bulk update predictions
- `ensure_prediction_columns(table_name)`: Add prediction columns if missing
- `create_table_from_csv(csv_path, table_name)`: Create table from CSV file

### Usage Examples

```python
from risk.db import load_data_from_db, update_predictions_in_db

# Load training data
df = load_data_from_db("beneficiary")

# Update predictions
update_predictions_in_db(predictions_df, "beneficiary")
```

## Running the Project

### Training
```bash
python train.py
```

### Prediction
```bash
python predict.py
```

## Database Schema

The database expects the following prediction columns to be added automatically:
- `RISK_30D`: 30-day risk score (integer)
- `RISK_60D`: 60-day risk score (integer)
- `RISK_90D`: 90-day risk score (integer)
- `RISK_LABEL`: Risk category (text)
- `TOP_3_FEATURES`: Top 3 contributing features (text)

## Advantages of SQLite3

1. **No Server Required**: SQLite is serverless and file-based
2. **Zero Configuration**: No database server setup needed
3. **Portable**: Database file can be easily backed up or moved
4. **ACID Compliant**: Full transaction support
5. **Python Integration**: Excellent support through SQLAlchemy

## Troubleshooting

### Database File Not Found
If you get errors about the database file not existing:
1. Run `python setup_database.py` to create the database
2. Ensure you have CSV files in the `data/` directory

### Table Not Found
If you get "table not found" errors:
1. Check that your CSV files are in the `data/` directory
2. Run the setup script again
3. Verify table names match what your code expects

### Permission Errors
Ensure your application has write permissions in the project directory for creating the SQLite database file.

## Migration from PostgreSQL

If you were previously using PostgreSQL:
1. The database URL has been changed to SQLite3
2. All database functions have been updated for SQLite compatibility
3. No additional configuration is needed
4. Your existing CSV data will be imported automatically

## Backup and Maintenance

### Backup Database
```bash
cp risk_data.db risk_data_backup.db
```

### Reset Database
```bash
rm risk_data.db
python setup_database.py
```

## Performance Considerations

- SQLite3 is suitable for datasets up to several GB
- For larger datasets, consider using PostgreSQL or other server databases
- SQLite3 performs well for read-heavy workloads
- Write performance is good for moderate concurrent access

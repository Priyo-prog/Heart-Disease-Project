from pathlib import Path
import psycopg2
from omegaconf import OmegaConf
import csv

# Current directory
current_directory = Path().absolute()

# data directory
data_directory = current_directory/"Data"

config = OmegaConf.load(Path("config.yaml"))

# Establish a connection
conn = psycopg2.connect(host=config.database_conn.host, 
                       port=config.database_conn.port, 
                       database=config.database_conn.database,
                       user=config.database_conn.user,
                       password=config.database_conn.password)

# Create cursor to execute SQL
cursor = conn.cursor()

# Create table if not exist
create_table_query = f"""CREATE TABLE IF NOT EXISTS {config.db_tab_name}
                            (age varchar(10), sex varchar(10), cp varchar(10), restbp varchar(10),
                            chol varchar(10), fbs varchar(10), restecg varchar(10), 
                            thalach varchar(10), exang varchar(10), oldpeak varchar(10), 
                            slope varchar(10), ca varchar(10), thal varchar(10), hd varchar(10))"""

cursor.execute(create_table_query)
conn.commit()

# Record any update in csv file in the database

with open(Path(f"{data_directory}/heart_disease.csv")) as file:
    reader = csv.reader(file)
    next(reader) # Skip the header row if it exist

    # Insert each row from csv into the POSTGRE SQL table
    for row in reader:
        insert_query = f"""INSERT INTO {config.db_tab_name} 
                   (age, sex, cp, restbp,
                    chol, fbs, restecg, 
                    thalach, exang, oldpeak, 
                    slope, ca, thal, hd ) VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(insert_query, row)
        conn.commit()

# Close the database connection        
cursor.close()
conn.close()




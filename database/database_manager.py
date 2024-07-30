# from sexy_logger import logger
import tracker_config as tkc
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import os
import shutil
from logger_setup import logger

user_dir = os.path.expanduser('~')
db_path = os.path.join(os.getcwd(), tkc.DB_NAME)  # Database Name
target_db_path = os.path.join(user_dir, tkc.DB_NAME)  # Database Name


def initialize_database():
    try:
        if not os.path.exists(target_db_path):
            if os.path.exists(db_path):
                shutil.copy(db_path, target_db_path)
            else:
                db = QSqlDatabase.addDatabase('QSQLITE')
                db.setDatabaseName(target_db_path)
                if not db.open():
                    logger.error("Error: Unable to create database")
                db.close()
    except Exception as e:
        logger.error("Error: Unable to create database", str(e))


class DataManager:
    
    def __init__(self,
                 db_name=target_db_path):
        try:
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(db_name)
            
            if not self.db.open():
                logger.error("Error: Unable to open database")
            logger.info("DB INITIALIZING")
            self.query = QSqlQuery()
            self.setup_tables()
        except Exception as e:
            logger.error(f"Error: Unable to open database {e}", exc_info=True)
    
    def setup_tables(self):
        self.setup_sleep_table()
        self.setup_total_hours_slept_table()
        self.setup_woke_up_like_table()
        self.setup_sleep_quality_table()
        self.setup_shower()
        self.setup_exercise()
        self.setup_teethbrush()
        self.setup_diet_table()
        self.setup_hydration_table()
    
    def setup_diet_table(self):
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS diet_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        diet_date TEXT,
                        diet_time TEXT,
                        food_eaten TEXT,
                        calories INTEGER
                        )"""):
            logger.error(f"Error creating table: diet_table", self.query.lastError().text())
    
    def insert_into_diet_table(self,
                               diet_date,
                               diet_time,
                               food_eaten,
                               calories):
        
        sql = f"""INSERT INTO diet_table(diet_date, diet_time, food_eaten, calories) VALUES
                (?, ?, ?, ?)"""
        
        bind_values = [diet_date, diet_time, food_eaten, calories]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"Mismatch: diet_table Expected {sql.count('?')} bind values, got "
                                 f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(f"Error inserting data: diet_table - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError diet_table: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: diet_table", str(e))
    
    def setup_hydration_table(self):
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS hydration_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        diet_date TEXT,
                        diet_time TEXT,
                        hydration INTEGER
                        )"""):
            logger.error(f"Error creating table: hydration_table", self.query.lastError().text())
        
        # database_manager.py
    
    def insert_into_hydration_table(self,
                                    diet_date,
                                    diet_time,
                                    hydration):
        sql = """INSERT INTO hydration_table(diet_date, diet_time, hydration) VALUES (?, ?, ?)"""
        
        bind_values = [diet_date, diet_time, hydration]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"Mismatch: hydration_table Expected {sql.count('?')} bind values, got {len(bind_values)}.")
            if not self.query.exec():
                logger.error(f"Error inserting data: hydration_table - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError hydration_table: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: hydration_table", str(e))
        
        # -:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-
        # SLEEP table
        # -:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-
    
    def setup_shower(self) -> None:
        if not self.query.exec(f"""
                                CREATE TABLE IF NOT EXISTS shower_table (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                basics_date TEXT,
                                basics_time TEXT,
                                shower_check BOOL
                                )"""):
            logger.error(f"Error creating table: shower_table", self.query.lastError().text())
    
    def insert_into_shower_table(self,
                                 basics_date: str,
                                 basics_time: str,
                                 shower_check: int) -> None:
        
        sql: str = f"""INSERT INTO shower_table(basics_date, basics_time,
                shower_check) VALUES (?, ?, ?)"""
        
        bind_values: List[Union[str, bool]] = [basics_date, basics_time,
                                               shower_check]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: shower_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: shower_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError shower_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: shower_table {e}", exc_info=True)
    
    def setup_exercise(self) -> None:
        if not self.query.exec(f"""
                                CREATE TABLE IF NOT EXISTS exercise_table (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                basics_date TEXT,
                                basics_time TEXT,
                                exerc_check BOOL
                                )"""):
            logger.error(f"Error creating table: exercise_table", self.query.lastError().text())
    
    def insert_into_exercise_table(self,
                                   basics_date: str,
                                   basics_time: str,
                                   exerc_check: int) -> None:
        
        sql: str = f"""INSERT INTO exercise_table(basics_date, basics_time,
                exerc_check) VALUES (?, ?, ?)"""
        
        bind_values: List[Union[str, bool]] = [basics_date, basics_time,
                                               exerc_check]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: exercise_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: exercise_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError exercise_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: exercise_table {e}", exc_info=True)
        
        # Teethbrushing Table
    
    def setup_teethbrush(self) -> None:
        if not self.query.exec(f"""
                                CREATE TABLE IF NOT EXISTS tooth_table (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                basics_date TEXT,
                                basics_time TEXT,
                                tooth_check BOOL
                                )"""):
            logger.error(f"Error creating table: tooth_table", self.query.lastError().text())
    
    def insert_into_tooth_table(self,
                                basics_date: str,
                                basics_time: str,
                                tooth_check: int) -> None:
        
        sql: str = f"""INSERT INTO tooth_table(basics_date, basics_time,
                tooth_check) VALUES (?, ?, ?)"""
        
        bind_values: List[Union[str, bool]] = [basics_date, basics_time,
                                               tooth_check]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: tooth_table Expected {sql.count('?')}
                            bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: tooth_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError tooth_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: tooth_table {e}", exc_info=True)
    
    # SLEEP TIMES TABLE 
    def setup_sleep_table(self):
        if not self.query.exec(f"""
                CREATE TABLE IF NOT EXISTS sleep_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sleep_date TEXT,
                time_asleep TEXT,
                time_awake TEXT
                )"""):
            logger.error(f"Error creating table: sleep_table", self.query.lastError().text())
    
    def insert_into_sleep_table(self,
                                sleep_date,
                                time_asleep,
                                time_awake):
        sql = f"""INSERT INTO sleep_table(sleep_date, time_asleep, time_awake) VALUES (?, ?, ?)"""
        bind_values = [sleep_date, time_asleep, time_awake]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: sleep_table Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: sleep_table - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError sleep_table: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: sleep_table", str(e))
    
    # -:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-
    # BASICS table
    # -:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-
    def setup_total_hours_slept_table(self):
        if not self.query.exec(f"""
                CREATE TABLE IF NOT EXISTS total_hours_slept_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                sleep_date TEXT,
                total_hours_slept TEXT                                
                )"""):
            logger.error(f"Error creating table: total_hours_slept", self.query.lastError().text())
    
    def insert_into_total_hours_slept_table(self,
                                            sleep_date,
                                            total_hours_slept):
        # Prepare the SQL statement
        sql = f"""INSERT INTO total_hours_slept_table(sleep_date, total_hours_slept) VALUES (?, ?)"""
        bind_values = [sleep_date, total_hours_slept]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: total_hours_slept Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: total_hours_slept - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError total_hours_slept: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: total_hours_slept", str(e))
    
    def setup_woke_up_like_table(self):
        if not self.query.exec(f"""
                CREATE TABLE IF NOT EXISTS woke_up_like_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sleep_date TEXT,
                woke_up_like TEXT
                )"""):
            logger.error(f"Error creating table: woke_up_like", self.query.lastError().text())
    
    def insert_woke_up_like_table(self,
                                  sleep_date,
                                  woke_up_like):
        # Prepare the SQL statement
        sql = f"""INSERT INTO woke_up_like_table(sleep_date, woke_up_like) VALUES (?, ?)"""
        bind_values = [sleep_date, woke_up_like]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: woke_up_like Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: woke_up_like - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError woke_up_like: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: woke_up_like", str(e))
    
    def setup_sleep_quality_table(self):
        if not self.query.exec(f"""
                CREATE TABLE IF NOT EXISTS sleep_quality_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sleep_date TEXT,
                sleep_quality TEXT
                )"""):
            logger.error(f"Error creating table: sleep_quality", self.query.lastError().text())
    
    def insert_into_sleep_quality_table(self,
                                        sleep_date,
                                        sleep_quality):
        # Prepare the SQL statement
        sql = f"""INSERT INTO sleep_quality_table(sleep_date, sleep_quality) VALUES (?, ?)"""
        bind_values = [sleep_date, sleep_quality]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(
                    f"Mismatch: sleep_quality Expected {sql.count('?')} bind values, got "
                    f"{len(bind_values)}.")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: sleep_quality - {self.query.lastError().text()}")
        except ValueError as ve:
            logger.error(f"ValueError sleep_quality: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during data insertion: sleep_quality", str(e))


def close_database(self):
    try:
        logger.info("if database is open")
        if self.db.isOpen():
            logger.info("the database is closed successfully")
            self.db.close()
    except Exception as e:
        logger.exception(f"Error closing database: {e}")

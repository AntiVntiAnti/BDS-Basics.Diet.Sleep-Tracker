import datetime
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QSettings, QTime, Qt, QByteArray, QDateTime
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QTextEdit, QPushButton, QDialog, QFormLayout, QLineEdit
from PyQt6.QtPrintSupport import QPrintDialog

import tracker_config as tkc

#############################################################################
# UI
from ui.main_ui.gui import Ui_MainWindow

#############################################################################
# LOGGER
#############################################################################
from logger_setup import logger

#############################################################################
# NAVIGATION
#############################################################################
from navigation.master_navigation import (
    change_stackedWidget_page, change_basics_page, )
#############################################################################
# UTILITY
#############################################################################
from utility.app_operations.diet_calc import (
    calculate_calories)
from utility.app_operations.save_generic import (
    TextEditSaver)

# Window geometry and frame
from utility.app_operations.frameless_window import (
    FramelessWindow)
from utility.app_operations.window_controls import (
    WindowController)
from utility.app_operations.current_date_highlighter import (
    DateHighlighter)
from utility.widgets_set_widgets.line_connections import (
    line_edit_times)

from utility.widgets_set_widgets.slider_timers import (
    connect_slider_timeedits)
from utility.widgets_set_widgets.buttons_set_time import (
    btn_times)

from utility.app_operations.show_hide import (
    toggle_views)

from utility.widgets_set_widgets.buttons_set_time import (
    btn_times)
from database.add_data.teethbrushing import (
    add_teethbrush_data)
from database.add_data.exercise import (
    add_exercise_data)
from database.add_data.shower import (
    add_shower_data)


##############################################################################
# DATABASE Magicks w/ Wizardry & Necromancy
##############################################################################
# Database connections
from database.database_manager import (
    DataManager)

# Delete Records
from database.database_utility.delete_records import (
    delete_selected_rows)

# setup Models
from database.database_utility.model_setup import (
    create_and_set_model)
# Add personal diet
from database.add_data.diet import add_diet_data
from database.add_data.hydration import add_hydration_data
# Basics add sleep and basics
from database.add_data.woke_up_like_data import add_woke_up_like_data
from database.add_data.total_hours_slept import add_total_hours_slept_data
from database.add_data.sleep_data import add_sleep_data
from database.add_data.sleep_quality_data import add_sleep_quality_data


class MainWindow(FramelessWindow, QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.sleep_quality_model = None
        self.woke_up_like_model = None
        self.sleep_model = None
        self.total_hours_slept_model = None
        self.total_hrs_slept = None
        self.basics_model = None
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        # Database init
        self.db_manager = DataManager()
        self.setup_models()
        # QSettings settings_manager setup
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
        self.window_controller = WindowController()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.restore_state()
        self.app_operations()
        self.auto_datetime()
        self.calculate_total_hours_slept()
        self.stack_navigation()
        self.delete_actions()
        self.sleep_commit()
        self.total_hours_commit()
        self.woke_up_like_commit()
        self.sleep_quality_commit()
        self.switch_to_page1()
        self.diet_data_commit()
        self.shower_commit()
        self.exercise_commit()
        self.teethbrush_commit()
        self.init_hydration_tracker()
        
    def init_hydration_tracker(self):
        try:
            self.eight_ounce_cup.clicked.connect(lambda: self.commit_hydration(8))
            self.sixteen_ounce_cup.clicked.connect(lambda: self.commit_hydration(16))
            self.twenty_four_ounce_cup.clicked.connect(lambda: self.commit_hydration(24))
            self.thirty_two_ounce_cup.clicked.connect(lambda: self.commit_hydration(32))
        except Exception as e:
            logger.error(f"Error initializing hydration tracker buttons: {e}", exc_info=True)
   
    def switch_to_page1(self):
        """
        Makes certain that when returning to the input page the size of the page shrinks to not
        look like a beached whale with three oddly specific shaped eyes. Or something. ITs better.
        """
        self.basics_stack.setCurrentWidget(self.input)
        self.resize(300, 270)
        self.setFixedSize(300, 270)
    
    def switch_to_page2(self):
        """
        MAKES IT FAT like a beached whale except I don't know why I said beached whale for I love
        whales and all animals so having the thought of one beached is sad and thus I suck.
        Anywho
        This makes it so when navvy'atin' towards thems data showers called QTableViews :D it
        blows itself the DUBMOS up like the Elephant dumbo, that wasn't a real elephant or was
        it? I don't know. Maybe Disney took some liberties WOULD not be the first nor last?
        heheh.
        """
        self.basics_stack.setCurrentWidget(self.sleepPage)
        self.setMaximumSize(540, 540)
        self.setFixedSize(540, 540)
    
    def switch_to_page3(self):
        """
        MAKES IT FAT like a beached whale except I don't know why I said beached whale for I love
        whales and all animals so having the thought of one beached is sad and thus I suck.
        Anywho
        This makes it so when navvy'atin' towards thems data showers called QTableViews :D it
        blows itself the DUBMOS up like the Elephant dumbo, that wasn't a real elephant or was
        it? I don't know. Maybe Disney took some liberties WOULD not be the first nor last?
        heheh.
        """
        self.basics_stack.setCurrentWidget(self.dietPage)
        self.setMaximumSize(800, 540)
        self.setFixedSize(800, 540)
    
    def switch_to_page4(self):
        """
        MAKES IT FAT like a beached whale except I don't know why I said beached whale for I love
        whales and all animals so having the thought of one beached is sad and thus I suck.
        Anywho
        This makes it so when navvy'atin' towards thems data showers called QTableViews :D it
        blows itself the DUBMOS up like the Elephant dumbo, that wasn't a real elephant or was
        it? I don't know. Maybe Disney took some liberties WOULD not be the first nor last?
        heheh.
        """
        self.basics_stack.setCurrentWidget(self.basicsPage)
        self.setMaximumSize(540, 540)
        self.setFixedSize(540, 540)
        
    def auto_datetime(self) -> None:
        try:
            self.diet_time.setTime(QTime.currentTime())
            self.diet_date.setDate(QDate.currentDate())
            self.sleep_date.setDate(QDate.currentDate())
            self.sleep_time.setTime(QTime.currentTime())
            self.basics_date.setDate(QDate.currentDate())
            self.basics_time.setTime(QTime.currentTime())
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    ##########################################################################################
    # APP-OPERATIONS setup
    ##########################################################################################
    def app_operations(self):
        try:
            self.basics_stack.currentChanged.connect(self.on_page_changed)
            self.basics_stack.currentChanged.connect(self.on_page_changed)
            self.hide_check_frame.setVisible(False)
            last_index = self.settings.value("lastPageIndex", 0, type=int)
            self.basics_stack.setCurrentIndex(last_index)
            self.actionTotalHours.triggered.connect(self.calculate_total_hours_slept)
            last_index = self.settings.value("lastPageIndex", 0, type=int)
            self.basics_stack.setCurrentIndex(last_index)
        except Exception as e:
            logger.error(f"Error occurred while setting up app_operations : {e}", exc_info=True)
    
    def commits_set_times(self):
        self.btn_times = {
            self.shower_c: self.basics_time, self.exercise_commit: self.basics_time,
            self.teethbrush_commit: self.basics_time,
        }
        
        # Connect lineEdits to the centralized function
        for app_btns, times_edit in self.btn_times.items():
            btn_times(app_btns, times_edit)
        
        #########################################################################
        # UPDATE TIME support
        #########################################################################
    @staticmethod
    def update_time(state,
                    time_label):
        try:
            if state == 2:  # checked state
                current_time = QTime.currentTime()
                time_label.setTime(current_time)
        except Exception as e:
            logger.error(f"Error updating time. {e}", exc_info=True)
    
    def on_page_changed(self,
                        index):
        """
        Callback method triggered when the page is changed in the UI.

        Args:
            index (int): The index of the new page.
        """
        self.settings.setValue("lastPageIndex", index)
    
    def calculate_total_hours_slept(self) -> None:
        """
        Calculates the total hours slept based on the awake time and asleep time.

        This method calculates the total hours slept by subtracting the awake time from the
        asleep time.
        If the time spans past midnight, it adds 24 hours worth of minutes to the total.
        The result is then converted to hours and minutes and displayed in the
        total_hours_slept_lineedit.

        Raises:
            Exception: If an error occurs while calculating the total hours slept.

        """
        
        try:
            time_asleep = self.time_awake.time()
            time_awake = self.time_asleep.time()
            
            # Convert time to total minutes since the start of the day
            minutes_asleep = (time_asleep.hour() * 60 + time_asleep.minute())
            minutes_awake = (time_awake.hour() * 60 + time_awake.minute())
            
            # Calculate the difference in minutes
            total_minutes = minutes_asleep - minutes_awake
            
            # Handle case where the time spans past midnight
            if total_minutes < 0:
                total_minutes += (24 * 60)  # Add 24 hours worth of minutes
            
            # Convert back to hours and minutes
            hours = total_minutes // 60
            minutes = total_minutes % 60
            
            # Create the total_hours_slept string in HH:mm format
            self.total_hrs_slept = f"{hours:02}:{minutes:02}"
            
            # Update the lineEdit with the total hours slept
            self.total_hours_slept.setText(self.total_hrs_slept)
        
        except Exception as e:
            logger.error(f"Error occurred while calculating total hours slept {e}", exc_info=True)
    
    #############################################################################################
    # Agenda Journal Navigation
    #############################################################################################
    def stack_navigation(self):
        self.actionShowPageOne.triggered.connect(lambda: change_stackedWidget_page(self.basics_stack, 0))
        self.actionShowBasicsData.triggered.connect(lambda: change_stackedWidget_page(self.basics_stack, 1))
        self.actionShowSleepData.triggered.connect(lambda: change_stackedWidget_page(self.basics_stack, 2))
        self.actionShowDietData.triggered.connect(lambda: change_stackedWidget_page(self.basics_stack, 3))
        self.actionShowPageOne.triggered.connect(self.switch_to_page1)
        self.actionShowBasicsData.triggered.connect(self.switch_to_page4)
        self.actionShowSleepData.triggered.connect(self.switch_to_page2)
        self.actionShowDietData.triggered.connect(self.switch_to_page3)
    
    # SLEEP COMMIT
    #######################################################################################
    def sleep_commit(self):
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_sleep_data(self, {
                "sleep_date": "sleep_date", "time_asleep": "time_asleep", "time_awake":
                    "time_awake", "model": "sleep_model",
            },
                                                                             self.db_manager.insert_into_sleep_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def total_hours_commit(self):
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_total_hours_slept_data(self, {
                "sleep_date": "sleep_date", "total_hours_slept": "total_hours_slept", "model":
                    "total_hours_slept_model",
            },
                                                                             self.db_manager.insert_into_total_hours_slept_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def woke_up_like_commit(self):
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_woke_up_like_data(self, {
                "sleep_date": "sleep_date", "woke_up_like": "woke_up_like", "model":
                    "woke_up_like_model",
            },
                                                                             self.db_manager.insert_woke_up_like_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def sleep_quality_commit(self):
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_sleep_quality_data(self, {
                "sleep_date": "sleep_date", "sleep_quality": "sleep_quality", "model":
                    "sleep_quality_model",
            },
                                                                             self.db_manager.insert_into_sleep_quality_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    # MY DIET Commit Method
    #########################################################################
    def diet_data_commit(self):
        try:
            self.actionCommitDiet.triggered.connect(lambda: add_diet_data(self, {
                "diet_date": "diet_date", "diet_time": "diet_time", "food_eaten": "food_eaten",
                "calories": "calories", "model": "diet_model",
            }, self.db_manager.insert_into_diet_table, ))
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    def commit_hydration(self,
                         amount):
        try:
            date = QDate.currentDate().toString("yyyy-MM-dd")
            time = QTime.currentTime().toString("hh:mm:ss")
            self.db_manager.insert_into_hydration_table(date, time, amount)
            logger.info(f"Committed {amount} oz of water at {date} {time}")
            self.hydro_model.select()
        except Exception as e:
            logger.error(f"Error committing hydration data: {e}", exc_info=True)
    
    def shower_commit(self):
        try:
            self.shower_c.clicked.connect(lambda: add_shower_data(self, {
                "basics_date": "basics_date", "basics_time": "basics_time",
                "shower_check": "shower_check", "model": "shower_model",
            },
                                                                  self.db_manager.insert_into_shower_table, ))
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
    
    def exercise_commit(self):
        
        self.yoga_commit.clicked.connect(lambda: add_exercise_data(self, {
            "basics_date": "basics_date", "basics_time": "basics_time",
            "exerc_check": "exerc_check", "model": "exercise_model",
        }, self.db_manager.insert_into_exercise_table, ))
    
    def teethbrush_commit(self):
        self.teeth_commit.clicked.connect(lambda: add_teethbrush_data(self, {
            "basics_date": "basics_date", "basics_time": "basics_time",
            "tooth_check": "tooth_check", "model": "tooth_model",
        }, self.db_manager.insert_into_tooth_table, ))
        
    def delete_actions(self):
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'sleep_tableview',
                'sleep_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'total_hours_slept_tableview',
                'total_hours_slept_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'woke_up_like_tableview',
                'woke_up_like_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'sleep_quality_tableview',
                'sleep_quality_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'shower_table',
                'shower_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'teethbrushed_table',
                'tooth_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'yoga_table',
                'exercise_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'diet_table',
                'diet_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'hydration_table',
                'hydro_model'
            )
        )
    
    def setup_models(self) -> None:
        try:
            self.sleep_model = create_and_set_model(
                "sleep_table",
                self.sleep_tableview
            )
            self.total_hours_slept_model = create_and_set_model(
                "total_hours_slept_table",
                self.total_hours_slept_tableview)
            self.woke_up_like_model = create_and_set_model(
                "woke_up_like_table",
                self.woke_up_like_tableview)
            self.sleep_quality_model = create_and_set_model(
                "sleep_quality_table",
                self.sleep_quality_tableview)
            self.shower_model = create_and_set_model(
                "shower_table",
                self.shower_table
            )
            # SLEEP: model creates and set
            self.tooth_model = create_and_set_model(
                "tooth_table",
                self.teethbrushed_table
            )
            self.exercise_model = create_and_set_model(
                "exercise_table",
                self.yoga_table
            )
            self.diet_model = create_and_set_model(
                "diet_table",
                self.diet_table
            )
            self.hydro_model = create_and_set_model(
                "hydration_table",
                self.hydration_table
            )
        except Exception as e:
            logger.error(f"Error setting up models: {e}", exc_info=True)
    
    def save_state(self):
        # save window geometry state
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
    
    def restore_state(self) -> None:
        
        try:
            # restore window geometry state
            self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring the minds module : stress state {e}")
        
        try:
            self.restoreState(self.settings.value("windowState", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring WINDOW STATE {e}", exc_info=True)
    
    def closeEvent(self,
                   event: QCloseEvent) -> None:
        try:
            self.save_state()
        except Exception as e:
            logger.error(f"error saving state during closure: {e}", exc_info=True)

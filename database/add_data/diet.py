from PyQt6.QtCore import QDate, QTime
from logger_setup import logger


def add_diet_data(main_window_instance, widget_names, db_insert_method):
    """
    Inserts diet data into the database.

    Parameters:
        main_window_instance (MainWindow): An instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets.
        db_insert_method (function): The method used to insert data into the database.

    Returns:
        None
    """
    try:
        widget_methods = {
            widget_names['diet_date']: (None, 'date', "yyyy-MM-dd"),
            widget_names['diet_time']: (None, 'time', "hh:mm:ss"),
            widget_names['food_eaten']: (None, 'text', ""),
            widget_names['calories']: (None, 'value', None),
            }
        
        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)
        
        db_insert_method(*data_to_insert)
        reset_diet_form(main_window_instance, widget_names)

    except Exception as e:
        logger.exception(f"Error occurred when adding diet data: {e}", exc_info=True)


def reset_diet_form(main_window_instance, widget_names):
    """
    Reset the diet form by setting the default values for all the input fields.

    Parameters:
        main_window_instance (object): The instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets.

    Returns:
        None
    """
    try:
        getattr(main_window_instance, widget_names['diet_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['diet_time']).setTime(QTime.currentTime())
        getattr(main_window_instance, widget_names['food_eaten']).clear()
        getattr(main_window_instance, widget_names['calories']).setValue(0)
        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()

    except Exception as e:
        logger.exception(f"Error occurred when resetting the diet form: {e}", exc_info=True)
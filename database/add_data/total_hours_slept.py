from PyQt6.QtCore import QDate, QTime
from logger_setup import logger


def add_total_hours_slept_data(main_window_instance, widget_names, db_insert_method):
    """
    Add sleep data to the database.

    Args:
        main_window_instance: An instance of the main window.
        widget_names: A dictionary containing names of the widgets.
        db_insert_method: A method to insert data into the database.

    Returns:
        None
    """
    try:
        widget_methods = {
            widget_names['sleep_date']: (None, 'date', 'yyyy-MM-dd'),
            widget_names['total_hours_slept']: (None, 'text', ''),
            }

        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)

        db_insert_method(*data_to_insert)
        reset_total_hours_slept(main_window_instance, widget_names)
    except Exception as e:
        logger.error(f"error while adding sleep data: {e}", exc_info=True)


def reset_total_hours_slept(main_window_instance, widget_names):
    """
    Reset the sleep form with default values.

    :param main_window_instance: An instance of the main window.
    :type main_window_instance: MainWindow

    :param widget_names: A dictionary containing the names of the widgets.
    :type widget_names: dict

    :return: None
    """
    try:
        # set date to today and time to
        getattr(main_window_instance, widget_names['sleep_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['total_hours_slept']).clear()        
        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"error while resetting sleep form: {e}", exc_info=True)

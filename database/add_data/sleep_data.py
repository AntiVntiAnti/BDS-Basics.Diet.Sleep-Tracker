from PyQt6.QtCore import QDate, QTime
from logger_setup import logger


def add_sleep_data(main_window_instance,
                   widget_names,
                   db_insert_method):
    try:
        # Log the widget_names dictionary to debug the issue
        logger.debug(f"widget_names: {widget_names}")
        
        # Ensure widget_names has the required keys
        required_keys = ['sleep_date', 'time_asleep', 'time_awake']
        for key in required_keys:
            if key not in widget_names:
                raise KeyError(f"Missing required key '{key}' in widget_names")
        
        widget_methods = {
            widget_names['sleep_date']: (None, 'date', 'yyyy-MM-dd'),
            widget_names['time_asleep']: (None, 'time', 'hh:mm:ss'),
            widget_names['time_awake']: (None, 'time', 'hh:mm:ss'),
        }
        
        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)
        
        db_insert_method(*data_to_insert)
        reset_time_asleep(main_window_instance, widget_names)
    except KeyError as ke:
        logger.error(f"Key error: {ke}")
    except Exception as e:
        logger.error(f"Error while adding sleep data: {e}", exc_info=True)


def reset_time_asleep(main_window_instance,
                      widget_names):
    try:
        # Ensure widget_names has the required keys
        required_keys = ['sleep_date', 'time_asleep', 'time_awake']
        for key in required_keys:
            if key not in widget_names:
                raise KeyError(f"Missing required key '{key}' in widget_names")
        
        # Set date to today and time to current time
        getattr(main_window_instance, widget_names['sleep_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['time_asleep']).setTime(QTime.currentTime())
        getattr(main_window_instance, widget_names['time_awake']).setTime(QTime.currentTime())
        
        # Assuming there is a model for each day
        if 'model' in widget_names:
            getattr(main_window_instance, widget_names['model']).select()
    except KeyError as ke:
        logger.error(f"Key error: {ke}")
    except Exception as e:
        logger.error(f"Error while resetting sleep form: {e}", exc_info=True)

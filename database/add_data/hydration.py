from PyQt6.QtCore import QDate, QTime
from logger_setup import logger


def add_hydration_data(main_window_instance,
                  widget_names,
                  db_insert_method):
    try:
        widget_methods = {
            widget_names['diet_date']: (None, 'date', "yyyy-MM-dd"),
            widget_names['diet_time']: (None, 'time', "hh:mm:ss"),
            widget_names['hydration']: (None, 'value', None),
        }
        
        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)
        
        db_insert_method(*data_to_insert)
        reset_hydration_form(main_window_instance, widget_names)
    
    except Exception as e:
        logger.exception(f"Error occurred when adding hydration data: {e}", exc_info=True)


def reset_hydration_form(main_window_instance,
                    widget_names):
    try:
        getattr(main_window_instance, widget_names['diet_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['diet_time']).setTime(QTime.currentTime())
        getattr(main_window_instance, widget_names['hydration']).setValue(0)
        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()
    
    except Exception as e:
        logger.exception(f"Error occurred when resetting the hydration form: {e}", exc_info=True)
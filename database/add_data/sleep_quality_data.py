from PyQt6.QtCore import QDate, QTime
from logger_setup import logger


def add_sleep_quality_data(main_window_instance,
                           widget_names,
                           db_insert_method):
    try:
        widget_methods = {
            widget_names['sleep_date']: (None, 'date', 'yyyy-MM-dd'),
            widget_names['sleep_quality']: (None, 'value', None),
        }
        
        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)
        
        db_insert_method(*data_to_insert)
        reset_sleep_quality(main_window_instance, widget_names)
    except Exception as e:
        logger.error(f"error while adding sleep data: {e}", exc_info=True)


def reset_sleep_quality(main_window_instance,
                        widget_names):
    
    try:
        # set date to today and time to
        getattr(main_window_instance, widget_names['sleep_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['sleep_quality']).setValue(0)
        
        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"error while resetting sleep form: {e}", exc_info=True)

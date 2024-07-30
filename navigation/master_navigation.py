# from sexy_logger import logger
from logger_setup import logger
from typing import Any


def change_diet_stack(diet_stack: Any,
                      index: int) -> None:
    """
    Change the current index of the alpha stack.

    Args:
    diet_stack (Any): The alpha stack object.
    index (int): The new index to set.

    Returns:
    None
    """
    try:
        diet_stack.setCurrentIndex(index)
        logger.info("Alpha Stack Page Change")
    except Exception as e:
        logger.error(f"Alpha Stack Page Change Error: {e}", exc_info=True)


def change_stackedWidget_page(basics_stack: Any, index: int) -> None:
    """
    Change the current index of the alpha stack.

    Args:
    stackedWidget (Any): The alpha stack object.
    index (int): The new index to set.

    Returns:
    None
    """
    try:
        basics_stack.setCurrentIndex(index)
        logger.info("Alpha Stack Page Change")
    except Exception as e:
        logger.error(f"Alpha Stack Page Change Error: {e}", exc_info=True)


def change_basics_page(sleep_basics_stack: Any, index: int) -> None:
    """
    Change the current page of the sleep basics stack.

    Args:
        sleep_basics_stack (Any): The sleep basics stack widget.
        index (int): The index of the page to change to.

    Returns:
        None

    Raises:
        Exception: If an error occurs while changing the page.

    """
    try:
        sleep_basics_stack.setCurrentIndex(index)
        logger.info("Basics Stack Page Change")
    except Exception as e:
        logger.error(f"Basics Stack Page Change Error: {e}", exc_info=True)


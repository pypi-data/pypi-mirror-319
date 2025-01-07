from . import UI
from epyk.core import Page

EXTENSION_NAME = "jqui"
""" Package extension's name """


def extend(page = None) -> UI.Components:
    """Extends Epyk Framework with more components.
    The returned object will be the interface for the new components.

    :param page: Page object.
    :return:
    """
    if not page:
        page = Page.Report()
    if EXTENSION_NAME not in page._props["fwks"]:
        page._props["fwks"][EXTENSION_NAME] = UI.Components(page)
    return page._props["fwks"][EXTENSION_NAME]

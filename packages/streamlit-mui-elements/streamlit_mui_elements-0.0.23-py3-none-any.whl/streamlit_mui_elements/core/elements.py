import json
import time
from streamlit import session_state, rerun

from streamlit_mui_elements.core.exceptions import ElementsFrameError
from streamlit_mui_elements.core.element import Element
from streamlit_mui_elements.core.render import render_component
from streamlit_mui_elements.core.events import start_event_server, event_store

ELEMENTS_FRAME_KEY = f"{__name__}.elements_frame"
RERUN_COOLDOWN = 0.1
RERUN_EVENT_TYPES = {'file-change', 'filter-change', 'sort-change', 'pagination-change', 'selection-change'}

class ElementsManager:
    def __init__(self, key):
        self.key = f"{ELEMENTS_FRAME_KEY}.{key}"
        self.frame = None
        # Start Flask server when ElementsManager is initialized
        if not hasattr(ElementsManager, '_event_server_started'):
            start_event_server()
            ElementsManager._event_server_started = True
    
    def __enter__(self):
        self.frame = ElementsFrame(self.key)
        session_state[ELEMENTS_FRAME_KEY] = self.frame
        self.frame.capture_children()
        return self.frame
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.frame:
                ui_tree = self.frame.to_dict()
                if ui_tree:
                    self._handle_component(ui_tree)
        except Exception as e:
            raise e
        finally:
            if ELEMENTS_FRAME_KEY in session_state:
                del session_state[ELEMENTS_FRAME_KEY]
    
    def _handle_component(self, ui_tree):
        ui_description = json.dumps(ui_tree)
        render_component(data=ui_description, key=self.key, default=None)
        print(f"rendered component {self.key}") 
        
def new_element(module, element):
    if ELEMENTS_FRAME_KEY not in session_state:
        raise ElementsFrameError("Cannot create element outside a frame.")
    return Element(session_state[ELEMENTS_FRAME_KEY], module, element)

def get_elements_frame():
    if ELEMENTS_FRAME_KEY not in session_state:
        raise ElementsFrameError("Frame was not created.")
    return session_state[ELEMENTS_FRAME_KEY]

class ElementsFrame:
    __slots__ = ('_children', '_parents', '_key', '_is_saving')

    def __init__(self, key):
        self._children = []
        self._parents = []
        self._key = key
        self._is_saving = False

    def capture_children(self):
        self._parents.append(self._children)
        self._children = []

    def save_children(self, element):
        if self._is_saving:
            raise RuntimeError("Reentrant save_children call detected.")

        if not self._parents:
            raise RuntimeError("save_children called without active context.")

        self._is_saving = True
        captured_children = self._children
        self._children = self._parents.pop()

        # Only process children that haven't been added to a parent yet
        filtered_children = []
        for child in captured_children:
            if not child._is_prop and not child._parent:
                child._parent = element
                filtered_children.append(child)

        if filtered_children:
            element(*filtered_children)

        # Only add the element if it's not a prop and doesn't have a parent
        if not element._is_prop and not element._parent and element not in self._children:
            self._children.append(element)

        captured_children.clear()
        self._is_saving = False

    def is_capturing_children(self):
        return len(self._parents) > 0

    def to_dict(self):
        result = [child.to_dict() for child in self._children]
        return result

import os
from .view import ViewCls, WorkflowCls
import time
from pycoze import utils


socket = utils.socket
params = utils.params

class TabCls:

    def open_workflow(self, workflow_id: str, wait_for_open) -> WorkflowCls:
        item_path = os.path.join(params["workspacePath"], 'workflow', workflow_id)
        if not os.path.isabs(item_path):
            item_path = os.path.abspath(item_path)
        location = ["FileOrDir", item_path]
        socket.post("add-tab", {"location": location, "name": "todo"})
        if wait_for_open:
            self._wait_for_tab_open(location)
        return WorkflowCls(location)
    
    def get_active(self) -> ViewCls:
        result = socket.post_and_recv_result("get-active-tab", {})
        return self._result_to_view(result)
    
    def _wait_for_tab_open(self, location: list[str] | ViewCls):
        times = 0
        while not self.is_tab_open(location):
            time.sleep(0.01)
            times += 1
            if times > 1000:
                raise Exception("Tab open timeout")

    def get_all(self) -> list[ViewCls]:
        results = socket.post_and_recv_result("get-all-tabs", {})
        return [self._result_to_view(result) for result in results]

    def close_tab(self, location: list[str] | ViewCls):
        if isinstance(location, ViewCls):
            location = location.location
        self.wait_for_tab_open(location)
        socket.post("close-tab", {"location": location})

    def switch_tab(self, location: list[str] | ViewCls):
        if isinstance(location, ViewCls):
            location = location.location
        self.wait_for_tab_open(location)
        socket.post("switchTab", {"location": location})

    def is_tab_open(self, location: list[str] | ViewCls):
        if isinstance(location, ViewCls):
            location = location.location
        result = socket.post_and_recv_result("is-tab-open", {"location": location})
        return result

    def pin_tab(self, location: list[str] | ViewCls):
        if isinstance(location, ViewCls):
            location = location.location
        self.wait_for_tab_open(location)
        socket.post("pin-tab", {"location": location})

    def unpin_tab(self, location: list[str] | ViewCls):
        if isinstance(location, ViewCls):
            location = location.location
        self.wait_for_tab_open(location)
        socket.post("unpin-tab", {"location": location})

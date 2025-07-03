from fletx import Xstate

from .home_child_state import HomeState, FindState, ManagerState

class HomeViewState(Xstate):
    def __init__(self, page):
        super().__init__(page)
        self.home_state: HomeState = HomeState(page)
        self.find_state: FindState = FindState(page)
        self.manager_state: ManagerState = ManagerState(page)



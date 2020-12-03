class Domain:
    def __init__(self, values) -> None:
        self.values = values
        self._states = [values]

    def revert_state(self):
        if self._states:
            state = self._states.pop()
            self.values = state

    def save_state(self):
        self._states.append(self.values)

    def replace(self, values):
        self.values = values

    # boring stuff

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]

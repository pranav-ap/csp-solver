class Domain:
    def __init__(self, values) -> None:
        self._values = values
        self._states = [values]

    def revert_state(self):
        if self._states:
            state = self._states.pop()
            self._values = state

    def save_state(self):
        self._states.append(self._values)

    def replace(self, values):
        self._values = values

    # boring stuff

    def __len__(self):
        return len(self._values)

    def __getitem__(self, index):
        return self._values[index]

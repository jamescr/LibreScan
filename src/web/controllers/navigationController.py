

class NavigationController:

    def __init__(self, p_env):
        self.env = p_env

    def home(self):
        return self.env.get_template('index.jade').render()
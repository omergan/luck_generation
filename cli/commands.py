from cli.initializer import Initializer


class Commands:
    def __init__(self, initializer: Initializer):
        self.initializer = initializer
        pass

    def run_generating_luck_simulation(self):
        options = self.initializer.options
        self.initializer.LG.generating_luck(options.username, options.context, options.network)
        pass

    def run_build_full_graph(self):
        pass

    def run_build_sub_graph(self):
        pass



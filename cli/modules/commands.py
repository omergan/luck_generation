from cli.modules.initializer import Initializer


class Commands:
    def __init__(self, initializer: Initializer):
        self.initializer = initializer
        pass

    def run_generating_luck_simulation(self, online: bool):
        options = self.initializer.options
        tsm = self.initializer.TSM
        self.initializer.LG.generating_luck(options.username, options.context, options.network, tsm)

    def run_build_full_graph(self, directed: bool):
        self.initializer.TSM.network.draw()

    def run_build_sub_graph(self):
        pass



from cli.modules.initializer import Initializer
from graph_utils import filter_topology


class Commands:
    def __init__(self, initializer: Initializer):
        self.initializer = initializer
        pass

    def run_generating_luck_simulation(self, online: bool):
        options = self.initializer.options
        tsm = self.initializer.TSM
        self.initializer.LG.generating_luck(options.username, options.context, options.network, tsm)

    def run_build_sub_graph_by_topology(self, topology):
        tsm = self.initializer.TSM
        if self.initializer.EXCEL is None:
            raise Exception('Excel not found')

        filtered = filter_topology(self.initializer.EXCEL, self.initializer.TSM.network.graph,
                                   self.initializer.LG.user, int(topology),
                                   self.initializer.TSM.network.user_dict)
        tsm.network.create_subgraph(filtered)
        tsm.network.draw()

    def run_build_full_graph(self, directed: bool):
        self.initializer.TSM.network.draw()

    def run_build_sub_graph(self):
        pass

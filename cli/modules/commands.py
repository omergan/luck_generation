from cli.modules.initializer import Initializer
from graph_utils import filter_topology, map_size, map_colors, map_labels

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
        size_map = map_size(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                            self.initializer.TSM.network.user_dict)
        colors_map = map_colors(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict)
        labels_map = map_labels(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict)
        tsm.network.draw(color_map=colors_map, size_map=size_map, label_map=labels_map)

    def run_build_full_graph(self, directed: bool):
        self.initializer.TSM.network.draw()

    def run_build_sub_graph(self):
        pass

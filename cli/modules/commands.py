from cli.modules.initializer import Initializer
from graph_utils import filter_topology, map_size, map_colors, map_labels, filter_excel
from utils import Logger
logger = Logger()
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
        self.initializer.EXCEL = filter_excel(self.initializer.EXCEL, self.initializer.TSM.network.graph,
                                   self.initializer.TSM.network.user_dict)
        size_map = map_size(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                            self.initializer.TSM.network.user_dict)
        colors_map = map_colors(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict, type=self.initializer.TSM.network.mapping_type)
        labels_map = map_labels(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict)
        tsm.network.draw(color_map=colors_map, size_map=size_map, label_map=labels_map)

    def run_build_full_graph(self, directed: bool):
        size_map = map_size(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                            self.initializer.TSM.network.user_dict)
        colors_map = map_colors(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict)
        labels_map = map_labels(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict)
        self.initializer.TSM.network.draw(color_map=colors_map, size_map=size_map, label_map=labels_map)

    def run_map_color_by_luck(self):
        self.initializer.TSM.network.mapping_type = "luck"
        logger.debug("Mapping type has been changed to luck")

    def run_map_color_by_relevance_and_surprise(self):
        self.initializer.TSM.network.mapping_type = "relevance_and_surprise"
        logger.debug("Mapping type has been changed to relevance and surprise")
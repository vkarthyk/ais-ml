from collections import MutableSequence

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from stix.core.stix_package import STIXPackage

from common.Logger import Logger


class GraphicWorker:
    '''
    Describe: Walk through each node/attribute, and record the father-child
              relationship in self.fieldTree

    Params: cur_node: current node;
            cur_label: the lable of current node
            father_id: the node name + the label of parent node
            prefix: use in case that want to pprint the layers, don't care about it otherwise
    '''
    def initG(self):
        self.G=nx.DiGraph()
        # self.G = nx.balanced_tree()
        # self.G=nx.Graph()
        # self.leafNode=[]
        self.logger = Logger(self)

    '''
    Describe: Combine node name and lable to a id used in the tree
    Params: node: the node
            label: the label of the node
    '''
    def __getTreeID(self, node, label):
        # return str(type(node))+'@@'+str(label)
        return str(label)

    def __dumpObjFields(self, obj):
        return obj.__dict__['_fields']

    def dontDraw(self, label):
        return False
        # return label[:5] == '<type' or label in ['id', 'valueOf_']
        # return label in ['id', 'valueOf_']

    def iterField(self, cur_node, cur_label, father_id, prefix=''):

        # init the row if this is the first this father show up.
        # if not self.fieldTree.has_key(father_id):
        #     self.fieldTree[father_id] = []
        if not self.G.has_node(father_id) and not self.dontDraw(father_id):
            self.G.add_node(father_id)

        # combine node name and label and get an id used in the tree
        my_id = self.__getTreeID(cur_node, cur_label)

        # insert child node(this node) in father's row
        # if my_id not in self.fieldTree[father_id]:
        #     self.fieldTree[father_id].append(my_id)
        if not self.G.has_edge(father_id, my_id) and not self.dontDraw(my_id):
            self.G.add_edge(father_id, my_id)

        # if cur_node is a list or EntityList or TypedList or else, enum them
        if isinstance(cur_node, list) or isinstance(cur_node, MutableSequence):
            for ind, item in enumerate(cur_node):
                # self.iterField(item, cur_label + '[i]', self.__getTreeID(cur_node, cur_label), prefix + '--')
                self.iterField(item, cur_label, self.__getTreeID(cur_node, cur_label), prefix + '--')

        # if cur_node has listable fields, enum them
        if hasattr(cur_node, '_fields'):
            fdict = self.__dumpObjFields(cur_node)
            for f in fdict:
                # print prefix,f,'<<',fdict[f]#str(father)
                self.iterField(fdict[f], str(f), self.__getTreeID(cur_node, cur_label), prefix + '--')

    def iterField_diff_color(self, cur_node, cur_label, father_id, prefix=''):

        # init the row if this is the first this father show up.
        # if not self.fieldTree.has_key(father_id):
        #     self.fieldTree[father_id] = []
        if not self.G.has_node(father_id) and not self.dontDraw(father_id):
            self.G.add_node(father_id)
            self.leafNode.append(father_id)

        # combine node name and label and get an id used in the tree
        my_id = self.__getTreeID(cur_node, cur_label)

        # insert child node(this node) in father's row
        # if my_id not in self.fieldTree[father_id]:
        #     self.fieldTree[father_id].append(my_id)
        if not self.G.has_edge(father_id, my_id) and not self.dontDraw(my_id):
            self.G.add_edge(father_id, my_id)
            if father_id in self.leafNode:
                self.leafNode.remove(father_id)

        # if cur_node is a list or EntityList or TypedList or else, enum them
        if isinstance(cur_node, list) or isinstance(cur_node, MutableSequence):
            for ind, item in enumerate(cur_node):
                # self.iterField(item, cur_label + '[i]', self.__getTreeID(cur_node, cur_label), prefix + '--')
                self.iterField(item, cur_label, self.__getTreeID(cur_node, cur_label), prefix + '--')

        # if cur_node has listable fields, enum them
        if hasattr(cur_node, '_fields'):
            fdict = self.__dumpObjFields(cur_node)
            for f in fdict:
                # print prefix,f,'<<',fdict[f]#str(father)
                self.iterField(fdict[f], str(f), self.__getTreeID(cur_node, cur_label), prefix + '--')

    def outputDegree(self, filename):
        degreelist=self.G.degree()
        self.logger.log('info', 'output degree list to:',filename)
        with open(filename, 'wb') as f:
            f.write('NODE NAME'+','+'DEGREE\n')
            for k in degreelist:
                f.write(str(k)+','+str(degreelist[k])+'\n')
        self.logger.log('info', 'output degree list done')

    def outputWeight(self, filename):
        self.outputDegree(filename)

    def draw(self):
        # nx.draw(self.G, with_labels=True)
        # nx.draw_graphviz(self.G)

        # nx.nx_agraph.write_dot(self.G, 'test.dot')
        # nx.draw(self.G, pos=graphviz_layout(self.G))
        self.DiG = self.G
        self.UnDiG = self.G.to_undirected()
        self.UnDiG = nx.minimum_spanning_tree(self.UnDiG)

        plt.figure(1)
        # plt.title("stix structure tree")
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        pos = graphviz_layout(self.UnDiG, prog='dot', args='-Grankdir=LR')
        nx.draw(self.UnDiG, node_size=40, pos=pos, edge_color='y')
        nx.draw_networkx_labels(self.UnDiG, pos=pos, font_color='b')

        plt.figure(2)
        # plt.title("minimum spinning tree")
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        pos = graphviz_layout(self.DiG, prog='dot', args='-Grankdir=LR')
        nx.draw(self.DiG, node_size=40, pos=pos, edge_color='y')
        nx.draw_networkx_labels(self.DiG, pos=pos, font_color='b')
        # nx.draw_networkx_nodes(self.G, nodelist=self.leafNode, node_color='b')

        # nx.draw_graphviz(self.G,'dot')
        # nx.draw_networkx(self.G)
        # plt.show()
        # nx.draw_shell(self.G, with_labels=True)
        plt.show()

    def doYourWork(self, stix_package):
        assert isinstance(stix_package, STIXPackage)

        self.initG()

        self.iterField(stix_package, 'stix_package', self.__getTreeID(STIXPackage,'root_start'), '-')

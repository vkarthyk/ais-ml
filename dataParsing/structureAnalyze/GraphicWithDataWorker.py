from collections import MutableSequence

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from stix.core.stix_package import STIXPackage
from mixbox.typedlist import TypedList
from stix.common.kill_chains import KillChainPhase
from stix.core.ttps import TTPs

from common.Logger import Logger

class GraphicWithDataWorker():
    def __init__(self):
        self.logger = Logger(self)
        self.is_clustering_node_by_name=False
        self.is_full_structure=False
        self.is_display_list_node_index=False
        self.clear_graph()

    # def initG(self):
        # self.G=nx.DiGraph()
        # self.G = nx.balanced_tree()
        # self.G=nx.Graph()
        # self.leafNode=[]
        # self.node_index=0
        # self.nodelabel_to_displaylabel_dict={}

    def set_is_clustering_node_by_name(self):
        self.is_clustering_node_by_name=True

    def set_is_full_structure(self):
        self.is_full_structure = True

    def set_is_display_list_node_index(self):
        self.is_display_list_node_index=True

    def clear_graph(self):
        self.G=nx.DiGraph()
        self.edge_weight_dict={}
        self.is_first_node=True
        self.first_node_label='root_start_123123123123123'
        self.node_index=0
        self.nodelabel_to_displaylabel_dict={}

    def __getTreeID(self, node, label):
        # return str(type(node))+'@@'+str(label)
        typename=str(type(node))
        typename = typename.split('\'')[1]
        typename = typename.split('.')[-1]
        # return str(label)+'@'+typename
        if not self.is_clustering_node_by_name:
            displaylabel=str(label).split('|')[-1]
            nodelabel=str(self.node_index)+'|'+displaylabel
            self.node_index+=1
            self.nodelabel_to_displaylabel_dict[nodelabel]=displaylabel
            return nodelabel
        else:
            return str(label)
        # return str(type(node))

    def __getListObjTreeID(self, node, listname, i):
        typename=str(type(node))
        typename = typename.split('\'')[1]
        typename = typename.split('.')[-1]
        # return listname+'['+str(i)+']@'+typename
        if not self.is_clustering_node_by_name:
            if self.is_display_list_node_index:
                displaylabel=listname.split('|')[-1]+'['+str(i)+']'
            else:
                displaylabel=listname.split('|')[-1]+'[i]'
            nodelabel=str(self.node_index)+'|'+displaylabel
            self.node_index+=1
            self.nodelabel_to_displaylabel_dict[nodelabel]=displaylabel
            return nodelabel
        else:
            if self.is_display_list_node_index:
                return listname+'['+str(i)+']'
            else:
                return listname+'[i]'
        # return listname + '[i]'

    def __dumpObjFields(self, obj):
        return obj.__dict__['_fields']

    def dontDraw(self, label):
        # return False
        # return label[:5] == '<type' or label in ['id', 'valueOf_']
        return label in [self.first_node_label, 'id', 'valueOf_']

    def __add_edge_weight(self, fr, to):
        if not self.edge_weight_dict.has_key(fr):
            self.edge_weight_dict[fr] = {}
        if not self.edge_weight_dict[fr].has_key(to):
            self.edge_weight_dict[fr][to]=0
        self.edge_weight_dict[fr][to]+=1

    def iterField(self, cur_node, cur_label, father_id, prefix=''):
        # init the row if this is the first this father show up.
        # if not self.fieldTree.has_key(father_id):
        #     self.fieldTree[father_id] = []
        if not self.G.has_node(father_id) and not self.dontDraw(father_id):
            if father_id == self.first_node_label:
                self.logger.log('WTF')
            self.G.add_node(father_id)

        # combine node name and label and get an id used in the tree
        my_id = self.__getTreeID(cur_node, cur_label)

        # insert child node(this node) in father's row
        # if my_id not in self.fieldTree[father_id]:
        #     self.fieldTree[father_id].append(my_id)
        self.__add_edge_weight(father_id, my_id)
        if self.G.has_edge(father_id, my_id):
            self.logger.log('shouldnt have output',father_id,my_id)
        if not self.G.has_edge(father_id, my_id) and not self.dontDraw(father_id) and not self.dontDraw(my_id):
            self.G.add_edge(father_id, my_id)

        # if cur_node is a list or EntityList or TypedList or else, enum them
        # if isinstance(cur_node, list) or isinstance(cur_node, MutableSequence):

        '''
        if isinstance(cur_node, MutableSequence):
            for ind, item in enumerate(cur_node):
                if cur_label is 'Marking_Structure':
                    print father_id
                # i_label = cur_label + '['+str(ind)+']'
                # i_label = cur_label + '[i]'
                # i_label = self.__getListObjTreeID(cur_label, ind)
                # self.iterField(item, i_label, self.__getTreeID(cur_node, i_label), prefix + '--')
                i_label = self.__getListObjTreeID(item, my_id, ind)
                self.iterField(item, i_label, my_id, prefix + '--')
                # self.iterField(item, cur_label, self.__getTreeID(cur_node, cur_label), prefix + '--')
        '''

        # if cur_node has listable fields, enum them
        # if cur_label in ['kill_chain_phase','kill_chain_phases', 'kill_chain', 'kill_chains', 'TTPs', 'ttps']:
        if hasattr(cur_node, '_fields'):
            fdict = self.__dumpObjFields(cur_node)
            for f in fdict:
                # print prefix,f,'<<',fdict[f]#str(father)
                # if cur_node.__getattribute__(f):

                # self.iterField(fdict[f], str(f), self.__getTreeID(cur_node, cur_label), prefix + '--')
                # if isinstance(cur_node, MutableSequence) and isinstance(fdict[f], MutableSequence):
                # if (isinstance(cur_node, MutableSequence) or isinstance(cur_node, TypedList)) and (isinstance(fdict[f], MutableSequence) or isinstance(fdict[f], TypedList)):
                if (isinstance(cur_node, MutableSequence) and isinstance(fdict[f], MutableSequence)) or isinstance(fdict[f], TypedList):
                # if (isinstance(fdict[f], MutableSequence) or isinstance(fdict[f], TypedList)):
                    for ind, item in enumerate(fdict[f]):
                        # i_label = cur_label + '['+str(ind)+']'
                        # i_label = cur_label + '[i]'
                        # i_label = self.__getListObjTreeID(cur_label, ind)
                        # self.iterField(item, i_label, self.__getTreeID(cur_node, i_label), prefix + '--')
                        i_label = self.__getListObjTreeID(item, str(f), ind)
                        self.iterField(item, i_label, my_id, prefix + '--')
                        # self.iterField(item, cur_label, self.__getTreeID(cur_node, cur_label), prefix + '--')

                elif self.is_full_structure or fdict[f] is not None:
                    self.iterField(fdict[f], str(f), my_id, prefix + '--')


    def __get_display_labels(self, G):
        labels={}
        for node in G:
            labels[node]=self.nodelabel_to_displaylabel_dict[node]
        return labels

    def __set_edge_weights(self, G):
        for u, v, d in G.edges(data=True):
            d['weight']=self.edge_weight_dict[u][v]

    def __get_edge_weights(self, G):
        return [G[u][v]['weight'] for u,v in G.edges()]

    def ava_degree_conn(self):
        self.logger.log('rst', 'average_degree_connectivity',nx.average_degree_connectivity(self.G))

    def get_edge_weight_dict(self):
        return self.edge_weight_dict

    def get_graph(self):
        return self.G

    # def get_child_parent_lists(self):
    #     parent_list=[]
    #     child_list=[]
    #     for p in self.edge_weight_dict:
    #         parent_list.append(p)
    #         for c in self.edge_weight_dict[p]:
    #             try:
    #                 child_list.index(c)
    #             except ValueError, err:
    #                 child_list.append(c)
    #     return child_list, parent_list

    def draw(self, stix_name=0, is_width_as_weight=False, is_draw_min_spin_tree=False, pic_num_minspintree=100000):
        # nx.draw(self.G, with_labels=True)
        # nx.draw_graphviz(self.G)

        # nx.nx_agraph.write_dot(self.G, 'test.dot')
        # nx.draw(self.G, pos=graphviz_layout(self.G))

        self.DiG = self.G

        # self.DiG = nx.path_graph(6)
        # self.DiG.edge[1][2]['weight'] = 3

        if isinstance(stix_name, int):
            stix_name = '#'+stix_name
        plt.figure("Structure Tree for STIX PACKAGE [ " + stix_name + ' ]')
        # plt.title("stix structure tree")
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        pos = graphviz_layout(self.DiG, prog='dot', args='-Grankdir=LR')

        if is_width_as_weight:
            self.__set_edge_weights(self.DiG)
            weights=self.__get_edge_weights(self.DiG)

            nx.draw(self.DiG, node_size=40, pos=pos, edge_color='y', with_labels=False, width=weights)
        else:
            nx.draw(self.DiG, node_size=40, pos=pos, edge_color='y', with_labels=False)
        if not self.is_clustering_node_by_name:
            labels=self.__get_display_labels(self.DiG)
            nx.draw_networkx_labels(self.DiG, pos=pos, labels=labels, font_color='b')
        else:
            nx.draw_networkx_labels(self.DiG, pos=pos, font_color='b')

        if is_draw_min_spin_tree:
            self.UnDiG = self.G.to_undirected()
            self.UnDiG = nx.minimum_spanning_tree(self.UnDiG)

            plt.figure("Minimun Spinning Tree for STIX PACKAGE [ " + stix_name + ' ]')
            # plt.title("minimum spinning tree")
            mng= plt.get_current_fig_manager()
            mng.resize(*mng.window.maxsize())
            pos = graphviz_layout(self.UnDiG, prog='dot', args='-Grankdir=LR')
            nx.draw(self.UnDiG, node_size=40, pos=pos, edge_color='y')
            nx.draw_networkx_labels(self.UnDiG, pos=pos, font_color='b')
            # nx.draw_networkx_nodes(self.G, nodelist=self.leafNode, node_color='b')

        # nx.draw_graphviz(self.G,'dot')
        # nx.draw_networkx(self.G)
        # plt.show()
        # nx.draw_shell(self.G, with_labels=True)

    def draw_show(self):
        plt.show()

    def doYourWork(self, stix_package):
        assert isinstance(stix_package, STIXPackage)

        # self.initG()

        # self.logger.log('info', 'working: stix id:',stix_package.id_)
        # self.logger.log('info', 'working: stix kill...:',type(stix_package.ttps.kill_chains[0].kill_chain_phases))
        # self.logger.log('info', 'working: stix kill...:',stix_package.ttps.kill_chains[0].kill_chain_phases[1])
        # self.logger.log('info', 'working: stix kill...:',stix_package.ttps.kill_chains[0].kill_chain_phases[1])
        # self.logger.log('info', 'working: stix ttp:',type(stix_package.ttps))

        self.iterField(stix_package, 'stix_package', self.__getTreeID(STIXPackage, self.first_node_label), '-')

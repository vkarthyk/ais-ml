from common.Logger import Logger
import pickle


class IOWorker:
    def __init__(self):
        self.logger = Logger(self)
        # self.is_titles_wrote = False

    '''
        weights: ex.: {'parent1': {'child1': 5, 'child2': 4}, 'parent2': {'child2':3, 'child3': 1}}
        rowlist: ex.: ['child1', 'child2'...]
        collist: ex.: ['parent1', 'parent2'...]
        target table:
                  parent1     parent2
        child1      5            0
        child2      4            3
        child3      0            1
    '''
    def outputWeightTable(self, weights, filename, rowlist=None, collist=None):
        assert isinstance(weights, dict)
        assert isinstance(rowlist, list) or rowlist is None
        assert isinstance(collist, list) or collist is None

        self.logger.log('info', 'writing weight dict to:', filename)
        if rowlist is not None and collist is not None:
            self.logger.log('info', 'using provided row and col index.')
        else:
            self.logger.log('info', 'building row and col index by myself.')
            rowlist, collist = self.get_child_parent_lists(weights)

        target_table=[]
        for i in range(len(rowlist)):
            child_name = rowlist[i]
            this_row = []
            for j in range(len(collist)):
                parent_name=collist[j]
                w = weights[parent_name][child_name] if weights.has_key(parent_name) and weights[parent_name].has_key(child_name) else 0
                this_row.append(w)
            target_table.append(this_row)

        self.logger.log('info', target_table)

        with open(filename, 'wb') as f:
            for parent_name in collist:
                f.write(',' + parent_name)
            f.write('\n')
            for ind, row in enumerate(target_table):
                f.write(rowlist[ind])
                for cell in row:
                    f.write(',' + str(cell))
                f.write('\n')
        self.logger.log('info', 'writing weight dict is done.')

        return
        # degreelist = self.G.

    '''
    def writeWeightTitle(self, filename, allstructure=None, weights=None):
        if allstructure is not None:
            self.logger.log('info', 'using provided col names.')
        else:
            self.logger.log('info', 'building row and col names by myself.')
            allstructure = weights
        title_row = 'Stix_Name'
        for p in allstructure:
            for c in allstructure[p]:
                # title_row = title_row + p+'_to_'+c + ','
                title_row = title_row + ',' + p+'->'+c
        with open(filename, 'w') as f:
                f.write(title_row + '\n')
        # self.is_titles_wrote = True
    '''


    def get_child_parent_lists(self, weight_dict):
        parent_list=[]
        child_list=[]
        for p in weight_dict:
            parent_list.append(p)
            for c in weight_dict[p]:
                try:
                    child_list.index(c)
                except ValueError, err:
                    child_list.append(c)
        return child_list, parent_list

    def pickle_dump(self, obj, filename):
        print obj
        pickle.dump(obj, open(filename, 'wb'))
        self.logger.log('info', 'dump obj as pickle to', filename)


    def pickle_load(self, filename):
        self.logger.log('info', 'load obj from pickle file', filename)
        return pickle.load(open(filename, 'rb'))

from stix.core.stix_package import STIXPackage
from stix.core import Indicators
from stix.indicator.indicator import Indicator
from stix import EntityList,TypedList
from collections import MutableSequence
from printUtils import saveObjToFile, loadObjFrFile
from dataParsing.Logger import Logger

class FieldsDocumentaryWorker():
    # stix_fields_list = []
    # indicator_fields_list = []
    # stix_values_list = []
    # indicator_values_list = []
    fieldTree = {}

    def __init__(self):
        self.logger = Logger(self)

    '''
    Describe: Main method, takes a stix object in and parse it.
    Params: stix_package: STIXPackage object
    '''
    def consumeStix(self, stix_package):
        assert isinstance(stix_package, STIXPackage)

        '''Enable this if want to use the test function, ignore otherwise'''
        # self.iterFieldAndPrint(stix_package, '-', stix_package)

        self.iterField(stix_package, 'stix_package', self.__getTreeID(STIXPackage,'root_start'), '-')

        '''for test'''
        # for node in stix_package.walk():
            # if isinstance(stix_package, )
            # print type(node)



    '''
    Describe: This version is similar to iterField(), but it's a
              test version which is going to print the tree to 
              console in a tree-like way as the parsing goes by.
              This is only an experimental function.
    '''
    def iterFieldAndPrint(self, obj, prefix, father, label=''):
        # if isinstance(obj, list) or isinstance(obj, EntityList):
        if isinstance(obj, list) or isinstance(obj, MutableSequence):
            for item in obj:
                self.iterFieldAndPrint(item, prefix+'--', obj)
        self.logger.log('rst',prefix,obj.__class__,'@@',label,'<<',father.__class__)#str(father)
        # don't delete this, enable this to check if there is any List like Entity List
        print '+'+prefix[1:],obj,'<<',father#str(father)
        if not hasattr(obj, '_fields'):
            return
        fdict = self.__dumpObjFields(obj)
        for f in fdict:
            # print prefix,f,'<<',fdict[f]#str(father)
            # print '+'+prefix[1:],type(f),'<<',fdict[f]#str(father)

            # if isinstance(fdict[f], Indicators):
            # if isinstance(fdict[f], EntityList):
            #     print 'here we go!'
            #     for item in fdict[f]:
            #         print type(item)
            #     print 'here we go end!'
            self.iterFieldAndPrint(fdict[f], prefix+'--', obj, f)


    '''
    Describe: Combine node name and lable to a id used in the tree
    Params: node: the node
            label: the label of the node
    '''
    def __getTreeID(self, node, label):
        return str(type(node))+'@@'+str(label)


    '''
    Describe: Walk through each node/attribute, and record the father-child 
              relationship in self.fieldTree
    
    Params: cur_node: current node; 
            cur_label: the lable of current node
            father_id: the node name + the label of parent node
            prefix: use in case that want to pprint the layers, don't care about it otherwise
    '''
    def iterField(self, cur_node, cur_label, father_id, prefix=''):

        # init the row if this is the first this father show up.
        if not self.fieldTree.has_key(father_id):
            self.fieldTree[father_id] = []

        # combine node name and label and get an id used in the tree
        my_id = self.__getTreeID(cur_node, cur_label)

        # insert child node(this node) in father's row
        if my_id not in self.fieldTree[father_id]:
            self.fieldTree[father_id].append(my_id)

        # if cur_node is a list or EntityList or TypedList or else, enum them
        if isinstance(cur_node, list) or isinstance(cur_node, MutableSequence):
            for ind, item in enumerate(cur_node):
                self.iterField(item, cur_label + '[i]', self.__getTreeID(cur_node, cur_label), prefix + '--')

        # if cur_node has listable fields, enum them
        if hasattr(cur_node, '_fields'):
            fdict = self.__dumpObjFields(cur_node)
            for f in fdict:
                # print prefix,f,'<<',fdict[f]#str(father)
                self.iterField(fdict[f], str(f), self.__getTreeID(cur_node, cur_label), prefix + '--')


    def __dumpObjFields(self, obj):
        return obj.__dict__['_fields']


    '''
    Describe: write the tree structure to a csv file
    '''
    def printTree2Csv(self, fieldTree, csvfilename):
        self.logger.log('info', 'Writing tree to CSV file \'', csvfilename, '\'...')
        with open(csvfilename,'wb') as f:
            for father in fieldTree:
                ostr = str(father)
                ostr += ';'
                ostr += ';'.join(str(child) for child in fieldTree[father])
                f.write(ostr+'\n')
        self.logger.log('info', 'Writing finished.')

    '''
    Describe: print the tree structure to console
    '''
    def printTree2Console(self, fieldTree):
        for father in fieldTree:
            ostr = str(father)
            ostr += ';'
            ostr += ';'.join(str(child) for child in fieldTree[father])
            self.logger.log('rst', ostr)

    def getTree(self):
        return self.fieldTree

    '''
    Describe: Dump the field tree with pickle and store it to file
    '''
    def saveTreeToFile(self, fieldTree, filename):
        if not filename or type(filename) is not str or filename=='':
            self.logger.log('err', 'I need a file name where the object is going be saved')
            return -1
        self.logger.log('info', 'Dumping tree object to pickle file \'', filename, '\'...')
        saveObjToFile(fieldTree, filename)
        self.logger.log('info', 'Dumping finished')

    '''
    Describe: Load field tree from pickle file
    '''
    def loadTreeFrFile(self, filename=''):
        if not filename or type(filename) is not str or filename=='':
            self.logger.log('err', 'I need a file name to load from')
            return -1
        self.logger.log('info', 'Loading tree object from pickle file \'', filename, '\'...')
        return loadObjFrFile(filename)


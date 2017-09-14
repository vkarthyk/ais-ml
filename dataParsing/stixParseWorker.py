from stix.core import STIXPackage,STIXHeader
from stix.extensions.marking.tlp import TLPMarkingStructure

class StixParseWorker:
    # stix_list=[]
    # indicator_list=[]
    stix_fields_list_of_list=[]
    indicator_fields_list_of_list=[]
    kill_chain_list_of_list = []

    stix_fields_dict_of_list={}
    indicator_fields_dict_of_list={}
    kill_chain_dict_of_list = {}

    stix_title_list = []
    stix_package_intent_list = []
    stix_description_list = []
    stix_marking_color_list = []
    stix_produced_time_list = []
    stix_indicator_id_list_list = []
    stix_kill_chain_id_list_list = []

    indicator_id_list = []
    indicator_description_list = []
    indicator_type_list = []

    def __mergeKillChainPhase(self, kill_chain):
        pass

    def __processKillChainFieldsList(self, kill_chain):
        pass

    def __processStixFieldsList(self, stix_package):

        assert isinstance(stix_package, STIXPackage)
        self.stix_title_list.append(stix_package.stix_header.title)
        self.stix_package_intent_list.append(stix_package.stix_header.package_intents[0].__str__())
        self.stix_description_list.append(stix_package.stix_header.description.__str__())
        # self.stix_marking_color_list.append('|'.join(ms.color for ms in stix_package.stix_header.handling.marking[0].marking_structures))
        tmpstr=''
        for ms in stix_package.stix_header.handling.marking[0].marking_structures:
            if isinstance(ms, TLPMarkingStructure):
                tmpstr += ms.color
        self.stix_marking_color_list.append(tmpstr)
        self.stix_produced_time_list.append(stix_package.stix_header.information_source.time.produced_time.to_dict())

        indicator_id_list = []
        for indicator in stix_package.indicators:
            if not indicator.composite_indicator_expression:
                indicator_id_list.append(indicator.id_)
                self.__processIndicatorFieldsList(indicator)
        ind_ids_str = '|'.join(id for id in indicator_id_list)
        self.stix_indicator_id_list_list.append(ind_ids_str)

        # kill_chain_id_list = []
        # for kill_chain in stix_package.kill_chains:
        #     kill_chain_id_list.append(kill_chain.id)
        #     self.__processKillChainFieldsList(kill_chain)
        # kchain_ids_str = '|'.join(id for id in kill_chain_id_list)
        # self.stix_kill_chain_id_list_list.append(kchain_ids_str)


    def __processIndicatorFieldsList(self, indicator):
        self.indicator_id_list.append(indicator.id_)
        self.indicator_description_list.append(indicator.description.__str__())
        self.indicator_type_list.append(indicator.indicator_types[0].__str__())

    def consumeStix(self, stix_package):
        self.__processStixFieldsList(stix_package)

        self.stix_fields_list_of_list.append(self.stix_title_list)
        self.stix_fields_list_of_list.append(self.stix_package_intent_list)
        self.stix_fields_list_of_list.append(self.stix_description_list)
        self.stix_fields_list_of_list.append(self.stix_marking_color_list)
        self.stix_fields_list_of_list.append(self.stix_produced_time_list)
        self.stix_fields_list_of_list.append(self.stix_indicator_id_list_list)
        self.stix_fields_list_of_list.append(self.stix_kill_chain_id_list_list)

        self.stix_fields_dict_of_list['title'] = self.stix_title_list
        self.stix_fields_dict_of_list['package_intent'] = self.stix_package_intent_list
        self.stix_fields_dict_of_list['description'] = self.stix_description_list
        self.stix_fields_dict_of_list['marking_color'] = self.stix_marking_color_list
        self.stix_fields_dict_of_list['produced_time'] = self.stix_produced_time_list
        self.stix_fields_dict_of_list['indicators_ids'] = self.stix_indicator_id_list_list
        self.stix_fields_dict_of_list['kill_chains_ids'] = self.stix_kill_chain_id_list_list

        self.indicator_fields_list_of_list.append(self.indicator_id_list)
        self.indicator_fields_list_of_list.append(self.indicator_description_list)
        self.indicator_fields_list_of_list.append(self.indicator_type_list)


    def getStixFieldsList(self):
        return self.stix_fields_list_of_list

    def getIndicatorFieldsList(self):
        return self.indicator_fields_list_of_list

    def getStixFieldsDict(self):
        return self.stix_fields_dict_of_list

    def getIndicatorFieldsDict(self):
        return self.indicator_fields_dict_of_list
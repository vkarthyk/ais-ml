from enum import Enum

class JobType(Enum):
    ParseStixFromXmlAndPrintValuesToConsole=0
    # QuitBeforeRound=1
    # JustDoThisRound=2
    LoadFieldTree=3
    SaveFieldTree=4
    AnalyzeStixFromXmlAndBuildFieldTree=5
    PrintFieldTreeToConsole=6
    PrintFieldTreeToCsvFile=7
    GrabAStixFromXmlAndSaveToTmpStix=8
    LoadAStixFromFile=9
    SaveAStixToFile=10
    AnalyzeStixFromXmlAndDrawAGraph=11

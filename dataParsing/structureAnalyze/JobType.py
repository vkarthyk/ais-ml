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

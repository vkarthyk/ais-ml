# Feature Extraction Framework

## How to run the framework
- please run mainFB.py (the name is stupid, I know)
- before you run, make sure to replace the csv file name in main function


## Intro
- this is very easy to use.
- main framework class: FeatureBuilder
- only need to implement modules in new files and put them under modules/
- please check **IpAdressScoreDemo.py** and **KillChainPhaseIdScoreDemo** as examples for how to write modules

## conig.py
- there are two levels of runing - normal and aggressive, basically aggressive mode will generate more features than normal ones
- there is black list and white list implemented against modules, used to manage modules

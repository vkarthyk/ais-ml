import yaml


def pprintDict(dictionary):
    # print '--------------'
    print yaml.dump(dictionary, allow_unicode=True, default_flow_style=False)

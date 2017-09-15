#coding=utf-8

class Logger():
    STYLE = {
        'fore':
            {
                'black'    : 30,   #  黑色
                'red'      : 31,   #  红色
                'green'    : 32,   #  绿色
                'yellow'   : 33,   #  黄色
                'blue'     : 34,   #  蓝色
                'purple'   : 35,   #  紫红色
                'cyan'     : 36,   #  青蓝色
                'white'    : 37,   #  白色
            },

        'back' :
            {
                'black'     : 40,
                'red'       : 41,
                'green'     : 42,
                'yellow'    : 43,
                'blue'      : 44,
                'purple'    : 45,
                'cyan'      : 46,
                'white'     : 47,
            },

        'mode' :
            {
                'mormal'    : 0,
                'bold'      : 1,
                'underline' : 4,
                'blink'     : 5,
                'invert'    : 7,
                'hide'      : 8,
            },

        'default' :
            {
                'end' : 0,
            },
    }

    def __init__(self, obj=False):
        self.objname=obj.__class__ if obj else '<unknown>'


    # def UseStyle(string, mode = '', fore = '', back = ''):
    def UseStyle(self, string, *stringList, **options):
        mode = options.get('mode', '')
        fore = options.get('fore', '')
        back = options.get('back', '')

        mode = '%s' % self.STYLE['mode'][mode] if self.STYLE['mode'].has_key(mode) else ''

        fore = '%s' % self.STYLE['fore'][fore] if self.STYLE['fore'].has_key(fore) else ''

        back = '%s' % self.STYLE['back'][back] if self.STYLE['back'].has_key(back) else ''

        style = ';'.join([s for s in [mode, fore, back] if s])

        style = '\033[%sm' % style if style else ''

        end = '\033[%sm' % self.STYLE['default']['end'] if style else ''

        for s in stringList:
            string = string + ' ' + str(s)
        return '%s%s%s' % (style, string, end)


    def log(self, type, *log):
        if type == 'err':
            logstr = self.UseStyle('{err}', *log, mode='underline', fore='red')
        elif type == 'rst':  # result
            logstr = self.UseStyle(*log, mode='bold', fore='blue')
        elif type == 'info':
            logstr = self.UseStyle('{info}', *log, fore='yellow')
        else:
            logstr = self.UseStyle('{debug}', *log)

        if type in ['rst']:
            print logstr
        else:
            print '[',self.objname,']:',logstr

logger=Logger()
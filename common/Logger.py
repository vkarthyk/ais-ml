#coding=utf-8
import datetime

has_set_time = False
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
        if type(obj) is str:
            self.objname = obj
        else:
            self.objname=obj.__class__ if obj else '<unknown>'
        if not globals()['has_set_time']:
            globals()['logpath'] = datetime.datetime.today().isoformat() + '.log'
            globals()['has_set_time'] = True


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
    def __output(self, logstr):
        print logstr
        with open(globals()['logpath'], 'a+') as f:
            f.write(logstr+'\n')
    
    def __combine_str(self, string, *stringList):
        for s in stringList:
            string = string + ' ' + str(s)
        return string

    def err(self, *log):
        logstr = self.UseStyle('{err}', *log, mode='underline', fore='red')
        logstr = self.__combine_str('[',self.objname,']:',logstr)
        self.__output(*logstr)

    def info(self, *log):
        logstr = self.UseStyle('{info}', *log, fore='yellow')
        logstr = self.__combine_str('[',self.objname,']:',logstr)
        self.__output(logstr)

    def rst(self, *log):
        logstr = self.UseStyle('', *log, mode='bold', fore='blue')
        self.__output(logstr)

    def dbg(self, *log):
        logstr = self.UseStyle('{debug}', *log, fore='red')
        logstr = self.__combine_str('[',self.objname,']:',logstr)
        self.__output(logstr)

    def warn(self, *log):
        logstr = self.UseStyle('{warning}', *log, fore='red')
        logstr = self.__combine_str('[',self.objname,']:',logstr)
        self.__output(logstr)

    def log(self, type, *log):

        #black list for log
        # if str(self.objname) == "IOWorker.IOWorker":
        #     return

        if type == 'err':
            logstr = self.UseStyle('{err}', *log, mode='underline', fore='red')
        elif type == 'warn':
            logstr = self.UseStyle('{warning}', *log, fore='red')
        elif type == 'rst':  # result
            logstr = self.UseStyle(*log, mode='bold', fore='blue')
        elif type == 'info':
            logstr = self.UseStyle('{info}', *log, fore='yellow')
        else:
            type = 'debug'
            logstr = self.UseStyle('{debug}', *log)

        # if type in ['debug', 'info']:
        if type in ['debug']:
            return

        if type in ['rst']:
            self.__output(logstr)
        else:
            logstr = self.__combine_str('[',self.objname,']:',logstr)
            self.__output(logstr)

logger=Logger()

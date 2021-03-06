from utils.IO import IO
from configs.config import Config
import os, shutil

class Testcase:

    def __init__(self):
        self.name = ""
        self.path = ""
        self.hex = ""
        self.asm = ""
        self.display = ""

    @staticmethod
    def loadFrom(confname):
        conf = Config.getConfig(confname)
        ret = Testcase()
        ret.path = os.path.dirname(confname)
        ret.name = conf['name']
        ret.hex = conf['hex']
        ret.asm = None
        ret.display = None
        if 'asm' in conf:
            ret.asm = conf['asm']
        if 'display' in conf:
            ret.display = conf['display']
        return ret
    @staticmethod
    def caseList():
        # caselist = Config.getValue('configs/global.json', 'testcases')
        caselist = Config.getValue('configs/testcase.json', 'testcases')
        ret = []
        for item in caselist:
            # print(item)
            case = Testcase.loadFrom(item['path'])
            if not case is None:
                ret.append(case)
        return ret

    @staticmethod
    def importAsm(asm, dst):
        mars = Config.getValue('configs/global.json', 'marsPath')
        
        testname = os.path.basename(asm).split('.')[0]
        dst = dst + '/' + testname
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)
        # Create Test
        # asm
        asmname = testname + '.asm'
        shutil.copy(src=asm, dst=dst+'/'+asmname)
        # hex
        hexname = testname + '.hex'
        os.system("java -jar {mars} db nc mc CompactDataAtZero a dump .text HexText {hex} {asm}".format(
            mars=mars, hex=dst+'/'+hexname, asm=dst+'/'+asmname))
        # display
        dispname = testname + '.txt'
        os.system("java -jar {mars} 100000 lg db nc mc CompactDataAtZero {asm} > {disp}".format(
            mars=mars, asm=dst+'/'+asmname, disp=dst+'/'+dispname))
        # json configuration
        jsonname = testname+'.json'
        caseconf = {"name": testname, "asm": asmname, "hex": hexname, "display": dispname}
        Config.saveConfig(dst+'/'+jsonname, caseconf)
        # added into testcase-set
        testcases = Config.getValue('configs/testcase.json', 'testcases')
        testcases.append({'name': testname, 'path': dst+'/'+jsonname})
        Config.setValue('configs/testcase.json', 'testcases', testcases)
    @staticmethod
    def rmcase(name):
        caselist = Config.getValue('configs/testcase.json', 'testcases')
        caselist.pop(name, 404)
        Config.setValue('configs/testcase.json', 'testcases', caselist)
    
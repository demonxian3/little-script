#coding: utf-8
#pip install colorama 

import os;
import sys;
import pprint
import subprocess;
from datetime import datetime;
from optparse import OptionParser
from threading import Thread
from colorama import Fore, Style, init



#d directory
#s string
#i number
#b boolean
#n node
#l link
#a array
#dt datetime

class Color:
    RED     = '';
    GREEN   = '';
    YELLOW  = '';
    BLUE    = '';
    PINK = '';
    CYAN    = '';
    WHITE   = '';
    bRED     = '';
    bGREEN   = '';
    bYELLOW  = '';
    bBLUE    = '';
    bPINK = '';
    bCYAN    = '';
    bWHITE   = '';
    RST = '';
    
    @staticmethod
    def setMode(mode):
        
        if mode == 1:
            init(autoreset=True)
            Color.RED      = Fore.RED;
            Color.GREEN    = Fore.GREEN;
            Color.YELLOW   = Fore.YELLOW;
            Color.BLUE     = Fore.BLUE;
            Color.bPINK    = Fore.MAGENTA;
            Color.CYAN     = Fore.CYAN;
            Color.WHITE    = Fore.WHITE;
            Color.bRED     = Style.BRIGHT + Fore.RED;
            Color.bGREEN   = Style.BRIGHT + Fore.GREEN;
            Color.bYELLOW  = Style.BRIGHT + Fore.YELLOW;
            Color.bBLUE    = Style.BRIGHT + Fore.BLUE;
            Color.bbPINK   = Style.BRIGHT + Fore.MAGENTA;
            Color.bCYAN    = Style.BRIGHT + Fore.CYAN;
            Color.bWHITE   = Style.BRIGHT + Fore.WHITE;
            Color.RST = Style.RESET_ALL + Fore.RESET
            
            
        elif mode == 2:
            Color.RED      = '\033[31m';
            Color.GREEN    = '\033[32m';
            Color.YELLOW   = '\033[33m';
            Color.BLUE     = '\033[34m';
            Color.PINK     = '\033[35m';
            Color.CYAN     = '\033[36m';
            Color.WHITE    = '\033[37m';
            Color.bRED     = '\033[1;31m';
            Color.bGREEN   = '\033[1;32m';
            Color.bYELLOW  = '\033[1;33m';
            Color.bBLUE    = '\033[1;34m';
            Color.bMAGENTA = '\033[1;35m';
            Color.bCYAN    = '\033[1;36m';
            Color.bWHITE   = '\033[1;37m';
            Color.RST      = '\033[0m';

class Node:
    def __init__(self, sShortHash, sFullHash, sComment, sTime, sAuthor, pPrev=None, pNext=None):
        self.time = 0;
        self.id = sShortHash;
        self.hash = sFullHash;
        self.comment = sComment;
        self.author = sAuthor;
        self.prev = pPrev;
        self.next = pNext;

        if sTime:
            iTime = int(sTime);
            dtTime = datetime.fromtimestamp(iTime);
            self.time = dtTime.strftime("%Y-%m-%d %H:%M:%S");

class Link:
    def __init__(self):
        self.head = Node('','','','','');
        self.lenght = 0;

class Options:
    
    def __init__(self):
        self.options = {
            'first': ['boolean', '显示文件首次修改的日期和哈希，默认显示文件最后一次的修改日期和哈希'],
            'include': ['array', '包含关键字，多个关键字使用空格分隔，元素间逻辑与'],
            'exclude': ['array', '剔除关键字，多个关键字使用空格分隔'],
            'verbose': ['boolean', '显示扫描详情'],
            'type': ['array', '按照文件类型划分显示如: -t biz:/lib/biz -t tsx:.tsx'],
            'rtx': ['string', '提交作者'],
            'all': ['boolean', '全扫描'],
            'color': ['string', '显示颜色：1 通用兼容颜色，2 linux高亮颜色'],
        }

        usage = "%prog [OPTION]... [较早的commit] [较晚的commit]";
        parser = OptionParser(usage=usage);

        for key in self.options:
            sShort = '-' + key[0];
            sFull = '--' + key;
            sType = self.options[key][0];
            sHelp = self.options[key][1];

            if sType == 'array':
                parser.add_option(sShort, sFull, action="append", type="string", dest=key, help=sHelp, default=[]);
            if sType == 'boolean':
                parser.add_option(sShort, sFull, action="store_true", dest=key, help=sHelp, default=False);
            if sType == 'string':
                parser.add_option(sShort, sFull, type="string", dest=key, help=sHelp, default='');

        (self.opts, self.args) = parser.parse_args();
        self.parse();

    def parse(self):
        dOptions = self.opts;
        aArgumnet = self.args;

        if not dOptions.rtx:
            print("rtx 为必填项，请使用-r/--rtx参数指定你的rtx");
            sys.exit();

        if not dOptions.include and not dOptions.all and not aArgumnet:
            print("请至少指定一个过滤关键字，否则历史提交版本数据会很多，使用-i/--include");
            sys.exit();

        self.rtx = dOptions.rtx;
        self.include = dOptions.include;
        self.exclude = dOptions.exclude;
        self.verbose = dOptions.verbose;
        self.first = dOptions.first;
        self.color = dOptions.color;
        self.mode = 'scan-all';

        self.typesort = {};
        for sType in dOptions.type:
            part = sType.split(':');
            self.typesort[part[0]] = part[1];

        if aArgumnet :
            if len(aArgumnet) != 2:
                print("传递commit区间时，需要指定两个commit版本");
                sys.exit();
            
            self.startHash = aArgumnet[0];
            self.stopHash = aArgumnet[1];

            if len(self.startHash) == 40 and len(self.stopHash) == 40:
                self.mode = 'scan-fullhash-range';
            else:
                self.mode = 'scan-shorthash-range';

class Pdiff:
    def __init__(self):
        self.dFileLog = {'M':{}, 'D':{}, 'R':{}, 'A':{}, 'C':{}, 'T':{}, 'U':{}, 'X':{}, 'B':{}};
        self.dMergeLog = {'M':{}, 'D':{}, 'R':{}, 'A':{}, 'C':{}, 'T':{}, 'U':{}, 'X':{}, 'B':{}};
        self.dCommitLog = {};
        self.options = Options();
        self.mode = self.options.mode;
        self.typesort = self.options.typesort;
        self.openDiff = True;
        self.hasMergeFile = False;

        if self.mode != 'scan-all':
            self.openDiff = False;
            self.startHash = self.options.startHash;
            self.stopHash = self.options.stopHash;

        
        Color.setMode(int( self.options.color if self.options.color else 0));
        lHistoryCommit = Link();
        pCommit = lHistoryCommit.head;

        sLastPushHash = "";
        aHistoryCommit = self.getCommitHistory();

        for sCommit in aHistoryCommit:
            aCommit = sCommit.split('|');

            if len(aCommit) == 0:
                continue;

            nCommit = Node(*aCommit[:5], pCommit, None);
            pCommit.next = nCommit;
            pCommit = nCommit;

            sId = nCommit.id;
            sHash = nCommit.hash;
            sAuthor = nCommit.author;
            sComment = nCommit.comment;
            dtTime = nCommit.time;

            if "Merge" in sComment and nCommit.prev.hash == sLastPushHash:
                self.diff(nCommit, nCommit.prev, True);
            
            
            bWillDiff = self.openDiff;

            if self.mode == 'scan-fullhash-range':
                self.openDiff = True if self.startHash == sHash else self.openDiff ;
                self.openDiff = False if self.stopHash == sHash else self.openDiff ;

            elif self.mode == 'scan-shorthash-range':
                self.openDiff = True if self.startHash in sId else self.openDiff ;
                self.openDiff = False if self.stopHash in sId else self.openDiff ;


            self.dCommitLog[sId] = nCommit;

            for sSearch in self.options.include:
                if sSearch not in (sHash + dtTime + sAuthor + sComment):
                    bWillDiff = False;
                    break;

            for sSearch in self.options.exclude:
                if sSearch in  (sHash + dtTime + sAuthor + sComment):
                    bWillDiff = False;
                    break;
            
            if sAuthor != self.options.rtx:
                continue;

            if bWillDiff:
                if self.options.verbose:
                    print("正在扫描历史版本: %s %s %s %s" %(sHash, dtTime, sAuthor, sComment))
                
                if (not nCommit.hash) or (not nCommit.prev.hash):
                    continue

                self.diff(nCommit, nCommit.prev);
                sLastPushHash = nCommit.hash;

        
        self.showFileLog(self.dFileLog);
        if self.hasMergeFile:
            print('\n\n\n*** 以下文件检测于Merge中，可能为其他人修改的文件 ***');
            self.showFileLog(self.dMergeLog);
    
    def execute(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate();
        try:
            return output.decode('utf-8');
        except:
            return output;

    def getCommitHistory(self):
        sCmd = 'git log --pretty=format:"%h|%H|%s|%ct|%an" --abbrev-commit --reverse';
        sHistoryCommit = self.execute(sCmd);
        if not len(sHistoryCommit):
            print("请在Git项目下执行该命令");
            sys.exit();
        return sHistoryCommit.split('\n');

    def diff(self, nCur, nPrev, bMerge=False):
        sId = nCur.id;
        sRtx = nCur.author;
        dtTime = nCur.time;
        sHash1 = nCur.hash;
        sHash2 = nPrev.hash;

        if bMerge:
            sCmd = 'git diff --name-status %s %s ' % (sHash1, sHash2);
        else:    
            sCmd = 'git diff --name-status %s %s ' % (sHash2, sHash1);

        sDiff = self.execute(sCmd);

        if not sDiff:
            print("命令执行异常: "+sCmd);
        
        aDiff = str(sDiff).split('\n');

        for sLine in aDiff:
            aRow = sLine.split();
            nCount = len(aRow);

            if not nCount:
                continue;

            sOpera = aRow[0][0];
            sFilename = aRow[1];
            sRename =  aRow[2] if nCount>2 else ''

            if not bMerge:
                if sFilename not in self.dFileLog[sOpera]:
                    self.dFileLog[sOpera][sFilename] = { 'rename': sRename, 'time': dtTime, 'hash': sId, 'rtx': sRtx};
                elif not self.options.first:
                    self.dFileLog[sOpera][sFilename]['rename'] = sRename;
                    self.dFileLog[sOpera][sFilename]['time'] = dtTime;
                    self.dFileLog[sOpera][sFilename]['hash'] = sId;
                    self.dFileLog[sOpera][sFilename]['rtx'] = sRtx;
            else:
                if sFilename in self.dFileLog[sOpera]:
                    self.hasMergeFile = True;
                    self.dMergeLog[sOpera][sFilename] = self.dFileLog[sOpera][sFilename];
                    del self.dFileLog[sOpera][sFilename];

    def showFileLog(self, dFileLog):
        dOperaMap = {
            'R': ['重名', Color.bYELLOW  ],
            'A': ['添加', Color.bGREEN   ],
            'M': ['修改', Color.bCYAN    ],
            'C': ['复制', Color.bYELLOW  ],
            'D': ['移除', Color.bPINK    ],
        }

        if not self.options.typesort:
            for sOpera in dFileLog:
                dFileInfo = dFileLog[sOpera];
                for sFilename in dFileInfo:
                    sLabel = dOperaMap[sOpera][0];
                    sColor = dOperaMap[sOpera][1];
                    dInfo = dFileInfo[sFilename];

                    sId = dInfo['hash'];
                    sRtx = dInfo['rtx'];
                    dtTime = dInfo['time'];
                    sRename = dInfo['rename'];

                    if sOpera == 'R':
                        print("[%s] %s(%s) - %s%s %s => %s%s" % (dtTime, Color.RED, sId,  sColor, sLabel, sRename, sFilename, Color.RST ));
                    else:
                        print("[%s] %s(%s) - %s%s %s%s" % (dtTime, Color.RED, sId,  sColor, sLabel, sFilename, Color.RST));

        
        else:
            dFileLog = self.sortFileLog(dFileLog);
            for sFileType in dFileLog:
                print(Color.bWHITE + sFileType + Color.RST);
                for sFilename in dFileLog[sFileType]:
                    for sOpera in dFileLog[sFileType][sFilename]:
                        sLabel = dOperaMap[sOpera][0];
                        sColor = dOperaMap[sOpera][1];
                        dInfo = dFileLog[sFileType][sFilename][sOpera];

                        sId = dInfo['hash'];
                        sRtx = dInfo['rtx'];
                        dtTime = dInfo['time'];
                        sRename = dInfo['rename'];

                        if sOpera == 'R':
                            print("[%s] %s(%s) - %s%s %s => %s%s" % (dtTime, Color.RED, sId,  sColor, sLabel, sRename, sFilename, Color.RST ));
                        else:
                            print("[%s] %s(%s) - %s%s %s%s" % (dtTime, Color.RED, sId,  sColor, sLabel, sFilename, Color.RST));
        
    def sortFileLog(self, dFileLog):
        dResult = {'other':{}}
        dCheckKey = self.typesort;

        for key in self.typesort:
            dResult[key] = {};

        for sOpera in dFileLog:
            for sFilename in dFileLog[sOpera]:
                bHasType = False;
                for sType in dCheckKey:
                    if dCheckKey[sType] in sFilename:
                        if sFilename not in dResult[sType]:
                            dResult[sType][sFilename] = {sOpera: {}};
                        
                        dResult[sType][sFilename][sOpera] = dFileLog[sOpera][sFilename];
                        bHasType = True;
                        break;
                
                if not bHasType:
                    if sFilename not in dResult['other']:
                        dResult['other'][sFilename] = {sOpera: {}};

                    dResult['other'][sFilename][sOpera] = dFileLog[sOpera][sFilename];

        return dResult;


if __name__ == '__main__':
    Pdiff();

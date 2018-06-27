#!coding: utf-8
import os
import sys

#Global contstant
if os.name == "nt":
    CR = "\r\n";

elif os.name == "posix":
    CR = "\n";

TAB = "    ";

def preProcess(content):
    content = content.replace("\r","");
    content = content.replace("\n","");
    elements = content.split(">");
    
    elements.pop();
    result = "";

    for elem in elements:
        if "strong" in elem or "<title" in elem:
            result += elem + ">";
        else:
            result += elem + ">" + CR;
    
    return result;


def autoTypeTab(content):
    TabDeepth = 0;
    elements = content.split(CR);

    Belem = ["<tr", "<td", "<table", "<head"];
    Eelem = ["</tr", "</td", "</table", "</head"];

    for elem in elements:
        for ee in Eelem:
            if ee in elem:
                TabDeepth -= 1;
                break;

        print (TAB * TabDeepth) + elem;

        for be in Belem:
            if be in elem:
                TabDeepth += 1;
                break;
        



if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Please special filename: ";
        sys.exit(2);

    filename = sys.argv[1];
    fp = open(filename , "r");
    content = fp.read();
    fp.close();

    res = preProcess(content)
    autoTypeTab(res);









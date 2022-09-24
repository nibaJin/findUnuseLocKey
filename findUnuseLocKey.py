# 找出Localizable.strings未使用的keys
# Aut: fujin
# 使用: 
# 参数说明：
# --fl=英文多语言文件地址
# --fd=项目根目录
# --delete= 是否直接删除无用的keys(默认为false)
# python findUnuseLocKey.py --fl=/Users/jinfu/Desktop/python练习/banggood/en.lproj/Localizable.strings --fd=/Users/jinfu/Desktop/python练习/banggood --delete=1
# 当前目录下生成文件：unuseLocKeys.txt(未使用到的key会生成个文件输出)

import os
import argparse

parser = argparse.ArgumentParser(description="需要传入两个参数，--string=国际化string路径  和 --dir=遍历的目录")
parser.add_argument('--fl', type=str, help="英文string路径，例如：--fl=banggood/en.lproj/Localizable.strings", required=True)
parser.add_argument('--fd', type=str, help="项目目录路径，例如：--fd=../banggood", required=True)
parser.add_argument('--delete', type=bool, help="是否删除未使用的keys，默认不删除", default=False, required=False)

# global val
ENPath = ''
KAllKeys = set()
KBlackFileList = ["TZImagePickControllerLocalizable.bundle"] #忽略文件

def sortStringKey(line):
    """从某一行赛选出strings key"""
    key = ''
    arr = line.split("=")
    if len(arr) >= 2:
        firstKey = arr[0].strip()
        second = arr[1].strip()
        if len(firstKey)>0 and firstKey[0] == "\"" and firstKey[-1] == "\"" and len(second)>0 and second[0] ==  "\"":
            key = firstKey
    return key


def featchLocalizableAllKeys ():
    """找出en文件所有的keys"""
    global ENPath
    f = open(ENPath)
    allKeys = set()
    for line in f:
        key = sortStringKey(line)
        if len(key)>0:
            allKeys.add(key)
    f.close()
    return allKeys
            
def filterUseKey(path):
    """过滤文件使用过的key"""
    global KAllKeys
    f = open(path)
    for line in f:
        KAllUseKeys = set()
        for key in KAllKeys:
            result = line.find(key)
            if result>0:
                KAllUseKeys.add(key)
        KAllKeys = KAllKeys-KAllUseKeys
    f.close()

def findUnuseLocalizableKeys(dirPath):
    """遍历dirPath目录下所有文件，并过滤使用过的key"""
    paths = os.listdir(dirPath)
    for path in paths:
        path = os.path.join(dirPath, path)
        if os.path.isdir(path):
            findUnuseLocalizableKeys(path)
        elif os.path.isfile(path) and os.path.splitext(path)[1]=='.m':
            print(path)
            filterUseKey(path)

def deleteAllLinesOfFile(path):
    """删除该路径的文件下未使用的keys， 同时删掉文件中的空行"""
    print("1")
    global KAllKeys
    fileContent = ""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            isFindLine = False
            if line.strip() == "": # 去掉空行
                isFindLine = True
                continue
            print(line)
            orginKey = sortStringKey(line)
            if len(orginKey)>0 and orginKey in KAllKeys:
                isFindLine = True
                print("发现未使用行：" + line)
            if isFindLine == False:
                fileContent += line
    # print("fileContent:" + fileContent)
    with open(path, "w", encoding="utf-8") as f:
        f.write(fileContent)


def deleteAllUnUseLines(dirPath):
    """删除掉所有未使用的key所在的行 和 删除空格行"""
    global KBlackFileList
    paths = os.listdir(dirPath)
    for path in paths:
        if path in KBlackFileList: #黑名单
            continue
        path = os.path.join(dirPath, path)
        if os.path.isdir(path):
            deleteAllUnUseLines(path)
        elif os.path.isfile(path) and os.path.basename(path) == 'Localizable.strings':
            print(path)
            deleteAllLinesOfFile(path)

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    ENPath = args.fl
    orginDir = args.fd
    delete = args.delete
    print(delete)
    print("英文string地址：",ENPath) 
    print("源目录：", orginDir)
    KAllKeys = featchLocalizableAllKeys()
    orginCnt = len(KAllKeys)
    findUnuseLocalizableKeys(orginDir)
    unuseCnt = len(KAllKeys)
    print("国际化语言没有使用到的key：\n")
    print(KAllKeys)
    print("总共keys: "+ str(orginCnt) + ",未使用的kyes: " + str(unuseCnt))
    f = open('unuseLocKeys.txt', 'w')
    for unusekey in KAllKeys:
        f.write(unusekey + '\n')
    f.close()
    if delete:
        print("开始删除。。。")
        deleteAllUnUseLines(orginDir)
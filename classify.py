'''
2017年11月10日更新：
每个章节单独一个文件夹；
以文件夹为单位归类。


只需要在此增加或删除想要的文件类型（扩展名）即可！
'''
extensionWanted = ['pdf', 'doc', 'docx']


'''
本函数功能：将好多的 pdf 或 word 文件自动按设备号归类（GEN012除外，GEN012要单独自己弄）。比如：
A000VOI123ZH_00.pdf 与 E100VOI123ZH_00.pdf 都放到一个VOI123文件夹里
C000PIN105ZH_00.pdf 放到PIN105文件夹里

使用时，把该脚本文件与一大把PDF文件放在一起，扔在同一个文件夹中

注意：
1、如果有的文件没被归类移到对应文件夹里，极有可能是对应文件夹里已经有这个文件了，所以程序默认取消了
   对该文件的复制。具体见本文档末尾的详细说明
2、GEN012因为文件名格式奇葩，所以还是手动自己搞下比较好。
'''
def getFileAndFolderList(p, extensionWanted):
    if p[-1] != '\\':
        p = p + '\\'
    a = os.listdir(p)
    files = []
    folders = []
    for x in a:
        if x.split('.')[-1].lower() in extensionWanted:
            files.append(x)
        elif os.path.isdir(p+x) and (len(x) == 15 or len(x) == 14):
            folders.append(x)
    return files, folders

import os, shutil
cwd = os.getcwd()
if cwd[-1]!='\\':
    cwd = cwd + '\\'
files, folders = getFileAndFolderList(cwd, extensionWanted) # 获得当前目录下 (current working directory) 的所有想要的列表

for chap in folders:
    eqp = chap[4:10]
    if not os.path.isdir(cwd+eqp):
        os.makedirs(cwd+eqp) # 如果第一次出现此设备，新建文件夹
    if not os.path.isdir(cwd+eqp+'\\'+chap):
        shutil.move(cwd+chap, cwd+eqp)
for pdf in files:
    eqp = pdf[4:10]

    if pdf[13].isdigit:
        chapter = pdf[:15]
    else:
        chapter = pdf[:14]
    chapter = chapter[:12] + '_' + chapter[13:]
    if not os.path.isdir(cwd+eqp):
        os.makedirs(cwd+eqp) # 如果第一次出现此设备，新建文件夹

    destination = cwd+eqp+'\\'+chapter
    if not os.path.isdir(destination):
        os.makedirs(destination) # 如果第一次出现此章节，新建文件夹
    if not os.path.isfile(destination+'\\'+pdf):
        shutil.move(cwd+pdf, destination) #如果不是第一次出现，那么文件夹肯定已经建好了，直接把文件挪过去。
        # 注意，文件如果已存在，则取消复制。比如之前你归类400个文件，运行此脚本，归类好后，又在文件夹里
        # 放了300个文件，结果这300个文件里有一个文件在之前的400个文件里已经有了，此时再跑此脚本，这个重复
        # 的文件不会再被归类移到对应文件夹里，而是孤零零地留在原来的位置。这时你要自己检查为啥重复了，如何取舍。


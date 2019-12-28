## Sail_vina打包版本
SailVina - Autodock Vina分子对接全套整合软件  
在线文档见：githubxxx
1. 介绍  
SailVina只是一个带界面的脚本，批量调用Autodock Vina，openbabel等来便捷使用Vina进行分子对接。
本软件可以实现以下功能：  
1.下载受体，自动准备受体。  
2.配体格式转换，根据取代基批量生成配体。  
3.验证对接方案(Protocol)是否可以还原实验结果。  
4.单个/多个配体和单个/多个受体进行对接。  
5.将对接的多个配体提取出来。  
6.提取对接的分数  
7.将配体和受体合并成一个文件。  
毕业临近，这应该是最终的版本了，不会再添加新功能。欢迎对项目进行再制作，本人也只是个业余喜欢编程的菜鸟，代码可能不太好看，欢迎交流讨论。
2. 安装SailVina  
必要软件（安装完整路径切记不要有中文和空格！！比如C:/program files/mgltools和D:/软件/mgltools等都是不合法的！!运行脚本是可能会出现意想不到的错误！）  
Mgltools(http://mgltools.scripps.edu/downloads)：用于调用pdbqt转换脚本。  
Openbabel(https://sourceforge.net/projects/openbabel/files/openbabel/2.4.1/)：用于格式转换。  
可选软件  
ChemOffice：用于化学结构的绘制和格式转换。  
Pymol：用于查看结构。  
2.1 使用python运行  
使用pip命令安装额外运行库：  
requests（下载受体）  
lxml（下载受体）  
Biopython（修复受体）  
scipy（计算RMSD）  
2.2 直接运行exe程序  
下载main.7z，解压后运行其中的main.exe即可。  
注意：解压路径不要包含空格，中文！！比如C:/Program files/、D:/软件/。会出现软件打不开，路径不识别等错误。  
3. 常用操作教程
使用本软件之前请务必点击“脚本配置”来选择相应的程序。
--------
后面有待补充

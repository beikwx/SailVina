# 主窗口文字
WINDOWS_TITLE = "SailVina"

# 切换卡文字
TAB1_TEXT = "准备受体"
TAB2_TEXT = "准备对接配置"
TAB3_TEXT = "准备配体"
TAB4_TEXT = "分子对接"
TAB5_TEXT = "工具"
TAB6_TEXT = "生成复合物"
TAB7_TEXT = "关于"
TAB8_TEXT = "其他工具"

# 帮助文本
TAB1_HELP_TEXT = "本界面用于下载和准备受体文件\n\n" \
                 "下载受体窗口\n" \
                 "1.输入pdbid（只能输入四位PDB代码）\n" \
                 "2.选择要保存的路径\n" \
                 "3.点击“开始下载”\n\n" \
                 "准备受体窗口\n" \
                 "1.点击“选择受体”选择要进行准备的单个pdb文件。点击“选择多个受体”选择包含多个pdb受体的文件夹\n" \
                 "2.点击“受体输出路径”选择输出目录。\n" \
                 "3.选择需要的参数。\n" \
                 "如果是单个受体，勾选biopython功能可以对某些蛋白进行自动修复。\n" \
                 "如果选择的是文件夹，将批量进行受体准备\n\n"

TAB2_HELP_TEXT = "本界面来生成Vina对接所需要的配置文件。\n\n" \
                 "操作步骤\n" \
                 "1.在“主要参数”、“可选”中填写数值\n" \
                 "2.选择输出目录，点击输出即可。\n\n" \
                 "工具的使用\n" \
                 "1.如果有要修改的config文件，通过“读取配置文件”来进行读取。" \
                 "选择相应的config.txt，点击读取到参数，修改后再输出即可。\n" \
                 "2.本工具可以使用共晶位点中的配体来自动计算对接位点，" \
                 "\n参考文献：Feinstein WP, Brylinski M. (2015) Calculating an optimal box size for ligand docking and " \
                 "virtual screening against experimental and predicted binding pockets. J Cheminform 7 (1):18\n" \
                 "注意：选择的配体必须是pdbqt格式，可以使用ADT或者在“准备受体”中提取配体。"

TAB3_HELP_TEXT = "本界面用于进行对接配体的格式转换\n\n" \
                 "操作步骤\n" \
                 "1.在“脚本配置”中选择ADT中的python.exe文件（需要安装mgltools，详情见教程）\n" \
                 "2.在“输入选项”中选择输入格式，选择配体或者配体所在的文件夹\n" \
                 "3.在“输出选项”中选择输出格式，输入转换格式的pH值，是否生成" \
                 "3D构象，是否进行能量最小化，选择能量最小化的力场，选择要输出配体的文件夹\n" \
                 "4.点击开始转换。\n\n" \
                 "脚本说明\n" \
                 "由于格式转化调用的是obabel的格式转换功能，obabel转换成pdbqt文件会出现问题，导致苯环断裂" \
                 "等问题。所以当转换成pdbqt文件时，先通过obabel转换成pdb文件，再通过adt的方法转换成pdbqt格式，" \
                 "所以进度条会显示两遍。"

TAB4_HELP_TEXT = "本界面用于调用vina进行分子对接\n\n" \
                 "操作步骤\n" \
                 "1.选择配体\n" \
                 "2.选择受体\n" \
                 "3.选择结果输出的文件夹\n" \
                 "4.输入每个配体要对接的次数\n" \
                 "5.点击开始对接\n\n" \
                 "对接说明\n" \
                 "1.选择的配体只能是pdbqt文件或者含有pdbqt文件的文件夹\n" \
                 "2.选择的受体是一个文件夹，受体在文件夹中，必须命名为“preped.pdbqt”" \
                 "否则无法识别，并且需要config.txt文件，否则无法对接。\n" \
                 "如果要对多个受体进行对接，请选择包含这些受体文件夹的文件夹。比如要对接的" \
                 "受体为A、B、C，分别为C:/receptors/A，C:/receptors/B，C:/receptors/C，选择" \
                 "C:/receptors即可。"

TAB5_HELP_TEXT = "工具"

TAB6_HELP_TEXT = "本界面用于生成配体-受体复合物\n\n" \
                 "操作步骤\n" \
                 "1.选择输入配体\n" \
                 "2.选择受体（只支持pdbqt格式）\n" \
                 "3.选择输入文件夹\n" \
                 "4.点击“结合”\n\n" \
                 "说明\n" \
                 "1.对于对接生成的pdbqt文件，可以直接选择构象结合\n" \
                 "2.脚本首先将pdbqt文件转换成pdb文件再结合生成pdb文件。"

TAB7_HELP_TEXT = "SailVina\n\n" \
                 "本软件由python的Tkinter开发，调用biopython（受体准备），mgltools（准备配体，受体）" \
                 "，openbabel（格式转化，文件合并）\n\n" \
                 "开发者：beikwx\n" \
                 "Bug及反馈邮箱：studyforever0225@gmail.com\n" \
                 "Github开源地址：https://github.com/beikwx/SailVina\n" \
                 "我的个人博客：https://beikwx.top/\n\n" \
                 "感谢提出意见和bug反馈的各位同学，本人读研事情也比较多，平时偶尔用到分子对接，但是现在对接没有" \
                 "一个好用的GUI，所以想编写这个软件一劳永逸，更新较慢，如果有好的想法希望多多交流。\n\n" \
                 "Happy docking!"

TAB8_HELP_TEXT = "其他工具都放在这里"
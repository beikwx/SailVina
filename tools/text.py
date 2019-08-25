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

# 帮助文本
TAB1_HELP_TEXT = "本界面用于下载和准备受体文件\n\n" \
                 "操作步骤\n" \
                 "下载受体\n" \
                 "1.输入pdbid（只能输入四位代码）\n" \
                 "2.选择要保存的路径\n" \
                 "3.点击“开始下载”\n\n" \
                 "准备受体\n" \
                 "1.点击“选择受体”选择要进行准备的pdb文件。可以是单个文件，也可以是包含pdb文件的文件夹\n" \
                 "2.点击“受体输出路径”选择输出目录。\n" \
                 "3.选择需要的参数，点击“准备受体”，根据提示操作即可。\n\n"

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

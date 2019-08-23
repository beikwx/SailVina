from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilenames


class SFile(object):

    @staticmethod
    def open_file(initial_dir, title, file_type, parent=""):
        if parent == "":
            filename = askopenfilename(initialdir=initial_dir, title=title,
                                       filetypes=(("%s文件" % file_type, "*.%s" % file_type), ("所有文件", "*.*")))
            if filename == "":
                return initial_dir
            return filename
        else:
            filename = askopenfilename(parent=parent, initialdir=initial_dir, title=title,
                                       filetypes=(("%s文件" % file_type, "*.%s" % file_type), ("所有文件", "*.*")))
            if filename == "":
                return initial_dir
            return filename

    @staticmethod
    def open_files(initial_dir, title, file_type):
        filenames = askopenfilenames(initialdir=initial_dir, title=title,
                                     filetypes=(("%s文件" % file_type, "*.%s" % file_type), ("所有文件", "*.*")))
        if filenames == "":
            return initial_dir
        filename_text = ""
        for filename in filenames:
            filename_text += "%s;" % filename
        return filename_text

    @staticmethod
    def open_dir(initial_dir, title):
        dir_name = askdirectory(initialdir=initial_dir, title=title)
        if dir_name == "":
            return initial_dir
        return dir_name

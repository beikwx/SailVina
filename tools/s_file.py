import os
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
            sep_name = str(filename).replace("/", os.sep)
            return sep_name
        else:
            filename = askopenfilename(parent=parent, initialdir=initial_dir, title=title,
                                       filetypes=(("%s文件" % file_type, "*.%s" % file_type), ("所有文件", "*.*")))
            if filename == "":
                return initial_dir
            sep_name = str(filename).replace("/", os.sep)
            return sep_name

    @staticmethod
    def open_files(initial_dir, title, file_type, parent=""):
        if parent != "":
            filenames = askopenfilenames(parent=parent, initialdir=initial_dir, title=title,
                                         filetypes=(("%s文件" % file_type, "*.%s" % file_type), ("所有文件", "*.*")))
            if filenames == "":
                return initial_dir
            filename_text = ""
            for filename in filenames:
                filename_text += "%s;" % filename
            sep_filename = str(filename_text).replace("/", os.sep)
            return sep_filename
        else:
            filenames = askopenfilenames(initialdir=initial_dir, title=title,
                                         filetypes=(("%s文件" % file_type, "*.%s" % file_type), ("所有文件", "*.*")))
            if filenames == "":
                return initial_dir
            filename_text = ""
            for filename in filenames:
                filename_text += "%s;" % filename
            sep_filename = str(filename_text).replace("/", os.sep)
            return sep_filename

    @staticmethod
    def open_dir(initial_dir, title, parent=""):
        if parent != "":
            dir_name = askdirectory(parent=parent, initialdir=initial_dir, title=title)
            if dir_name == "":
                return initial_dir
            sep_dir_name = str(dir_name).replace("/", os.sep)
            return sep_dir_name
        else:
            dir_name = askdirectory(initialdir=initial_dir, title=title)
            if dir_name == "":
                return initial_dir
            sep_dir_name = str(dir_name).replace("/", os.sep)
            return sep_dir_name

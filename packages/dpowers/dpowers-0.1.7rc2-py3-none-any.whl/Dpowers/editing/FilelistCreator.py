#
#
# Copyright (c) 2020-2025 DPS, dps@my.mail.de
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#
import os, warnings, sys, random, functools, shutil
from collections import defaultdict
from contextlib import contextmanager, redirect_stdout
path=os.path

from Dhelpers.boolean_function import BooleanFunction


class Filelist(BooleanFunction):
    creator = None
    def __init__(self, name=None, func=None, add=True, **kwargs):
        self.last_found_paths=[]
        if name is None: add = False
        if not func:
            if not kwargs: raise ValueError
            func = lambda obj: self.creator.default_selection_func(obj, **kwargs)
        BooleanFunction.__init__(self, name, func)
        if add: self.creator.add_inst(self)


class FilelistCreator:
    editor_class = None
    filelist_extension = ""
    file_start = ""
    allowed_file_extensions = "inherit"
    Filelist = None
    

    def _file_allowed(self, file):
        if self.allowed_file_extensions == "inherit":
            allowed_ext =  self.editor_class.allowed_file_extensions
        else:
            allowed_ext = self.allowed_file_extensions
        ext = os.path.splitext(file)[-1]
        if ext in allowed_ext: return True
        return False
    
    def __init__(self, basepath=None, destpath=None,insert_initial=None):
        filelist_cls = type(f"Filelist", (Filelist,), {})
        filelist_cls.creator = self
        self.Filelist = filelist_cls
        self.basepath = basepath
        self.destpath = destpath
        self.filelist_objs = {}
        self.file_paths = {}
        self.imported_lists = None
        self.filelist_combinations = list()
        self._custom_file_func = NotImplemented
        self.insert_initial = insert_initial
        
    @property
    def destpath(self):
        if not self._destpath and self.basepath:
            parent = os.path.split(self.basepath)[0]
            return os.path.join(parent, "__Playlists")
        return self._destpath
        
    @destpath.setter
    def destpath(self, val):
        self._destpath = val
        
    
    def add(self, name, func=None, **kwargs):
        new_inst = self.Filelist(name,func=func, **kwargs)
        self.add_inst(new_inst)
    
    def add_inst(self, filelist_inst):
        assert isinstance(filelist_inst, self.Filelist)
        name = filelist_inst.name
        self.filelist_objs[name] = filelist_inst
        self.file_paths[name] = filelist_inst.last_found_paths  #shortcut

    @staticmethod
    def default_selection_func(obj, case_sensitive=False, exact_match=False,
            **kwargs):
        for attr_name, value in kwargs.items():
            string = str(getattr(obj, attr_name))
            value = str(value)
            if not case_sensitive:
                value = value.lower()
                string = string.lower()
            if exact_match:
                if value != string: return False
            else:
                if value not in string: return False
        return True
    
    def find_files(self, *names, suppress_error=True, warn=True):
        for dirpath, _, files in os.walk(self.basepath):
            with self.Filelist.use_cache() as reset_cache:
                for file in files:
                    if not self._file_allowed(file): continue
                    file = os.path.realpath(os.path.join(dirpath, file))
                    try:
                        with self.editor_class(file) as obj:
                            for name in names:
                                filelist_obj = self.filelist_objs[name]
                                if filelist_obj(obj): yield name, file
                    except Exception as e:
                        if not suppress_error: raise
                        if warn:
                            warnings.warn(f"\nerror with file {file}:\n{e}")
                            print()
                    finally:
                        reset_cache()
    
    def assemble_lists(self, *names, **kwargs):
        if not names: names = self.file_paths.keys()
        for name in names:
            self.file_paths[name].clear()
        for name, file in self.find_files(*names, **kwargs):
            # print(name,file)
            self.file_paths[name].append(file)
    
    
    def write_paths(self, *names, assemble=True, insert_initial=None,
            overwrite = True, **kwargs):
        if assemble: self.assemble_lists(*names, **kwargs)
        print("Creating playlists:")
        os.makedirs(self.destpath, exist_ok=True)
        for name, file_path_list in self.file_paths.items():
            self._write_filelist(name,file_path_list, self.destpath,
                    insert_initial=insert_initial, overwrite=overwrite)
            
            
    def _write_filelist(self, name, file_path_list, path, overwrite=True,
            insert_initial = None):
        if insert_initial is None: insert_initial = self.insert_initial
        fpath_base = os.path.join(path, name)
        fpath = fpath_base + self.filelist_extension
        if overwrite is False:
            num = 0
            while os.path.isfile(fpath):
                num += 1
                fpath = fpath_base + "__" + str(num) + self.filelist_extension
        with open(fpath, "w") as new:
            new.write(self.file_start + "\n")
            if insert_initial:
                new.write(self.get_custom_file(insert_initial)+"\n")
            for file in file_path_list:
                new.write(file + "\n")
        print(f"{name}: {len(file_path_list)} songs in {fpath}")



    def import_lists(self, destpath=None, add_ext=()):
        if destpath is None: destpath = self.destpath
        allowed_ext = (self.filelist_extension,) + add_ext
        self.imported_lists = defaultdict(list)
        for file in os.listdir(destpath):
            name, ext = os.path.splitext(file)
            if ext not in allowed_ext: continue
            with open(os.path.join(destpath,file), "r") as opened:
                last_line = ""
                while last_line == "": last_line = opened.readline().strip()
                if self.insert_initial:
                    initial_lines = self.get_custom_file(
                            self.insert_initial).split("\n")
                    for in_line in initial_lines:
                        if in_line.strip() != last_line:
                            raise ValueError(in_line, last_line)
                        last_line = opened.readline().strip()
                        #this will pop out the initial lines before importing
                self.imported_lists[name].append(last_line)
                for line in opened.readlines():
                    self.imported_lists[name].append(line.strip())
        return self.imported_lists
    
    def define_combination(self, *args, **kwargs):
        c = FilelistCombination(self, *args,**kwargs)
        self.filelist_combinations.append(c)
        return c
    
    def write_combinations(self, *args,**kwargs):
        for c in self.filelist_combinations: c.write(*args,**kwargs)
        
    def get_custom_file(self, name_or_number):
        if self._custom_file_func is NotImplemented: raise NotImplementedError
        file = self._custom_file_func(self, name_or_number)
        if not os.path.isfile(file): raise FileNotFoundError(file)
        return file
    
    def custom_file_finder(self, func):
        """A decorator to define the function returning files for
        get_custom_file()"""
        self._custom_file_func = func
        return func

        
    def copy_files(self, filelist, dest_folder, numerate=False):
        os.makedirs(dest_folder)
        if isinstance(filelist, self.Filelist): filelist=filelist.name
        if isinstance(filelist, str):
            filelist = self.imported_lists[filelist]
        print(f"Copying {len(filelist)} files to {os.path.realpath(dest_folder)} ...")
        num = 0
        new_names = []
        for file in filelist:
            new_name = path.split(file)[1]
            if numerate:
                num += 1
                new_name = f"{num}__{new_name}"
            new_full_name = path.join(dest_folder, new_name)
            shutil.copy(file, new_full_name)
            new_names.append(new_full_name)
        print("Done.")
        return new_names

class FilelistCombination:
    
    def __init__(self, playlist_creator, name, file_list_names,*, insert=None,
            insert_initial=None, from_imported=True, destpath=None,
            avoid_double=True):
        # insert can be a file path or name of a previously defined
        # FileList. It will be inserted in between every entry. (Useful for
        # silence between music tracks e.g.)
        self.name = name
        self.creator = playlist_creator
        assert isinstance(file_list_names, (tuple, list))
        self.file_lists = file_list_names
        self.insert = insert
        self.insert_initial = insert_initial
        self.from_imported = from_imported
        self.destpath = destpath
        self.avoid_double = avoid_double
        
    def _process_fileinfo(self, list_info, defined_lists):
        if isinstance(list_info, self.creator.Filelist):
            list_info = list_info.name
            if not list_info: raise ValueError
        if list_info in defined_lists:
            return random.choice(defined_lists[list_info])
            #first, check if a FileList has been defined with that name
            # if not, then try to interpret the given name as an argument for
            # custom_file_finder
        else:
            return self.creator.get_custom_file(list_info)
    
    def create(self, insert=None, insert_initial=None, from_imported=None):
        if insert is None: insert = self.insert
        if insert_initial is None: insert_initial = self.insert_initial
        if from_imported is None: from_imported = self.from_imported
        creator = self.creator
        lists = creator.imported_lists if from_imported else creator.file_paths
        seq = list()
        clean_seq = list()
        if insert_initial:
            seq.append(self._process_fileinfo(insert_initial, lists))
        for name in self.file_lists:
            file = self._process_fileinfo(name, lists)
            if file:
                while self.avoid_double and file in clean_seq:
                    # by default, avoid picking the same file twice
                    file = self._process_fileinfo(name, lists)
                seq.append(file)
                clean_seq.append(file)
            if insert:
                if os.path.isfile(insert):
                    seq.append(insert) #just return the input, in case it is a
                    # explicit path
                else:
                    seq.append(self._process_fileinfo(insert, lists))
        return seq, clean_seq
    
    def write(self, name=None, destpath=None, overwrite=True,
            copy=False,**kwargs):
        name = name if name else self.name
        if not destpath:
            destpath = self.destpath if self.destpath else "combinations"
        if not path.isabs(destpath):
            destpath = path.join(self.creator.destpath, destpath)
        destpath = path.join(destpath, name)
        copy_folder = name+"_files"
        filelist, clean_filelist = self.create(**kwargs)
        #print(filelist)
        os.makedirs(destpath, exist_ok=True)
        writelist = filelist
        if copy is True:
            writelist = [path.join(copy_folder,path.split(file)[1]) for file in
                filelist]
        self.creator._write_filelist(name, writelist, destpath,
                overwrite=overwrite, insert_initial = False)
        
        try:
            print_command = self.creator.print_tags_to_file
        except AttributeError:
            pass
        else:
            print_command(clean_filelist, destpath, name, header=True)
                    
        if copy is True:
            copypath = path.join(destpath, copy_folder)
            if os.path.isdir(copypath): shutil.rmtree(copypath)
            self.creator.copy_files(filelist, copypath, numerate=False)
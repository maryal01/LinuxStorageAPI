from django.core.files.storage import  FileSystemStorage
import os
import shutil
import tarfile
from pprint import pprint

#difference between getFile, saveFile and copyFile?
# There are linux files and iRODS files. 
# getfile gets a file from iRODS to linux. 
# saveFile puts a file into iRODS from linux. 
# copyFile copies a file from one iRODS place to another. 
# Right now, the code uploads to /tmp, calls saveFile to save. 
# This is just cp. 
# When doing things with files it does getFile to /tmp, then processes. 
# This is also a cp in your case. 
# copyFile is a cp from one place to another. 

class LinuxStorage(FileSystemStorage):
        @property
        def getUniqueTmpPath(self):
                pass

        def download(self, name):
                return self.open(name, mode='rb')

        def getFile(self, source_name, destination_name):
                self.saveFile(source_name, destination_name)

        #do we need to implement this?
        # this is zip. You need to run the zip. 
        # these are not created equal. They're called elsewhere in the 
        # code and mostly they run zip. 
        def runBagitRule(self, rule_name, input_path, input_resouce):
                pass#irule

        #are input_name and output_name files or directories?
        # input_name is directory, output_name is zipfile
        def zipup(self, input_name, output_name):
                file_name = output_name.rsplit("/", 1)[1]
                tar = tarfile.open(file_name + ".tar.gz", "w:gz")
                tar.add(input_name, arcname=output_name)
                tar.close()

        def unzip(self, zip_file_path, unzipped_folder=None):
                abs_path = os.path.dirname(zip_file_path)
                if not unzipped_folder:
                        unzipped_folder = os.path.splitext(os.path.basename(zip_file_path))[0].strip()

                unzipped_folder = self._get_nonexistant_path(os.path.join(abs_path, unzipped_folder))
                tar = tarfile.open(zip_file_path)
                for member in tar.getmembers():
                        tar.extract(member, path=unzipped_folder)
                        tar.close()
                return unzipped_folder

        def _get_nonexistant_path(self, path):
                if not os.path.exists(path):
                        return path
                i = 1
                new_path = "{}-{}".format(path, i)
                while os.path.exists(new_path):
                        i += 1
                        new_path = "{}-{}".format(path, i)
                return new_path

        #do we need to implement this?
        # it needs to do what the other one did as return value. 
        # what this does is to store metadata associated with the file. 
        # mostly it is not necessary to do anything, but the return value
        # should be the same as for the original routine. 
        def setAVU(self, name, attName, attVal, attUnit=None):
                pass#imeta

        #do we need to implement this?
        # always return False
        # I can generate the default AVUs for everything. 
        # There is a lookup table for each one and its default value. 
        # look up the name and return the default value. 
        def getAVU(self, name, attName):
                pass#imeta

        #src_name and dest_name can be either directory or a file name
        def copyFiles(self, src_name, dest_name, ires=None):
                if src_name and dest_name:
                        if os.path.exists(dest_name):
                                shutil.rmtree(dest_name)
                        shutil.copytree(src_name, dest_name)
                return

        def moveFile(self, src_name, dest_name):
                if src_name and dest_name:
                        if os.path.exists(dest_name):
                                shutil.rmtree(dest_name)
                        shutil.move(src_name, dest_name)
                return

        def saveFile(self, from_name, to_name, create_directory=False, data_type_str=''):
                if create_directory:
                        splitstrs = to_name.rsplit('/', 1)
                        os.makedirs(splitstrs[0])
                        if len(splitstrs) <= 1:
                                return
                with open(from_name, 'r') as content_file:
                        content = content_file.read()
                        self.save(to_name, content)
                return

        #formatting of this? os.listdir(path) returns the list of content in that directory
        # the code is expecting a specific format. Look at what ils 
        # does and duplicate. You can also read the django docs on what 
        # this should return. 
        #SOLUTION == create management command in through ssh --- home
        def ils_l(self, path): 
                return os.listdir(path)


#where are the files uploaded being stored? if it is a different place,
# i need to use self.exists(path) rather than os.path.exists(path)?
# self.exists(path) is relative. 
# os.path.exists(path) is absolute. 
# if path starts with / these are the same. 
# if not, default directory prefix is added. 
# you can make up the prefix. Put in settings.py for now. 
# that directory will store all resources in the pattern 
# $dir/{resource_id}/data/contents/.....
# $dir/bags/{resource_id}.zip is the zipfile of that. 


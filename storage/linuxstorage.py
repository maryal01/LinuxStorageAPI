from django.core.files.storage import  FileSystemStorage
import os, tarfile, shutil, errno
from pprint import pprint

IRODS_PATH = "./irods/"
class LinuxStorage(FileSystemStorage):

        def prepend_path(path):
                if(not os.path.exists(IRODS_PATH)):
                        os.makedirs(IRODS_PATH)        
                if( path[0] != "/" ):
                        path = path[2:] if path[0:2] == "./" else path
                        return IRODS_PATH + path
                else:
                        return path
        
        @property
        def getUniqueTmpPath(self):
                pass

        def download(self, name):
                irods_name = self.prepend_path(name)
                return self.open(irods_name, mode='rb')

        def runBagitRule(self, rule_name, input_path, input_resouce):
                pass #irule

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
        '''
                What is AVU doing?
                setAVU -- stores the metadata associated with the file
                getAVU -- There is a lookup table for each one and its deafault value; check that and return the default value

                Alva: he will generate default AVUs for everything.
        '''
        def setAVU(self, name, attName, attVal, attUnit=None):
                pass

        def getAVU(self, name, attName):
                return False




##########################################################################################################################

        def removeDirecotry(self, dirname):
                directory = self.prepend_path(dirname)
                if(os.path.isfile(directory)):
                        os.remove(directory)
                elif(os.path.isdir(directory)):
                        shutil.rmtree(directory)

        # copies files or directories recursively within irods
        def copyFiles(self, src_name, dest_name, ires=None):
                src_irods = self.prepend_path(src_name)
                dest_irods = self.prepend_path(dest_name)
                try:
                        shutil.copytree(src_irods, dest_irods)
                except FileExistsError as e: 
                        # if a dest_name is already present, create a directory within dest_name
                        dest_irods = dest_irods + "/" + src_irods.rsplit("/",1)[1]
                        shutil.copytree(src_irods, dest_irods)
                except NotADirectoryError as exc: 
                        # if copying a file, use shutil.copy
                        if(not os.path.exists(dest_irods.rsplit('/', 1)[0])):
                                os.makedirs(dest_irods.rsplit('/', 1)[0]) 
                        shutil.copy(src_irods, dest_irods)

        # moves (copy and remove the source directory) files or directories recursively
        def moveFile(self, src_name, dest_name):
                self.copyFiles(LinuxStorage, src_name, dest_name)
                self.removeDirecotry(LinuxStorage, src_name)
        
        # copies files or directories recursively from linux to irods
        def saveFile(self, from_name, to_name, create_directory=False, data_type_str=''):
                if create_directory == True:
                        splitted_directory = to_name.rsplit("/",1)
                        os.makedirs(splitted_directory[0])
                        if (len(splitted_directory) <= 0):
                                return
                else:
                        if from_name:
                                dest_irods = self.prepend_path(to_name)
                                try:
                                        shutil.copytree(from_name, dest_irods)
                                except FileExistsError as e: 
                                        # if a dest_name is already present, create a directory within dest_name
                                        dest_irods = dest_irods + "/" + from_name.rsplit("/",1)[1]
                                        shutil.copytree(from_name, dest_irods)
                                except NotADirectoryError as exc: 
                                        # if copying a file, use shutil.copy
                                        if(not os.path.exists(dest_irods.rsplit('/', 1)[0])):
                                                os.makedirs(dest_irods.rsplit('/', 1)[0]) 
                                        shutil.copy(from_name, dest_irods)

        # copies files or directories recursively from irods to linux
        def getFile(self, source_name, destination_name):
                src_irods = self.prepend_path(source_name)
                try:
                        shutil.copytree(src_irods, destination_name)
                except FileExistsError as e: 
                        # if a dest_name is already present, create a directory within dest_name
                        destination_name = destination_name + "/" + src_irods.rsplit("/",1)[1]
                        shutil.copytree(src_irods, destination_name)
                except NotADirectoryError as exc: 
                        # if copying a file, use shutil.copy
                        if(not os.path.exists(destination_name.rsplit('/', 1)[0])):
                                os.makedirs(destination_name.rsplit('/', 1)[0]) 
                        shutil.copy(src_irods, destination_name)

        def ils_l(self, path): 
                return os.listdir(path)

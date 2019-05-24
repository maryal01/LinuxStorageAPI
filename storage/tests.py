from django.test import TestCase
from storage.linuxstorage import LinuxStorage
import os, shutil

class LinuxStorageTest(TestCase):
    def setUp(self):
        if (not os.path.exists("./test")):
            os.makedirs("./test/subtest1")
            os.makedirs("./test/subtest2")
            os.chdir("./test")
            open("testfile.txt","w+")
            os.chdir("./subtest1")
            open("testfile11.txt", "w+")
            open("testfile12.txt", "w+")
            os.chdir("../subtest2")
            open("testfile21.txt", "w+")
            open("testfile22.txt", "w+")
            os.chdir("../../")
        
    def tearDown(self):   
        for root, dirs, files in os.walk("./test", topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.removedirs(os.path.join(root, name))

    def test_savefile(self):
        LinuxStorage.saveFile(LinuxStorage, "./test/subtest2/testfile21.txt", "test2")
        self.assertTrue(os.path.exists("./irods/test2"))

        LinuxStorage.saveFile(LinuxStorage, "./test/subtest1", "test1")
        LinuxStorage.saveFile(LinuxStorage, "./test/subtest1", "test1")
        self.assertTrue(os.path.exists("./irods/test1"))
        self.assertTrue(os.path.exists("./irods/test1/subtest1"))
        self.assertTrue(os.path.exists("./irods/test1/testfile11.txt"))
        self.assertTrue(os.path.exists("./irods/test1/testfile12.txt"))
        shutil.rmtree("./irods")

    def test_movefile(self):
        LinuxStorage.saveFile(LinuxStorage, "./test", "./")
        print("Here!!!")
        #file --> directory
        LinuxStorage.moveFile(LinuxStorage, "test/testfile.txt", "test/subtest1")
        self.assertTrue(os.path.exists("./irods/test/subtest1/testfile.txt"))
        self.assertFalse(os.path.exists("./irods/test/testfile.txt"))
        
        #directory -> directory
        LinuxStorage.moveFile(LinuxStorage, "test/subtest2", "test/subtest1")
        self.assertTrue(os.path.exists("./irods/test/subtest1/subtest2/testfile21.txt"))
        self.assertTrue(os.path.exists("./irods/test/subtest1/subtest2/testfile22.txt"))
        self.assertFalse(os.path.exists("./irods/test/subtest2"))
        
        #file -> file
        #read the testfile11.txt
        LinuxStorage.moveFile(LinuxStorage, "test/subtest1/testfile11.txt", "test/subtest1/subtest2/testfile22.txt")
        #read the testfile22.txt
        self.assertFalse(False)
        
        shutil.rmtree("./irods")
    
    def test_getfile(self):
        pass
    
    def test_copyfile(self):
        self.assertTrue(True)


'''
storage class methods     | filesystem storage class
open                      | base_location
save                      | location
get_valid_name            | base_url
get_available_name ..     | file_permissions_mode
generate_filename         | directory_permissions_mode
path                      | get_storage_class
delete ..
exists ..
lsitdir ..
size ..
url ..
get_accessed_time
get_created_time
get_modified_time
'''
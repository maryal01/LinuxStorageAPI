from django.test import TestCase
from storage.linuxstorage import LinuxStorage

class LinuxStorageTest(TestCase):
    def test_basic_addition(self):
        
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
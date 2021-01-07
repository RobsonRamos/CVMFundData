import unittest
import sys
sys.path.append('../etl/')
import CVMDataLoader

class TestProject(unittest.TestCase):

    def TestDownload(self):
        loader = CVMDataLoader()
        loader.downloadFile('201701')
     
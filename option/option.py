import argparse


class Option:
    """
    Options for extracting or gathering
    """
    def __init__(self, select: str):
        self.select = select
        
    def initialize(self):
        arg = argparse.ArgumentParser()
        if self.select == 'extract':
            arg.add_argument('--img_folder', '-if', type=str, help='path of image folder')
            arg.add_argument('--output', '-op', type=str, default='../output/', help='path of output folder')
            arg.add_argument('--txt_file', '-tf', type=str, default='conversation_data_ext.txt', help='txt_file name')
        if self.select == 'collect':
            arg.add_argument('--txt_folder', '-txt_f', type=str, help='path of dir containing txt files')
            arg.add_argument('--output', '-op', type=str, default='../output/', help='path of output folder')
            arg.add_argument('--txt_file', '-tf', type=str, default='conversation_data_col.txt', help='txt_file name')            
        return arg.parse_args()
    
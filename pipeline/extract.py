import cv2
import os
import sys
import os.path as osp
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))
from util.util import Extract, merge_content
from option.option import Option


def main(opt):
    img_file_names = [f for f in os.listdir(opt.img_folder) if osp.isfile(osp.join(opt.img_folder, f))]
    dir_names = [f for f in os.listdir(opt.img_folder) if os.path.isdir(osp.join(opt.img_folder, f))]
    save_path = osp.join(opt.output, opt.txt_file)
    with open(save_path, 'w', encoding='utf-8') as f:
        for id, name in enumerate(img_file_names):
            img_path = osp.join(opt.img_folder, name)
            img = cv2.imread(img_path)
            paragr_infor = Extract(img).extracted_paragrs
            for para in paragr_infor:
                f.write(merge_content(para[0])+"\n")
            if id != len(name) - 1:
                f.write("!......!\n")
                f.write("\n")
        
        for id2, name2 in enumerate(dir_names):
            dir_path = osp.join(opt.img_folder, name2)
            subfile_names = [f for f in os.listdir(dir_path) if osp.isfile(osp.join(dir_path, f))]
            for sub_name in subfile_names:
                sub_path = osp.join(dir_path, sub_name)
                img = cv2.imread(sub_path)
                paragr_infor = Extract(img).extracted_paragrs
                for para in paragr_infor:
                    f.write(merge_content(para[0])+"\n")
            if id2 != len(name2):
                f.write("!......!\n")
                f.write("\n")
            
    
if __name__ == "__main__":
    opt = Option('extract').initialize()
    main(opt)
        
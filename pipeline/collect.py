import os
import os.path as osp
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(osp.join(__dir__, '..'))
from option.option import Option


def main(opt):
    save_path = osp.join(opt.output, opt.txt_file)
    with open(save_path, 'w', encoding='utf-8') as f:
        txt_files = [f for f in os.listdir(opt.txt_folder) if f.find('.txt') != -1]
        for id, txt_name in enumerate(txt_files):
            txt_file_path = os.path.join(opt.txt_folder, txt_name)
            with open(txt_file_path, 'r', encoding='utf-8') as g:
                a = g.readlines()
                if a[-1][-1:] != '\n':
                    f.writelines(a)
                    f.write("\n")
                else:
                    f.writelines(a)
            if id != len(txt_files) - 1:
                f.write("\n")
    
    
if __name__ == "__main__":
    opt= Option("collect").initialize()    
    main(opt)
    
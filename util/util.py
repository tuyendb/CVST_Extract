import pytesseract
from pytesseract import Output
import PIL.Image as Image
    

def merge_content(lines_ct: list) -> str:
        content = ""
        for line in lines_ct:
            for word in line:
                content += word + ' '
        return content
    
    
class Extract:
    """extract text from img by tesseract
    """
    def __init__(self, img):
        self.img = img
        
    @property
    def raw_text_features(self) -> dict:
        text_infor = None
        if text_infor is None:
            text_infor = pytesseract.image_to_data(self.img, lang='vie', output_type=Output.DICT)
        return text_infor
    
    @property
    def processed_text_features(self) -> dict:
        prc_text_infor = None
        if prc_text_infor is None:
            prc_text_infor = self.raw_text_features.copy()
            remove_ids = []
            for id, conf in enumerate(prc_text_infor['conf']):
                if conf == '-1' or conf < 40:
                    remove_ids.append(id)
            for key in prc_text_infor.keys():
                for id, val in enumerate(remove_ids):
                    del prc_text_infor[key][val - id]
        return prc_text_infor
    
    @property
    def extracted_paragrs(self) -> list:
        paragraphs_infor = None
        if paragraphs_infor is None:
            ptf = self.processed_text_features.copy()
            extract_ids = {}
            for ch_id in range(ptf['block_num'].__len__()):
                if not bool(extract_ids):
                    extract_ids = {1: {1: {1: [ch_id]}}}
                else:
                    max_block_num = (list(extract_ids.keys()))[-1]
                    max_par_num = (list(extract_ids[max_block_num].keys()))[-1]
                    max_line_num = (list(extract_ids[max_block_num][max_par_num].keys()))[-1]
                    if ptf['block_num'][ch_id] != max_block_num:
                        extract_ids[max_block_num + 1] = {1: {1: [ch_id]}}
                    else: 
                        if ptf['par_num'][ch_id] != max_par_num:
                            extract_ids[max_block_num][max_par_num + 1] = {1: [ch_id]}
                        else:
                            if ptf['line_num'][ch_id] != max_line_num:
                                extract_ids[max_block_num][max_par_num][max_line_num + 1] = [ch_id]
                            else:
                                extract_ids[max_block_num][max_par_num][max_line_num].append(ch_id)
            paragraphs_infor = []
            for bl in extract_ids.keys():
                for par in extract_ids[bl].keys():
                    pr_lines_ct = []
                    pr_lines_coords = []
                    for line in extract_ids[bl][par].keys():
                        begin_id = extract_ids[bl][par][line][0]
                        end_id = extract_ids[bl][par][line][-1]
                        b_x, b_y, b_w, b_h = ptf['left'][begin_id], ptf['top'][begin_id], ptf['width'][begin_id], ptf['height'][begin_id]
                        e_x, e_y, e_w, e_h = ptf['left'][end_id], ptf['top'][end_id], ptf['width'][end_id], ptf['height'][end_id]
                        x1, y1, x2, y2 = b_x, min(b_y, e_y), e_x + e_w, max(b_y + b_h, e_y, e_h)
                        pr_lines_coords.append([x1, y1, x2, y2])
                        line_ct = []
                        for word_idx in extract_ids[bl][par][line]:
                            line_ct.append(ptf['text'][word_idx])
                        pr_lines_ct.append(line_ct)
                    paragraphs_infor.append([pr_lines_ct, pr_lines_coords])
            return paragraphs_infor
        
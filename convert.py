import cv2
import numpy as np

base_width = 4
base_height = 4

cell_width = base_width
cell_height = base_height
symbol_size = 1

gs_presets = np.array([[.114, .587, .299], [.0722, .7152, .2126]])

char_list = ["#*:. "[::-1], " .:-=+*#%@", "@#S08Xx+=-;:,._ "[::-1], 
"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1], " 一二卜人个十大天米金我家样糖繁壁齉"]

def to_symbols(in_vid, gs_radio, char_radio, symbol_scale, resize):
    
    global symbol_size, cell_width, cell_height
    symbol_size = symbol_scale
    cell_width = int(base_width * symbol_size)
    cell_height = int(base_height * symbol_size)
    
    orig_resized = cv2.VideoCapture((resize_vid(in_vid, "orig") if not resize else in_vid))
    
    frame_width = int(orig_resized.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(orig_resized.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = orig_resized.get(cv2.CAP_PROP_FPS)

    output_path = "outputs/symbolized.mp4"  
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 

    symbol_vid = cv2.VideoWriter(output_path, fourcc, fps, (frame_width*cell_width, frame_height*cell_height))
    
    char_set = char_list[char_radio]
    char_lut = create_char_lut(char_set)
    
    while orig_resized.isOpened():
        ret, frame = orig_resized.read()
        if not ret:
            break
                
        indices = (
            np.sqrt(cv2.transform(frame, gs_presets[gs_radio]) / 255.0) * (len(char_set) - 1)
        ).astype(np.uint8)

        symbols = char_lut[indices]

        rows = len(symbols)
        cols = len(symbols[0])

        symbol_img = symbols.transpose(0, 2, 1, 3).reshape(
            rows * cell_height,
            cols * cell_width
        )

        colors = np.repeat(
            np.repeat(frame, cell_height, axis=0),
            cell_width,
            axis=1
        )

        # Apply colors to symbols
        img = (
            symbol_img[:, :, None] * colors
        ).astype(np.uint8)
                
        symbol_vid.write(img)
    
    orig_resized.release()
    symbol_vid.release()
    
    return output_path


def resize_vid(in_vid, name):
    
    vid = cv2.VideoCapture(in_vid)
    if not vid.isOpened():
        print("Error: Could not open input video.")
        return ""

    frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vid.get(cv2.CAP_PROP_FPS)

    rs_output_path = "outputs/" + name + "_resized.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    target_width = int(frame_width/(cell_width))
    target_height = int(frame_height/(cell_height))

    rs_vid = cv2.VideoWriter(rs_output_path, fourcc, fps, (target_width, target_height))

    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break

        resized = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
        rs_vid.write(resized)

    vid.release()
    rs_vid.release()

    return rs_output_path


def create_char_lut(char_set):

    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 0.3*symbol_size
    thickness = 2

    lut = np.zeros(
        (len(char_set), cell_height, cell_width),
        dtype=np.uint8
    )

    for i, char in enumerate(char_set):

        (w, h), baseline = cv2.getTextSize(
            char, font, font_scale, thickness
        )

        x = (cell_width - w) // 2
        y = (cell_height + h - baseline) // 2

        cv2.putText(
            lut[i],
            char,
            (x, y),
            font,
            font_scale,
            1,
            thickness,
            cv2.LINE_8
        )

    return lut
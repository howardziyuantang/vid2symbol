import cv2
import numpy as np

cell_width = 8
cell_height = 8
rs_output_path = "outputs/resized.mp4"  

gs_presets = np.array([[.114, .587, .299],
          [.0722, .7152, .2126]])

char_list = ["#*:. "[::-1], " .:-=+*#%@", "@#S08Xx+=-;:,._ "[::-1], 
             "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]]

def to_symbols(in_vid):
    
    chars_select = 1
    
    vid = cv2.VideoCapture(in_vid)
    resized = cv2.VideoCapture(rs_output_path)
    if not vid.isOpened():
        print("Error: Could not open input video.")
        return ""
    
    frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vid.get(cv2.CAP_PROP_FPS)

    output_path = "outputs/symbolized.mp4"  
    fourcc = cv2.VideoWriter_fourcc(*'avc1') 

    symbol_vid = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    while vid.isOpened():
        gs_ret, gs_frame = vid.read()
        if not gs_ret:
            break
        rs_ret, rs_frame = resized.read()
        
        chars = np.array(list(char_list[chars_select]))[int(gs_frame / 255.0 * (len(char_list[chars_select])-1))]

        rows = len(chars)
        cols = len(chars[0])

        img = np.zeros(
            (rows * cell_height, cols * cell_width, 3),
            dtype=np.uint8
        )

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2

        for r in range(rows):
            for c in range(cols):

                char = chars[r][c]

                x_center = c * cell_width + cell_width // 2
                y_center = r * cell_height + cell_height // 2

                (text_width, text_height), baseline = cv2.getTextSize(
                    char, font, font_scale, thickness
                )

                x = x_center - text_width // 2
                y = y_center + text_height // 2

                cv2.putText(
                    img,
                    char,
                    (x, y),
                    font,
                    font_scale,
                    rs_frame[r][c],
                    thickness,
                    cv2.LINE_AA)
                
        symbol_vid.write(img)
    
    vid.release()
    resized.release()
    symbol_vid.release()
    
    return output_path

def to_grayscale(in_vid):

    preset_select = 0
    
    vid = cv2.VideoCapture(in_vid)
    if not vid.isOpened():
        print("Error: Could not open input video.")
        return ""
    
    frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)/cell_width)
    frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)/cell_height)
    fps = vid.get(cv2.CAP_PROP_FPS)

    gs_output_path = "outputs/grayscale.mp4"  
    fourcc = cv2.VideoWriter_fourcc(*'avc1') 

    gs_vid = cv2.VideoWriter(gs_output_path, fourcc, fps, (frame_width, frame_height), isColor=False)
    rs_vid = cv2.VideoWriter(rs_output_path, fourcc, fps, (frame_width, frame_height))
    
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break
        
        resized = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
        rs_vid.write(resized)
        
        gs_frame = cv2.transform(resized, gs_presets[preset_select])
        gs_frame = np.clip(gs_frame, 0, 255).astype(np.uint8)
        gs_vid.write(gs_frame)
    
    vid.release()
    gs_vid.release()
    rs_vid.release()
    
    return gs_output_path
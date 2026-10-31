import cv2
import numpy as np

luma = np.array([.114, .587, .299])
perc_lum = np.array([.0722, .7152, .2126])

def vid2sym(in_vid):
    out_vid = ""
    return out_vid

def to_grayscale(in_vid):

    vid = cv2.VideoCapture(in_vid)
    if not vid.isOpened():
        print("Error: Could not open input video.")
        return ""
    
    frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vid.get(cv2.CAP_PROP_FPS)

    output_path = "outputs/grayscale.mp4"  
    fourcc = cv2.VideoWriter_fourcc(*'avc1') 

    gs_vid = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)
    
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break
        
        gs_frame = cv2.transform(frame, luma)
        gs_frame = np.clip(gs_frame, 0, 255).astype(np.uint8)
        gs_vid.write(gs_frame)
    
    vid.release()
    gs_vid.release()
    
    return output_path
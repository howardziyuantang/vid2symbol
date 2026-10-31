import gradio as gr
import convert as cvt

with gr.Blocks() as app:
    
    gr.Markdown(
        """
        # Vid2Symbol
        Convert any MP4 video into a colorful animation of symbols!
        """)
    
    with gr.Row():
        vid_in = gr.Video(label='Original video')
        vid_out = gr.Video(label='Converted video')
        
    gs_btn = gr.Button('Convert to grayscale')
    
    vid2symbol_btn = gr.Button('Convert to symbols')
    symbol_vid = gr.Video(label='Symbolized video')
        
    gs_btn.click(fn=cvt.to_grayscale, inputs=[vid_in], outputs=vid_out)
    vid2symbol_btn.click(fn=cvt.to_symbols, inputs=[vid_out], outputs=symbol_vid)

app.launch()

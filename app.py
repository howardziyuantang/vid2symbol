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
        
    with gr.Row():
        gs_btn = gr.Button('Convert to grayscale')
        download_btn = gr.Button('Download video')
        
    gs_btn.click(fn=cvt.to_grayscale, inputs=[vid_in], outputs=vid_out)

app.launch()

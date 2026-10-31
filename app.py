import gradio as gr
from convert import vid2sym

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
        convert_btn = gr.Button('Convert to symbols!')
        download_btn = gr.Button('Download converted video')
        
    convert_btn.click(fn=vid2sym, inputs=[vid_in], outputs=vid_out)

app.launch()

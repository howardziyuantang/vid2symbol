import gradio as gr
import convert as cvt

with gr.Blocks() as app:
    
    gr.Markdown(
        """
        # Vid2Symbol
        ## Convert any MP4 video into a colorful animation of symbols!
        """)
    
    with gr.Row():
        vid_in = gr.Video(label='Original video')
        vid_out = gr.Video(label='Converted video')
    
    with gr.Row():
        with gr.Column(scale=1):
            gs_radio = gr.Radio(
                choices=["Luma", "Perceived Luminance"],
                value="Luma",
                label="Grayscale conversion function:",
                type="index",
            )
            symbol_size = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                label="Symbol size:",
            )
            
        with gr.Column(scale=1):
            char_radio = gr.Radio(
                choices=["#*:. "[::-1], " .:-=+*#%@", "@#S08Xx+=-;:,._ "[::-1], 
    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1], " 一二卜人个十大天米金我家样糖繁壁齉"],
                value="#*:. "[::-1],
                label="Character set:",
                type="index",
            )
    
    convert_btn = gr.Button('Convert to symbols!')
            
    convert_btn.click(fn=cvt.to_symbols, inputs=[vid_in, gs_radio, char_radio, symbol_size], outputs=vid_out)

app.launch()

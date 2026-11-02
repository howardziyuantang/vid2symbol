# Vid2Symbol

Vid2Symbol turns a video into a colorful animation made from characters. It runs a Gradio interface locally and uses OpenCV to process the video frame by frame: each frame is converted to grayscale to select symbols by brightness, while the symbols are colored using the corresponding colors from the original frame. Symbol shapes use full color; the space around them uses a slightly transparent version of the frame color, so the background does not become too dark.

Upload a video (or use your webcam as the video input), choose the conversion options, and click **Convert to symbols!** The converted video appears in the output component and can be played or downloaded to your device.

Examples:

| Input | Output |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/1a51cb09-d00c-4a2e-8f1f-1b5087acd65c" width="450"> | <img src="https://github.com/user-attachments/assets/aca1d448-786f-4035-8be6-e495b771eac0" width="450"> |
| <img src="https://github.com/user-attachments/assets/42286241-6d84-4610-b476-27a7685c97a9" width="450"> | <img src="https://github.com/user-attachments/assets/958c6b13-3f28-4741-8cad-01e6d2198ff8" width="450"> |


## Quickstart

You need Python and pip installed. From the project directory, install the dependencies listed in [`requirements.txt`](requirements.txt):

```bash
python -m pip install -r requirements.txt
```

Start the app:

```bash
python app.py
```

Open the local URL printed in the terminal. Use the **Original video** component to upload a video or record one with your webcam. After conversion, view and download the result from **Converted video**.

## Conversion options

- **Grayscale conversion function:** Choose **Luma** or **Perceived Luminance**. These options use different grayscale conversions to determine each pixel's brightness, which affects which character is selected.
- **Symbol size:** Adjusts the size of the characters. Each symbol is based on a 4 × 4 pixel cell, and this setting directly multiplies that base size. For example, size 2 uses 8 × 8 cells.
- **Character set:** Choose from several character sets to change the output's visual texture. Sets include simple symbols, denser character ramps, and Chinese characters.
- **Preserve input resolution:** Controls whether the video is resized before conversion:
  - **Checked:** The video is not resized first. Every input pixel becomes a character, so the output's width and height are each multiplied by four at symbol size 1 (16 times the pixel area), and the output file can be very large. **Set symbol size to 1** when using this option to avoid exceeding output size limits.
  - **Unchecked:** The video is resized down first so that replacing each resized pixel with a symbol produces output dimensions approximately the same as the input. The output dimensions stay similar, but the input resolution is reduced.

## Troubleshooting

- **“Video not playable” error when uploading:** Gradio may occasionally fail on the first upload. Close the error and remove the missing video, then try uploading again; the next attempt usually works.
- **Conversion error in the output video component:** The output may be too large, especially when **Preserve input resolution** is enabled with a high-quality video or a large symbol size. Try unchecking the option to reduce the processing resolution, using a lower-quality input video, or reducing the symbol size.

## Performance

Conversion time depends on the input video's resolution and length, as well as the selected options. Short, lower-quality videos around 720p–1080p with **Preserve input resolution** off may take a few seconds. High-quality 2K or 4K videos, longer clips, and especially preserving the input resolution can take a few minutes because they produce much larger, higher-resolution output videos.

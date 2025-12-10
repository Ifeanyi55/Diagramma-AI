import gradio as gr
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import numpy as np
import tempfile
import os

def create_infographic(subject_area, api_key, image_size, aspect_ratio, design_style, layout_style):
    try:
        prompt = f"""
        Design an infographic on {subject_area} that embodies {design_style} visual principles with a {layout_style} structure.
        Include relevant data, clear hierarchies, and engaging visuals.
        The final output should not contain the literal terms '{design_style}' or '{layout_style}' anywhere in the text.
        """
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=(
                prompt
                if "how to" in subject_area.lower()
                else "Generate an image with a plain white background, no props, and a bold text in black color that says: 'This AI only creates \"How-to guides\" infographics!'"
            ),
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=image_size
                )
            )
        )

        image_parts = [part for part in response.parts if part.inline_data]
        img_bytes = image_parts[0].inline_data.data
        img = Image.open(BytesIO(img_bytes))
        return img

    except Exception as e:
        img = Image.open("sad-face.png")
        return img

def clear_all():
    return "", None

def export_image(img, format_type):
    if img is None:
        return None

    # convert numpy array to PIL Image if necessary
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img.astype('uint8'))
    elif isinstance(img, str):
        # if it's a file path (like the error image), load it
        img = Image.open(img)

    # create a temporary file with the appropriate extension
    extension = format_type.lower()
    if extension == "jpeg":
        extension = "jpg"

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{extension}")
    temp_path = temp_file.name
    temp_file.close()

    # save the image
    if format_type == "PDF":
        img_rgb = img.convert('RGB')
        img_rgb.save(temp_path, format='PDF')
    elif format_type == "JPEG":
        img_rgb = img.convert('RGB')
        img_rgb.save(temp_path, format='JPEG')
    else:
        img.save(temp_path, format=format_type)

    return temp_path

# define the styles for the app
styles = """
.gen {
  display: flex;
  align-items: center;
  font-family: inherit;
  font-weight: 500;
  font-size: 16px;
  padding: 0.7em 1.4em 0.7em 1.1em;
  color: white;
  background: #ad5389;
  background: linear-gradient(0deg, rgba(20,167,62,1) 0%, rgba(102,247,113,1) 100%);
  border: none;
  box-shadow: 0 0.7em 1.5em -0.5em #14a73e98;
  letter-spacing: 0.05em;
  border-radius: 20em;
  cursor: pointer;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

.gen:hover {
  box-shadow: 0 0.5em 1.5em -0.5em #14a73e98;
}

.gen:active {
  box-shadow: 0 0.3em 1em -0.5em #14a73e98;
}
footer {display: none !important;}
.image {
  box-shadow: 0 0.7em 1.5em -0.5em #31D492 !important;
  border-radius:12px;
  padding:5px;
}
.text {
  box-shadow: 0 0.7em 1.5em -0.5em #31D492 !important;
  border-radius:12px;
  padding:5px;
}
.side {
  box-shadow: 0 0.7em 1.5em -0.5em #31D492 !important;
  padding:5px;
}
"""

with gr.Blocks(theme=gr.themes.Ocean(), title="Diagramma AI", css=styles) as app:
    gr.HTML("""<h1 style="text-align:center;font-size:35px;"><strong>Diagramma AI</strong></h1>""")
    gr.HTML("""<h4 style="text-align:center;margin-top:-15px;"><strong>Create Infographics for "How-to" Guides.</strong></h4>""")

    with gr.Sidebar(elem_classes="side"):
        # sidebar controls
        gr.Markdown("### Settings")
        api_key = gr.Text(label="Gemini API Key", type="password")
        image_size = gr.Radio(
            label="Select Image Size",
            choices=["1K", "2K", "4K"],
            value="4K"
        )
        aspect_ratio = gr.Dropdown(
            label="Select Aspect Ratio",
            choices=["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
            value="16:9"
        )
        design_style = gr.Dropdown(
            label="Select Design Style",
            choices=[
                "SketchCraft",
                "Minimal Muse",
                "Blueprint/Technical style",
                "IsoVision 3D",
                "RealFrame",
                "Retro/Vintage",
                "Neon Cyberscape",
                "GeoAbstract",
                "Corporate/Professional",
                "Pop-Art style",
                "DataGrid Pro",
                "Gradient/Modern",
                "Playful Illustration",
                "Executive Slate",
                "Comic/Manga style"
            ],
            value="Corporate/Professional"
        )
        layout_style = gr.Dropdown(
            label="Select Layout Style",
            choices=[
                "Step-by-step vertical flow",
                "2-column instructional",
                "Process flowchart",
                "Do & Don't",
                "Dashboard",
                "Cluster/Bubble",
                "Poster",
                "Storyboard",
                "Overlay/full-image",
                "Zigzag",
                "S-Curve",
                "Timeline or flowchart",
                "Decision tree",
                "Road Map",
                "Radial/Circular",
                "Comparison",
                "Before-after"
            ],
            value="Step-by-step vertical flow"
        )

    # main panel
    subject_area = gr.Text(
        label="\"How-To\" Subject Area",
        placeholder="Enter a \"How-To\" subject area",
        elem_classes = "text"
    )

    with gr.Row():
        run_btn = gr.Button("Create Infographic", variant="primary",elem_classes = "gen")
        clear_btn = gr.Button("Clear",elem_classes = "gen")

    output_image = gr.Image(label="Generated Infographic",elem_classes = "image",container=True)

    with gr.Row():
        # hidden download components
        download_jpg = gr.DownloadButton(label = "Export JPG",elem_classes = "gen")
        download_png = gr.DownloadButton(label = "Export PNG",elem_classes = "gen")
        download_pdf = gr.DownloadButton(label = "Export PDF",elem_classes = "gen")

    # event handlers
    run_btn.click(
        fn=create_infographic,
        inputs=[subject_area, api_key, image_size, aspect_ratio, design_style, layout_style],
        outputs=output_image
    )

    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[subject_area, output_image]
    )

    download_jpg.click(
        fn=lambda img: export_image(img, "JPEG"),
        inputs=output_image,
        outputs=download_jpg
    )

    download_png.click(
        fn=lambda img: export_image(img, "PNG"),
        inputs=output_image,
        outputs=download_png
    )

    download_pdf.click(
        fn=lambda img: export_image(img, "PDF"),
        inputs=output_image,
        outputs=download_pdf
    )

# launch the app
if __name__ == "__main__":
    app.launch()
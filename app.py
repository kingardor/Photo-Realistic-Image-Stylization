from __future__ import print_function
import torch
import process_stylization
from photo_wct import PhotoWCT
import gradio as gr

# Load model
model_path = './models/photo_wct.pth'
p_wct = PhotoWCT()
p_wct.load_state_dict(torch.load(model_path))

def run(content_img, style_img, cuda, post_processing, fast):
    if fast == 0:
        from photo_gif import GIFSmoothing
        p_pro = GIFSmoothing(r=35, eps=0.001)
    else:
        from photo_smooth import Propagator
        p_pro = Propagator()
    
    if cuda:
        p_wct.cuda(0)
    
    output_img = process_stylization.stylization_gradio(
        stylization_module=p_wct,
        smoothing_module=p_pro,
        content_image=content_img,
        style_image=style_img,
        cuda=cuda,
        post_processing=post_processing
    )

    return output_img

if __name__ == '__main__':

    style = gr.Interface(
        fn=run, 
        inputs=[
            gr.Image(label='Content Image'),
            gr.Image(label='Stylize Image'),
            gr.Checkbox(value=False, label='Use CUDA'),
            gr.Checkbox(value=False, label='Post Processing'),
            gr.Radio(choices=["Guided Image Filtering (Fast)", "Photorealisitic Smoothing (Slow)"], value="Guided Image Filtering (Fast)", type="index", label="Algorithm"),
        ], 
        outputs=[gr.Image(
            type="pil",
            label="Result"),
        ]    
    )
    style.launch()
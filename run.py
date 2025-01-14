from setting import gradio_args as gr_args
# 如果你要指定显卡，请确保setting 是第一位

import gradio as gr

from modules.model import infer
from modules.model_setting import num_frames, num_steps


def main():
    gr_auth = gr_args.get('auth', {})
    auth = (gr_auth['username'], gr_auth['password']) if 'username' in gr_auth and 'password' in gr_auth else None
    auth_message = gr_auth.get('message')

    with gr.Blocks(title='Stable Video Diffusion WebUI', css='assets/style_custom.css') as demo:
        gr.HTML(gr_args.get('head_html'))  # add head html
        with gr.Row():
            image = gr.Image(label="input image", type="filepath", elem_id='img-box')
            video_out = gr.Video(label="generated video", elem_id='video-box')
        with gr.Column():
            resize_image = gr.Checkbox(label="resize to optimal size/自动剪裁图片尺寸", value=True)
            btn = gr.Button("Run")
            with gr.Accordion(label="Advanced options", open=False):
                n_frames = gr.Number(precision=0, label="number of frames", value=num_frames)
                n_steps = gr.Number(precision=0, label="number of steps", value=num_steps)
                seed = gr.Text(value="random", label="seed (integer or 'random')", )
                decoding_t = gr.Number(precision=0, label="number of frames decoded at a time", value=2)
        examples = [
            ["https://raw.githubusercontent.com/xx025/stable-video-diffusion-webui/main/demo/demo.jpeg"]
        ]
        inputs = [image, resize_image, n_frames, n_steps, seed, decoding_t]
        outputs = [video_out]
        btn.click(infer, inputs=inputs, outputs=outputs)
        gr.Examples(examples=examples, inputs=inputs, outputs=outputs, fn=infer)
        demo.queue().launch(
            debug=True,
            auth=auth,
            auth_message=auth_message,
            share=gr_args.get('share', True),
            show_api=gr_args.get('show_api', True),
            show_error=True,
        )


if __name__ == "__main__":
    main()

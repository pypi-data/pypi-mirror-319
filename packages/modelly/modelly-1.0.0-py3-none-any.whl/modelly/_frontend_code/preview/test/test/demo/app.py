
from modelly_test import Test

import modelly as gr

example = Test().example_inputs()

with gr.Blocks() as demo:
    Test(value=example, interactive=True)
    Test(value=example, interactive=False)


demo.launch()

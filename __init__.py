import os
import numpy as np
from PIL import Image
import folder_paths

class SaveImageWithoutWorkflow:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "ComfyUI"})
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def save_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            # 核心部分：我们不传递 metadata 或 pnginfo 给 save 方法
            # 这确保了只有图像数据被保存
            
            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), optimize=True)
            
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return { "ui": { "images": results } }

# 告诉 ComfyUI 如何加载这个节点
NODE_CLASS_MAPPINGS = {
    "SaveImageWithoutWorkflow": SaveImageWithoutWorkflow
}

# 给节点一个在界面中显示的名字
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageWithoutWorkflow": "Save Image (No Workflow)"
}
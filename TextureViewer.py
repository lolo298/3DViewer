import pyglet
from pyglet.image import Texture, AbstractImage
from PIL import Image, ImageDraw
from pyglet.gl import glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA

class TextureViewer(pyglet.window.Window):
    texture:Image = None
    canvas:Image = None
    is_drawing = False
    overlay:Image = None

    def __init__(self, texture:str):
        super().__init__(800, 800, "Texture Viewer", resizable=True)
        self.texture = Image.open(texture, formats=('PNG',)).convert('RGBA')
        print("Image mode:", self.texture.mode)
        print("Image size:", self.texture.size)
        print("Byte length:", len(self.texture.tobytes()))
        self.set_size(self.texture.width, self.texture.height)
        self.new_canvas()
        self.new_overlay()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.dispatch_event('on_draw')

    def on_draw(self):
        self.clear()
        pyglet.image.ImageData(self.texture.width, self.texture.height, 'RGBA', self.texture.transpose(Image.Transpose.FLIP_TOP_BOTTOM).tobytes()).blit(0, 0)
        pyglet.image.ImageData(self.canvas.width, self.canvas.height, 'RGBA', self.canvas.tobytes()).blit(0, 0, 1)
        pyglet.image.ImageData(self.overlay.width, self.overlay.height, 'RGBA', self.overlay.tobytes()).blit(0, 0, 1)


    def on_mouse_press(self, x, y, button, modifiers):
        print("Mouse pressed")
        if button == pyglet.window.mouse.LEFT:
            self.is_drawing = True
            print(f"Mouse pressed at: ({x}, {y})")
    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.is_drawing = False
            self.canvas_interface = None
            print(f"Mouse released at: ({x}, {y})")
            self.save_texture()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == pyglet.window.mouse.LEFT:
            print(f"Mouse moved to: ({x}, {y})")
            # You can add your drawing logic here
            canvas_interface = ImageDraw.Draw(self.canvas)
            canvas_interface.line([(x-1, y), (x+1, y)], fill=(255, 0, 0, 255), width=3)
    def save_texture(self):
        flipped_texture = self.canvas.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        self.texture.paste(flipped_texture, (0,0), flipped_texture)
        self.texture.save("drawed_body.png")
        self.new_canvas()
        print("Texture saved as drawed_body.png")
    def show_uvs(self, uvs, faces):
        # Convert the UV coordinates to pixel coordinates
        pixel_coords = [(int(u * self.texture.width), int(v * self.texture.height)) for u, v in uvs]
        self.new_overlay()
        overlay_interface = ImageDraw.Draw(self.overlay)
        # Draw the UV coordinates on the texture
        for i, (x, y) in enumerate(pixel_coords):
            overlay_interface.line([(x-1, y), (x+1, y)], fill=(255, 255, 0, 255), width=2)
            print(f"Drawing UV at: ({x}, {y})")
            # Draw lines between uvs

        # Now iterate over each face and draw the corresponding UV edges
        for face in faces:
            # Each face is defined by 3 vertices, so we get the UVs for each of those vertices
            uv1 = pixel_coords[face[0]]  # First vertex
            uv2 = pixel_coords[face[1]]  # Second vertex
            uv3 = pixel_coords[face[2]]  # Third vertex

            # Draw lines between the UV vertices that form the edges of the face
            overlay_interface.line([uv1, uv2], fill=(0, 0, 0, 127), width=1)  # Red lines
            overlay_interface.line([uv2, uv3], fill=(0, 0, 0, 127), width=1)  # Red lines
            overlay_interface.line([uv3, uv1], fill=(0, 0, 0, 127), width=1)  # Red lines




        self.dispatch_event('on_draw')
        print("UVs drawn on canvas")
    def new_canvas(self):
        self.canvas = Image.new("RGBA", (self.texture.width, self.texture.height), (255, 0, 255, 0))
        print("Canvas cleared")
    def new_overlay(self):
        self.overlay = Image.new("RGBA", (self.texture.width, self.texture.height), (255, 0, 255, 0))
        print("Overlay cleared")
from time import sleep
from typing import Tuple

import numpy as np
import trimesh.path
from PIL import Image
import pyglet
from numpy._typing import NDArray
from trimesh import load_mesh, Scene, load_path, Trimesh
from trimesh.scene import Camera
from trimesh.visual import TextureVisuals, ColorVisuals
from trimesh.transformations import translation_matrix
from trimesh.path.exchange.misc import edges_to_path
from trimesh.path.path import Path
from TextureViewer import TextureViewer
from trimesh.viewer.windowed import SceneViewer
from watchdog.events import FileModifiedEvent, FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer
from ModelParts import ModelParts, find_segment, get_segment_indices, get_segment_color

texture_file = "drawed_body.png"
# texture_file = "body.png"
texture_img = Image.open(texture_file)
texture_data = np.array(texture_img)

image_viewer = TextureViewer(texture_file)
# noinspection PyTypeChecker
mesh = load_mesh('./models/trimesh_uv.obj', process=False)
segmented_mesh = load_mesh('./models/trimesh_uv_labeled.obj', process=False)

total_faces = len(mesh.faces)
total_vertices = len(mesh.vertices)

print(total_faces)
print(total_vertices)


camera = Camera(name="main_camera", fov=(90, 90), resolution=(800, 800))
scene = Scene(geometry=mesh, camera=camera)

scene.graph.update(
    frame_from="main_camera",
    frame_to="world",
    matrix=translation_matrix([0, -1, -2])
)

viewer = SceneViewer(scene=scene, start_loop=False)
# noinspection PyTypeChecker
# viewer = scene.show(start_loop=False, callback=lambda s: None)

# # On clicking the window, raycast to get the click location in 3d world, and print the uv coordinates
# # of the corresponding face
# while viewer.is_alive:
#     click = viewer.pick()
#     if click is not None:
#         location, face_id = click
#         face = mesh.faces[face_id]
#         uv = mesh.visual.uv[face]
#         print(uv)
#

# TODO
def update_texture(dt = None, file: str = "") -> None:
    """
    Update the texture of the mesh with the new texture file.
    """
    texture = Image.open(file)
    mesh.visual = TextureVisuals(image=texture, uv=mesh.visual.uv)
    viewer.dispatch_event("on_draw")
    print("Texture updated", dt, file)


update_texture(file=texture_file)


class TextureChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        print("file event")
    def on_modified(self, event):
        sleep(1)
        pyglet.clock.schedule_once(update_texture, 0, texture_file)


event_handler = TextureChangeHandler()
observer = Observer()
observer.schedule(event_handler, path=".", recursive=False)
observer.start()



mouse_dragged = False

@viewer.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global mouse_dragged
    mouse_dragged = True


@viewer.event
def on_mouse_release(x, y, button, modifiers):
    global mouse_dragged, image_viewer
    if mouse_dragged or button != pyglet.window.mouse.LEFT:
        mouse_dragged = False
        return
    mouse_dragged = False

    # Find rays from camera
    origins, drctns, pixels = scene.camera_rays()

    # Get index of ray corresponding to mouse location
    rows = np.where((pixels[:, 0] == x) & (pixels[:, 1] == y))
    row = rows[0][0]

    # Pull origin and direction of that ray
    origin = origins[row, :]
    drctn = drctns[row, :]


    # Display 5 meters of the ray in the scene
#    ray = np.array([origin, origin + 5 * drctn])
 #   viewer.scene.add_geometry(load_path(ray))


    # Find the face that the ray intersects
    location, index_ray, index_tri = mesh.ray.intersects_location(origin.reshape(1, -1), drctn.reshape(1, -1))
    print(location, index_ray, index_tri)


    if location.size > 0 :
        # Get the face index
        face_index = index_tri[0]  # First intersected face
        face_vertex_indices = mesh.faces[face_index]  # Get face vertex indices

        # Extract the segment from the intersected face vertices
        segment = find_segment(face_vertex_indices[0])
        segment_vertex_indices = get_segment_indices(segment)

        # Get the corresponding vertices for the segment
        segment_vertices = mesh.vertices[segment_vertex_indices]
        segment_faces = []

        # Iterate through each face and check if it references any vertex from the segment
        for face_vertex_indices in mesh.faces:
            # Check if the face contains any of the segment vertices
            if np.any(np.isin(face_vertex_indices, segment_vertex_indices)):
                # Remap the face indices to the new segment vertex indices
                new_face = [np.where(segment_vertex_indices == vertex)[0][0] for vertex in face_vertex_indices]
                segment_faces.append(new_face)

        # Create a new Trimesh object for the highlighted segment
        highlight_face = trimesh.Trimesh(
            vertices=segment_vertices,
            faces=np.array(segment_faces),
            vertex_colors=[get_segment_color(segment)] * len(segment_vertices),
            process=False
        )


        # Add to scene
        if viewer.scene.geometry.get("highlighted_face") is not None:
            viewer.scene.delete_geometry("highlighted_face")
        viewer.scene.add_geometry(highlight_face, geom_name="highlighted_face")
        # Get selected uvs
        selected_uvs = mesh.visual.uv[segment_vertex_indices]
        image_viewer.show_uvs(selected_uvs, segment_faces)
    else:
        print('No intersection')


    pass

if __name__ == "__main__":
    pyglet.app.run()
    pass




import numpy as np
from trimesh import load_mesh
from trimesh.visual import TextureVisuals, ColorVisuals
from ModelParts import ModelParts

head = np.load('indices/head.npy')
torso = np.load('indices/torso.npy')

l_hand = np.load('indices/l_hand.npy')
l_arm = np.load('indices/l_arm.npy')
l_leg = np.load('indices/l_leg.npy')
l_foot = np.load('indices/l_foot.npy')

r_hand = np.load('indices/r_hand.npy')
r_arm = np.load('indices/r_arm.npy')
r_leg = np.load('indices/r_leg.npy')
r_foot = np.load('indices/r_foot.npy')

# noinspection PyTypeChecker
m = load_mesh('./models/trimesh_uv.obj', force='mesh', process=False)

vc = 255*np.ones((m.vertices.shape[0],4)).astype('uint8')
vc[head] = ModelParts.HEAD.value
vc[torso] = ModelParts.TORSO.value

vc[l_hand] = ModelParts.L_HAND.value
vc[l_arm] = ModelParts.L_ARM.value
vc[l_leg] = ModelParts.L_LEG.value
vc[l_foot] = ModelParts.L_FOOT.value

vc[r_hand] = ModelParts.R_HAND.value
vc[r_arm] = ModelParts.R_ARM.value
vc[r_leg] = ModelParts.R_LEG.value
vc[r_foot] = ModelParts.R_FOOT.value


vis = ColorVisuals(m,vertex_colors=vc)
m.visual = vis
_ = m.export('./models/trimesh_uv_labeled.obj', include_normals=True, include_color=True)
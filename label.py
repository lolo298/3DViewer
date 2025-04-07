import trimesh
import os
import numpy as np
from tqdm import tqdm
import natsort
from psbody.mesh import Mesh

src = './models'
info = './indices/'

#meshes = natsort.natsorted(os.listdir(src))

#for meshname in tqdm(meshes):
m = trimesh.load(src+'/smpl_uv.obj',process=False, force='mesh')
head = np.load(info+'head.npy') - 1
torso = np.load(info+'torso.npy') - 1
neck = np.load(info+'neck.npy') - 1
hair = np.load(info+'hair.npy') - 1
lower_torso = np.load(info+'lower_torso.npy') - 1
l_foot = np.load(info+'l_foot.npy') - 1
r_foot = np.load(info+'r_foot.npy') - 1
l_arm = np.load(info+'l_arm.npy') - 1
r_arm = np.load(info+'r_arm.npy') - 1

vc = 255*np.ones((m.vertices.shape[0],4)).astype('uint8')
vc[head] = [210,200,130,255]
vc[torso] = [255,85,85,255]
vc[neck] = [100,100,255,255]
vc[hair] = [50,10,10,255]
vc[lower_torso] = [30,85,85,255]
vc[l_foot] = [255,255,0,255]
vc[r_foot] = [255,170,0,255]
vc[l_arm] = [50,200,50,255]
vc[r_arm] = [160,70,250,255]

vis = trimesh.visual.ColorVisuals(m,vertex_colors=vc)
m.visual = vis
scene = trimesh.scene.Scene()
scene.add_geometry(m)
# scene.show('gl')
_ = m.export(src+'/smpl_uv_labeled.obj')
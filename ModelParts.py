from enum import Enum

import numpy as np

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


class ModelParts(Enum):
    HEAD = 0
    TORSO = 1

    L_HAND = 2
    L_ARM  = 3
    L_LEG  = 4
    L_FOOT = 5

    R_HAND = 6
    R_ARM  = 7
    R_LEG  = 8
    R_FOOT = 9

model_indicies = {
    ModelParts.HEAD: head,
    ModelParts.TORSO: torso,
    ModelParts.L_HAND: l_hand,
    ModelParts.L_ARM: l_arm,
    ModelParts.L_LEG: l_leg,
    ModelParts.L_FOOT: l_foot,
    ModelParts.R_HAND: r_hand,
    ModelParts.R_ARM: r_arm,
    ModelParts.R_LEG: r_leg,
    ModelParts.R_FOOT: r_foot
}

model_colors = {
    ModelParts.HEAD: [249, 237, 105, 130],
    ModelParts.TORSO: [255, 46, 99, 130],
    ModelParts.L_HAND: [168, 216, 234, 130],
    ModelParts.L_ARM: [96, 153, 102, 130],
    ModelParts.L_LEG: [37, 42, 52, 130],
    ModelParts.L_FOOT: [234, 234, 234, 130],
    ModelParts.R_HAND: [106, 44, 112, 130],
    ModelParts.R_ARM: [252, 186, 211, 130],
    ModelParts.R_LEG: [170, 150, 218, 130],
    ModelParts.R_FOOT: [255, 255, 210, 130]
}

def find_segment(vertex:np.ndarray) -> ModelParts:
    print(f"vertex: {vertex}")
    for segment in ModelParts:
        print(f"segment: {segment}")
        if np.isin(vertex, model_indicies[segment]):
            return segment
    return ModelParts.TORSO

def get_segment_color(segment:ModelParts) -> list[int]:
    return model_colors[segment]
def get_segment_indices(segment:ModelParts) -> np.ndarray:
    return model_indicies[segment]
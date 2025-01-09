import logging, os, sys

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
logger.debug(__file__)
import cv2
import numpy as np


arcface_dst = np.array(
    [
        [38.2946, 51.6963],
        [73.5318, 51.5014],
        [56.0252, 71.7366],
        [41.5493, 92.3655],
        [70.7299, 92.2041],
    ],
    dtype=np.float32,
)


def estimate_norm(lmk, image_size=112, mode="arcface"):
    assert lmk.shape == (5, 2)
    assert image_size % 112 == 0 or image_size % 128 == 0

    # Compute ratio and offset
    if image_size % 112 == 0:
        ratio = float(image_size) / 112.0
        diff_x = 0
    else:
        ratio = float(image_size) / 128.0
        diff_x = 8.0 * ratio

    # Scale and shift the destination landmarks
    dst = arcface_dst * ratio
    dst[:, 0] += diff_x

    # Compute centroids
    src_center = np.mean(lmk, axis=0)
    dst_center = np.mean(dst, axis=0)

    # Normalize points by centroids
    lmk_norm = lmk - src_center
    dst_norm = dst - dst_center

    # Compute rotation and scale using SVD
    U, S, Vt = np.linalg.svd(np.dot(dst_norm.T, lmk_norm))  # Covariance matrix decomposition
    R = U @ Vt  # Enforce orthogonality for rotation
    if np.linalg.det(R) < 0:  # Ensure no reflection
        U[:, -1] *= -1
        R = U @ Vt

    # Compute uniform scale
    scale = np.sum(S) / np.sum(lmk_norm ** 2)

    # Final affine matrix construction
    M = np.zeros((3, 3))
    M[:2, :2] = scale * R
    M[:2, 2] = dst_center - scale * R @ src_center
    M[2, 2] = 1  # Homogeneous row

    # Return 2x3 affine matrix compatible with OpenCV
    return M[:2, :]


def norm_crop(img, landmark, image_size=112, mode="arcface"):
    M = estimate_norm(landmark, image_size, mode)
    warped = cv2.warpAffine(img, M, (image_size, image_size), borderValue=0.0)
    return warped


def norm_crop2(img, landmark, image_size=112, mode="arcface"):
    M = estimate_norm(landmark, image_size, mode)
    warped = cv2.warpAffine(img, M, (image_size, image_size), borderValue=0.0)
    return warped, M


def square_crop(im, S):
    if im.shape[0] > im.shape[1]:
        height = S
        width = int(float(im.shape[1]) / im.shape[0] * S)
        scale = float(S) / im.shape[0]
    else:
        width = S
        height = int(float(im.shape[0]) / im.shape[1] * S)
        scale = float(S) / im.shape[1]
    resized_im = cv2.resize(im, (width, height))
    det_im = np.zeros((S, S, 3), dtype=np.uint8)
    det_im[: resized_im.shape[0], : resized_im.shape[1], :] = resized_im
    return det_im, scale


def transform(data, center, output_size, scale, rotation):
    # Convert rotation angle from degrees to radians
    rot_rad = np.deg2rad(rotation)

    # Compute scaling and rotation matrix
    scale_rot_matrix = np.array([
        [scale * np.cos(rot_rad), -scale * np.sin(rot_rad)],
        [scale * np.sin(rot_rad), scale * np.cos(rot_rad)]
    ])

    # Compute translation
    src_center = np.array(center)
    dst_center = np.array([output_size / 2, output_size / 2])
    src_transformed = scale_rot_matrix @ src_center  # Rotate and scale center
    translation = dst_center - src_transformed  # Final translation

    # Create affine matrix
    M = np.hstack([scale_rot_matrix, translation.reshape(-1, 1)])

    # Apply affine transformation
    cropped = cv2.warpAffine(data, M, (output_size, output_size),
                             borderValue=(0, 0, 0) if len(data.shape) == 3 else 0.0)
    return cropped, M


def trans_points2d(pts, M):
    new_pts = np.zeros(shape=pts.shape, dtype=np.float32)
    for i in range(pts.shape[0]):
        pt = pts[i]
        new_pt = np.array([pt[0], pt[1], 1.0], dtype=np.float32)
        new_pt = np.dot(M, new_pt)
        # print('new_pt', new_pt.shape, new_pt)
        new_pts[i] = new_pt[0:2]

    return new_pts


def trans_points3d(pts, M):
    scale = np.sqrt(M[0][0] * M[0][0] + M[0][1] * M[0][1])
    # print(scale)
    new_pts = np.zeros(shape=pts.shape, dtype=np.float32)
    for i in range(pts.shape[0]):
        pt = pts[i]
        new_pt = np.array([pt[0], pt[1], 1.0], dtype=np.float32)
        new_pt = np.dot(M, new_pt)
        # print('new_pt', new_pt.shape, new_pt)
        new_pts[i][0:2] = new_pt[0:2]
        new_pts[i][2] = pts[i][2] * scale

    return new_pts


def trans_points(pts, M):
    if pts.shape[1] == 2:
        return trans_points2d(pts, M)
    else:
        return trans_points3d(pts, M)

# webknossos_utils/__init__.py

import numpy as np
from webknossos import BoundingBox
from collections import namedtuple

Annotation = namedtuple("Annotation", ["ID", "Dataset", "Name"])
Annotation.__doc__ = """
A namedtuple representing an annotation layer in WebKnossos.

Fields:
    ID (int): The unique identifier of the annotation layer.
    Dataset (str): The identifier of the dataset the annotation layer belongs to.
    Name (str): The name of the annotation layer.
"""

Pixel_size = namedtuple("Pixel_size", ["x", "y", "z", "MAG", "unit"])
Pixel_size.__doc__ = """
A namedtuple representing the pixel size information for WebKnossos data.

Fields:
    x (float): The pixel size along the x-axis.
    y (float): The pixel size along the y-axis.
    z (float): The pixel size along the z-axis.
    MAG (Vector): A Vector object representing the magnification factors.
    unit (str): The unit of measurement for the pixel sizes.
"""


def skibbox2wkbbox(ski_bbox, pSize):
    """
    Convert a bounding box from scikit-image format to WebKnossos format. Assumes at the moment a singe z plane

    Args:
        ski_bbox (dict): A dictionary containing the bounding box coordinates in scikit-image format.
            The dictionary should have keys 'bbox-0', 'bbox-1', 'bbox-2', and 'bbox-3' representing
            the minimum x, minimum y, maximum x, and maximum y coordinates, respectively.
        pSize (namedtuple): A namedtuple containing the 'MAG' field with the pixel size information
            from WebKnossos.

    Returns:
        BoundingBox: A BoundingBox object representing the bounding box in WebKnossos format.

    Raises:
        AssertionError: If ski_bbox is not a dictionary, if the 'bbox-0', 'bbox-1', 'bbox-2', and 'bbox-3'
            keys are not present in ski_bbox, or if pSize is not a namedtuple with the 'MAG' field.

    Example:
        >>> ski_bbox = {'bbox-0': 10, 'bbox-1': 20, 'bbox-2': 30, 'bbox-3': 40}
        >>> pSize = Pixel_size(MAG=Vector(1.0, 2.0, 3.0))
        >>> wk_bbox = skibbox2wkbbox(ski_bbox, pSize)
        >>> print(wk_bbox)
        BoundingBox(corner=array([20., 10.,  0.]), size=array([20., 40.,  3.]))
    """
    assert isinstance(ski_bbox, dict), "ski_bbox must be a dict"
    assert all(key in ski_bbox for key in ('bbox-0', 'bbox-1', 'bbox-2', 'bbox-3')), "bbox is ill defined"
    assert isinstance(pSize, Pixel_size), "pSize is a namedtuple and must contain a MAG from webknossos"
    assert "MAG" in pSize._fields, "issues with pixel size info, mag missing"
    MAG = pSize.MAG
    corner = np.array([ski_bbox['bbox-1'], ski_bbox['bbox-0'], 0]) * np.array([MAG.x, MAG.y, MAG.z])
    size = np.array([ski_bbox['bbox-3'] - ski_bbox['bbox-1'], ski_bbox['bbox-2'] - ski_bbox['bbox-0'], 1]) * np.array([MAG.x, MAG.y, MAG.z])
    wk_bbox = BoundingBox(corner, size).align_with_mag(MAG, True)

    return wk_bbox
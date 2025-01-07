# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to resize image/frame.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""

import cv2
import numpy as np

from PIL import Image


class Resizer:
    """
    :ivar frame: original frame;
    :ivar frame_resized: resized frame;
    :ivar image: original image;
    :ivar image_path: image path;
    :ivar image_resized: image resized;
    :ivar model_height: model height;
    :ivar model_width: model width.
    """
    def __init__(self):
        """
        Constructor method for the Resizer class.
        """
        self.frame = None
        self.frame_resized = None
        self.image = None
        self.image_path = None
        self.image_resized = None
        self.model_height = None
        self.model_width = None

    def set_sizes(self, engine_input_details=None):
        """
        Set the height and width model size.
        """
        if engine_input_details is not None:
            _, self.model_height, self.model_width, _ = engine_input_details[0]['shape']
   
    def resize_frame(self, frame=None, width=None, height=None, expand_dims=True):
        """
        Resize the frame.

        Args:
            frame (numpy array): original frame to be resized;
            width (int): new width to resize;
            height (int): new height to resize;
            expand_dims (bool): if expand dimensions or not

        Returns:
            The :obj:`numpy.array` resized frame is stored at the frame_resized attribute.
        """
        if frame is not None:
            self.frame = frame
            if width is not None and isinstance(width, int):
                self.model_width = width
            if height is not None and isinstance(height, int):
                self.model_height = height
            self.frame_resized = cv2.resize(frame, (self.model_width, self.model_height))
            if expand_dims:
                self.frame_resized = np.expand_dims(self.frame_resized, axis=0)

    def resize_image(self, image_path=None, width=None, height=None, expand_dims=True):
        """
        Resize the image.

        Args:
            image_path (numpy array): original image to be resized;
            width (int): new width to resize;
            height (int): new height to resize;
            expand_dims (bool): if expand dimensions or not

        Returns:
            The :obj:`numpy.array` resized image is stored at image_resized attribute.
        """
        if image_path is not None:
            self.image_path = image_path
            if width is not None and isinstance(width, int):
                self.model_width = width
            if height is not None and isinstance(height, int):
                self.model_height = height
            with Image.open(self.image_path) as img:            
                self.image = np.array(img)
                self.image = self.image[:, :, ::-1].copy()
                self.image_resized = img.resize((self.model_width, self.model_height))
                if expand_dims:
                    self.image_resized = np.expand_dims(self.image_resized, axis=0)

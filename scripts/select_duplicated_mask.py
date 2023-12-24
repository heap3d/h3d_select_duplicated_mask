#!/usr/bin/python
# ================================
# (C)2020-2023 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select duplicated material mask, keep topmost unselected
# ================================

import modo
import lx

import h3d_utilites.scripts.h3d_utils as h3du
from h3d_utilites.scripts.h3d_debug import H3dDebug
from h3d_utilites.scripts.h3d_exceptions import H3dExitException


PTYP = 'ptyp'
PTAG = 'ptag'
PTAG_MATERIAL = 'Material'


def get_masks():
    return modo.Scene().items(itype=modo.c.MASK_TYPE)


class MaskInfo:
    def __init__(self, mask):
        self.blend = self.get_blend_mode(mask)
        self.item_name = self.get_item_name(mask)
        self.ptyp = self.get_ptyp(mask)
        self.ptag = self.get_ptag(mask)
        self.scope = self.get_scope(mask)

    def get_ptyp(self, mask):
        if not mask:
            return None
        mask_channel = mask.channel(PTYP)
        if not mask_channel:
            return None
        channel_value = mask_channel.get()
        if h3du.is_material_ptyp(channel_value):
            return PTAG_MATERIAL

        return channel_value

    def get_ptag(self, mask):
        if not mask:
            return None
        mask_channel = mask.channel(PTAG)
        if not mask_channel:
            return None
        channel_value = mask_channel.get()

        return channel_value

    def get_blend_mode(self, mask):
        if not mask:
            return None
        mask_channel = mask.channel('blend')
        if not mask_channel:
            return None
        channel_value = mask_channel.get()

        return channel_value

    def get_item_name(self, mask):
        if not mask:
            return None
        mask.select(replace=True)

        return lx.eval('mask.setMesh ?')

    def get_scope(self, mask):
        if not mask:
            return None
        mask_channel = mask.channel('surfType')
        if not mask_channel:
            return None
        channel_value = mask_channel.get()

        return channel_value


def main():
    mask_infos = dict()
    masks = get_masks()
    for mask in masks:
        mask_infos[mask] = MaskInfo(mask)
        h3dd.print_debug('mask: <{}>   mask info: {}'.format(mask.name, mask_infos[mask]))


if __name__ == '__main__':
    h3dd = H3dDebug(enable=False, file=h3du.replace_file_ext(modo.Scene().filename, ".log"))
    try:
        main()
    except H3dExitException as e:
        print(e.message)

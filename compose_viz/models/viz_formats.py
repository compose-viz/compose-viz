from enum import Enum


class VizFormats(str, Enum):
    png = "png"
    dot = "dot"
    jpeg = "jpeg"
    json = "json"
    svg = "svg"

    bmp = "bmp"
    canon = "canon"
    cmap = "cmap"
    cmapx = "cmapx"
    cmapx_np = "cmapx_np"
    dot_json = "dot_json"
    emf = "emf"
    emfplus = "emfplus"
    eps = "eps"
    fig = "fig"
    gif = "gif"
    gv = "gv"
    imap = "imap"
    imap_np = "imap_np"
    ismap = "ismap"
    jpe = "jpe"
    jpg = "jpg"
    json0 = "json0"
    metafile = "metafile"
    mp = "mp"
    pdf = "pdf"
    pic = "pic"
    plain = "plain"
    plain_ext = "plain-ext"
    pov = "pov"
    ps = "ps"
    ps2 = "ps2"
    tif = "tif"
    tiff = "tiff"
    tk = "tk"
    vml = "vml"
    xdot = "xdot"
    xdot1_2 = "xdot1.2"
    xdot1_4 = "xdot1.4"
    xdot_json = "xdot_json"

    def __str__(self):
        # Python 3.11+ broken __str__
        # https://github.com/python/cpython/issues/100458
        return self.name

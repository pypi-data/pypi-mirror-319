# coding: UTF-8
import sys
bstack1ll111_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack11l1ll_opy_ = 7
def bstack11l11_opy_ (bstack1lllllll_opy_):
    global bstack11l1l1_opy_
    bstack1111l1l_opy_ = ord (bstack1lllllll_opy_ [-1])
    bstack1l1l11l_opy_ = bstack1lllllll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1111l1l_opy_ % len (bstack1l1l11l_opy_)
    bstack1l1111l_opy_ = bstack1l1l11l_opy_ [:bstack1l1llll_opy_] + bstack1l1l11l_opy_ [bstack1l1llll_opy_:]
    if bstack1ll111_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack1l1111_opy_ + bstack1111l1l_opy_) % bstack11l1ll_opy_) for bstack1l1111_opy_, char in enumerate (bstack1l1111l_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack1l1111_opy_ + bstack1111l1l_opy_) % bstack11l1ll_opy_) for bstack1l1111_opy_, char in enumerate (bstack1l1111l_opy_)])
    return eval (bstack1ll1l1_opy_)
from browserstack_sdk.bstack1l1l111ll1_opy_ import bstack11l11ll1l_opy_
from browserstack_sdk.bstack111llll11l_opy_ import RobotHandler
def bstack1llll11111_opy_(framework):
    if framework.lower() == bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᎈ"):
        return bstack11l11ll1l_opy_.version()
    elif framework.lower() == bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᎉ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫᎊ"):
        import behave
        return behave.__version__
    else:
        return bstack11l11_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭ᎋ")
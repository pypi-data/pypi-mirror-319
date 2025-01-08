# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll1ll_opy_ = 7
def bstack1l11_opy_ (bstack1l11ll_opy_):
    global bstack1ll1lll_opy_
    bstack11l1_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack1111l1l_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1llll11_opy_ = bstack11l1_opy_ % len (bstack1111l1l_opy_)
    bstack1l11111_opy_ = bstack1111l1l_opy_ [:bstack1llll11_opy_] + bstack1111l1l_opy_ [bstack1llll11_opy_:]
    if bstack1ll11_opy_:
        bstack1l1ll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack1ll1l11_opy_ + bstack11l1_opy_) % bstack1ll1ll_opy_) for bstack1ll1l11_opy_, char in enumerate (bstack1l11111_opy_)])
    else:
        bstack1l1ll1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack1ll1l11_opy_ + bstack11l1_opy_) % bstack1ll1ll_opy_) for bstack1ll1l11_opy_, char in enumerate (bstack1l11111_opy_)])
    return eval (bstack1l1ll1l_opy_)
from browserstack_sdk.bstack11111l11_opy_ import bstack1l1l11l1_opy_
from browserstack_sdk.bstack111lll11ll_opy_ import RobotHandler
def bstack1lll111ll1_opy_(framework):
    if framework.lower() == bstack1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᎈ"):
        return bstack1l1l11l1_opy_.version()
    elif framework.lower() == bstack1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᎉ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫᎊ"):
        import behave
        return behave.__version__
    else:
        return bstack1l11_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭ᎋ")
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
import threading
import logging
import bstack_utils.bstack111lll111l_opy_ as bstack1lll11ll_opy_
from bstack_utils.helper import bstack11l1l11l1_opy_
logger = logging.getLogger(__name__)
def bstack1l1ll11111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1l1l11l11l_opy_(context, *args):
    tags = getattr(args[0], bstack11l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧၪ"), [])
    bstack1lll11ll1_opy_ = bstack1lll11ll_opy_.bstack1l1lll1l1_opy_(tags)
    threading.current_thread().isA11yTest = bstack1lll11ll1_opy_
    try:
      bstack11ll111lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll11111_opy_(bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩၫ")) else context.browser
      if bstack11ll111lll_opy_ and bstack11ll111lll_opy_.session_id and bstack1lll11ll1_opy_ and bstack11l1l11l1_opy_(
              threading.current_thread(), bstack11l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪၬ"), None):
          threading.current_thread().isA11yTest = bstack1lll11ll_opy_.bstack1l1llll11l_opy_(bstack11ll111lll_opy_, bstack1lll11ll1_opy_)
    except Exception as e:
       logger.debug(bstack11l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬၭ").format(str(e)))
def bstack1lll111l11_opy_(bstack11ll111lll_opy_):
    if bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪၮ"), None) and bstack11l1l11l1_opy_(
      threading.current_thread(), bstack11l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ၯ"), None) and not bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫၰ"), False):
      threading.current_thread().a11y_stop = True
      bstack1lll11ll_opy_.bstack1ll1ll1l1l_opy_(bstack11ll111lll_opy_, name=bstack11l11_opy_ (u"ࠤࠥၱ"), path=bstack11l11_opy_ (u"ࠥࠦၲ"))
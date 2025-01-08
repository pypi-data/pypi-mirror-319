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
import threading
import logging
import bstack_utils.bstack111ll11l11_opy_ as bstack1l1l11llll_opy_
from bstack_utils.helper import bstack1ll111111l_opy_
logger = logging.getLogger(__name__)
def bstack1llll11l1l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1ll1ll1l_opy_(context, *args):
    tags = getattr(args[0], bstack1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧၪ"), [])
    bstack111llll1_opy_ = bstack1l1l11llll_opy_.bstack1lll1l1l1_opy_(tags)
    threading.current_thread().isA11yTest = bstack111llll1_opy_
    try:
      bstack1lll1ll11l_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11l1l_opy_(bstack1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩၫ")) else context.browser
      if bstack1lll1ll11l_opy_ and bstack1lll1ll11l_opy_.session_id and bstack111llll1_opy_ and bstack1ll111111l_opy_(
              threading.current_thread(), bstack1l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪၬ"), None):
          threading.current_thread().isA11yTest = bstack1l1l11llll_opy_.bstack1llll1llll_opy_(bstack1lll1ll11l_opy_, bstack111llll1_opy_)
    except Exception as e:
       logger.debug(bstack1l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬၭ").format(str(e)))
def bstack1l1111l111_opy_(bstack1lll1ll11l_opy_):
    if bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪၮ"), None) and bstack1ll111111l_opy_(
      threading.current_thread(), bstack1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ၯ"), None) and not bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫၰ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1l11llll_opy_.bstack11l1111l1_opy_(bstack1lll1ll11l_opy_, name=bstack1l11_opy_ (u"ࠤࠥၱ"), path=bstack1l11_opy_ (u"ࠥࠦၲ"))
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
import os
import threading
from bstack_utils.helper import bstack1l1llll1l1_opy_
from bstack_utils.constants import bstack11111ll1ll_opy_, EVENTS, STAGE
from bstack_utils.bstack11l111l1_opy_ import get_logger
logger = get_logger(__name__)
class bstack111lll111_opy_:
    bstack1ll11l1l1l1_opy_ = None
    @classmethod
    def bstack1ll11111ll_opy_(cls):
        if cls.on():
            logger.info(
                bstack1l11_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨᢅ").format(os.environ[bstack1l11_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧᢆ")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᢇ"), None) is None or os.environ[bstack1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᢈ")] == bstack1l11_opy_ (u"ࠤࡱࡹࡱࡲࠢᢉ"):
            return False
        return True
    @classmethod
    def bstack1l1lll11l1l_opy_(cls, bs_config, framework=bstack1l11_opy_ (u"ࠥࠦᢊ")):
        bstack1l1lll111ll_opy_ = False
        for fw in bstack11111ll1ll_opy_:
            if fw in framework:
                bstack1l1lll111ll_opy_ = True
        return bstack1l1llll1l1_opy_(bs_config.get(bstack1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᢋ"), bstack1l1lll111ll_opy_))
    @classmethod
    def bstack1l1lll1111l_opy_(cls, framework):
        return framework in bstack11111ll1ll_opy_
    @classmethod
    def bstack1ll111111ll_opy_(cls, bs_config, framework):
        return cls.bstack1l1lll11l1l_opy_(bs_config, framework) is True and cls.bstack1l1lll1111l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᢌ"), None)
    @staticmethod
    def bstack11l1l111ll_opy_():
        if getattr(threading.current_thread(), bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᢍ"), None):
            return {
                bstack1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬᢎ"): bstack1l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᢏ"),
                bstack1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᢐ"): getattr(threading.current_thread(), bstack1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᢑ"), None)
            }
        if getattr(threading.current_thread(), bstack1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᢒ"), None):
            return {
                bstack1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᢓ"): bstack1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᢔ"),
                bstack1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᢕ"): getattr(threading.current_thread(), bstack1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᢖ"), None)
            }
        return None
    @staticmethod
    def bstack1l1lll111l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111lll111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1111ll1_opy_(test, hook_name=None):
        bstack1l1lll11l11_opy_ = test.parent
        if hook_name in [bstack1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᢗ"), bstack1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᢘ"), bstack1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᢙ"), bstack1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᢚ")]:
            bstack1l1lll11l11_opy_ = test
        scope = []
        while bstack1l1lll11l11_opy_ is not None:
            scope.append(bstack1l1lll11l11_opy_.name)
            bstack1l1lll11l11_opy_ = bstack1l1lll11l11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1l1ll1lllll_opy_(hook_type):
        if hook_type == bstack1l11_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦᢛ"):
            return bstack1l11_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦᢜ")
        elif hook_type == bstack1l11_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧᢝ"):
            return bstack1l11_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤᢞ")
    @staticmethod
    def bstack1l1lll11111_opy_(bstack1l1l11lll1_opy_):
        try:
            if not bstack111lll111_opy_.on():
                return bstack1l1l11lll1_opy_
            if os.environ.get(bstack1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣᢟ"), None) == bstack1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᢠ"):
                tests = os.environ.get(bstack1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤᢡ"), None)
                if tests is None or tests == bstack1l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᢢ"):
                    return bstack1l1l11lll1_opy_
                bstack1l1l11lll1_opy_ = tests.split(bstack1l11_opy_ (u"ࠧ࠭ࠩᢣ"))
                return bstack1l1l11lll1_opy_
        except Exception as exc:
            logger.debug(bstack1l1ll1llll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࡽࡶࡸࡷ࠮ࡥࡹࡥࠬࢁࠧᢤ"))
        return bstack1l1l11lll1_opy_
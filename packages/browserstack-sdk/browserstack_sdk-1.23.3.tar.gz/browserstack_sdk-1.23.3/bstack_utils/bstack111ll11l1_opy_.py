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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111l11l111_opy_, bstack1ll111l1l1_opy_, get_host_info, bstack1llll1lll11_opy_, \
 bstack1ll1lllll1_opy_, bstack1ll111111l_opy_, bstack11l11llll1_opy_, bstack1llll1ll111_opy_, bstack11ll1111l1_opy_
import bstack_utils.bstack111ll11l11_opy_ as bstack1l1l11llll_opy_
from bstack_utils.bstack11l1ll1111_opy_ import bstack111lll111_opy_
from bstack_utils.percy import bstack1lllll11ll_opy_
from bstack_utils.config import Config
bstack111l11ll1_opy_ = Config.bstack11ll111lll_opy_()
logger = logging.getLogger(__name__)
percy = bstack1lllll11ll_opy_()
@bstack11l11llll1_opy_(class_method=False)
def bstack1ll11111lll_opy_(bs_config, bstack1l1l11ll1l_opy_):
  try:
    data = {
        bstack1l11_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ᡇ"): bstack1l11_opy_ (u"ࠧ࡫ࡵࡲࡲࠬᡈ"),
        bstack1l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧᡉ"): bs_config.get(bstack1l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᡊ"), bstack1l11_opy_ (u"ࠪࠫᡋ")),
        bstack1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᡌ"): bs_config.get(bstack1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᡍ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᡎ"): bs_config.get(bstack1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᡏ")),
        bstack1l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᡐ"): bs_config.get(bstack1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᡑ"), bstack1l11_opy_ (u"ࠪࠫᡒ")),
        bstack1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᡓ"): bstack11ll1111l1_opy_(),
        bstack1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪᡔ"): bstack1llll1lll11_opy_(bs_config),
        bstack1l11_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩᡕ"): get_host_info(),
        bstack1l11_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨᡖ"): bstack1ll111l1l1_opy_(),
        bstack1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᡗ"): os.environ.get(bstack1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᡘ")),
        bstack1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨᡙ"): os.environ.get(bstack1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩᡚ"), False),
        bstack1l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧᡛ"): bstack111l11l111_opy_(),
        bstack1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᡜ"): bstack1l1lll1l1l1_opy_(),
        bstack1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫᡝ"): bstack1l1lll1l111_opy_(bstack1l1l11ll1l_opy_),
        bstack1l11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᡞ"): bstack1llll1l111_opy_(bs_config, bstack1l1l11ll1l_opy_.get(bstack1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪᡟ"), bstack1l11_opy_ (u"ࠪࠫᡠ"))),
        bstack1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᡡ"): bstack1ll1lllll1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨᡢ").format(str(error)))
    return None
def bstack1l1lll1l111_opy_(framework):
  return {
    bstack1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᡣ"): framework.get(bstack1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨᡤ"), bstack1l11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᡥ")),
    bstack1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᡦ"): framework.get(bstack1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᡧ")),
    bstack1l11_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᡨ"): framework.get(bstack1l11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᡩ")),
    bstack1l11_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᡪ"): bstack1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᡫ"),
    bstack1l11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᡬ"): framework.get(bstack1l11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᡭ"))
  }
def bstack1llll1l111_opy_(bs_config, framework):
  bstack1l1ll11l_opy_ = False
  bstack1ll1ll1lll_opy_ = False
  bstack1l1lll11lll_opy_ = False
  if bstack1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᡮ") in bs_config:
    bstack1l1lll11lll_opy_ = True
  elif bstack1l11_opy_ (u"ࠫࡦࡶࡰࠨᡯ") in bs_config:
    bstack1l1ll11l_opy_ = True
  else:
    bstack1ll1ll1lll_opy_ = True
  bstack1l1l11l111_opy_ = {
    bstack1l11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᡰ"): bstack111lll111_opy_.bstack1l1lll11l1l_opy_(bs_config, framework),
    bstack1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᡱ"): bstack1l1l11llll_opy_.bstack1111lll111_opy_(bs_config),
    bstack1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᡲ"): bs_config.get(bstack1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᡳ"), False),
    bstack1l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᡴ"): bstack1ll1ll1lll_opy_,
    bstack1l11_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᡵ"): bstack1l1ll11l_opy_,
    bstack1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᡶ"): bstack1l1lll11lll_opy_
  }
  return bstack1l1l11l111_opy_
@bstack11l11llll1_opy_(class_method=False)
def bstack1l1lll1l1l1_opy_():
  try:
    bstack1l1lll11ll1_opy_ = json.loads(os.getenv(bstack1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᡷ"), bstack1l11_opy_ (u"࠭ࡻࡾࠩᡸ")))
    return {
        bstack1l11_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ᡹"): bstack1l1lll11ll1_opy_
    }
  except Exception as error:
    logger.error(bstack1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ᡺").format(str(error)))
    return {}
def bstack1l1lllll1ll_opy_(array, bstack1l1lll1lll1_opy_, bstack1l1lll1ll1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1l1lll1lll1_opy_]
    result[key] = o[bstack1l1lll1ll1l_opy_]
  return result
def bstack1ll1111l111_opy_(bstack11ll11111l_opy_=bstack1l11_opy_ (u"ࠩࠪ᡻")):
  bstack1l1lll1ll11_opy_ = bstack1l1l11llll_opy_.on()
  bstack1l1lll1llll_opy_ = bstack111lll111_opy_.on()
  bstack1l1lll1l11l_opy_ = percy.bstack11ll11ll1l_opy_()
  if bstack1l1lll1l11l_opy_ and not bstack1l1lll1llll_opy_ and not bstack1l1lll1ll11_opy_:
    return bstack11ll11111l_opy_ not in [bstack1l11_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ᡼"), bstack1l11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ᡽")]
  elif bstack1l1lll1ll11_opy_ and not bstack1l1lll1llll_opy_:
    return bstack11ll11111l_opy_ not in [bstack1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᡾"), bstack1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᡿"), bstack1l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᢀ")]
  return bstack1l1lll1ll11_opy_ or bstack1l1lll1llll_opy_ or bstack1l1lll1l11l_opy_
@bstack11l11llll1_opy_(class_method=False)
def bstack1ll1111lll1_opy_(bstack11ll11111l_opy_, test=None):
  bstack1l1lll1l1ll_opy_ = bstack1l1l11llll_opy_.on()
  if not bstack1l1lll1l1ll_opy_ or bstack11ll11111l_opy_ not in [bstack1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᢁ")] or test == None:
    return None
  return {
    bstack1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᢂ"): bstack1l1lll1l1ll_opy_ and bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᢃ"), None) == True and bstack1l1l11llll_opy_.bstack1lll1l1l1_opy_(test[bstack1l11_opy_ (u"ࠫࡹࡧࡧࡴࠩᢄ")])
  }
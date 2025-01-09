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
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111l1l111l_opy_, bstack1111lllll_opy_, get_host_info, bstack1lllll11l1l_opy_, \
 bstack1l1l11l1l1_opy_, bstack11l1l11l1_opy_, bstack11l11ll1ll_opy_, bstack1lllll1l111_opy_, bstack1ll1l1l11l_opy_
import bstack_utils.bstack111lll111l_opy_ as bstack1lll11ll_opy_
from bstack_utils.bstack11l1l11l11_opy_ import bstack1l111l1l_opy_
from bstack_utils.percy import bstack1l1l1l1lll_opy_
from bstack_utils.config import Config
bstack1111ll1l1_opy_ = Config.bstack1llll1lll_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1l1l1lll_opy_()
@bstack11l11ll1ll_opy_(class_method=False)
def bstack1ll1111l1ll_opy_(bs_config, bstack1ll11l1l_opy_):
  try:
    data = {
        bstack11l11_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ᡇ"): bstack11l11_opy_ (u"ࠧ࡫ࡵࡲࡲࠬᡈ"),
        bstack11l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧᡉ"): bs_config.get(bstack11l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᡊ"), bstack11l11_opy_ (u"ࠪࠫᡋ")),
        bstack11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᡌ"): bs_config.get(bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᡍ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᡎ"): bs_config.get(bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᡏ")),
        bstack11l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᡐ"): bs_config.get(bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᡑ"), bstack11l11_opy_ (u"ࠪࠫᡒ")),
        bstack11l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᡓ"): bstack1ll1l1l11l_opy_(),
        bstack11l11_opy_ (u"ࠬࡺࡡࡨࡵࠪᡔ"): bstack1lllll11l1l_opy_(bs_config),
        bstack11l11_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩᡕ"): get_host_info(),
        bstack11l11_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨᡖ"): bstack1111lllll_opy_(),
        bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᡗ"): os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᡘ")),
        bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨᡙ"): os.environ.get(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩᡚ"), False),
        bstack11l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧᡛ"): bstack111l1l111l_opy_(),
        bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᡜ"): bstack1l1lll1l1l1_opy_(),
        bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫᡝ"): bstack1l1lll11lll_opy_(bstack1ll11l1l_opy_),
        bstack11l11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᡞ"): bstack1l11ll11l1_opy_(bs_config, bstack1ll11l1l_opy_.get(bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪᡟ"), bstack11l11_opy_ (u"ࠪࠫᡠ"))),
        bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᡡ"): bstack1l1l11l1l1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨᡢ").format(str(error)))
    return None
def bstack1l1lll11lll_opy_(framework):
  return {
    bstack11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᡣ"): framework.get(bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨᡤ"), bstack11l11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᡥ")),
    bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᡦ"): framework.get(bstack11l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᡧ")),
    bstack11l11_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᡨ"): framework.get(bstack11l11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᡩ")),
    bstack11l11_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᡪ"): bstack11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᡫ"),
    bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᡬ"): framework.get(bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᡭ"))
  }
def bstack1l11ll11l1_opy_(bs_config, framework):
  bstack1lll1111ll_opy_ = False
  bstack1llll11l1l_opy_ = False
  bstack1l1lll1lll1_opy_ = False
  if bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᡮ") in bs_config:
    bstack1l1lll1lll1_opy_ = True
  elif bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨᡯ") in bs_config:
    bstack1lll1111ll_opy_ = True
  else:
    bstack1llll11l1l_opy_ = True
  bstack1l111111_opy_ = {
    bstack11l11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᡰ"): bstack1l111l1l_opy_.bstack1l1lll1l11l_opy_(bs_config, framework),
    bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᡱ"): bstack1lll11ll_opy_.bstack111l1l1111_opy_(bs_config),
    bstack11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᡲ"): bs_config.get(bstack11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᡳ"), False),
    bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᡴ"): bstack1llll11l1l_opy_,
    bstack11l11_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᡵ"): bstack1lll1111ll_opy_,
    bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᡶ"): bstack1l1lll1lll1_opy_
  }
  return bstack1l111111_opy_
@bstack11l11ll1ll_opy_(class_method=False)
def bstack1l1lll1l1l1_opy_():
  try:
    bstack1l1lll1ll1l_opy_ = json.loads(os.getenv(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᡷ"), bstack11l11_opy_ (u"࠭ࡻࡾࠩᡸ")))
    return {
        bstack11l11_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ᡹"): bstack1l1lll1ll1l_opy_
    }
  except Exception as error:
    logger.error(bstack11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ᡺").format(str(error)))
    return {}
def bstack1l1llll11l1_opy_(array, bstack1l1lll1llll_opy_, bstack1l1lll1l111_opy_):
  result = {}
  for o in array:
    key = o[bstack1l1lll1llll_opy_]
    result[key] = o[bstack1l1lll1l111_opy_]
  return result
def bstack1l1llllll11_opy_(bstack11lll11l1l_opy_=bstack11l11_opy_ (u"ࠩࠪ᡻")):
  bstack1l1lll1ll11_opy_ = bstack1lll11ll_opy_.on()
  bstack1l1lll11ll1_opy_ = bstack1l111l1l_opy_.on()
  bstack1l1lll11l1l_opy_ = percy.bstack1ll1l111l_opy_()
  if bstack1l1lll11l1l_opy_ and not bstack1l1lll11ll1_opy_ and not bstack1l1lll1ll11_opy_:
    return bstack11lll11l1l_opy_ not in [bstack11l11_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ᡼"), bstack11l11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ᡽")]
  elif bstack1l1lll1ll11_opy_ and not bstack1l1lll11ll1_opy_:
    return bstack11lll11l1l_opy_ not in [bstack11l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᡾"), bstack11l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᡿"), bstack11l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᢀ")]
  return bstack1l1lll1ll11_opy_ or bstack1l1lll11ll1_opy_ or bstack1l1lll11l1l_opy_
@bstack11l11ll1ll_opy_(class_method=False)
def bstack1ll111111l1_opy_(bstack11lll11l1l_opy_, test=None):
  bstack1l1lll1l1ll_opy_ = bstack1lll11ll_opy_.on()
  if not bstack1l1lll1l1ll_opy_ or bstack11lll11l1l_opy_ not in [bstack11l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᢁ")] or test == None:
    return None
  return {
    bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᢂ"): bstack1l1lll1l1ll_opy_ and bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᢃ"), None) == True and bstack1lll11ll_opy_.bstack1l1lll1l1_opy_(test[bstack11l11_opy_ (u"ࠫࡹࡧࡧࡴࠩᢄ")])
  }
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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack111l1111l1_opy_ as bstack111l111lll_opy_, EVENTS
from bstack_utils.bstack11lllll1ll_opy_ import bstack11lllll1ll_opy_
from bstack_utils.helper import bstack1ll1l1l11l_opy_, bstack11l1111111_opy_, bstack1l1l11l1l1_opy_, bstack111l1ll1l1_opy_, \
  bstack1111llll11_opy_, bstack1111lllll_opy_, get_host_info, bstack111l1l111l_opy_, bstack1lllll1l1_opy_, bstack11l11ll1ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11llll1ll1_opy_ import get_logger
from bstack_utils.bstack1111l1l11_opy_ import bstack111l1l1l1l_opy_
logger = get_logger(__name__)
bstack1111l1l11_opy_ = bstack111l1l1l1l_opy_()
@bstack11l11ll1ll_opy_(class_method=False)
def _1111llllll_opy_(driver, bstack111ll1ll1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l11_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪྟ"): caps.get(bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩྠ"), None),
        bstack11l11_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨྡ"): bstack111ll1ll1l_opy_.get(bstack11l11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨྡྷ"), None),
        bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬྣ"): caps.get(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬྤ"), None),
        bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪྥ"): caps.get(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪྦ"), None)
    }
  except Exception as error:
    logger.debug(bstack11l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧྦྷ") + str(error))
  return response
def on():
    if os.environ.get(bstack11l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩྨ"), None) is None or os.environ[bstack11l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪྩ")] == bstack11l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦྪ"):
        return False
    return True
def bstack111l1l1111_opy_(config):
  return config.get(bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧྫ"), False) or any([p.get(bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨྫྷ"), False) == True for p in config.get(bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬྭ"), [])])
def bstack1l11111111_opy_(config, bstack1l1l1l1ll_opy_):
  try:
    if not bstack1l1l11l1l1_opy_(config):
      return False
    bstack111l1ll111_opy_ = config.get(bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪྮ"), False)
    if int(bstack1l1l1l1ll_opy_) < len(config.get(bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧྯ"), [])) and config[bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨྰ")][bstack1l1l1l1ll_opy_]:
      bstack1111lll111_opy_ = config[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩྱ")][bstack1l1l1l1ll_opy_].get(bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧྲ"), None)
    else:
      bstack1111lll111_opy_ = config.get(bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨླ"), None)
    if bstack1111lll111_opy_ != None:
      bstack111l1ll111_opy_ = bstack1111lll111_opy_
    bstack111l1l1ll1_opy_ = os.getenv(bstack11l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧྴ")) is not None and len(os.getenv(bstack11l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨྵ"))) > 0 and os.getenv(bstack11l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩྶ")) != bstack11l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪྷ")
    return bstack111l1ll111_opy_ and bstack111l1l1ll1_opy_
  except Exception as error:
    logger.debug(bstack11l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ྸ") + str(error))
  return False
def bstack1l1lll1l1_opy_(test_tags):
  bstack111l11ll1l_opy_ = os.getenv(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨྐྵ"))
  if bstack111l11ll1l_opy_ is None:
    return True
  bstack111l11ll1l_opy_ = json.loads(bstack111l11ll1l_opy_)
  try:
    include_tags = bstack111l11ll1l_opy_[bstack11l11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ྺ")] if bstack11l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧྻ") in bstack111l11ll1l_opy_ and isinstance(bstack111l11ll1l_opy_[bstack11l11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨྼ")], list) else []
    exclude_tags = bstack111l11ll1l_opy_[bstack11l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ྽")] if bstack11l11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ྾") in bstack111l11ll1l_opy_ and isinstance(bstack111l11ll1l_opy_[bstack11l11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ྿")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢ࿀") + str(error))
  return False
def bstack111l11111l_opy_(config, bstack111l1111ll_opy_, bstack1111llll1l_opy_, bstack111l111l1l_opy_):
  bstack1111lll11l_opy_ = bstack111l1ll1l1_opy_(config)
  bstack111l111l11_opy_ = bstack1111llll11_opy_(config)
  if bstack1111lll11l_opy_ is None or bstack111l111l11_opy_ is None:
    logger.error(bstack11l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ࿁"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ࿂"), bstack11l11_opy_ (u"ࠪࡿࢂ࠭࿃")))
    data = {
        bstack11l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ࿄"): config[bstack11l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ࿅")],
        bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦ࿆ࠩ"): config.get(bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ࿇"), os.path.basename(os.getcwd())),
        bstack11l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫ࿈"): bstack1ll1l1l11l_opy_(),
        bstack11l11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ࿉"): config.get(bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭࿊"), bstack11l11_opy_ (u"ࠫࠬ࿋")),
        bstack11l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ࿌"): {
            bstack11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭࿍"): bstack111l1111ll_opy_,
            bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ࿎"): bstack1111llll1l_opy_,
            bstack11l11_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ࿏"): __version__,
            bstack11l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ࿐"): bstack11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ࿑"),
            bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ࿒"): bstack11l11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ࿓"),
            bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿔"): bstack111l111l1l_opy_
        },
        bstack11l11_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ࿕"): settings,
        bstack11l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩ࿖"): bstack111l1l111l_opy_(),
        bstack11l11_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩ࿗"): bstack1111lllll_opy_(),
        bstack11l11_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬ࿘"): get_host_info(),
        bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭࿙"): bstack1l1l11l1l1_opy_(config)
    }
    headers = {
        bstack11l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ࿚"): bstack11l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ࿛"),
    }
    config = {
        bstack11l11_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ࿜"): (bstack1111lll11l_opy_, bstack111l111l11_opy_),
        bstack11l11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ࿝"): headers
    }
    response = bstack1lllll1l1_opy_(bstack11l11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ࿞"), bstack111l111lll_opy_ + bstack11l11_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪ࿟"), data, config)
    bstack111l11llll_opy_ = response.json()
    if bstack111l11llll_opy_[bstack11l11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ࿠")]:
      parsed = json.loads(os.getenv(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭࿡"), bstack11l11_opy_ (u"࠭ࡻࡾࠩ࿢")))
      parsed[bstack11l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࿣")] = bstack111l11llll_opy_[bstack11l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭࿤")][bstack11l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ࿥")]
      os.environ[bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ࿦")] = json.dumps(parsed)
      bstack11lllll1ll_opy_.bstack111l111111_opy_(bstack111l11llll_opy_[bstack11l11_opy_ (u"ࠫࡩࡧࡴࡢࠩ࿧")][bstack11l11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭࿨")])
      bstack11lllll1ll_opy_.bstack111l1l1lll_opy_(bstack111l11llll_opy_[bstack11l11_opy_ (u"࠭ࡤࡢࡶࡤࠫ࿩")][bstack11l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ࿪")])
      bstack11lllll1ll_opy_.store()
      return bstack111l11llll_opy_[bstack11l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭࿫")][bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ࿬")], bstack111l11llll_opy_[bstack11l11_opy_ (u"ࠪࡨࡦࡺࡡࠨ࿭")][bstack11l11_opy_ (u"ࠫ࡮ࡪࠧ࿮")]
    else:
      logger.error(bstack11l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭࿯") + bstack111l11llll_opy_[bstack11l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿰")])
      if bstack111l11llll_opy_[bstack11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿱")] == bstack11l11_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪ࿲"):
        for bstack111l11l1ll_opy_ in bstack111l11llll_opy_[bstack11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ࿳")]:
          logger.error(bstack111l11l1ll_opy_[bstack11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿴")])
      return None, None
  except Exception as error:
    logger.error(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧ࿵") +  str(error))
    return None, None
def bstack111l11l1l1_opy_():
  if os.getenv(bstack11l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ࿶")) is None:
    return {
        bstack11l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿷"): bstack11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭࿸"),
        bstack11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿹"): bstack11l11_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨ࿺")
    }
  data = {bstack11l11_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫ࿻"): bstack1ll1l1l11l_opy_()}
  headers = {
      bstack11l11_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ࿼"): bstack11l11_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭࿽") + os.getenv(bstack11l11_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦ࿾")),
      bstack11l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭࿿"): bstack11l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫက")
  }
  response = bstack1lllll1l1_opy_(bstack11l11_opy_ (u"ࠩࡓ࡙࡙࠭ခ"), bstack111l111lll_opy_ + bstack11l11_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬဂ"), data, { bstack11l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬဃ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l11_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨင") + bstack11l1111111_opy_().isoformat() + bstack11l11_opy_ (u"࡚࠭ࠨစ"))
      return {bstack11l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧဆ"): bstack11l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩဇ"), bstack11l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဈ"): bstack11l11_opy_ (u"ࠪࠫဉ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢည") + str(error))
    return {
        bstack11l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬဋ"): bstack11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬဌ"),
        bstack11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨဍ"): str(error)
    }
def bstack1lll1111_opy_(caps, options, desired_capabilities={}):
  try:
    bstack111l11ll11_opy_ = caps.get(bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩဎ"), {}).get(bstack11l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ဏ"), caps.get(bstack11l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪတ"), bstack11l11_opy_ (u"ࠫࠬထ")))
    if bstack111l11ll11_opy_:
      logger.warn(bstack11l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤဒ"))
      return False
    if options:
      bstack111l1ll1ll_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack111l1ll1ll_opy_ = desired_capabilities
    else:
      bstack111l1ll1ll_opy_ = {}
    browser = caps.get(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫဓ"), bstack11l11_opy_ (u"ࠧࠨန")).lower() or bstack111l1ll1ll_opy_.get(bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ပ"), bstack11l11_opy_ (u"ࠩࠪဖ")).lower()
    if browser != bstack11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪဗ"):
      logger.warn(bstack11l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢဘ"))
      return False
    browser_version = caps.get(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭မ")) or caps.get(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨယ")) or bstack111l1ll1ll_opy_.get(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨရ")) or bstack111l1ll1ll_opy_.get(bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩလ"), {}).get(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪဝ")) or bstack111l1ll1ll_opy_.get(bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫသ"), {}).get(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ဟ"))
    if browser_version and browser_version != bstack11l11_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬဠ") and int(browser_version.split(bstack11l11_opy_ (u"࠭࠮ࠨအ"))[0]) <= 98:
      logger.warn(bstack11l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠻࠲ࠧဢ"))
      return False
    if not options:
      bstack111l1ll11l_opy_ = caps.get(bstack11l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ဣ")) or bstack111l1ll1ll_opy_.get(bstack11l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧဤ"), {})
      if bstack11l11_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧဥ") in bstack111l1ll11l_opy_.get(bstack11l11_opy_ (u"ࠫࡦࡸࡧࡴࠩဦ"), []):
        logger.warn(bstack11l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢဧ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣဨ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack111l11l111_opy_ = config.get(bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧဩ"), {})
    bstack111l11l111_opy_[bstack11l11_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫဪ")] = os.getenv(bstack11l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧါ"))
    bstack111l11lll1_opy_ = json.loads(os.getenv(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫာ"), bstack11l11_opy_ (u"ࠫࢀࢃࠧိ"))).get(bstack11l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ီ"))
    caps[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ု")] = True
    if bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨူ") in caps:
      caps[bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩေ")][bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩဲ")] = bstack111l11l111_opy_
      caps[bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫဳ")][bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫဴ")][bstack11l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ဵ")] = bstack111l11lll1_opy_
    else:
      caps[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬံ")] = bstack111l11l111_opy_
      caps[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ့࠭")][bstack11l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩး")] = bstack111l11lll1_opy_
  except Exception as error:
    logger.debug(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻္ࠢࠥ") +  str(error))
def bstack1l1llll11l_opy_(driver, bstack111l111ll1_opy_):
  try:
    setattr(driver, bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰ်ࠪ"), True)
    session = driver.session_id
    if session:
      bstack111l11l11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111l11l11l_opy_ = False
      bstack111l11l11l_opy_ = url.scheme in [bstack11l11_opy_ (u"ࠦ࡭ࡺࡴࡱࠤျ"), bstack11l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦြ")]
      if bstack111l11l11l_opy_:
        if bstack111l111ll1_opy_:
          logger.info(bstack11l11_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨွ"))
      return bstack111l111ll1_opy_
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥှ") + str(e))
    return False
def bstack1ll1ll1l1l_opy_(driver, name, path):
  try:
    bstack1111lll1ll_opy_ = {
        bstack11l11_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨဿ"): threading.current_thread().current_test_uuid,
        bstack11l11_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ၀"): os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ၁"), bstack11l11_opy_ (u"ࠫࠬ၂")),
        bstack11l11_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩ၃"): os.environ.get(bstack11l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ၄"), bstack11l11_opy_ (u"ࠧࠨ၅"))
    }
    bstack111l1l11l1_opy_ = bstack1111l1l11_opy_.bstack111l1l1l11_opy_(EVENTS.bstack1l1l11111_opy_.value)
    bstack1111l1l11_opy_.mark(bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ၆"))
    logger.debug(bstack11l11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ၇"))
    try:
      logger.debug(driver.execute_async_script(bstack11lllll1ll_opy_.perform_scan, {bstack11l11_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥ၈"): name}))
      bstack1111l1l11_opy_.end(bstack111l1l11l1_opy_, bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ၉"), bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ၊"), True, None)
    except Exception as error:
      bstack1111l1l11_opy_.end(bstack111l1l11l1_opy_, bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ။"), bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ၌"), False, str(error))
    bstack111l1l11l1_opy_ = bstack1111l1l11_opy_.bstack111l1l1l11_opy_(EVENTS.bstack1111lll1l1_opy_.value)
    bstack1111l1l11_opy_.mark(bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ၍"))
    try:
      logger.debug(driver.execute_async_script(bstack11lllll1ll_opy_.bstack111l1l11ll_opy_, bstack1111lll1ll_opy_))
      bstack1111l1l11_opy_.end(bstack111l1l11l1_opy_, bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ၎"), bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ၏"),True, None)
    except Exception as error:
      bstack1111l1l11_opy_.end(bstack111l1l11l1_opy_, bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦၐ"), bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥၑ"),False, str(error))
    logger.info(bstack11l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤၒ"))
  except Exception as bstack1111lllll1_opy_:
    logger.error(bstack11l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤၓ") + str(path) + bstack11l11_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥၔ") + str(bstack1111lllll1_opy_))
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
import atexit
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.measure import bstack1111l1l11_opy_
from bstack_utils.percy import *
from browserstack_sdk.bstack11lll111ll_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l111111l1_opy_ import bstack1lllll1lll_opy_
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack11llllll1l_opy_():
  global CONFIG
  headers = {
        bstack11l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll1ll1l1_opy_(CONFIG, bstack1l1l1ll111_opy_)
  try:
    response = requests.get(bstack1l1l1ll111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11l1lll1l_opy_ = response.json()[bstack11l11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11ll11111l_opy_.format(response.json()))
      return bstack11l1lll1l_opy_
    else:
      logger.debug(bstack11ll1l11l1_opy_.format(bstack11l11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11ll1l11l1_opy_.format(e))
def bstack1l1l1l1l1l_opy_(hub_url):
  global CONFIG
  url = bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11l11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll1ll1l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l11l11_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1l1lll1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.SINGLE)
def bstack1l111ll1l_opy_():
  try:
    global bstack1ll1111lll_opy_
    bstack11l1lll1l_opy_ = bstack11llllll1l_opy_()
    bstack111ll1111_opy_ = []
    results = []
    for bstack111ll11ll_opy_ in bstack11l1lll1l_opy_:
      bstack111ll1111_opy_.append(bstack11ll1ll111_opy_(target=bstack1l1l1l1l1l_opy_,args=(bstack111ll11ll_opy_,)))
    for t in bstack111ll1111_opy_:
      t.start()
    for t in bstack111ll1111_opy_:
      results.append(t.join())
    bstack11111l111_opy_ = {}
    for item in results:
      hub_url = item[bstack11l11_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11l11_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11111l111_opy_[hub_url] = latency
    bstack1lllll111_opy_ = min(bstack11111l111_opy_, key= lambda x: bstack11111l111_opy_[x])
    bstack1ll1111lll_opy_ = bstack1lllll111_opy_
    logger.debug(bstack11l11lll1_opy_.format(bstack1lllll111_opy_))
  except Exception as e:
    logger.debug(bstack111l11l11_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack11llll1ll1_opy_
from bstack_utils.helper import bstack11l111111_opy_, bstack1lllll1l1_opy_, bstack1ll11l111_opy_, bstack11l1l11l1_opy_, \
  bstack1l1l11l1l1_opy_, \
  Notset, bstack11llllll_opy_, \
  bstack1lll11111_opy_, bstack1l11l11ll_opy_, bstack1l111ll1_opy_, bstack1111lllll_opy_, bstack1111llll_opy_, bstack1l11111lll_opy_, \
  bstack1ll111l1ll_opy_, \
  bstack11llll1l1_opy_, bstack1ll1l11ll_opy_, bstack1llllll11l_opy_, bstack11lll11l1_opy_, \
  bstack1l1l1ll11l_opy_, bstack1l111lll1_opy_, bstack1ll1l1l11_opy_, bstack1l11l1ll1l_opy_
from bstack_utils.bstack1l111l11l1_opy_ import bstack1llll11111_opy_
from bstack_utils.bstack1l1l11ll11_opy_ import bstack1ll11lll11_opy_
from bstack_utils.bstack11ll1llll_opy_ import bstack1ll1ll1l11_opy_, bstack11111lll1_opy_
from bstack_utils.bstack11lllll1ll_opy_ import bstack11lllll1ll_opy_
from bstack_utils.proxy import bstack1l1111l11l_opy_, bstack1ll1ll1l1_opy_, bstack1l1ll1ll1l_opy_, bstack1l11l11l1l_opy_
from browserstack_sdk.bstack1l1l111ll1_opy_ import *
from browserstack_sdk.bstack1ll1111l_opy_ import *
from bstack_utils.bstack11l1llll1_opy_ import bstack11l1ll1l_opy_
from browserstack_sdk.bstack11l1111l1_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack11llll1ll1_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack11lll1l1_opy_, stage=STAGE.SINGLE)
def bstack1ll1lll11_opy_():
    global bstack1ll1111lll_opy_
    try:
        bstack1l111l1ll1_opy_ = bstack1ll1l11l1l_opy_()
        bstack11l1l1ll1_opy_(bstack1l111l1ll1_opy_)
        hub_url = bstack1l111l1ll1_opy_.get(bstack11l11_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack11l11_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack11l11_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack11l11_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1ll1111lll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1ll1l11l1l_opy_():
    global CONFIG
    bstack11lll11111_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack11l11_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack11l11_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack11lll11111_opy_, str):
        raise ValueError(bstack11l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1l111l1ll1_opy_ = bstack111l11111_opy_(bstack11lll11111_opy_)
        return bstack1l111l1ll1_opy_
    except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack111l11111_opy_(bstack11lll11111_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack11l11_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1lllll11ll_opy_ + bstack11lll11111_opy_
        auth = (CONFIG[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11l11l1l1_opy_ = json.loads(response.text)
            return bstack11l11l1l1_opy_
    except ValueError as ve:
        logger.error(bstack11l11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11l1l1ll1_opy_(bstack1lll1l1ll_opy_):
    global CONFIG
    if bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack11l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack11l11_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1lll1l1ll_opy_:
        bstack111lllll_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack11l11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack111lllll_opy_)
        bstack11l1l1l1l_opy_ = bstack1lll1l1ll_opy_.get(bstack11l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack11l111l1_opy_ = bstack11l11_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack11l1l1l1l_opy_)
        logger.debug(bstack11l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack11l111l1_opy_)
        bstack11ll1lll1_opy_ = {
            bstack11l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack11l11_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack11l11_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack11l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack11l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack11l111l1_opy_
        }
        bstack111lllll_opy_.update(bstack11ll1lll1_opy_)
        logger.debug(bstack11l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack111lllll_opy_)
        CONFIG[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack111lllll_opy_
        logger.debug(bstack11l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1l11lllll_opy_():
    bstack1l111l1ll1_opy_ = bstack1ll1l11l1l_opy_()
    if not bstack1l111l1ll1_opy_[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack11l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1l111l1ll1_opy_[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack11l11_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1llllll11_opy_, stage=STAGE.SINGLE)
def bstack11lll111l1_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1lll1111l_opy_
        logger.debug(bstack11l11_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11l11_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack11l11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1ll11111l_opy_ = json.loads(response.text)
                bstack11ll1lllll_opy_ = bstack1ll11111l_opy_.get(bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack11ll1lllll_opy_:
                    bstack1l1l1l11_opy_ = bstack11ll1lllll_opy_[0]
                    bstack1l11l11l_opy_ = bstack1l1l1l11_opy_.get(bstack11l11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack111lll11l_opy_ = bstack1l1lll1l1l_opy_ + bstack1l11l11l_opy_
                    result.extend([bstack1l11l11l_opy_, bstack111lll11l_opy_])
                    logger.info(bstack1l1ll1ll_opy_.format(bstack111lll11l_opy_))
                    bstack1lll1lll1l_opy_ = CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1lll1lll1l_opy_ += bstack11l11_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1lll1lll1l_opy_ != bstack1l1l1l11_opy_.get(bstack11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack11ll1lll_opy_.format(bstack1l1l1l11_opy_.get(bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1lll1lll1l_opy_))
                    return result
                else:
                    logger.debug(bstack11l11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack11l11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack11l11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack11l11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
import bstack_utils.bstack1l1ll111ll_opy_ as bstack1l1l111l1l_opy_
import bstack_utils.bstack1l11ll1111_opy_ as bstack111l1l11l_opy_
bstack1l1llll1l1_opy_ = bstack11l11_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࢹ")
bstack1lll1l111_opy_ = bstack11l11_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧࢺ")
from ._version import __version__
bstack1l111l11l_opy_ = None
CONFIG = {}
bstack1l1111l11_opy_ = {}
bstack1llllll1ll_opy_ = {}
bstack1l1111l1l_opy_ = None
bstack1ll11l1l1l_opy_ = None
bstack1l1l1ll1_opy_ = None
bstack11ll11l111_opy_ = -1
bstack111111l1l_opy_ = 0
bstack1ll1111111_opy_ = bstack1l1lllll1l_opy_
bstack11ll111l_opy_ = 1
bstack1l11ll1lll_opy_ = False
bstack1l11l1l111_opy_ = False
bstack1l11111l1l_opy_ = bstack11l11_opy_ (u"ࠩࠪࢻ")
bstack111lll1l1_opy_ = bstack11l11_opy_ (u"ࠪࠫࢼ")
bstack11l1l1l1_opy_ = False
bstack11111ll11_opy_ = True
bstack1l1111ll1l_opy_ = bstack11l11_opy_ (u"ࠫࠬࢽ")
bstack1llll111_opy_ = []
bstack1ll1111lll_opy_ = bstack11l11_opy_ (u"ࠬ࠭ࢾ")
bstack1l11l1l1l1_opy_ = False
bstack1111l11l_opy_ = None
bstack1l1l111111_opy_ = None
bstack11l1ll1ll_opy_ = None
bstack11llll11ll_opy_ = -1
bstack1ll1ll11l_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"࠭ࡾࠨࢿ")), bstack11l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣀ"), bstack11l11_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣁ"))
bstack1llll1llll_opy_ = 0
bstack1ll11lll1l_opy_ = 0
bstack1l1ll11l_opy_ = []
bstack11ll111ll_opy_ = []
bstack1ll11ll11_opy_ = []
bstack1l1lll11_opy_ = []
bstack1111l11ll_opy_ = bstack11l11_opy_ (u"ࠩࠪࣂ")
bstack11l11111l_opy_ = bstack11l11_opy_ (u"ࠪࠫࣃ")
bstack1l1lll1l11_opy_ = False
bstack1llll1ll1_opy_ = False
bstack1l11ll111l_opy_ = {}
bstack11ll1ll11l_opy_ = None
bstack111l1l1l1_opy_ = None
bstack1l1l11l1ll_opy_ = None
bstack11l11llll_opy_ = None
bstack1ll11111_opy_ = None
bstack111ll1l11_opy_ = None
bstack1lll11ll11_opy_ = None
bstack11ll11ll_opy_ = None
bstack1l1lll1ll1_opy_ = None
bstack1l111111ll_opy_ = None
bstack111llll1_opy_ = None
bstack11ll11l1l_opy_ = None
bstack1llll11ll1_opy_ = None
bstack1l11l11ll1_opy_ = None
bstack1111l1ll1_opy_ = None
bstack1llll1111l_opy_ = None
bstack1l1l11l11_opy_ = None
bstack1l1l1l11l_opy_ = None
bstack11lll1l1ll_opy_ = None
bstack1lll111l1_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack1ll1lllll_opy_ = None
bstack1l1l1111l_opy_ = False
bstack11l11l1l_opy_ = bstack11l11_opy_ (u"ࠦࠧࣄ")
logger = bstack11llll1ll1_opy_.get_logger(__name__, bstack1ll1111111_opy_)
bstack1111ll1l1_opy_ = Config.bstack1llll1lll_opy_()
percy = bstack1l1l1l1lll_opy_()
bstack1ll11l1111_opy_ = bstack1lllll1lll_opy_()
bstack1l1111lll_opy_ = bstack11l1111l1_opy_()
def bstack11lll1llll_opy_():
  global CONFIG
  global bstack1l1lll1l11_opy_
  global bstack1111ll1l1_opy_
  bstack11ll1111l_opy_ = bstack1l1l1111_opy_(CONFIG)
  if bstack1l1l11l1l1_opy_(CONFIG):
    if (bstack11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࣅ") in bstack11ll1111l_opy_ and str(bstack11ll1111l_opy_[bstack11l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࣆ")]).lower() == bstack11l11_opy_ (u"ࠧࡵࡴࡸࡩࠬࣇ")):
      bstack1l1lll1l11_opy_ = True
    bstack1111ll1l1_opy_.bstack11ll1ll1_opy_(bstack11ll1111l_opy_.get(bstack11l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬࣈ"), False))
  else:
    bstack1l1lll1l11_opy_ = True
    bstack1111ll1l1_opy_.bstack11ll1ll1_opy_(True)
def bstack11ll11l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1111ll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11ll111111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11l11_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨࣉ") == args[i].lower() or bstack11l11_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪࠦ࣊") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1111ll1l_opy_
      bstack1l1111ll1l_opy_ += bstack11l11_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠡࠩ࣋") + path
      return path
  return None
bstack1ll1l1111_opy_ = re.compile(bstack11l11_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿ࠣ࣌"))
def bstack111l11lll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1ll1l1111_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11l11_opy_ (u"ࠨࠤࡼࠤ࣍") + group + bstack11l11_opy_ (u"ࠢࡾࠤ࣎"), os.environ.get(group))
  return value
def bstack1l111l11ll_opy_():
  bstack1l11lll1l_opy_ = bstack11ll111111_opy_()
  if bstack1l11lll1l_opy_ and os.path.exists(os.path.abspath(bstack1l11lll1l_opy_)):
    fileName = bstack1l11lll1l_opy_
  if bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉ࣏ࠬ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࣐࠭")])) and not bstack11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩ࣑ࠬ") in locals():
    fileName = os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")]
  if bstack11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫࣓ࠧ") in locals():
    bstack1lll1ll_opy_ = os.path.abspath(fileName)
  else:
    bstack1lll1ll_opy_ = bstack11l11_opy_ (u"࠭ࠧࣔ")
  bstack1l111ll11_opy_ = os.getcwd()
  bstack11111111l_opy_ = bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣕ")
  bstack11lll11l11_opy_ = bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣖ")
  while (not os.path.exists(bstack1lll1ll_opy_)) and bstack1l111ll11_opy_ != bstack11l11_opy_ (u"ࠤࠥࣗ"):
    bstack1lll1ll_opy_ = os.path.join(bstack1l111ll11_opy_, bstack11111111l_opy_)
    if not os.path.exists(bstack1lll1ll_opy_):
      bstack1lll1ll_opy_ = os.path.join(bstack1l111ll11_opy_, bstack11lll11l11_opy_)
    if bstack1l111ll11_opy_ != os.path.dirname(bstack1l111ll11_opy_):
      bstack1l111ll11_opy_ = os.path.dirname(bstack1l111ll11_opy_)
    else:
      bstack1l111ll11_opy_ = bstack11l11_opy_ (u"ࠥࠦࣘ")
  if not os.path.exists(bstack1lll1ll_opy_):
    bstack111111ll_opy_(
      bstack11lll1ll11_opy_.format(os.getcwd()))
  try:
    with open(bstack1lll1ll_opy_, bstack11l11_opy_ (u"ࠫࡷ࠭ࣙ")) as stream:
      yaml.add_implicit_resolver(bstack11l11_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣚ"), bstack1ll1l1111_opy_)
      yaml.add_constructor(bstack11l11_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࠢࣛ"), bstack111l11lll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1lll1ll_opy_, bstack11l11_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack111111ll_opy_(bstack1lllll11_opy_.format(str(exc)))
def bstack1l1l1lll11_opy_(config):
  bstack1lll111l_opy_ = bstack1l1lll1ll_opy_(config)
  for option in list(bstack1lll111l_opy_):
    if option.lower() in bstack11lll1ll1_opy_ and option != bstack11lll1ll1_opy_[option.lower()]:
      bstack1lll111l_opy_[bstack11lll1ll1_opy_[option.lower()]] = bstack1lll111l_opy_[option]
      del bstack1lll111l_opy_[option]
  return config
def bstack11llll1lll_opy_():
  global bstack1llllll1ll_opy_
  for key, bstack1llll1l1l_opy_ in bstack1l11lll1ll_opy_.items():
    if isinstance(bstack1llll1l1l_opy_, list):
      for var in bstack1llll1l1l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1llllll1ll_opy_[key] = os.environ[var]
          break
    elif bstack1llll1l1l_opy_ in os.environ and os.environ[bstack1llll1l1l_opy_] and str(os.environ[bstack1llll1l1l_opy_]).strip():
      bstack1llllll1ll_opy_[key] = os.environ[bstack1llll1l1l_opy_]
  if bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣝ") in os.environ:
    bstack1llllll1ll_opy_[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣞ")] = {}
    bstack1llllll1ll_opy_[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣟ")][bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")] = os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ࣡")]
def bstack11lllll1l_opy_():
  global bstack1l1111l11_opy_
  global bstack1l1111ll1l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11l11_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣢").lower() == val.lower():
      bstack1l1111l11_opy_[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣣࠫ")] = {}
      bstack1l1111l11_opy_[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣤ")][bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣥ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1lllll1ll1_opy_ in bstack111l1l11_opy_.items():
    if isinstance(bstack1lllll1ll1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lllll1ll1_opy_:
          if idx < len(sys.argv) and bstack11l11_opy_ (u"ࠪ࠱࠲ࣦ࠭") + var.lower() == val.lower() and not key in bstack1l1111l11_opy_:
            bstack1l1111l11_opy_[key] = sys.argv[idx + 1]
            bstack1l1111ll1l_opy_ += bstack11l11_opy_ (u"ࠫࠥ࠳࠭ࠨࣧ") + var + bstack11l11_opy_ (u"ࠬࠦࠧࣨ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11l11_opy_ (u"࠭࠭࠮ࣩࠩ") + bstack1lllll1ll1_opy_.lower() == val.lower() and not key in bstack1l1111l11_opy_:
          bstack1l1111l11_opy_[key] = sys.argv[idx + 1]
          bstack1l1111ll1l_opy_ += bstack11l11_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + bstack1lllll1ll1_opy_ + bstack11l11_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack11ll1ll1l_opy_(config):
  bstack1l1lll111_opy_ = config.keys()
  for bstack1lll111ll_opy_, bstack11ll1l1l1l_opy_ in bstack1l11lllll1_opy_.items():
    if bstack11ll1l1l1l_opy_ in bstack1l1lll111_opy_:
      config[bstack1lll111ll_opy_] = config[bstack11ll1l1l1l_opy_]
      del config[bstack11ll1l1l1l_opy_]
  for bstack1lll111ll_opy_, bstack11ll1l1l1l_opy_ in bstack111l1lll_opy_.items():
    if isinstance(bstack11ll1l1l1l_opy_, list):
      for bstack11111lll_opy_ in bstack11ll1l1l1l_opy_:
        if bstack11111lll_opy_ in bstack1l1lll111_opy_:
          config[bstack1lll111ll_opy_] = config[bstack11111lll_opy_]
          del config[bstack11111lll_opy_]
          break
    elif bstack11ll1l1l1l_opy_ in bstack1l1lll111_opy_:
      config[bstack1lll111ll_opy_] = config[bstack11ll1l1l1l_opy_]
      del config[bstack11ll1l1l1l_opy_]
  for bstack11111lll_opy_ in list(config):
    for bstack1l1ll1l11l_opy_ in bstack11lllll1l1_opy_:
      if bstack11111lll_opy_.lower() == bstack1l1ll1l11l_opy_.lower() and bstack11111lll_opy_ != bstack1l1ll1l11l_opy_:
        config[bstack1l1ll1l11l_opy_] = config[bstack11111lll_opy_]
        del config[bstack11111lll_opy_]
  bstack1l11l111l1_opy_ = [{}]
  if not config.get(bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࣬")):
    config[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࣭࠭")] = [{}]
  bstack1l11l111l1_opy_ = config[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ࣮ࠧ")]
  for platform in bstack1l11l111l1_opy_:
    for bstack11111lll_opy_ in list(platform):
      for bstack1l1ll1l11l_opy_ in bstack11lllll1l1_opy_:
        if bstack11111lll_opy_.lower() == bstack1l1ll1l11l_opy_.lower() and bstack11111lll_opy_ != bstack1l1ll1l11l_opy_:
          platform[bstack1l1ll1l11l_opy_] = platform[bstack11111lll_opy_]
          del platform[bstack11111lll_opy_]
  for bstack1lll111ll_opy_, bstack11ll1l1l1l_opy_ in bstack111l1lll_opy_.items():
    for platform in bstack1l11l111l1_opy_:
      if isinstance(bstack11ll1l1l1l_opy_, list):
        for bstack11111lll_opy_ in bstack11ll1l1l1l_opy_:
          if bstack11111lll_opy_ in platform:
            platform[bstack1lll111ll_opy_] = platform[bstack11111lll_opy_]
            del platform[bstack11111lll_opy_]
            break
      elif bstack11ll1l1l1l_opy_ in platform:
        platform[bstack1lll111ll_opy_] = platform[bstack11ll1l1l1l_opy_]
        del platform[bstack11ll1l1l1l_opy_]
  for bstack11ll111l11_opy_ in bstack1lll1l11ll_opy_:
    if bstack11ll111l11_opy_ in config:
      if not bstack1lll1l11ll_opy_[bstack11ll111l11_opy_] in config:
        config[bstack1lll1l11ll_opy_[bstack11ll111l11_opy_]] = {}
      config[bstack1lll1l11ll_opy_[bstack11ll111l11_opy_]].update(config[bstack11ll111l11_opy_])
      del config[bstack11ll111l11_opy_]
  for platform in bstack1l11l111l1_opy_:
    for bstack11ll111l11_opy_ in bstack1lll1l11ll_opy_:
      if bstack11ll111l11_opy_ in list(platform):
        if not bstack1lll1l11ll_opy_[bstack11ll111l11_opy_] in platform:
          platform[bstack1lll1l11ll_opy_[bstack11ll111l11_opy_]] = {}
        platform[bstack1lll1l11ll_opy_[bstack11ll111l11_opy_]].update(platform[bstack11ll111l11_opy_])
        del platform[bstack11ll111l11_opy_]
  config = bstack1l1l1lll11_opy_(config)
  return config
def bstack1lll1l1l_opy_(config):
  global bstack111lll1l1_opy_
  bstack1l1llllll1_opy_ = False
  if bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦ࣯ࠩ") in config and str(config[bstack11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࣰࠪ")]).lower() != bstack11l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪࣱ࠭"):
    if bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࣲࠬ") not in config or str(config[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ࣳ")]).lower() == bstack11l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
      config[bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪࣵ")] = False
    else:
      bstack1l111l1ll1_opy_ = bstack1ll1l11l1l_opy_()
      if bstack11l11_opy_ (u"ࠬ࡯ࡳࡕࡴ࡬ࡥࡱࡍࡲࡪࡦࣶࠪ") in bstack1l111l1ll1_opy_:
        if not bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࣷ") in config:
          config[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣸ")] = {}
        config[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣹࠬ")][bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࣺࠫ")] = bstack11l11_opy_ (u"ࠪࡥࡹࡹ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩࣻ")
        bstack1l1llllll1_opy_ = True
        bstack111lll1l1_opy_ = config[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")].get(bstack11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ"))
  if bstack1l1l11l1l1_opy_(config) and bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࣾ") in config and str(config[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ")]).lower() != bstack11l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ") and not bstack1l1llllll1_opy_:
    if not bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ") in config:
      config[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧं")] = {}
    if not config[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨः")].get(bstack11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠩऄ")) and not bstack11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨअ") in config[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")]:
      bstack1ll1l1l11l_opy_ = datetime.datetime.now()
      bstack1llll1l11_opy_ = bstack1ll1l1l11l_opy_.strftime(bstack11l11_opy_ (u"ࠨࠧࡧࡣࠪࡨ࡟ࠦࡊࠨࡑࠬइ"))
      hostname = socket.gethostname()
      bstack1l111l11_opy_ = bstack11l11_opy_ (u"ࠩࠪई").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l11_opy_ (u"ࠪࡿࢂࡥࡻࡾࡡࡾࢁࠬउ").format(bstack1llll1l11_opy_, hostname, bstack1l111l11_opy_)
      config[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ")][bstack11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऋ")] = identifier
    bstack111lll1l1_opy_ = config[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")].get(bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऍ"))
  return config
def bstack1ll11llll1_opy_():
  bstack1l1l11l1_opy_ =  bstack1111lllll_opy_()[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠧऎ")]
  return bstack1l1l11l1_opy_ if bstack1l1l11l1_opy_ else -1
def bstack111111111_opy_(bstack1l1l11l1_opy_):
  global CONFIG
  if not bstack11l11_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫए") in CONFIG[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ")]:
    return
  CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ")] = CONFIG[bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ")].replace(
    bstack11l11_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨओ"),
    str(bstack1l1l11l1_opy_)
  )
def bstack1lll1l111l_opy_():
  global CONFIG
  if not bstack11l11_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭औ") in CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")]:
    return
  bstack1ll1l1l11l_opy_ = datetime.datetime.now()
  bstack1llll1l11_opy_ = bstack1ll1l1l11l_opy_.strftime(bstack11l11_opy_ (u"ࠩࠨࡨ࠲ࠫࡢ࠮ࠧࡋ࠾ࠪࡓࠧख"))
  CONFIG[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬग")] = CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")].replace(
    bstack11l11_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫङ"),
    bstack1llll1l11_opy_
  )
def bstack1ll111l1_opy_():
  global CONFIG
  if bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच") in CONFIG and not bool(CONFIG[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")]):
    del CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")]
    return
  if not bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG:
    CONFIG[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = bstack11l11_opy_ (u"ࠫࠨࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧट")
  if bstack11l11_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫठ") in CONFIG[bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")]:
    bstack1lll1l111l_opy_()
    os.environ[bstack11l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫढ")] = CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪण")]
  if not bstack11l11_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫत") in CONFIG[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]:
    return
  bstack1l1l11l1_opy_ = bstack11l11_opy_ (u"ࠫࠬद")
  bstack1l1ll1l11_opy_ = bstack1ll11llll1_opy_()
  if bstack1l1ll1l11_opy_ != -1:
    bstack1l1l11l1_opy_ = bstack11l11_opy_ (u"ࠬࡉࡉࠡࠩध") + str(bstack1l1ll1l11_opy_)
  if bstack1l1l11l1_opy_ == bstack11l11_opy_ (u"࠭ࠧन"):
    bstack111l1ll1l_opy_ = bstack1l1111l1l1_opy_(CONFIG[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪऩ")])
    if bstack111l1ll1l_opy_ != -1:
      bstack1l1l11l1_opy_ = str(bstack111l1ll1l_opy_)
  if bstack1l1l11l1_opy_:
    bstack111111111_opy_(bstack1l1l11l1_opy_)
    os.environ[bstack11l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬप")] = CONFIG[bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
def bstack1l1lllllll_opy_(bstack11lll1ll1l_opy_, bstack11l1l111l_opy_, path):
  bstack1l11l1l1l_opy_ = {
    bstack11l11_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧब"): bstack11l1l111l_opy_
  }
  if os.path.exists(path):
    bstack1ll1lllll1_opy_ = json.load(open(path, bstack11l11_opy_ (u"ࠫࡷࡨࠧभ")))
  else:
    bstack1ll1lllll1_opy_ = {}
  bstack1ll1lllll1_opy_[bstack11lll1ll1l_opy_] = bstack1l11l1l1l_opy_
  with open(path, bstack11l11_opy_ (u"ࠧࡽࠫࠣम")) as outfile:
    json.dump(bstack1ll1lllll1_opy_, outfile)
def bstack1l1111l1l1_opy_(bstack11lll1ll1l_opy_):
  bstack11lll1ll1l_opy_ = str(bstack11lll1ll1l_opy_)
  bstack1l1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"࠭ࡾࠨय")), bstack11l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧर"))
  try:
    if not os.path.exists(bstack1l1lll1lll_opy_):
      os.makedirs(bstack1l1lll1lll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠨࢀࠪऱ")), bstack11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩल"), bstack11l11_opy_ (u"ࠪ࠲ࡧࡻࡩ࡭ࡦ࠰ࡲࡦࡳࡥ࠮ࡥࡤࡧ࡭࡫࠮࡫ࡵࡲࡲࠬळ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l11_opy_ (u"ࠫࡼ࠭ऴ")):
        pass
      with open(file_path, bstack11l11_opy_ (u"ࠧࡽࠫࠣव")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l11_opy_ (u"࠭ࡲࠨश")) as bstack11ll11ll1_opy_:
      bstack1lll1llll1_opy_ = json.load(bstack11ll11ll1_opy_)
    if bstack11lll1ll1l_opy_ in bstack1lll1llll1_opy_:
      bstack11llllll1_opy_ = bstack1lll1llll1_opy_[bstack11lll1ll1l_opy_][bstack11l11_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫष")]
      bstack1l111ll11l_opy_ = int(bstack11llllll1_opy_) + 1
      bstack1l1lllllll_opy_(bstack11lll1ll1l_opy_, bstack1l111ll11l_opy_, file_path)
      return bstack1l111ll11l_opy_
    else:
      bstack1l1lllllll_opy_(bstack11lll1ll1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll111l1l1_opy_.format(str(e)))
    return -1
def bstack1ll11ll1l_opy_(config):
  if not config[bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪस")] or not config[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬह")]:
    return True
  else:
    return False
def bstack1ll11lllll_opy_(config, index=0):
  global bstack11l1l1l1_opy_
  bstack1lll11lll_opy_ = {}
  caps = bstack1l111l1l11_opy_ + bstack1ll1llllll_opy_
  if config.get(bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧऺ"), False):
    bstack1lll11lll_opy_[bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨऻ")] = True
    bstack1lll11lll_opy_[bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")] = config.get(bstack11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪऽ"), {})
  if bstack11l1l1l1_opy_:
    caps += bstack1l11ll1l1_opy_
  for key in config:
    if key in caps + [bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪा")]:
      continue
    bstack1lll11lll_opy_[key] = config[key]
  if bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫि") in config:
    for bstack1111l1lll_opy_ in config[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬी")][index]:
      if bstack1111l1lll_opy_ in caps:
        continue
      bstack1lll11lll_opy_[bstack1111l1lll_opy_] = config[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")][index][bstack1111l1lll_opy_]
  bstack1lll11lll_opy_[bstack11l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ू")] = socket.gethostname()
  if bstack11l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ृ") in bstack1lll11lll_opy_:
    del (bstack1lll11lll_opy_[bstack11l11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧॄ")])
  return bstack1lll11lll_opy_
def bstack1l1ll111l_opy_(config):
  global bstack11l1l1l1_opy_
  bstack1l1l1ll1l_opy_ = {}
  caps = bstack1ll1llllll_opy_
  if bstack11l1l1l1_opy_:
    caps += bstack1l11ll1l1_opy_
  for key in caps:
    if key in config:
      bstack1l1l1ll1l_opy_[key] = config[key]
  return bstack1l1l1ll1l_opy_
def bstack11111ll1l_opy_(bstack1lll11lll_opy_, bstack1l1l1ll1l_opy_):
  bstack11ll111ll1_opy_ = {}
  for key in bstack1lll11lll_opy_.keys():
    if key in bstack1l11lllll1_opy_:
      bstack11ll111ll1_opy_[bstack1l11lllll1_opy_[key]] = bstack1lll11lll_opy_[key]
    else:
      bstack11ll111ll1_opy_[key] = bstack1lll11lll_opy_[key]
  for key in bstack1l1l1ll1l_opy_:
    if key in bstack1l11lllll1_opy_:
      bstack11ll111ll1_opy_[bstack1l11lllll1_opy_[key]] = bstack1l1l1ll1l_opy_[key]
    else:
      bstack11ll111ll1_opy_[key] = bstack1l1l1ll1l_opy_[key]
  return bstack11ll111ll1_opy_
def bstack111111l1_opy_(config, index=0):
  global bstack11l1l1l1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1lllll1ll_opy_ = bstack11l111111_opy_(bstack1ll1l1lll_opy_, config, logger)
  bstack1l1l1ll1l_opy_ = bstack1l1ll111l_opy_(config)
  bstack1111l1111_opy_ = bstack1ll1llllll_opy_
  bstack1111l1111_opy_ += bstack1l11llll11_opy_
  bstack1l1l1ll1l_opy_ = update(bstack1l1l1ll1l_opy_, bstack1lllll1ll_opy_)
  if bstack11l1l1l1_opy_:
    bstack1111l1111_opy_ += bstack1l11ll1l1_opy_
  if bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॅ") in config:
    if bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ॆ") in config[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬे")][index]:
      caps[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨै")] = config[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ")][index][bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ")]
    if bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧो") in config[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index]:
      caps[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯्ࠩ")] = str(config[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॏ")])
    bstack1l1l111lll_opy_ = bstack11l111111_opy_(bstack1ll1l1lll_opy_, config[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index], logger)
    bstack1111l1111_opy_ += list(bstack1l1l111lll_opy_.keys())
    for bstack1llll1l111_opy_ in bstack1111l1111_opy_:
      if bstack1llll1l111_opy_ in config[bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index]:
        if bstack1llll1l111_opy_ == bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ॒"):
          try:
            bstack1l1l111lll_opy_[bstack1llll1l111_opy_] = str(config[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index][bstack1llll1l111_opy_] * 1.0)
          except:
            bstack1l1l111lll_opy_[bstack1llll1l111_opy_] = str(config[bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index][bstack1llll1l111_opy_])
        else:
          bstack1l1l111lll_opy_[bstack1llll1l111_opy_] = config[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index][bstack1llll1l111_opy_]
        del (config[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1llll1l111_opy_])
    bstack1l1l1ll1l_opy_ = update(bstack1l1l1ll1l_opy_, bstack1l1l111lll_opy_)
  bstack1lll11lll_opy_ = bstack1ll11lllll_opy_(config, index)
  for bstack11111lll_opy_ in bstack1ll1llllll_opy_ + list(bstack1lllll1ll_opy_.keys()):
    if bstack11111lll_opy_ in bstack1lll11lll_opy_:
      bstack1l1l1ll1l_opy_[bstack11111lll_opy_] = bstack1lll11lll_opy_[bstack11111lll_opy_]
      del (bstack1lll11lll_opy_[bstack11111lll_opy_])
  if bstack11llllll_opy_(config):
    bstack1lll11lll_opy_[bstack11l11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫॗ")] = True
    caps.update(bstack1l1l1ll1l_opy_)
    caps[bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭क़")] = bstack1lll11lll_opy_
  else:
    bstack1lll11lll_opy_[bstack11l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ख़")] = False
    caps.update(bstack11111ll1l_opy_(bstack1lll11lll_opy_, bstack1l1l1ll1l_opy_))
    if bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬग़") in caps:
      caps[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩज़")] = caps[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")]
      del (caps[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")])
    if bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़") in caps:
      caps[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧय़")] = caps[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧॠ")]
      del (caps[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ")])
  return caps
def bstack11l11l111_opy_():
  global bstack1ll1111lll_opy_
  global CONFIG
  if bstack1111ll1l_opy_() <= version.parse(bstack11l11_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨॢ")):
    if bstack1ll1111lll_opy_ != bstack11l11_opy_ (u"ࠩࠪॣ"):
      return bstack11l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ।") + bstack1ll1111lll_opy_ + bstack11l11_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ॥")
    return bstack1lll111111_opy_
  if bstack1ll1111lll_opy_ != bstack11l11_opy_ (u"ࠬ࠭०"):
    return bstack11l11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ१") + bstack1ll1111lll_opy_ + bstack11l11_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ२")
  return bstack1llll111l1_opy_
def bstack1l11lll1l1_opy_(options):
  return hasattr(options, bstack11l11_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ३"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1llll11lll_opy_(options, bstack111ll11l1_opy_):
  for bstack1ll1llll11_opy_ in bstack111ll11l1_opy_:
    if bstack1ll1llll11_opy_ in [bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ४"), bstack11l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ५")]:
      continue
    if bstack1ll1llll11_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll1llll11_opy_] = update(options._experimental_options[bstack1ll1llll11_opy_],
                                                         bstack111ll11l1_opy_[bstack1ll1llll11_opy_])
    else:
      options.add_experimental_option(bstack1ll1llll11_opy_, bstack111ll11l1_opy_[bstack1ll1llll11_opy_])
  if bstack11l11_opy_ (u"ࠫࡦࡸࡧࡴࠩ६") in bstack111ll11l1_opy_:
    for arg in bstack111ll11l1_opy_[bstack11l11_opy_ (u"ࠬࡧࡲࡨࡵࠪ७")]:
      options.add_argument(arg)
    del (bstack111ll11l1_opy_[bstack11l11_opy_ (u"࠭ࡡࡳࡩࡶࠫ८")])
  if bstack11l11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ९") in bstack111ll11l1_opy_:
    for ext in bstack111ll11l1_opy_[bstack11l11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ॰")]:
      options.add_extension(ext)
    del (bstack111ll11l1_opy_[bstack11l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॱ")])
def bstack1l1ll11ll1_opy_(options, bstack11llll1l1l_opy_):
  if bstack11l11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩॲ") in bstack11llll1l1l_opy_:
    for bstack1l111111l_opy_ in bstack11llll1l1l_opy_[bstack11l11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪॳ")]:
      if bstack1l111111l_opy_ in options._preferences:
        options._preferences[bstack1l111111l_opy_] = update(options._preferences[bstack1l111111l_opy_], bstack11llll1l1l_opy_[bstack11l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫॴ")][bstack1l111111l_opy_])
      else:
        options.set_preference(bstack1l111111l_opy_, bstack11llll1l1l_opy_[bstack11l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ")][bstack1l111111l_opy_])
  if bstack11l11_opy_ (u"ࠧࡢࡴࡪࡷࠬॶ") in bstack11llll1l1l_opy_:
    for arg in bstack11llll1l1l_opy_[bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ")]:
      options.add_argument(arg)
def bstack1l11ll11l_opy_(options, bstack1l11l1111l_opy_):
  if bstack11l11_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪॸ") in bstack1l11l1111l_opy_:
    options.use_webview(bool(bstack1l11l1111l_opy_[bstack11l11_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫॹ")]))
  bstack1llll11lll_opy_(options, bstack1l11l1111l_opy_)
def bstack1l111ll1ll_opy_(options, bstack1llll1lll1_opy_):
  for bstack1l1lll11l1_opy_ in bstack1llll1lll1_opy_:
    if bstack1l1lll11l1_opy_ in [bstack11l11_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨॺ"), bstack11l11_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")]:
      continue
    options.set_capability(bstack1l1lll11l1_opy_, bstack1llll1lll1_opy_[bstack1l1lll11l1_opy_])
  if bstack11l11_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ") in bstack1llll1lll1_opy_:
    for arg in bstack1llll1lll1_opy_[bstack11l11_opy_ (u"ࠧࡢࡴࡪࡷࠬॽ")]:
      options.add_argument(arg)
  if bstack11l11_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬॾ") in bstack1llll1lll1_opy_:
    options.bstack1lll1l1l11_opy_(bool(bstack1llll1lll1_opy_[bstack11l11_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ॿ")]))
def bstack11ll11lll1_opy_(options, bstack11ll1l1lll_opy_):
  for bstack1l1l1lll1l_opy_ in bstack11ll1l1lll_opy_:
    if bstack1l1l1lll1l_opy_ in [bstack11l11_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧঀ"), bstack11l11_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      continue
    options._options[bstack1l1l1lll1l_opy_] = bstack11ll1l1lll_opy_[bstack1l1l1lll1l_opy_]
  if bstack11l11_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩং") in bstack11ll1l1lll_opy_:
    for bstack11ll1l11_opy_ in bstack11ll1l1lll_opy_[bstack11l11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ")]:
      options.bstack11lllll11_opy_(
        bstack11ll1l11_opy_, bstack11ll1l1lll_opy_[bstack11l11_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঄")][bstack11ll1l11_opy_])
  if bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ") in bstack11ll1l1lll_opy_:
    for arg in bstack11ll1l1lll_opy_[bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ")]:
      options.add_argument(arg)
def bstack1ll11ll111_opy_(options, caps):
  if not hasattr(options, bstack11l11_opy_ (u"ࠪࡏࡊ࡟ࠧই")):
    return
  if options.KEY == bstack11l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঈ") and options.KEY in caps:
    bstack1llll11lll_opy_(options, caps[bstack11l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪউ")])
  elif options.KEY == bstack11l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫঊ") and options.KEY in caps:
    bstack1l1ll11ll1_opy_(options, caps[bstack11l11_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঋ")])
  elif options.KEY == bstack11l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঌ") and options.KEY in caps:
    bstack1l111ll1ll_opy_(options, caps[bstack11l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ঍")])
  elif options.KEY == bstack11l11_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ঎") and options.KEY in caps:
    bstack1l11ll11l_opy_(options, caps[bstack11l11_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬএ")])
  elif options.KEY == bstack11l11_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫঐ") and options.KEY in caps:
    bstack11ll11lll1_opy_(options, caps[bstack11l11_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ঑")])
def bstack1lll1ll1l1_opy_(caps):
  global bstack11l1l1l1_opy_
  if isinstance(os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ঒")), str):
    bstack11l1l1l1_opy_ = eval(os.getenv(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩও")))
  if bstack11l1l1l1_opy_:
    if bstack11ll11l1_opy_() < version.parse(bstack11l11_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨঔ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪক")
    if bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩখ") in caps:
      browser = caps[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ")]
    elif bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧঘ") in caps:
      browser = caps[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨঙ")]
    browser = str(browser).lower()
    if browser == bstack11l11_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨচ") or browser == bstack11l11_opy_ (u"ࠩ࡬ࡴࡦࡪࠧছ"):
      browser = bstack11l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪজ")
    if browser == bstack11l11_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬঝ"):
      browser = bstack11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬঞ")
    if browser not in [bstack11l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ট"), bstack11l11_opy_ (u"ࠧࡦࡦࡪࡩࠬঠ"), bstack11l11_opy_ (u"ࠨ࡫ࡨࠫড"), bstack11l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩঢ"), bstack11l11_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫণ")]:
      return None
    try:
      package = bstack11l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ত").format(browser)
      name = bstack11l11_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l11lll1l1_opy_(options):
        return None
      for bstack11111lll_opy_ in caps.keys():
        options.set_capability(bstack11111lll_opy_, caps[bstack11111lll_opy_])
      bstack1ll11ll111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll1l1111l_opy_(options, bstack1lll1l1lll_opy_):
  if not bstack1l11lll1l1_opy_(options):
    return
  for bstack11111lll_opy_ in bstack1lll1l1lll_opy_.keys():
    if bstack11111lll_opy_ in bstack1l11llll11_opy_:
      continue
    if bstack11111lll_opy_ in options._caps and type(options._caps[bstack11111lll_opy_]) in [dict, list]:
      options._caps[bstack11111lll_opy_] = update(options._caps[bstack11111lll_opy_], bstack1lll1l1lll_opy_[bstack11111lll_opy_])
    else:
      options.set_capability(bstack11111lll_opy_, bstack1lll1l1lll_opy_[bstack11111lll_opy_])
  bstack1ll11ll111_opy_(options, bstack1lll1l1lll_opy_)
  if bstack11l11_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬদ") in options._caps:
    if options._caps[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬধ")] and options._caps[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ন")].lower() != bstack11l11_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ঩"):
      del options._caps[bstack11l11_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩপ")]
def bstack1l1l11llll_opy_(proxy_config):
  if bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨফ") in proxy_config:
    proxy_config[bstack11l11_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧব")] = proxy_config[bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪভ")]
    del (proxy_config[bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম")])
  if bstack11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫয") in proxy_config and proxy_config[bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬর")].lower() != bstack11l11_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪ঱"):
    proxy_config[bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল")] = bstack11l11_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬ঳")
  if bstack11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫ঴") in proxy_config:
    proxy_config[bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack11l11_opy_ (u"ࠨࡲࡤࡧࠬশ")
  return proxy_config
def bstack11llll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨষ") in config:
    return proxy
  config[bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩস")] = bstack1l1l11llll_opy_(config[bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪহ")])
  if proxy == None:
    proxy = Proxy(config[bstack11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺")])
  return proxy
def bstack1l1l1llll_opy_(self):
  global CONFIG
  global bstack11ll11l1l_opy_
  try:
    proxy = bstack1l1ll1ll1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l11_opy_ (u"࠭࠮ࡱࡣࡦࠫ঻")):
        proxies = bstack1l1111l11l_opy_(proxy, bstack11l11l111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1lll111l_opy_ = proxies.popitem()
          if bstack11l11_opy_ (u"ࠢ࠻࠱࠲়ࠦ") in bstack1l1lll111l_opy_:
            return bstack1l1lll111l_opy_
          else:
            return bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤঽ") + bstack1l1lll111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨা").format(str(e)))
  return bstack11ll11l1l_opy_(self)
def bstack1l1llll11_opy_():
  global CONFIG
  return bstack1l11l11l1l_opy_(CONFIG) and bstack1l11111lll_opy_() and bstack1111ll1l_opy_() >= version.parse(bstack1lll11llll_opy_)
def bstack1ll1ll11l1_opy_():
  global CONFIG
  return (bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ি") in CONFIG or bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨী") in CONFIG) and bstack1ll111l1ll_opy_()
def bstack1l1lll1ll_opy_(config):
  bstack1lll111l_opy_ = {}
  if bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩু") in config:
    bstack1lll111l_opy_ = config[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪূ")]
  if bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ৃ") in config:
    bstack1lll111l_opy_ = config[bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৄ")]
  proxy = bstack1l1ll1ll1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৅")) and os.path.isfile(proxy):
      bstack1lll111l_opy_[bstack11l11_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৆")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩে")):
        proxies = bstack1ll1ll1l1_opy_(config, bstack11l11l111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1lll111l_opy_ = proxies.popitem()
          if bstack11l11_opy_ (u"ࠧࡀ࠯࠰ࠤৈ") in bstack1l1lll111l_opy_:
            parsed_url = urlparse(bstack1l1lll111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l11_opy_ (u"ࠨ࠺࠰࠱ࠥ৉") + bstack1l1lll111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1lll111l_opy_[bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ৊")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1lll111l_opy_[bstack11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫো")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1lll111l_opy_[bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬৌ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1lll111l_opy_[bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ্࠭")] = str(parsed_url.password)
  return bstack1lll111l_opy_
def bstack1l1l1111_opy_(config):
  if bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩৎ") in config:
    return config[bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৏")]
  return {}
def bstack1l11l111l_opy_(caps):
  global bstack111lll1l1_opy_
  if bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৐") in caps:
    caps[bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৑")][bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ৒")] = True
    if bstack111lll1l1_opy_:
      caps[bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓")][bstack11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৔")] = bstack111lll1l1_opy_
  else:
    caps[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ৕")] = True
    if bstack111lll1l1_opy_:
      caps[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৖")] = bstack111lll1l1_opy_
@measure(event_name=EVENTS.bstack1l11l1l11l_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack111lll11_opy_():
  global CONFIG
  if not bstack1l1l11l1l1_opy_(CONFIG):
    return
  if bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪৗ") in CONFIG and bstack1ll1l1l11_opy_(CONFIG[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৘")]):
    if (
      bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৙") in CONFIG
      and bstack1ll1l1l11_opy_(CONFIG[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৚")].get(bstack11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ৛")))
    ):
      logger.debug(bstack11l11_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧড়"))
      return
    bstack1lll111l_opy_ = bstack1l1lll1ll_opy_(CONFIG)
    bstack1l1l1l1ll1_opy_(CONFIG[bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨঢ়")], bstack1lll111l_opy_)
def bstack1l1l1l1ll1_opy_(key, bstack1lll111l_opy_):
  global bstack1l111l11l_opy_
  logger.info(bstack11ll11l1ll_opy_)
  try:
    bstack1l111l11l_opy_ = Local()
    bstack11ll1111l1_opy_ = {bstack11l11_opy_ (u"࠭࡫ࡦࡻࠪ৞"): key}
    bstack11ll1111l1_opy_.update(bstack1lll111l_opy_)
    logger.debug(bstack11ll1l1l11_opy_.format(str(bstack11ll1111l1_opy_)))
    bstack1l111l11l_opy_.start(**bstack11ll1111l1_opy_)
    if bstack1l111l11l_opy_.isRunning():
      logger.info(bstack11111l1ll_opy_)
  except Exception as e:
    bstack111111ll_opy_(bstack111ll1ll_opy_.format(str(e)))
def bstack1111lll11_opy_():
  global bstack1l111l11l_opy_
  if bstack1l111l11l_opy_.isRunning():
    logger.info(bstack1lll1ll111_opy_)
    bstack1l111l11l_opy_.stop()
  bstack1l111l11l_opy_ = None
def bstack1l111l111_opy_(bstack1lllll11l_opy_=[]):
  global CONFIG
  bstack1ll1ll1l_opy_ = []
  bstack11111l1l1_opy_ = [bstack11l11_opy_ (u"ࠧࡰࡵࠪয়"), bstack11l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫৠ"), bstack11l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ৡ"), bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬৢ"), bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩৣ"), bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৤")]
  try:
    for err in bstack1lllll11l_opy_:
      bstack1ll1l1l1_opy_ = {}
      for k in bstack11111l1l1_opy_:
        val = CONFIG[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৥")][int(err[bstack11l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭০")])].get(k)
        if val:
          bstack1ll1l1l1_opy_[k] = val
      if(err[bstack11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ১")] != bstack11l11_opy_ (u"ࠩࠪ২")):
        bstack1ll1l1l1_opy_[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩ৩")] = {
          err[bstack11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ৪")]: err[bstack11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")]
        }
        bstack1ll1ll1l_opy_.append(bstack1ll1l1l1_opy_)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ৬") + str(e))
  finally:
    return bstack1ll1ll1l_opy_
def bstack1l11lll1_opy_(file_name):
  bstack111l1llll_opy_ = []
  try:
    bstack1l11llll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l11llll_opy_):
      with open(bstack1l11llll_opy_) as f:
        bstack1l111l1111_opy_ = json.load(f)
        bstack111l1llll_opy_ = bstack1l111l1111_opy_
      os.remove(bstack1l11llll_opy_)
    return bstack111l1llll_opy_
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡪࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡯࡭ࡸࡺ࠺ࠡࠩ৭") + str(e))
    return bstack111l1llll_opy_
def bstack1llllllll_opy_():
  try:
      from bstack_utils.constants import bstack1lllllll1_opy_, EVENTS
      from bstack_utils.helper import bstack1lllll1l1_opy_, get_host_info, bstack1111ll1l1_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1l1l1lllll_opy_ = os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ৮"), bstack11l11_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬ৯"))
      lock = FileLock(bstack1l1l1lllll_opy_+bstack11l11_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤৰ"))
      def bstack1lllll1111_opy_():
          try:
              with lock:
                  with open(bstack1l1l1lllll_opy_, bstack11l11_opy_ (u"ࠦࡷࠨৱ"), encoding=bstack11l11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ৲")) as file:
                      data = json.load(file)
                      config = {
                          bstack11l11_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢ৳"): {
                              bstack11l11_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨ৴"): bstack11l11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦ৵"),
                          }
                      }
                      bstack111l1ll11_opy_ = datetime.utcnow()
                      bstack1ll1l1l11l_opy_ = bstack111l1ll11_opy_.strftime(bstack11l11_opy_ (u"ࠤࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠢࡘࡘࡈࠨ৶"))
                      bstack1lll11l11_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ৷")) if os.environ.get(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ৸")) else bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢ৹"))
                      payload = {
                          bstack11l11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠥ৺"): bstack11l11_opy_ (u"ࠢࡴࡦ࡮ࡣࡪࡼࡥ࡯ࡶࡶࠦ৻"),
                          bstack11l11_opy_ (u"ࠣࡦࡤࡸࡦࠨৼ"): {
                              bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠣ৽"): bstack1lll11l11_opy_,
                              bstack11l11_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࡣࡩࡧࡹࠣ৾"): bstack1ll1l1l11l_opy_,
                              bstack11l11_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࠣ৿"): bstack11l11_opy_ (u"࡙ࠧࡄࡌࡈࡨࡥࡹࡻࡲࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࠨ਀"),
                              bstack11l11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡰࡳࡰࡰࠥਁ"): {
                                  bstack11l11_opy_ (u"ࠢ࡮ࡧࡤࡷࡺࡸࡥࡴࠤਂ"): data
                              },
                              bstack11l11_opy_ (u"ࠣࡷࡶࡩࡷࡥࡤࡢࡶࡤࠦਃ"): bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ਄")),
                              bstack11l11_opy_ (u"ࠥ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴࠨਅ"): get_host_info()
                          }
                      }
                      response = bstack1lllll1l1_opy_(bstack11l11_opy_ (u"ࠦࡕࡕࡓࡕࠤਆ"), bstack1lllllll1_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack11l11_opy_ (u"ࠧࡊࡡࡵࡣࠣࡷࡪࡴࡴࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡵࡱࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧਇ").format(bstack1lllllll1_opy_, payload))
                      else:
                          logger.debug(bstack11l11_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡧࡱࡵࠤࢀࢃࠠࡸ࡫ࡷ࡬ࠥࡪࡡࡵࡣࠣࡿࢂࠨਈ").format(bstack1lllllll1_opy_, payload))
          except Exception as e:
              logger.debug(bstack11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡࡽࢀࠦਉ").format(e))
      bstack1lllll1111_opy_()
      bstack1l11l11ll_opy_(bstack1l1l1lllll_opy_, logger)
  except:
    pass
def bstack11ll1l111l_opy_():
  global bstack11l11l1l_opy_
  global bstack1llll111_opy_
  global bstack1l1ll11l_opy_
  global bstack11ll111ll_opy_
  global bstack1ll11ll11_opy_
  global bstack11l11111l_opy_
  global CONFIG
  bstack11ll1l1ll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩਊ"))
  if bstack11ll1l1ll_opy_ in [bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ਋"), bstack11l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ਌")]:
    bstack11l111ll_opy_()
  percy.shutdown()
  if bstack11l11l1l_opy_:
    logger.warning(bstack111lll1ll_opy_.format(str(bstack11l11l1l_opy_)))
  else:
    try:
      bstack1ll1lllll1_opy_ = bstack1lll11111_opy_(bstack11l11_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ਍"), logger)
      if bstack1ll1lllll1_opy_.get(bstack11l11_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ਎")) and bstack1ll1lllll1_opy_.get(bstack11l11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫਏ")).get(bstack11l11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩਐ")):
        logger.warning(bstack111lll1ll_opy_.format(str(bstack1ll1lllll1_opy_[bstack11l11_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭਑")][bstack11l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ਒")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack11ll1ll1ll_opy_)
  global bstack1l111l11l_opy_
  if bstack1l111l11l_opy_:
    bstack1111lll11_opy_()
  try:
    for driver in bstack1llll111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack111l1111_opy_)
  if bstack11l11111l_opy_ == bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਓ"):
    bstack1ll11ll11_opy_ = bstack1l11lll1_opy_(bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਔ"))
  if bstack11l11111l_opy_ == bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬਕ") and len(bstack11ll111ll_opy_) == 0:
    bstack11ll111ll_opy_ = bstack1l11lll1_opy_(bstack11l11_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਖ"))
    if len(bstack11ll111ll_opy_) == 0:
      bstack11ll111ll_opy_ = bstack1l11lll1_opy_(bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ਗ"))
  bstack1l11111l_opy_ = bstack11l11_opy_ (u"ࠨࠩਘ")
  if len(bstack1l1ll11l_opy_) > 0:
    bstack1l11111l_opy_ = bstack1l111l111_opy_(bstack1l1ll11l_opy_)
  elif len(bstack11ll111ll_opy_) > 0:
    bstack1l11111l_opy_ = bstack1l111l111_opy_(bstack11ll111ll_opy_)
  elif len(bstack1ll11ll11_opy_) > 0:
    bstack1l11111l_opy_ = bstack1l111l111_opy_(bstack1ll11ll11_opy_)
  elif len(bstack1l1lll11_opy_) > 0:
    bstack1l11111l_opy_ = bstack1l111l111_opy_(bstack1l1lll11_opy_)
  if bool(bstack1l11111l_opy_):
    bstack1llll111l_opy_(bstack1l11111l_opy_)
  else:
    bstack1llll111l_opy_()
  bstack1l11l11ll_opy_(bstack1l11l1llll_opy_, logger)
  if bstack11ll1l1ll_opy_ not in [bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪਙ")]:
    bstack1llllllll_opy_()
  bstack11llll1ll1_opy_.bstack1ll11l11ll_opy_(CONFIG)
  if len(bstack1ll11ll11_opy_) > 0:
    sys.exit(len(bstack1ll11ll11_opy_))
def bstack1ll11ll11l_opy_(bstack1l111lll11_opy_, frame):
  global bstack1111ll1l1_opy_
  logger.error(bstack111llll1l_opy_)
  bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭ਚ"), bstack1l111lll11_opy_)
  if hasattr(signal, bstack11l11_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬਛ")):
    bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਜ"), signal.Signals(bstack1l111lll11_opy_).name)
  else:
    bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ਝ"), bstack11l11_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫਞ"))
  bstack11ll1l1ll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩਟ"))
  if bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩਠ"):
    bstack1l11ll1l_opy_.stop(bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪਡ")))
  bstack11ll1l111l_opy_()
  sys.exit(1)
def bstack111111ll_opy_(err):
  logger.critical(bstack11lll1l11l_opy_.format(str(err)))
  bstack1llll111l_opy_(bstack11lll1l11l_opy_.format(str(err)), True)
  atexit.unregister(bstack11ll1l111l_opy_)
  bstack11l111ll_opy_()
  sys.exit(1)
def bstack1ll1l1l111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1llll111l_opy_(message, True)
  atexit.unregister(bstack11ll1l111l_opy_)
  bstack11l111ll_opy_()
  sys.exit(1)
def bstack1l1l1l111l_opy_():
  global CONFIG
  global bstack1l1111l11_opy_
  global bstack1llllll1ll_opy_
  global bstack11111ll11_opy_
  CONFIG = bstack1l111l11ll_opy_()
  load_dotenv(CONFIG.get(bstack11l11_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬਢ")))
  bstack11llll1lll_opy_()
  bstack11lllll1l_opy_()
  CONFIG = bstack11ll1ll1l_opy_(CONFIG)
  update(CONFIG, bstack1llllll1ll_opy_)
  update(CONFIG, bstack1l1111l11_opy_)
  CONFIG = bstack1lll1l1l_opy_(CONFIG)
  bstack11111ll11_opy_ = bstack1l1l11l1l1_opy_(CONFIG)
  os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨਣ")] = bstack11111ll11_opy_.__str__()
  bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧਤ"), bstack11111ll11_opy_)
  if (bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਥ") in CONFIG and bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਦ") in bstack1l1111l11_opy_) or (
          bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਧ") in CONFIG and bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਨ") not in bstack1llllll1ll_opy_):
    if os.getenv(bstack11l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ਩")):
      CONFIG[bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਪ")] = os.getenv(bstack11l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪਫ"))
    else:
      bstack1ll111l1_opy_()
  elif (bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਬ") not in CONFIG and bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪਭ") in CONFIG) or (
          bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਮ") in bstack1llllll1ll_opy_ and bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਯ") not in bstack1l1111l11_opy_):
    del (CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਰ")])
  if bstack1ll11ll1l_opy_(CONFIG):
    bstack111111ll_opy_(bstack1l1l1l111_opy_)
  Config.bstack1llll1lll_opy_().bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"ࠧࡻࡳࡦࡴࡑࡥࡲ࡫ࠢ਱"), CONFIG[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨਲ")])
  bstack1l11lll11l_opy_()
  bstack1lll1l11_opy_()
  if bstack11l1l1l1_opy_:
    CONFIG[bstack11l11_opy_ (u"ࠧࡢࡲࡳࠫਲ਼")] = bstack1l1l1l1111_opy_(CONFIG)
    logger.info(bstack1l1l11lll_opy_.format(CONFIG[bstack11l11_opy_ (u"ࠨࡣࡳࡴࠬ਴")]))
  if not bstack11111ll11_opy_:
    CONFIG[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਵ")] = [{}]
def bstack1ll1111ll_opy_(config, bstack11lllll1_opy_):
  global CONFIG
  global bstack11l1l1l1_opy_
  CONFIG = config
  bstack11l1l1l1_opy_ = bstack11lllll1_opy_
def bstack1lll1l11_opy_():
  global CONFIG
  global bstack11l1l1l1_opy_
  if bstack11l11_opy_ (u"ࠪࡥࡵࡶࠧਸ਼") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack11ll1l11ll_opy_)
    bstack11l1l1l1_opy_ = True
    bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ਷"), True)
def bstack1l1l1l1111_opy_(config):
  bstack1lll1ll11_opy_ = bstack11l11_opy_ (u"ࠬ࠭ਸ")
  app = config[bstack11l11_opy_ (u"࠭ࡡࡱࡲࠪਹ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll1lll_opy_:
      if os.path.exists(app):
        bstack1lll1ll11_opy_ = bstack1lllll1l1l_opy_(config, app)
      elif bstack1ll1ll1ll1_opy_(app):
        bstack1lll1ll11_opy_ = app
      else:
        bstack111111ll_opy_(bstack1l1lllll1_opy_.format(app))
    else:
      if bstack1ll1ll1ll1_opy_(app):
        bstack1lll1ll11_opy_ = app
      elif os.path.exists(app):
        bstack1lll1ll11_opy_ = bstack1lllll1l1l_opy_(app)
      else:
        bstack111111ll_opy_(bstack111l1lll1_opy_)
  else:
    if len(app) > 2:
      bstack111111ll_opy_(bstack1l1lllll11_opy_)
    elif len(app) == 2:
      if bstack11l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ਺") in app and bstack11l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ਻") in app:
        if os.path.exists(app[bstack11l11_opy_ (u"ࠩࡳࡥࡹ࡮਼ࠧ")]):
          bstack1lll1ll11_opy_ = bstack1lllll1l1l_opy_(config, app[bstack11l11_opy_ (u"ࠪࡴࡦࡺࡨࠨ਽")], app[bstack11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧਾ")])
        else:
          bstack111111ll_opy_(bstack1l1lllll1_opy_.format(app))
      else:
        bstack111111ll_opy_(bstack1l1lllll11_opy_)
    else:
      for key in app:
        if key in bstack1ll11l11l1_opy_:
          if key == bstack11l11_opy_ (u"ࠬࡶࡡࡵࡪࠪਿ"):
            if os.path.exists(app[key]):
              bstack1lll1ll11_opy_ = bstack1lllll1l1l_opy_(config, app[key])
            else:
              bstack111111ll_opy_(bstack1l1lllll1_opy_.format(app))
          else:
            bstack1lll1ll11_opy_ = app[key]
        else:
          bstack111111ll_opy_(bstack1llllll1l1_opy_)
  return bstack1lll1ll11_opy_
def bstack1ll1ll1ll1_opy_(bstack1lll1ll11_opy_):
  import re
  bstack1l11l1l1_opy_ = re.compile(bstack11l11_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨੀ"))
  bstack1lll1l11l_opy_ = re.compile(bstack11l11_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯࠵࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦੁ"))
  if bstack11l11_opy_ (u"ࠨࡤࡶ࠾࠴࠵ࠧੂ") in bstack1lll1ll11_opy_ or re.fullmatch(bstack1l11l1l1_opy_, bstack1lll1ll11_opy_) or re.fullmatch(bstack1lll1l11l_opy_, bstack1lll1ll11_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1l1l1ll1ll_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1lllll1l1l_opy_(config, path, bstack1lll1ll1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l11_opy_ (u"ࠩࡵࡦࠬ੃")).read()).hexdigest()
  bstack1l111llll_opy_ = bstack1l1ll11l1_opy_(md5_hash)
  bstack1lll1ll11_opy_ = None
  if bstack1l111llll_opy_:
    logger.info(bstack1l1111lll1_opy_.format(bstack1l111llll_opy_, md5_hash))
    return bstack1l111llll_opy_
  bstack1ll11lll_opy_ = MultipartEncoder(
    fields={
      bstack11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࠨ੄"): (os.path.basename(path), open(os.path.abspath(path), bstack11l11_opy_ (u"ࠫࡷࡨࠧ੅")), bstack11l11_opy_ (u"ࠬࡺࡥࡹࡶ࠲ࡴࡱࡧࡩ࡯ࠩ੆")),
      bstack11l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩੇ"): bstack1lll1ll1l_opy_
    }
  )
  response = requests.post(bstack1l11111l1_opy_, data=bstack1ll11lll_opy_,
                           headers={bstack11l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ੈ"): bstack1ll11lll_opy_.content_type},
                           auth=(config[bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ੉")], config[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ੊")]))
  try:
    res = json.loads(response.text)
    bstack1lll1ll11_opy_ = res[bstack11l11_opy_ (u"ࠪࡥࡵࡶ࡟ࡶࡴ࡯ࠫੋ")]
    logger.info(bstack11llllll11_opy_.format(bstack1lll1ll11_opy_))
    bstack11ll11llll_opy_(md5_hash, bstack1lll1ll11_opy_)
  except ValueError as err:
    bstack111111ll_opy_(bstack1l1ll1111l_opy_.format(str(err)))
  return bstack1lll1ll11_opy_
def bstack1l11lll11l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11ll111l_opy_
  bstack1ll111ll1_opy_ = 1
  bstack1l1111111_opy_ = 1
  if bstack11l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫੌ") in CONFIG:
    bstack1l1111111_opy_ = CONFIG[bstack11l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱ੍ࠬ")]
  else:
    bstack1l1111111_opy_ = bstack11ll11ll1l_opy_(framework_name, args) or 1
  if bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੎") in CONFIG:
    bstack1ll111ll1_opy_ = len(CONFIG[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੏")])
  bstack11ll111l_opy_ = int(bstack1l1111111_opy_) * int(bstack1ll111ll1_opy_)
def bstack11ll11ll1l_opy_(framework_name, args):
  if framework_name == bstack111l1l1ll_opy_ and args and bstack11l11_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭੐") in args:
      bstack111111l11_opy_ = args.index(bstack11l11_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧੑ"))
      return int(args[bstack111111l11_opy_ + 1]) or 1
  return 1
def bstack1l1ll11l1_opy_(md5_hash):
  bstack1ll1l1ll11_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠪࢂࠬ੒")), bstack11l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੓"), bstack11l11_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭੔"))
  if os.path.exists(bstack1ll1l1ll11_opy_):
    bstack1111l1l1_opy_ = json.load(open(bstack1ll1l1ll11_opy_, bstack11l11_opy_ (u"࠭ࡲࡣࠩ੕")))
    if md5_hash in bstack1111l1l1_opy_:
      bstack1l11ll1l11_opy_ = bstack1111l1l1_opy_[md5_hash]
      bstack1l1llll1_opy_ = datetime.datetime.now()
      bstack1l1111l1_opy_ = datetime.datetime.strptime(bstack1l11ll1l11_opy_[bstack11l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ੖")], bstack11l11_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ੗"))
      if (bstack1l1llll1_opy_ - bstack1l1111l1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l11ll1l11_opy_[bstack11l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ੘")]):
        return None
      return bstack1l11ll1l11_opy_[bstack11l11_opy_ (u"ࠪ࡭ࡩ࠭ਖ਼")]
  else:
    return None
def bstack11ll11llll_opy_(md5_hash, bstack1lll1ll11_opy_):
  bstack1l1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠫࢃ࠭ਗ਼")), bstack11l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬਜ਼"))
  if not os.path.exists(bstack1l1lll1lll_opy_):
    os.makedirs(bstack1l1lll1lll_opy_)
  bstack1ll1l1ll11_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"࠭ࡾࠨੜ")), bstack11l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ੝"), bstack11l11_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩਫ਼"))
  bstack1l1lll1111_opy_ = {
    bstack11l11_opy_ (u"ࠩ࡬ࡨࠬ੟"): bstack1lll1ll11_opy_,
    bstack11l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭੠"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l11_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ੡")),
    bstack11l11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ੢"): str(__version__)
  }
  if os.path.exists(bstack1ll1l1ll11_opy_):
    bstack1111l1l1_opy_ = json.load(open(bstack1ll1l1ll11_opy_, bstack11l11_opy_ (u"࠭ࡲࡣࠩ੣")))
  else:
    bstack1111l1l1_opy_ = {}
  bstack1111l1l1_opy_[md5_hash] = bstack1l1lll1111_opy_
  with open(bstack1ll1l1ll11_opy_, bstack11l11_opy_ (u"ࠢࡸ࠭ࠥ੤")) as outfile:
    json.dump(bstack1111l1l1_opy_, outfile)
def bstack11ll1llll1_opy_(self):
  return
def bstack111111lll_opy_(self):
  return
def bstack1ll11l111l_opy_(self):
  global bstack1llll11ll1_opy_
  bstack1llll11ll1_opy_(self)
def bstack111ll1lll_opy_():
  global bstack11l1ll1ll_opy_
  bstack11l1ll1ll_opy_ = True
@measure(event_name=EVENTS.bstack1ll1l1llll_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack11lll11lll_opy_(self):
  global bstack1l11111l1l_opy_
  global bstack1l1111l1l_opy_
  global bstack111l1l1l1_opy_
  try:
    if bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ੥") in bstack1l11111l1l_opy_ and self.session_id != None and bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭੦"), bstack11l11_opy_ (u"ࠪࠫ੧")) != bstack11l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ੨"):
      bstack1l111l1l1_opy_ = bstack11l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ੩") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭੪")
      if bstack1l111l1l1_opy_ == bstack11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ੫"):
        bstack1l1l1ll11l_opy_(logger)
      if self != None:
        bstack1ll1ll1l11_opy_(self, bstack1l111l1l1_opy_, bstack11l11_opy_ (u"ࠨ࠮ࠣࠫ੬").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11l11_opy_ (u"ࠩࠪ੭")
    if bstack11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ੮") in bstack1l11111l1l_opy_ and getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੯"), None):
      bstack11l11ll1l_opy_.bstack1ll1l111_opy_(self, bstack1l11ll111l_opy_, logger, wait=True)
    if bstack11l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬੰ") in bstack1l11111l1l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1ll1ll1l11_opy_(self, bstack11l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨੱ"))
      bstack111l1l11l_opy_.bstack1lll111l11_opy_(self)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣੲ") + str(e))
  bstack111l1l1l1_opy_(self)
  self.session_id = None
def bstack1lll11ll1l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack111ll111_opy_
    global bstack1l11111l1l_opy_
    command_executor = kwargs.get(bstack11l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫੳ"), bstack11l11_opy_ (u"ࠩࠪੴ"))
    bstack11l11l11l_opy_ = False
    if type(command_executor) == str and bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ੵ") in command_executor:
      bstack11l11l11l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ੶") in str(getattr(command_executor, bstack11l11_opy_ (u"ࠬࡥࡵࡳ࡮ࠪ੷"), bstack11l11_opy_ (u"࠭ࠧ੸"))):
      bstack11l11l11l_opy_ = True
    else:
      return bstack11ll1ll11l_opy_(self, *args, **kwargs)
    if bstack11l11l11l_opy_:
      bstack1l111111_opy_ = bstack1l1l111l1l_opy_.bstack1l11ll11l1_opy_(CONFIG, bstack1l11111l1l_opy_)
      if kwargs.get(bstack11l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ੹")):
        kwargs[bstack11l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ੺")] = bstack111ll111_opy_(kwargs[bstack11l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ੻")], bstack1l11111l1l_opy_, bstack1l111111_opy_)
      elif kwargs.get(bstack11l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ੼")):
        kwargs[bstack11l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ੽")] = bstack111ll111_opy_(kwargs[bstack11l11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ੾")], bstack1l11111l1l_opy_, bstack1l111111_opy_)
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨ੿").format(str(e)))
  return bstack11ll1ll11l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l11l111ll_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack11llll11_opy_(self, command_executor=bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯࠲࠴࠺࠲࠵࠴࠰࠯࠳࠽࠸࠹࠺࠴ࠣ઀"), *args, **kwargs):
  bstack1ll1l11111_opy_ = bstack1lll11ll1l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1l111l1l_opy_.on():
    return bstack1ll1l11111_opy_
  try:
    logger.debug(bstack11l11_opy_ (u"ࠨࡅࡲࡱࡲࡧ࡮ࡥࠢࡈࡼࡪࡩࡵࡵࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡨࡤࡰࡸ࡫ࠠ࠮ࠢࡾࢁࠬઁ").format(str(command_executor)))
    logger.debug(bstack11l11_opy_ (u"ࠩࡋࡹࡧࠦࡕࡓࡎࠣ࡭ࡸࠦ࠭ࠡࡽࢀࠫં").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ઃ") in command_executor._url:
      bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ઄"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨઅ") in command_executor):
    bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧઆ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1ll1l1l_opy_ = getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨઇ"), None)
  if bstack11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨઈ") in bstack1l11111l1l_opy_ or bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨઉ") in bstack1l11111l1l_opy_:
    bstack1l11ll1l_opy_.bstack11111l11l_opy_(self)
  if bstack11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪઊ") in bstack1l11111l1l_opy_ and bstack1l1ll1l1l_opy_ and bstack1l1ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫઋ"), bstack11l11_opy_ (u"ࠬ࠭ઌ")) == bstack11l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧઍ"):
    bstack1l11ll1l_opy_.bstack11111l11l_opy_(self)
  return bstack1ll1l11111_opy_
def bstack1ll11111ll_opy_(args):
  return bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ઎") in str(args)
def bstack1111ll1ll_opy_(self, driver_command, *args, **kwargs):
  global bstack1lll111l1_opy_
  global bstack1l1l1111l_opy_
  bstack11llll111l_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬએ"), None) and bstack11l1l11l1_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨઐ"), None)
  bstack1l1ll1lll1_opy_ = getattr(self, bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪઑ"), None) != None and getattr(self, bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ઒"), None) == True
  if not bstack1l1l1111l_opy_ and bstack11111ll11_opy_ and bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬઓ") in CONFIG and CONFIG[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ઔ")] == True and bstack11lllll1ll_opy_.bstack111ll1l1l_opy_(driver_command) and (bstack1l1ll1lll1_opy_ or bstack11llll111l_opy_) and not bstack1ll11111ll_opy_(args):
    try:
      bstack1l1l1111l_opy_ = True
      logger.debug(bstack11l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩક").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭ખ").format(str(err)))
    bstack1l1l1111l_opy_ = False
  response = bstack1lll111l1_opy_(self, driver_command, *args, **kwargs)
  if (bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨગ") in str(bstack1l11111l1l_opy_).lower() or bstack11l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪઘ") in str(bstack1l11111l1l_opy_).lower()) and bstack1l111l1l_opy_.on():
    try:
      if driver_command == bstack11l11_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨઙ"):
        bstack1l11ll1l_opy_.bstack1ll1l1l1l_opy_({
            bstack11l11_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫચ"): response[bstack11l11_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬછ")],
            bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧજ"): bstack1l11ll1l_opy_.current_test_uuid() if bstack1l11ll1l_opy_.current_test_uuid() else bstack1l111l1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11l1ll11l_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1l11l1ll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1l1111l1l_opy_
  global bstack11ll11l111_opy_
  global bstack1l1l1ll1_opy_
  global bstack1l11ll1lll_opy_
  global bstack1l11l1l111_opy_
  global bstack1l11111l1l_opy_
  global bstack11ll1ll11l_opy_
  global bstack1llll111_opy_
  global bstack11llll11ll_opy_
  global bstack1l11ll111l_opy_
  CONFIG[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪઝ")] = str(bstack1l11111l1l_opy_) + str(__version__)
  bstack1l1ll1l1_opy_ = os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧઞ")]
  bstack1l111111_opy_ = bstack1l1l111l1l_opy_.bstack1l11ll11l1_opy_(CONFIG, bstack1l11111l1l_opy_)
  CONFIG[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ટ")] = bstack1l1ll1l1_opy_
  CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ઠ")] = bstack1l111111_opy_
  command_executor = bstack11l11l111_opy_()
  logger.debug(bstack1lllll1l11_opy_.format(command_executor))
  proxy = bstack11llll1l_opy_(CONFIG, proxy)
  bstack1l1l1l1ll_opy_ = 0 if bstack11ll11l111_opy_ < 0 else bstack11ll11l111_opy_
  try:
    if bstack1l11ll1lll_opy_ is True:
      bstack1l1l1l1ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l11l1l111_opy_ is True:
      bstack1l1l1l1ll_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1l1l1ll_opy_ = 0
  bstack1lll1l1lll_opy_ = bstack111111l1_opy_(CONFIG, bstack1l1l1l1ll_opy_)
  logger.debug(bstack1l11llll1_opy_.format(str(bstack1lll1l1lll_opy_)))
  if bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩડ") in CONFIG and bstack1ll1l1l11_opy_(CONFIG[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪઢ")]):
    bstack1l11l111l_opy_(bstack1lll1l1lll_opy_)
  if bstack1lll11ll_opy_.bstack1l11111111_opy_(CONFIG, bstack1l1l1l1ll_opy_) and bstack1lll11ll_opy_.bstack1lll1111_opy_(bstack1lll1l1lll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1lll11ll_opy_.set_capabilities(bstack1lll1l1lll_opy_, CONFIG)
  if desired_capabilities:
    bstack1ll1l1ll1_opy_ = bstack11ll1ll1l_opy_(desired_capabilities)
    bstack1ll1l1ll1_opy_[bstack11l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧણ")] = bstack11llllll_opy_(CONFIG)
    bstack11ll11l11_opy_ = bstack111111l1_opy_(bstack1ll1l1ll1_opy_)
    if bstack11ll11l11_opy_:
      bstack1lll1l1lll_opy_ = update(bstack11ll11l11_opy_, bstack1lll1l1lll_opy_)
    desired_capabilities = None
  if options:
    bstack1ll1l1111l_opy_(options, bstack1lll1l1lll_opy_)
  if not options:
    options = bstack1lll1ll1l1_opy_(bstack1lll1l1lll_opy_)
  bstack1l11ll111l_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫત"))[bstack1l1l1l1ll_opy_]
  if proxy and bstack1111ll1l_opy_() >= version.parse(bstack11l11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩથ")):
    options.proxy(proxy)
  if options and bstack1111ll1l_opy_() >= version.parse(bstack11l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩદ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1111ll1l_opy_() < version.parse(bstack11l11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪધ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll1l1lll_opy_)
  logger.info(bstack1llll11l11_opy_)
  bstack1111l1l11_opy_.end(EVENTS.bstack1ll111ll_opy_.value, EVENTS.bstack1ll111ll_opy_.value + bstack11l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧન"), EVENTS.bstack1ll111ll_opy_.value + bstack11l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ઩"), status=True, failure=None, test_name=bstack1l1l1ll1_opy_)
  if bstack1111ll1l_opy_() >= version.parse(bstack11l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧપ")):
    bstack11ll1ll11l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1111ll1l_opy_() >= version.parse(bstack11l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧફ")):
    bstack11ll1ll11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1111ll1l_opy_() >= version.parse(bstack11l11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩબ")):
    bstack11ll1ll11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11ll1ll11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1ll1ll111l_opy_ = bstack11l11_opy_ (u"ࠪࠫભ")
    if bstack1111ll1l_opy_() >= version.parse(bstack11l11_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬમ")):
      bstack1ll1ll111l_opy_ = self.caps.get(bstack11l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧય"))
    else:
      bstack1ll1ll111l_opy_ = self.capabilities.get(bstack11l11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨર"))
    if bstack1ll1ll111l_opy_:
      bstack1llllll11l_opy_(bstack1ll1ll111l_opy_)
      if bstack1111ll1l_opy_() <= version.parse(bstack11l11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ઱")):
        self.command_executor._url = bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤલ") + bstack1ll1111lll_opy_ + bstack11l11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨળ")
      else:
        self.command_executor._url = bstack11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ઴") + bstack1ll1ll111l_opy_ + bstack11l11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧવ")
      logger.debug(bstack11lll1lll_opy_.format(bstack1ll1ll111l_opy_))
    else:
      logger.debug(bstack1l1l1llll1_opy_.format(bstack11l11_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨશ")))
  except Exception as e:
    logger.debug(bstack1l1l1llll1_opy_.format(e))
  if bstack11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬષ") in bstack1l11111l1l_opy_:
    bstack1ll11l11_opy_(bstack11ll11l111_opy_, bstack11llll11ll_opy_)
  bstack1l1111l1l_opy_ = self.session_id
  if bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧસ") in bstack1l11111l1l_opy_ or bstack11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨહ") in bstack1l11111l1l_opy_ or bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ઺") in bstack1l11111l1l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1ll1l1l_opy_ = getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ઻"), None)
  if bstack11l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ઼ࠫ") in bstack1l11111l1l_opy_ or bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫઽ") in bstack1l11111l1l_opy_:
    bstack1l11ll1l_opy_.bstack11111l11l_opy_(self)
  if bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ા") in bstack1l11111l1l_opy_ and bstack1l1ll1l1l_opy_ and bstack1l1ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧિ"), bstack11l11_opy_ (u"ࠨࠩી")) == bstack11l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪુ"):
    bstack1l11ll1l_opy_.bstack11111l11l_opy_(self)
  bstack1llll111_opy_.append(self)
  if bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૂ") in CONFIG and bstack11l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩૃ") in CONFIG[bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૄ")][bstack1l1l1l1ll_opy_]:
    bstack1l1l1ll1_opy_ = CONFIG[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૅ")][bstack1l1l1l1ll_opy_][bstack11l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૆")]
  logger.debug(bstack1ll111l11l_opy_.format(bstack1l1111l1l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1l11lllll_opy_
    def bstack1l11111ll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l11l1l1l1_opy_
      if(bstack11l11_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥે") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠩࢁࠫૈ")), bstack11l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪૉ"), bstack11l11_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭૊")), bstack11l11_opy_ (u"ࠬࡽࠧો")) as fp:
          fp.write(bstack11l11_opy_ (u"ࠨࠢૌ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ્")))):
          with open(args[1], bstack11l11_opy_ (u"ࠨࡴࠪ૎")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l11_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ૏") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1llll1l1_opy_)
            if bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧૐ") in CONFIG and str(CONFIG[bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ૑")]).lower() != bstack11l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ૒"):
                bstack1lll1lll11_opy_ = bstack1l11lllll_opy_()
                bstack1lll1l111_opy_ = bstack11l11_opy_ (u"࠭ࠧࠨࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࠽ࠍࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࠽ࠍࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡ࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠌࠣࠤࡹࡸࡹࠡࡽࡾࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠍࠤࠥࠦࠠࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࠾ࠎࠥࠦࡽࡾࠢࡦࡥࡹࡩࡨࠡࠪࡨࡼ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࡣࡰࡰࡶࡳࡱ࡫࠮ࡦࡴࡵࡳࡷ࠮ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠤ࠯ࠤࡪࡾࠩ࠼ࠌࠣࠤࢂࢃࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠐࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽࡾࠎࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࠧࡼࡥࡧࡴ࡚ࡸ࡬ࡾࠩࠣ࠯ࠥ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬ࠰ࠏࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࠏࠦࠠࡾࡿࠬ࠿ࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠌࢀࢁࡀࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏ࠭ࠧࠨ૓").format(bstack1lll1lll11_opy_=bstack1lll1lll11_opy_)
            lines.insert(1, bstack1lll1l111_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ૔")), bstack11l11_opy_ (u"ࠨࡹࠪ૕")) as bstack1l1l11lll1_opy_:
              bstack1l1l11lll1_opy_.writelines(lines)
        CONFIG[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ૖")] = str(bstack1l11111l1l_opy_) + str(__version__)
        bstack1l1ll1l1_opy_ = os.environ[bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ૗")]
        bstack1l111111_opy_ = bstack1l1l111l1l_opy_.bstack1l11ll11l1_opy_(CONFIG, bstack1l11111l1l_opy_)
        CONFIG[bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ૘")] = bstack1l1ll1l1_opy_
        CONFIG[bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ૙")] = bstack1l111111_opy_
        bstack1l1l1l1ll_opy_ = 0 if bstack11ll11l111_opy_ < 0 else bstack11ll11l111_opy_
        try:
          if bstack1l11ll1lll_opy_ is True:
            bstack1l1l1l1ll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l11l1l111_opy_ is True:
            bstack1l1l1l1ll_opy_ = int(threading.current_thread().name)
        except:
          bstack1l1l1l1ll_opy_ = 0
        CONFIG[bstack11l11_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ૚")] = False
        CONFIG[bstack11l11_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ૛")] = True
        bstack1lll1l1lll_opy_ = bstack111111l1_opy_(CONFIG, bstack1l1l1l1ll_opy_)
        logger.debug(bstack1l11llll1_opy_.format(str(bstack1lll1l1lll_opy_)))
        if CONFIG.get(bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ૜")):
          bstack1l11l111l_opy_(bstack1lll1l1lll_opy_)
        if bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૝") in CONFIG and bstack11l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ૞") in CONFIG[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૟")][bstack1l1l1l1ll_opy_]:
          bstack1l1l1ll1_opy_ = CONFIG[bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૠ")][bstack1l1l1l1ll_opy_][bstack11l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫૡ")]
        args.append(os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠧࡿࠩૢ")), bstack11l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨૣ"), bstack11l11_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ૤")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll1l1lll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l11_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ૥"))
      bstack1l11l1l1l1_opy_ = True
      return bstack1111l1ll1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l111lll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11ll11l111_opy_
    global bstack1l1l1ll1_opy_
    global bstack1l11ll1lll_opy_
    global bstack1l11l1l111_opy_
    global bstack1l11111l1l_opy_
    CONFIG[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭૦")] = str(bstack1l11111l1l_opy_) + str(__version__)
    bstack1l1ll1l1_opy_ = os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ૧")]
    bstack1l111111_opy_ = bstack1l1l111l1l_opy_.bstack1l11ll11l1_opy_(CONFIG, bstack1l11111l1l_opy_)
    CONFIG[bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ૨")] = bstack1l1ll1l1_opy_
    CONFIG[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ૩")] = bstack1l111111_opy_
    bstack1l1l1l1ll_opy_ = 0 if bstack11ll11l111_opy_ < 0 else bstack11ll11l111_opy_
    try:
      if bstack1l11ll1lll_opy_ is True:
        bstack1l1l1l1ll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l11l1l111_opy_ is True:
        bstack1l1l1l1ll_opy_ = int(threading.current_thread().name)
    except:
      bstack1l1l1l1ll_opy_ = 0
    CONFIG[bstack11l11_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ૪")] = True
    bstack1lll1l1lll_opy_ = bstack111111l1_opy_(CONFIG, bstack1l1l1l1ll_opy_)
    logger.debug(bstack1l11llll1_opy_.format(str(bstack1lll1l1lll_opy_)))
    if CONFIG.get(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭૫")):
      bstack1l11l111l_opy_(bstack1lll1l1lll_opy_)
    if bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૬") in CONFIG and bstack11l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ૭") in CONFIG[bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૮")][bstack1l1l1l1ll_opy_]:
      bstack1l1l1ll1_opy_ = CONFIG[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૯")][bstack1l1l1l1ll_opy_][bstack11l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૰")]
    import urllib
    import json
    if bstack11l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ૱") in CONFIG and str(CONFIG[bstack11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭૲")]).lower() != bstack11l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ૳"):
        bstack11lll111_opy_ = bstack1l11lllll_opy_()
        bstack1lll1lll11_opy_ = bstack11lll111_opy_ + urllib.parse.quote(json.dumps(bstack1lll1l1lll_opy_))
    else:
        bstack1lll1lll11_opy_ = bstack11l11_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭૴") + urllib.parse.quote(json.dumps(bstack1lll1l1lll_opy_))
    browser = self.connect(bstack1lll1lll11_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll111ll1l_opy_():
    global bstack1l11l1l1l1_opy_
    global bstack1l11111l1l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll11l1ll1_opy_
        global bstack1111ll1l1_opy_
        if not bstack11111ll11_opy_:
          global bstack1ll1lllll_opy_
          if not bstack1ll1lllll_opy_:
            from bstack_utils.helper import bstack1l1l11ll_opy_, bstack1l1l1l1l1_opy_, bstack11lll11ll_opy_
            bstack1ll1lllll_opy_ = bstack1l1l11ll_opy_()
            bstack1l1l1l1l1_opy_(bstack1l11111l1l_opy_)
            bstack1l111111_opy_ = bstack1l1l111l1l_opy_.bstack1l11ll11l1_opy_(CONFIG, bstack1l11111l1l_opy_)
            bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢ૵"), bstack1l111111_opy_)
          BrowserType.connect = bstack1ll11l1ll1_opy_
          return
        BrowserType.launch = bstack1l111lll_opy_
        bstack1l11l1l1l1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l11111ll1_opy_
      bstack1l11l1l1l1_opy_ = True
    except Exception as e:
      pass
def bstack1ll1l1ll_opy_(context, bstack11llll111_opy_):
  try:
    context.page.evaluate(bstack11l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ૶"), bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ૷")+ json.dumps(bstack11llll111_opy_) + bstack11l11_opy_ (u"ࠣࡿࢀࠦ૸"))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢૹ"), e)
def bstack1lll1lllll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦૺ"), bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩૻ") + json.dumps(message) + bstack11l11_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨૼ") + json.dumps(level) + bstack11l11_opy_ (u"࠭ࡽࡾࠩ૽"))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥ૾"), e)
@measure(event_name=EVENTS.bstack11llll11l_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1lll1l1111_opy_(self, url):
  global bstack1l11l11ll1_opy_
  try:
    bstack1111ll11_opy_(url)
  except Exception as err:
    logger.debug(bstack1l11l1ll_opy_.format(str(err)))
  try:
    bstack1l11l11ll1_opy_(self, url)
  except Exception as e:
    try:
      bstack1llll1111_opy_ = str(e)
      if any(err_msg in bstack1llll1111_opy_ for err_msg in bstack1l111l1l1l_opy_):
        bstack1111ll11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l11l1ll_opy_.format(str(err)))
    raise e
def bstack1llll1l1ll_opy_(self):
  global bstack1l1l111111_opy_
  bstack1l1l111111_opy_ = self
  return
def bstack111l1ll1_opy_(self):
  global bstack1111l11l_opy_
  bstack1111l11l_opy_ = self
  return
def bstack111ll1l1_opy_(test_name, bstack1l1111llll_opy_):
  global CONFIG
  if percy.bstack1ll1l111l_opy_() == bstack11l11_opy_ (u"ࠣࡶࡵࡹࡪࠨ૿"):
    bstack111ll11l_opy_ = os.path.relpath(bstack1l1111llll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack111ll11l_opy_)
    bstack111lll111_opy_ = suite_name + bstack11l11_opy_ (u"ࠤ࠰ࠦ଀") + test_name
    threading.current_thread().percySessionName = bstack111lll111_opy_
def bstack11111llll_opy_(self, test, *args, **kwargs):
  global bstack1l1l11l1ll_opy_
  test_name = None
  bstack1l1111llll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1111llll_opy_ = str(test.source)
  bstack111ll1l1_opy_(test_name, bstack1l1111llll_opy_)
  bstack1l1l11l1ll_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack111l11l1_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1l11ll11ll_opy_(driver, bstack111lll111_opy_):
  if not bstack1l1lll1l11_opy_ and bstack111lll111_opy_:
      bstack1111111l_opy_ = {
          bstack11l11_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪଁ"): bstack11l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଂ"),
          bstack11l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଃ"): {
              bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ଄"): bstack111lll111_opy_
          }
      }
      bstack11llllllll_opy_ = bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬଅ").format(json.dumps(bstack1111111l_opy_))
      driver.execute_script(bstack11llllllll_opy_)
  if bstack1ll11l1l1l_opy_:
      bstack11lll1111_opy_ = {
          bstack11l11_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨଆ"): bstack11l11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫଇ"),
          bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଈ"): {
              bstack11l11_opy_ (u"ࠫࡩࡧࡴࡢࠩଉ"): bstack111lll111_opy_ + bstack11l11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧଊ"),
              bstack11l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬଋ"): bstack11l11_opy_ (u"ࠧࡪࡰࡩࡳࠬଌ")
          }
      }
      if bstack1ll11l1l1l_opy_.status == bstack11l11_opy_ (u"ࠨࡒࡄࡗࡘ࠭଍"):
          bstack1llll1l1l1_opy_ = bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ଎").format(json.dumps(bstack11lll1111_opy_))
          driver.execute_script(bstack1llll1l1l1_opy_)
          bstack1ll1ll1l11_opy_(driver, bstack11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪଏ"))
      elif bstack1ll11l1l1l_opy_.status == bstack11l11_opy_ (u"ࠫࡋࡇࡉࡍࠩଐ"):
          reason = bstack11l11_opy_ (u"ࠧࠨ଑")
          bstack1ll1ll11_opy_ = bstack111lll111_opy_ + bstack11l11_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧ଒")
          if bstack1ll11l1l1l_opy_.message:
              reason = str(bstack1ll11l1l1l_opy_.message)
              bstack1ll1ll11_opy_ = bstack1ll1ll11_opy_ + bstack11l11_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧଓ") + reason
          bstack11lll1111_opy_[bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଔ")] = {
              bstack11l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨକ"): bstack11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩଖ"),
              bstack11l11_opy_ (u"ࠫࡩࡧࡴࡢࠩଗ"): bstack1ll1ll11_opy_
          }
          bstack1llll1l1l1_opy_ = bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪଘ").format(json.dumps(bstack11lll1111_opy_))
          driver.execute_script(bstack1llll1l1l1_opy_)
          bstack1ll1ll1l11_opy_(driver, bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ଙ"), reason)
          bstack1l111lll1_opy_(reason, str(bstack1ll11l1l1l_opy_), str(bstack11ll11l111_opy_), logger)
@measure(event_name=EVENTS.bstack1llll1ll_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1ll111llll_opy_(driver, test):
  if percy.bstack1ll1l111l_opy_() == bstack11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧଚ") and percy.bstack1llll1ll11_opy_() == bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥଛ"):
      bstack1l1l11ll1l_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଜ"), None)
      bstack11l1lll1_opy_(driver, bstack1l1l11ll1l_opy_, test)
  if bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧଝ"), None) and bstack11l1l11l1_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪଞ"), None):
      logger.info(bstack11l11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧଟ"))
      bstack1lll11ll_opy_.bstack1ll1ll1l1l_opy_(driver, name=test.name, path=test.source)
def bstack1lll1lll1_opy_(test, bstack111lll111_opy_):
    try:
      data = {}
      if test:
        data[bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫଠ")] = bstack111lll111_opy_
      if bstack1ll11l1l1l_opy_:
        if bstack1ll11l1l1l_opy_.status == bstack11l11_opy_ (u"ࠧࡑࡃࡖࡗࠬଡ"):
          data[bstack11l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨଢ")] = bstack11l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩଣ")
        elif bstack1ll11l1l1l_opy_.status == bstack11l11_opy_ (u"ࠪࡊࡆࡏࡌࠨତ"):
          data[bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫଥ")] = bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬଦ")
          if bstack1ll11l1l1l_opy_.message:
            data[bstack11l11_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ଧ")] = str(bstack1ll11l1l1l_opy_.message)
      user = CONFIG[bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩନ")]
      key = CONFIG[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ଩")]
      url = bstack11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧପ").format(user, key, bstack1l1111l1l_opy_)
      headers = {
        bstack11l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩଫ"): bstack11l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧବ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l1l11l111_opy_.format(str(e)))
def bstack1111ll11l_opy_(test, bstack111lll111_opy_):
  global CONFIG
  global bstack1111l11l_opy_
  global bstack1l1l111111_opy_
  global bstack1l1111l1l_opy_
  global bstack1ll11l1l1l_opy_
  global bstack1l1l1ll1_opy_
  global bstack11l11llll_opy_
  global bstack1ll11111_opy_
  global bstack111ll1l11_opy_
  global bstack1l11l1ll1_opy_
  global bstack1llll111_opy_
  global bstack1l11ll111l_opy_
  try:
    if not bstack1l1111l1l_opy_:
      with open(os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠬࢄࠧଭ")), bstack11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ମ"), bstack11l11_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩଯ"))) as f:
        bstack1ll1111l11_opy_ = json.loads(bstack11l11_opy_ (u"ࠣࡽࠥର") + f.read().strip() + bstack11l11_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ଱") + bstack11l11_opy_ (u"ࠥࢁࠧଲ"))
        bstack1l1111l1l_opy_ = bstack1ll1111l11_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1llll111_opy_:
    for driver in bstack1llll111_opy_:
      if bstack1l1111l1l_opy_ == driver.session_id:
        if test:
          bstack1ll111llll_opy_(driver, test)
        bstack1l11ll11ll_opy_(driver, bstack111lll111_opy_)
  elif bstack1l1111l1l_opy_:
    bstack1lll1lll1_opy_(test, bstack111lll111_opy_)
  if bstack1111l11l_opy_:
    bstack1ll11111_opy_(bstack1111l11l_opy_)
  if bstack1l1l111111_opy_:
    bstack111ll1l11_opy_(bstack1l1l111111_opy_)
  if bstack11l1ll1ll_opy_:
    bstack1l11l1ll1_opy_()
def bstack1l1ll1ll1_opy_(self, test, *args, **kwargs):
  bstack111lll111_opy_ = None
  if test:
    bstack111lll111_opy_ = str(test.name)
  bstack1111ll11l_opy_(test, bstack111lll111_opy_)
  bstack11l11llll_opy_(self, test, *args, **kwargs)
def bstack11l1ll111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lll11ll11_opy_
  global CONFIG
  global bstack1llll111_opy_
  global bstack1l1111l1l_opy_
  bstack11ll111lll_opy_ = None
  try:
    if bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪଳ"), None):
      try:
        if not bstack1l1111l1l_opy_:
          with open(os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠬࢄࠧ଴")), bstack11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ଵ"), bstack11l11_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩଶ"))) as f:
            bstack1ll1111l11_opy_ = json.loads(bstack11l11_opy_ (u"ࠣࡽࠥଷ") + f.read().strip() + bstack11l11_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫସ") + bstack11l11_opy_ (u"ࠥࢁࠧହ"))
            bstack1l1111l1l_opy_ = bstack1ll1111l11_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1llll111_opy_:
        for driver in bstack1llll111_opy_:
          if bstack1l1111l1l_opy_ == driver.session_id:
            bstack11ll111lll_opy_ = driver
    bstack1lll11ll1_opy_ = bstack1lll11ll_opy_.bstack1l1lll1l1_opy_(test.tags)
    if bstack11ll111lll_opy_:
      threading.current_thread().isA11yTest = bstack1lll11ll_opy_.bstack1l1llll11l_opy_(bstack11ll111lll_opy_, bstack1lll11ll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1lll11ll1_opy_
  except:
    pass
  bstack1lll11ll11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll11l1l1l_opy_
  bstack1ll11l1l1l_opy_ = self._test
def bstack1l1ll1llll_opy_():
  global bstack1ll1ll11l_opy_
  try:
    if os.path.exists(bstack1ll1ll11l_opy_):
      os.remove(bstack1ll1ll11l_opy_)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ଺") + str(e))
def bstack11llll1l11_opy_():
  global bstack1ll1ll11l_opy_
  bstack1ll1lllll1_opy_ = {}
  try:
    if not os.path.isfile(bstack1ll1ll11l_opy_):
      with open(bstack1ll1ll11l_opy_, bstack11l11_opy_ (u"ࠬࡽࠧ଻")):
        pass
      with open(bstack1ll1ll11l_opy_, bstack11l11_opy_ (u"ࠨࡷࠬࠤ଼")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1ll1ll11l_opy_):
      bstack1ll1lllll1_opy_ = json.load(open(bstack1ll1ll11l_opy_, bstack11l11_opy_ (u"ࠧࡳࡤࠪଽ")))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪା") + str(e))
  finally:
    return bstack1ll1lllll1_opy_
def bstack1ll11l11_opy_(platform_index, item_index):
  global bstack1ll1ll11l_opy_
  try:
    bstack1ll1lllll1_opy_ = bstack11llll1l11_opy_()
    bstack1ll1lllll1_opy_[item_index] = platform_index
    with open(bstack1ll1ll11l_opy_, bstack11l11_opy_ (u"ࠤࡺ࠯ࠧି")) as outfile:
      json.dump(bstack1ll1lllll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨୀ") + str(e))
def bstack11lll11l_opy_(bstack11ll1lll11_opy_):
  global CONFIG
  bstack11l1llll_opy_ = bstack11l11_opy_ (u"ࠫࠬୁ")
  if not bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨୂ") in CONFIG:
    logger.info(bstack11l11_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪୃ"))
  try:
    platform = CONFIG[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪୄ")][bstack11ll1lll11_opy_]
    if bstack11l11_opy_ (u"ࠨࡱࡶࠫ୅") in platform:
      bstack11l1llll_opy_ += str(platform[bstack11l11_opy_ (u"ࠩࡲࡷࠬ୆")]) + bstack11l11_opy_ (u"ࠪ࠰ࠥ࠭େ")
    if bstack11l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧୈ") in platform:
      bstack11l1llll_opy_ += str(platform[bstack11l11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୉")]) + bstack11l11_opy_ (u"࠭ࠬࠡࠩ୊")
    if bstack11l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫୋ") in platform:
      bstack11l1llll_opy_ += str(platform[bstack11l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬୌ")]) + bstack11l11_opy_ (u"ࠩ࠯ࠤ୍ࠬ")
    if bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ୎") in platform:
      bstack11l1llll_opy_ += str(platform[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭୏")]) + bstack11l11_opy_ (u"ࠬ࠲ࠠࠨ୐")
    if bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ୑") in platform:
      bstack11l1llll_opy_ += str(platform[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୒")]) + bstack11l11_opy_ (u"ࠨ࠮ࠣࠫ୓")
    if bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ୔") in platform:
      bstack11l1llll_opy_ += str(platform[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ୕")]) + bstack11l11_opy_ (u"ࠫ࠱ࠦࠧୖ")
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬୗ") + str(e))
  finally:
    if bstack11l1llll_opy_[len(bstack11l1llll_opy_) - 2:] == bstack11l11_opy_ (u"࠭ࠬࠡࠩ୘"):
      bstack11l1llll_opy_ = bstack11l1llll_opy_[:-2]
    return bstack11l1llll_opy_
def bstack11ll1l11l_opy_(path, bstack11l1llll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1ll111_opy_ = ET.parse(path)
    bstack1l1ll1111_opy_ = bstack1l1ll111_opy_.getroot()
    bstack1ll11lll1_opy_ = None
    for suite in bstack1l1ll1111_opy_.iter(bstack11l11_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭୙")):
      if bstack11l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ୚") in suite.attrib:
        suite.attrib[bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ୛")] += bstack11l11_opy_ (u"ࠪࠤࠬଡ଼") + bstack11l1llll_opy_
        bstack1ll11lll1_opy_ = suite
    bstack1lll111lll_opy_ = None
    for robot in bstack1l1ll1111_opy_.iter(bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪଢ଼")):
      bstack1lll111lll_opy_ = robot
    bstack1l11l1111_opy_ = len(bstack1lll111lll_opy_.findall(bstack11l11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୞")))
    if bstack1l11l1111_opy_ == 1:
      bstack1lll111lll_opy_.remove(bstack1lll111lll_opy_.findall(bstack11l11_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬୟ"))[0])
      bstack1l1l1lll_opy_ = ET.Element(bstack11l11_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ୠ"), attrib={bstack11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ୡ"): bstack11l11_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩୢ"), bstack11l11_opy_ (u"ࠪ࡭ࡩ࠭ୣ"): bstack11l11_opy_ (u"ࠫࡸ࠶ࠧ୤")})
      bstack1lll111lll_opy_.insert(1, bstack1l1l1lll_opy_)
      bstack1l11l1l11_opy_ = None
      for suite in bstack1lll111lll_opy_.iter(bstack11l11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୥")):
        bstack1l11l1l11_opy_ = suite
      bstack1l11l1l11_opy_.append(bstack1ll11lll1_opy_)
      bstack1l111lll1l_opy_ = None
      for status in bstack1ll11lll1_opy_.iter(bstack11l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭୦")):
        bstack1l111lll1l_opy_ = status
      bstack1l11l1l11_opy_.append(bstack1l111lll1l_opy_)
    bstack1l1ll111_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬ୧") + str(e))
def bstack1l11llll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1l1l11l_opy_
  global CONFIG
  if bstack11l11_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ୨") in options:
    del options[bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ୩")]
  bstack1l11l1l1l_opy_ = bstack11llll1l11_opy_()
  for bstack1lll1llll_opy_ in bstack1l11l1l1l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪ୪"), str(bstack1lll1llll_opy_), bstack11l11_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨ୫"))
    bstack11ll1l11l_opy_(path, bstack11lll11l_opy_(bstack1l11l1l1l_opy_[bstack1lll1llll_opy_]))
  bstack1l1ll1llll_opy_()
  return bstack1l1l1l11l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack111lll1l_opy_(self, ff_profile_dir):
  global bstack11ll11ll_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll11ll_opy_(self, ff_profile_dir)
def bstack11ll11111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack111lll1l1_opy_
  bstack1lllll11l1_opy_ = []
  if bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୬") in CONFIG:
    bstack1lllll11l1_opy_ = CONFIG[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୭")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣ୮")],
      pabot_args[bstack11l11_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤ୯")],
      argfile,
      pabot_args.get(bstack11l11_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢ୰")),
      pabot_args[bstack11l11_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨୱ")],
      platform[0],
      bstack111lll1l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l11_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ୲")] or [(bstack11l11_opy_ (u"ࠧࠨ୳"), None)]
    for platform in enumerate(bstack1lllll11l1_opy_)
  ]
def bstack1lllllll1l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1l1111ll_opy_=bstack11l11_opy_ (u"࠭ࠧ୴")):
  global bstack1l111111ll_opy_
  self.platform_index = platform_index
  self.bstack1ll11l1lll_opy_ = bstack1l1l1111ll_opy_
  bstack1l111111ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1l1l1l11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111llll1_opy_
  global bstack1l1111ll1l_opy_
  bstack1l1l11ll1_opy_ = copy.deepcopy(item)
  if not bstack11l11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ୵") in item.options:
    bstack1l1l11ll1_opy_.options[bstack11l11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ୶")] = []
  bstack1ll11ll1l1_opy_ = bstack1l1l11ll1_opy_.options[bstack11l11_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ୷")].copy()
  for v in bstack1l1l11ll1_opy_.options[bstack11l11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ୸")]:
    if bstack11l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ୹") in v:
      bstack1ll11ll1l1_opy_.remove(v)
    if bstack11l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ୺") in v:
      bstack1ll11ll1l1_opy_.remove(v)
    if bstack11l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ୻") in v:
      bstack1ll11ll1l1_opy_.remove(v)
  bstack1ll11ll1l1_opy_.insert(0, bstack11l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝ࡀࡻࡾࠩ୼").format(bstack1l1l11ll1_opy_.platform_index))
  bstack1ll11ll1l1_opy_.insert(0, bstack11l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨ୽").format(bstack1l1l11ll1_opy_.bstack1ll11l1lll_opy_))
  bstack1l1l11ll1_opy_.options[bstack11l11_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ୾")] = bstack1ll11ll1l1_opy_
  if bstack1l1111ll1l_opy_:
    bstack1l1l11ll1_opy_.options[bstack11l11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ୿")].insert(0, bstack11l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ࠾ࢀࢃࠧ஀").format(bstack1l1111ll1l_opy_))
  return bstack111llll1_opy_(caller_id, datasources, is_last, bstack1l1l11ll1_opy_, outs_dir)
def bstack1ll1llll1l_opy_(command, item_index):
  if bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭஁")):
    os.environ[bstack11l11_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧஂ")] = json.dumps(CONFIG[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪஃ")][item_index % bstack111111l1l_opy_])
  global bstack1l1111ll1l_opy_
  if bstack1l1111ll1l_opy_:
    command[0] = command[0].replace(bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ஄"), bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭அ") + str(
      item_index) + bstack11l11_opy_ (u"ࠪࠤࠬஆ") + bstack1l1111ll1l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪஇ"),
                                    bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩஈ") + str(item_index), 1)
def bstack1111ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1lll1ll1_opy_
  bstack1ll1llll1l_opy_(command, item_index)
  return bstack1l1lll1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll111l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1lll1ll1_opy_
  bstack1ll1llll1l_opy_(command, item_index)
  return bstack1l1lll1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l1l1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1lll1ll1_opy_
  bstack1ll1llll1l_opy_(command, item_index)
  return bstack1l1lll1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1ll111ll11_opy_(self, runner, quiet=False, capture=True):
  global bstack11lllll11l_opy_
  bstack1llll1l11l_opy_ = bstack11lllll11l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11l11_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭உ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l11_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫஊ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1llll1l11l_opy_
def bstack111l1111l_opy_(runner, hook_name, context, element, bstack1l1ll111l1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1l1111lll_opy_.bstack1ll11ll1ll_opy_(hook_name, element)
    bstack1l1ll111l1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1l1111lll_opy_.bstack1l1lll11l_opy_(element)
      if hook_name not in [bstack11l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ஋"), bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ஌")] and args and hasattr(args[0], bstack11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪ஍")):
        args[0].error_message = bstack11l11_opy_ (u"ࠫࠬஎ")
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡪࡤࡲࡩࡲࡥࠡࡪࡲࡳࡰࡹࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧஏ").format(str(e)))
@measure(event_name=EVENTS.bstack111l111l_opy_, stage=STAGE.SINGLE, hook_type=bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡇ࡬࡭ࠤஐ"), bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1ll1l11l1_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
    if runner.hooks.get(bstack11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ஑")).__name__ != bstack11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࡤࡪࡥࡧࡣࡸࡰࡹࡥࡨࡰࡱ࡮ࠦஒ"):
      bstack111l1111l_opy_(runner, name, context, runner, bstack1l1ll111l1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l1ll11111_opy_(bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨஓ")) else context.browser
      runner.driver_initialised = bstack11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢஔ")
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࠡࡣࡷࡸࡷ࡯ࡢࡶࡶࡨ࠾ࠥࢁࡽࠨக").format(str(e)))
def bstack1llll11l1_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
    bstack111l1111l_opy_(runner, name, context, context.feature, bstack1l1ll111l1_opy_, *args)
    try:
      if not bstack1l1lll1l11_opy_:
        bstack11ll111lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll11111_opy_(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ஖")) else context.browser
        if is_driver_active(bstack11ll111lll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ஗")
          bstack11llll111_opy_ = str(runner.feature.name)
          bstack1ll1l1ll_opy_(context, bstack11llll111_opy_)
          bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ஘") + json.dumps(bstack11llll111_opy_) + bstack11l11_opy_ (u"ࠨࡿࢀࠫங"))
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩச").format(str(e)))
def bstack1lllll111l_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
    if hasattr(context, bstack11l11_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ஛")):
        bstack1l1111lll_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack11l11_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ஜ")) else context.feature
    bstack111l1111l_opy_(runner, name, context, target, bstack1l1ll111l1_opy_, *args)
@measure(event_name=EVENTS.bstack1l111ll1l1_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack111l11l1l_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1l1111lll_opy_.start_test(context)
    bstack111l1111l_opy_(runner, name, context, context.scenario, bstack1l1ll111l1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack111l1l11l_opy_.bstack1l1l11l11l_opy_(context, *args)
    try:
      bstack11ll111lll_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ஝"), context.browser)
      if is_driver_active(bstack11ll111lll_opy_):
        bstack1l11ll1l_opy_.bstack11111l11l_opy_(bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬஞ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤட")
        if (not bstack1l1lll1l11_opy_):
          scenario_name = args[0].name
          feature_name = bstack11llll111_opy_ = str(runner.feature.name)
          bstack11llll111_opy_ = feature_name + bstack11l11_opy_ (u"ࠨࠢ࠰ࠤࠬ஠") + scenario_name
          if runner.driver_initialised == bstack11l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ஡"):
            bstack1ll1l1ll_opy_(context, bstack11llll111_opy_)
            bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ஢") + json.dumps(bstack11llll111_opy_) + bstack11l11_opy_ (u"ࠫࢂࢃࠧண"))
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭த").format(str(e)))
@measure(event_name=EVENTS.bstack111l111l_opy_, stage=STAGE.SINGLE, hook_type=bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪ࡙ࡴࡦࡲࠥ஥"), bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1ll111l11_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
    bstack111l1111l_opy_(runner, name, context, args[0], bstack1l1ll111l1_opy_, *args)
    try:
      bstack11ll111lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll11111_opy_(bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭஦")) else context.browser
      if is_driver_active(bstack11ll111lll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ஧")
        bstack1l1111lll_opy_.bstack11lll1l1l_opy_(args[0])
        if runner.driver_initialised == bstack11l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢந"):
          feature_name = bstack11llll111_opy_ = str(runner.feature.name)
          bstack11llll111_opy_ = feature_name + bstack11l11_opy_ (u"ࠪࠤ࠲ࠦࠧன") + context.scenario.name
          bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩப") + json.dumps(bstack11llll111_opy_) + bstack11l11_opy_ (u"ࠬࢃࡽࠨ஫"))
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪ஬").format(str(e)))
@measure(event_name=EVENTS.bstack111l111l_opy_, stage=STAGE.SINGLE, hook_type=bstack11l11_opy_ (u"ࠢࡢࡨࡷࡩࡷ࡙ࡴࡦࡲࠥ஭"), bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1111l111_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
  bstack1l1111lll_opy_.bstack1l11l1lll_opy_(args[0])
  try:
    bstack11111ll1_opy_ = args[0].status.name
    bstack11ll111lll_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧம") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11ll111lll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩய")
        feature_name = bstack11llll111_opy_ = str(runner.feature.name)
        bstack11llll111_opy_ = feature_name + bstack11l11_opy_ (u"ࠪࠤ࠲ࠦࠧர") + context.scenario.name
        bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩற") + json.dumps(bstack11llll111_opy_) + bstack11l11_opy_ (u"ࠬࢃࡽࠨல"))
    if str(bstack11111ll1_opy_).lower() == bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ள"):
      bstack11l1ll11_opy_ = bstack11l11_opy_ (u"ࠧࠨழ")
      bstack1ll111111_opy_ = bstack11l11_opy_ (u"ࠨࠩவ")
      bstack11lll1l111_opy_ = bstack11l11_opy_ (u"ࠩࠪஶ")
      try:
        import traceback
        bstack11l1ll11_opy_ = runner.exception.__class__.__name__
        bstack1ll1lll1ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll111111_opy_ = bstack11l11_opy_ (u"ࠪࠤࠬஷ").join(bstack1ll1lll1ll_opy_)
        bstack11lll1l111_opy_ = bstack1ll1lll1ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1l1ll1_opy_.format(str(e)))
      bstack11l1ll11_opy_ += bstack11lll1l111_opy_
      bstack1lll1lllll_opy_(context, json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥஸ") + str(bstack1ll111111_opy_)),
                          bstack11l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦஹ"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ஺"):
        bstack11111lll1_opy_(getattr(context, bstack11l11_opy_ (u"ࠧࡱࡣࡪࡩࠬ஻"), None), bstack11l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ஼"), bstack11l1ll11_opy_)
        bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ஽") + json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤா") + str(bstack1ll111111_opy_)) + bstack11l11_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫி"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥீ"):
        bstack1ll1ll1l11_opy_(bstack11ll111lll_opy_, bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ு"), bstack11l11_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦூ") + str(bstack11l1ll11_opy_))
    else:
      bstack1lll1lllll_opy_(context, bstack11l11_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤ௃"), bstack11l11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ௄"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௅"):
        bstack11111lll1_opy_(getattr(context, bstack11l11_opy_ (u"ࠫࡵࡧࡧࡦࠩெ"), None), bstack11l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧே"))
      bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫை") + json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦ௉")) + bstack11l11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧொ"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢோ"):
        bstack1ll1ll1l11_opy_(bstack11ll111lll_opy_, bstack11l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥௌ"))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡵࡷࡩࡵࡀࠠࡼࡿ்ࠪ").format(str(e)))
  bstack111l1111l_opy_(runner, name, context, args[0], bstack1l1ll111l1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l1ll11_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack11l1ll1l1_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
  bstack1l1111lll_opy_.end_test(args[0])
  try:
    bstack111ll1ll1_opy_ = args[0].status.name
    bstack11ll111lll_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ௎"), context.browser)
    bstack111l1l11l_opy_.bstack1lll111l11_opy_(bstack11ll111lll_opy_)
    if str(bstack111ll1ll1_opy_).lower() == bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭௏"):
      bstack11l1ll11_opy_ = bstack11l11_opy_ (u"ࠧࠨௐ")
      bstack1ll111111_opy_ = bstack11l11_opy_ (u"ࠨࠩ௑")
      bstack11lll1l111_opy_ = bstack11l11_opy_ (u"ࠩࠪ௒")
      try:
        import traceback
        bstack11l1ll11_opy_ = runner.exception.__class__.__name__
        bstack1ll1lll1ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll111111_opy_ = bstack11l11_opy_ (u"ࠪࠤࠬ௓").join(bstack1ll1lll1ll_opy_)
        bstack11lll1l111_opy_ = bstack1ll1lll1ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1l1ll1_opy_.format(str(e)))
      bstack11l1ll11_opy_ += bstack11lll1l111_opy_
      bstack1lll1lllll_opy_(context, json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ௔") + str(bstack1ll111111_opy_)),
                          bstack11l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ௕"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ௖") or runner.driver_initialised == bstack11l11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧௗ"):
        bstack11111lll1_opy_(getattr(context, bstack11l11_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭௘"), None), bstack11l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ௙"), bstack11l1ll11_opy_)
        bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ௚") + json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ௛") + str(bstack1ll111111_opy_)) + bstack11l11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ௜"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ௝") or runner.driver_initialised == bstack11l11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧ௞"):
        bstack1ll1ll1l11_opy_(bstack11ll111lll_opy_, bstack11l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ௟"), bstack11l11_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ௠") + str(bstack11l1ll11_opy_))
    else:
      bstack1lll1lllll_opy_(context, bstack11l11_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦ௡"), bstack11l11_opy_ (u"ࠦ࡮ࡴࡦࡰࠤ௢"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ௣") or runner.driver_initialised == bstack11l11_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭௤"):
        bstack11111lll1_opy_(getattr(context, bstack11l11_opy_ (u"ࠧࡱࡣࡪࡩࠬ௥"), None), bstack11l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ௦"))
      bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ௧") + json.dumps(str(args[0].name) + bstack11l11_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢ௨")) + bstack11l11_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪ௩"))
      if runner.driver_initialised == bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ௪") or runner.driver_initialised == bstack11l11_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭௫"):
        bstack1ll1ll1l11_opy_(bstack11ll111lll_opy_, bstack11l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ௬"))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ௭").format(str(e)))
  bstack111l1111l_opy_(runner, name, context, context.scenario, bstack1l1ll111l1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack111llllll_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
    target = context.scenario if hasattr(context, bstack11l11_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ௮")) else context.feature
    bstack111l1111l_opy_(runner, name, context, target, bstack1l1ll111l1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1l1l11l1l_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
    try:
      bstack11ll111lll_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௯"), context.browser)
      bstack1l11l11lll_opy_ = bstack11l11_opy_ (u"ࠫࠬ௰")
      if context.failed is True:
        bstack11l111l1l_opy_ = []
        bstack111l1l1l_opy_ = []
        bstack1l1ll11ll_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11l111l1l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1ll1lll1ll_opy_ = traceback.format_tb(exc_tb)
            bstack1llll1ll1l_opy_ = bstack11l11_opy_ (u"ࠬࠦࠧ௱").join(bstack1ll1lll1ll_opy_)
            bstack111l1l1l_opy_.append(bstack1llll1ll1l_opy_)
            bstack1l1ll11ll_opy_.append(bstack1ll1lll1ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack11ll1l1ll1_opy_.format(str(e)))
        bstack11l1ll11_opy_ = bstack11l11_opy_ (u"࠭ࠧ௲")
        for i in range(len(bstack11l111l1l_opy_)):
          bstack11l1ll11_opy_ += bstack11l111l1l_opy_[i] + bstack1l1ll11ll_opy_[i] + bstack11l11_opy_ (u"ࠧ࡝ࡰࠪ௳")
        bstack1l11l11lll_opy_ = bstack11l11_opy_ (u"ࠨࠢࠪ௴").join(bstack111l1l1l_opy_)
        if runner.driver_initialised in [bstack11l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ௵"), bstack11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ௶")]:
          bstack1lll1lllll_opy_(context, bstack1l11l11lll_opy_, bstack11l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ௷"))
          bstack11111lll1_opy_(getattr(context, bstack11l11_opy_ (u"ࠬࡶࡡࡨࡧࠪ௸"), None), bstack11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ௹"), bstack11l1ll11_opy_)
          bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௺") + json.dumps(bstack1l11l11lll_opy_) + bstack11l11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ௻"))
          bstack1ll1ll1l11_opy_(bstack11ll111lll_opy_, bstack11l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ௼"), bstack11l11_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣ௽") + str(bstack11l1ll11_opy_))
          bstack1l11111l11_opy_ = bstack11lll11l1_opy_(bstack1l11l11lll_opy_, runner.feature.name, logger)
          if (bstack1l11111l11_opy_ != None):
            bstack1l1lll11_opy_.append(bstack1l11111l11_opy_)
      else:
        if runner.driver_initialised in [bstack11l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ௾"), bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ௿")]:
          bstack1lll1lllll_opy_(context, bstack11l11_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤఀ") + str(runner.feature.name) + bstack11l11_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤఁ"), bstack11l11_opy_ (u"ࠣ࡫ࡱࡪࡴࠨం"))
          bstack11111lll1_opy_(getattr(context, bstack11l11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧః"), None), bstack11l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥఄ"))
          bstack11ll111lll_opy_.execute_script(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩఅ") + json.dumps(bstack11l11_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣఆ") + str(runner.feature.name) + bstack11l11_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣఇ")) + bstack11l11_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ఈ"))
          bstack1ll1ll1l11_opy_(bstack11ll111lll_opy_, bstack11l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨఉ"))
          bstack1l11111l11_opy_ = bstack11lll11l1_opy_(bstack1l11l11lll_opy_, runner.feature.name, logger)
          if (bstack1l11111l11_opy_ != None):
            bstack1l1lll11_opy_.append(bstack1l11111l11_opy_)
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫఊ").format(str(e)))
    bstack111l1111l_opy_(runner, name, context, context.feature, bstack1l1ll111l1_opy_, *args)
@measure(event_name=EVENTS.bstack111l111l_opy_, stage=STAGE.SINGLE, hook_type=bstack11l11_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡃ࡯ࡰࠧఋ"), bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack11ll1l1111_opy_(runner, name, context, bstack1l1ll111l1_opy_, *args):
    bstack111l1111l_opy_(runner, name, context, runner, bstack1l1ll111l1_opy_, *args)
def bstack1l1l111l1_opy_(self, name, context, *args):
  if bstack11111ll11_opy_:
    platform_index = int(threading.current_thread()._name) % bstack111111l1l_opy_
    bstack1l11ll1ll1_opy_ = CONFIG[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఌ")][platform_index]
    os.environ[bstack11l11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭఍")] = json.dumps(bstack1l11ll1ll1_opy_)
  global bstack1l1ll111l1_opy_
  if not hasattr(self, bstack11l11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࡧࠫఎ")):
    self.driver_initialised = None
  bstack11lllllll_opy_ = {
      bstack11l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫఏ"): bstack1ll1l11l1_opy_,
      bstack11l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩఐ"): bstack1llll11l1_opy_,
      bstack11l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭఑"): bstack1lllll111l_opy_,
      bstack11l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬఒ"): bstack111l11l1l_opy_,
      bstack11l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠩఓ"): bstack1ll111l11_opy_,
      bstack11l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩఔ"): bstack1111l111_opy_,
      bstack11l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧక"): bstack11l1ll1l1_opy_,
      bstack11l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪఖ"): bstack111llllll_opy_,
      bstack11l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨగ"): bstack1l1l11l1l_opy_,
      bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬఘ"): bstack11ll1l1111_opy_
  }
  handler = bstack11lllllll_opy_.get(name, bstack1l1ll111l1_opy_)
  handler(self, name, context, bstack1l1ll111l1_opy_, *args)
  if name in [bstack11l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪఙ"), bstack11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬచ"), bstack11l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨఛ")]:
    try:
      bstack11ll111lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll11111_opy_(bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬజ")) else context.browser
      bstack1l11111ll_opy_ = (
        (name == bstack11l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪఝ") and self.driver_initialised == bstack11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧఞ")) or
        (name == bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩట") and self.driver_initialised == bstack11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦఠ")) or
        (name == bstack11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬడ") and self.driver_initialised in [bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢఢ"), bstack11l11_opy_ (u"ࠨࡩ࡯ࡵࡷࡩࡵࠨణ")]) or
        (name == bstack11l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫత") and self.driver_initialised == bstack11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨథ"))
      )
      if bstack1l11111ll_opy_:
        self.driver_initialised = None
        bstack11ll111lll_opy_.quit()
    except Exception:
      pass
def bstack1lll11lll1_opy_(config, startdir):
  return bstack11l11_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢద").format(bstack11l11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤధ"))
notset = Notset()
def bstack1ll1l11lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1llll1111l_opy_
  if str(name).lower() == bstack11l11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫన"):
    return bstack11l11_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ఩")
  else:
    return bstack1llll1111l_opy_(self, name, default, skip)
def bstack111lllll1_opy_(item, when):
  global bstack1l1l11l11_opy_
  try:
    bstack1l1l11l11_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll11l11l_opy_():
  return
def bstack1lllllll11_opy_(type, name, status, reason, bstack11ll11lll_opy_, bstack1l1111ll11_opy_):
  bstack1111111l_opy_ = {
    bstack11l11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ప"): type,
    bstack11l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪఫ"): {}
  }
  if type == bstack11l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪబ"):
    bstack1111111l_opy_[bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬభ")][bstack11l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩమ")] = bstack11ll11lll_opy_
    bstack1111111l_opy_[bstack11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧయ")][bstack11l11_opy_ (u"ࠬࡪࡡࡵࡣࠪర")] = json.dumps(str(bstack1l1111ll11_opy_))
  if type == bstack11l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧఱ"):
    bstack1111111l_opy_[bstack11l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪల")][bstack11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ళ")] = name
  if type == bstack11l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬఴ"):
    bstack1111111l_opy_[bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭వ")][bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫశ")] = status
    if status == bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬష"):
      bstack1111111l_opy_[bstack11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩస")][bstack11l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧహ")] = json.dumps(str(reason))
  bstack11llllllll_opy_ = bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭఺").format(json.dumps(bstack1111111l_opy_))
  return bstack11llllllll_opy_
def bstack1l1llllll_opy_(driver_command, response):
    if driver_command == bstack11l11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭఻"):
        bstack1l11ll1l_opy_.bstack1ll1l1l1l_opy_({
            bstack11l11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦ఼ࠩ"): response[bstack11l11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪఽ")],
            bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬా"): bstack1l11ll1l_opy_.current_test_uuid()
        })
def bstack1l1l111l11_opy_(item, call, rep):
  global bstack11lll1l1ll_opy_
  global bstack1llll111_opy_
  global bstack1l1lll1l11_opy_
  name = bstack11l11_opy_ (u"࠭ࠧి")
  try:
    if rep.when == bstack11l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬీ"):
      bstack1l1111l1l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1lll1l11_opy_:
          name = str(rep.nodeid)
          bstack1l111llll1_opy_ = bstack1lllllll11_opy_(bstack11l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩు"), name, bstack11l11_opy_ (u"ࠩࠪూ"), bstack11l11_opy_ (u"ࠪࠫృ"), bstack11l11_opy_ (u"ࠫࠬౄ"), bstack11l11_opy_ (u"ࠬ࠭౅"))
          threading.current_thread().bstack1l1ll1l111_opy_ = name
          for driver in bstack1llll111_opy_:
            if bstack1l1111l1l_opy_ == driver.session_id:
              driver.execute_script(bstack1l111llll1_opy_)
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ె").format(str(e)))
      try:
        bstack11l1ll1l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨే"):
          status = bstack11l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨై") if rep.outcome.lower() == bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౉") else bstack11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪొ")
          reason = bstack11l11_opy_ (u"ࠫࠬో")
          if status == bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬౌ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11l11_opy_ (u"࠭ࡩ࡯ࡨࡲ్ࠫ") if status == bstack11l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ౎") else bstack11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ౏")
          data = name + bstack11l11_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ౐") if status == bstack11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ౑") else name + bstack11l11_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧ౒") + reason
          bstack11l1lllll_opy_ = bstack1lllllll11_opy_(bstack11l11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ౓"), bstack11l11_opy_ (u"࠭ࠧ౔"), bstack11l11_opy_ (u"ࠧࠨౕ"), bstack11l11_opy_ (u"ࠨౖࠩ"), level, data)
          for driver in bstack1llll111_opy_:
            if bstack1l1111l1l_opy_ == driver.session_id:
              driver.execute_script(bstack11l1lllll_opy_)
      except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭౗").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧౘ").format(str(e)))
  bstack11lll1l1ll_opy_(item, call, rep)
def bstack11l1lll1_opy_(driver, bstack1l1l1l11ll_opy_, test=None):
  global bstack11ll11l111_opy_
  if test != None:
    bstack1l1l1l1l_opy_ = getattr(test, bstack11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩౙ"), None)
    bstack1l1lll1l_opy_ = getattr(test, bstack11l11_opy_ (u"ࠬࡻࡵࡪࡦࠪౚ"), None)
    PercySDK.screenshot(driver, bstack1l1l1l11ll_opy_, bstack1l1l1l1l_opy_=bstack1l1l1l1l_opy_, bstack1l1lll1l_opy_=bstack1l1lll1l_opy_, bstack1l11l11l1_opy_=bstack11ll11l111_opy_)
  else:
    PercySDK.screenshot(driver, bstack1l1l1l11ll_opy_)
@measure(event_name=EVENTS.bstack1ll11llll_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1lll1111l1_opy_(driver):
  if bstack1ll11l1111_opy_.bstack11ll1l1l_opy_() is True or bstack1ll11l1111_opy_.capturing() is True:
    return
  bstack1ll11l1111_opy_.bstack1l1111ll_opy_()
  while not bstack1ll11l1111_opy_.bstack11ll1l1l_opy_():
    bstack1l11l1l1ll_opy_ = bstack1ll11l1111_opy_.bstack1l1llll1ll_opy_()
    bstack11l1lll1_opy_(driver, bstack1l11l1l1ll_opy_)
  bstack1ll11l1111_opy_.bstack11ll1111ll_opy_()
def bstack1llll1l1_opy_(sequence, driver_command, response = None, bstack111l1l111_opy_ = None, args = None):
    try:
      if sequence != bstack11l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭౛"):
        return
      if percy.bstack1ll1l111l_opy_() == bstack11l11_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ౜"):
        return
      bstack1l11l1l1ll_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫౝ"), None)
      for command in bstack1l1ll1l1ll_opy_:
        if command == driver_command:
          for driver in bstack1llll111_opy_:
            bstack1lll1111l1_opy_(driver)
      bstack1lll111l1l_opy_ = percy.bstack1llll1ll11_opy_()
      if driver_command in bstack1l11ll1ll_opy_[bstack1lll111l1l_opy_]:
        bstack1ll11l1111_opy_.bstack1l1111l111_opy_(bstack1l11l1l1ll_opy_, driver_command)
    except Exception as e:
      pass
@measure(event_name=EVENTS.bstack1ll111ll_opy_, stage=STAGE.bstack11lll1ll_opy_)
def bstack111l11ll1_opy_(framework_name):
  if bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭౞")):
      return
  bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ౟"), True)
  global bstack1l11111l1l_opy_
  global bstack1l11l1l1l1_opy_
  global bstack1llll1ll1_opy_
  bstack1l11111l1l_opy_ = framework_name
  logger.info(bstack11l11ll11_opy_.format(bstack1l11111l1l_opy_.split(bstack11l11_opy_ (u"ࠫ࠲࠭ౠ"))[0]))
  bstack11lll1llll_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11111ll11_opy_:
      Service.start = bstack11ll1llll1_opy_
      Service.stop = bstack111111lll_opy_
      webdriver.Remote.get = bstack1lll1l1111_opy_
      WebDriver.close = bstack1ll11l111l_opy_
      WebDriver.quit = bstack11lll11lll_opy_
      webdriver.Remote.__init__ = bstack1l11l1ll11_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack11111ll11_opy_:
        webdriver.Remote.__init__ = bstack11llll11_opy_
    WebDriver.execute = bstack1111ll1ll_opy_
    bstack1l11l1l1l1_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11111ll11_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack111ll1lll_opy_
  except Exception as e:
    pass
  bstack1ll111ll1l_opy_()
  if not bstack1l11l1l1l1_opy_:
    bstack1ll1l1l111_opy_(bstack11l11_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢౡ"), bstack11l11l1ll_opy_)
  if bstack1l1llll11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._1lll11111l_opy_ = bstack1l1l1llll_opy_
    except Exception as e:
      logger.error(bstack11111111_opy_.format(str(e)))
  if bstack1ll1ll11l1_opy_():
    bstack11llll1l1_opy_(CONFIG, logger)
  if (bstack11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬౢ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1ll1l111l_opy_() == bstack11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧౣ"):
          bstack1ll11lll11_opy_(bstack1llll1l1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack111lll1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack111l1ll1_opy_
      except Exception as e:
        logger.warn(bstack1ll1l1l1l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1llll1l1ll_opy_
      except Exception as e:
        logger.debug(bstack11llll11l1_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll1l1l1l1_opy_)
    Output.start_test = bstack11111llll_opy_
    Output.end_test = bstack1l1ll1ll1_opy_
    TestStatus.__init__ = bstack11l1ll111_opy_
    QueueItem.__init__ = bstack1lllllll1l_opy_
    pabot._create_items = bstack11ll11111_opy_
    try:
      from pabot import __version__ as bstack1l1llll1l_opy_
      if version.parse(bstack1l1llll1l_opy_) >= version.parse(bstack11l11_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨ౤")):
        pabot._run = bstack1l1l1lll1_opy_
      elif version.parse(bstack1l1llll1l_opy_) >= version.parse(bstack11l11_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ౥")):
        pabot._run = bstack1ll111l111_opy_
      else:
        pabot._run = bstack1111ll111_opy_
    except Exception as e:
      pabot._run = bstack1111ll111_opy_
    pabot._create_command_for_execution = bstack1l1l1l1l11_opy_
    pabot._report_results = bstack1l11llll1l_opy_
  if bstack11l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ౦") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1l1l111l_opy_)
    Runner.run_hook = bstack1l1l111l1_opy_
    Step.run = bstack1ll111ll11_opy_
  if bstack11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ౧") in str(framework_name).lower():
    if not bstack11111ll11_opy_:
      return
    try:
      if percy.bstack1ll1l111l_opy_() == bstack11l11_opy_ (u"ࠧࡺࡲࡶࡧࠥ౨"):
          bstack1ll11lll11_opy_(bstack1llll1l1_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1lll11lll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll11l11l_opy_
      Config.getoption = bstack1ll1l11lll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1l111l11_opy_
    except Exception as e:
      pass
def bstack1lll11l1ll_opy_():
  global CONFIG
  if bstack11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭౩") in CONFIG and int(CONFIG[bstack11l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ౪")]) > 1:
    logger.warn(bstack1111lll1l_opy_)
def bstack1111lll1_opy_(arg, bstack11lll11ll1_opy_, bstack111l1llll_opy_=None):
  global CONFIG
  global bstack1ll1111lll_opy_
  global bstack11l1l1l1_opy_
  global bstack11111ll11_opy_
  global bstack1111ll1l1_opy_
  bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ౫")
  if bstack11lll11ll1_opy_ and isinstance(bstack11lll11ll1_opy_, str):
    bstack11lll11ll1_opy_ = eval(bstack11lll11ll1_opy_)
  CONFIG = bstack11lll11ll1_opy_[bstack11l11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ౬")]
  bstack1ll1111lll_opy_ = bstack11lll11ll1_opy_[bstack11l11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ౭")]
  bstack11l1l1l1_opy_ = bstack11lll11ll1_opy_[bstack11l11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭౮")]
  bstack11111ll11_opy_ = bstack11lll11ll1_opy_[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ౯")]
  bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ౰"), bstack11111ll11_opy_)
  os.environ[bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ౱")] = bstack11ll1l1ll_opy_
  os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ౲")] = json.dumps(CONFIG)
  os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ౳")] = bstack1ll1111lll_opy_
  os.environ[bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ౴")] = str(bstack11l1l1l1_opy_)
  os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪ౵")] = str(True)
  if bstack1l111ll1_opy_(arg, [bstack11l11_opy_ (u"ࠬ࠳࡮ࠨ౶"), bstack11l11_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ౷")]) != -1:
    os.environ[bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ౸")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l11l11111_opy_)
    return
  bstack11ll1ll11_opy_()
  global bstack11ll111l_opy_
  global bstack11ll11l111_opy_
  global bstack111lll1l1_opy_
  global bstack1l1111ll1l_opy_
  global bstack11ll111ll_opy_
  global bstack1llll1ll1_opy_
  global bstack1l11ll1lll_opy_
  arg.append(bstack11l11_opy_ (u"ࠣ࠯࡚ࠦ౹"))
  arg.append(bstack11l11_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡐࡳࡩࡻ࡬ࡦࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡲࡶ࡯ࡳࡶࡨࡨ࠿ࡶࡹࡵࡧࡶࡸ࠳ࡖࡹࡵࡧࡶࡸ࡜ࡧࡲ࡯࡫ࡱ࡫ࠧ౺"))
  arg.append(bstack11l11_opy_ (u"ࠥ࠱࡜ࠨ౻"))
  arg.append(bstack11l11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾࡙࡮ࡥࠡࡪࡲࡳࡰ࡯࡭ࡱ࡮ࠥ౼"))
  global bstack11ll1ll11l_opy_
  global bstack111l1l1l1_opy_
  global bstack1lll111l1_opy_
  global bstack1lll11ll11_opy_
  global bstack11ll11ll_opy_
  global bstack1l111111ll_opy_
  global bstack111llll1_opy_
  global bstack1llll11ll1_opy_
  global bstack1l11l11ll1_opy_
  global bstack11ll11l1l_opy_
  global bstack1llll1111l_opy_
  global bstack1l1l11l11_opy_
  global bstack11lll1l1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll1ll11l_opy_ = webdriver.Remote.__init__
    bstack111l1l1l1_opy_ = WebDriver.quit
    bstack1llll11ll1_opy_ = WebDriver.close
    bstack1l11l11ll1_opy_ = WebDriver.get
    bstack1lll111l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l11l11l1l_opy_(CONFIG) and bstack1l11111lll_opy_():
    if bstack1111ll1l_opy_() < version.parse(bstack1lll11llll_opy_):
      logger.error(bstack1ll11111l1_opy_.format(bstack1111ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11ll11l1l_opy_ = RemoteConnection._1lll11111l_opy_
      except Exception as e:
        logger.error(bstack11111111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1llll1111l_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1l11l11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l1lllll_opy_)
  try:
    from pytest_bdd import reporting
    bstack11lll1l1ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11l11_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭౽"))
  bstack111lll1l1_opy_ = CONFIG.get(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ౾"), {}).get(bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ౿"))
  bstack1l11ll1lll_opy_ = True
  bstack111l11ll1_opy_(bstack1l11l11l11_opy_)
  os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩಀ")] = CONFIG[bstack11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫಁ")]
  os.environ[bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ಂ")] = CONFIG[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧಃ")]
  os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ಄")] = bstack11111ll11_opy_.__str__()
  from _pytest.config import main as bstack1111111ll_opy_
  bstack1l1111ll1_opy_ = []
  try:
    bstack11l111lll_opy_ = bstack1111111ll_opy_(arg)
    if bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪಅ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll1ll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1111ll1_opy_.append(bstack1ll1ll1ll_opy_)
    try:
      bstack1ll1lll1_opy_ = (bstack1l1111ll1_opy_, int(bstack11l111lll_opy_))
      bstack111l1llll_opy_.append(bstack1ll1lll1_opy_)
    except:
      bstack111l1llll_opy_.append((bstack1l1111ll1_opy_, bstack11l111lll_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l1111ll1_opy_.append({bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಆ"): bstack11l11_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪಇ") + os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩಈ")), bstack11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩಉ"): traceback.format_exc(), bstack11l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪಊ"): int(os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬಋ")))})
    bstack111l1llll_opy_.append((bstack1l1111ll1_opy_, 1))
def bstack1l11ll1l1l_opy_(arg):
  global bstack1ll11lll1l_opy_
  bstack111l11ll1_opy_(bstack1111l1ll_opy_)
  os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧಌ")] = str(bstack11l1l1l1_opy_)
  from behave.__main__ import main as bstack1lll11l111_opy_
  status_code = bstack1lll11l111_opy_(arg)
  if status_code != 0:
    bstack1ll11lll1l_opy_ = status_code
def bstack1l1l1111l1_opy_():
  logger.info(bstack1lll11l1l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭಍"), help=bstack11l11_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩಎ"))
  parser.add_argument(bstack11l11_opy_ (u"ࠩ࠰ࡹࠬಏ"), bstack11l11_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧಐ"), help=bstack11l11_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ಑"))
  parser.add_argument(bstack11l11_opy_ (u"ࠬ࠳࡫ࠨಒ"), bstack11l11_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬಓ"), help=bstack11l11_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨಔ"))
  parser.add_argument(bstack11l11_opy_ (u"ࠨ࠯ࡩࠫಕ"), bstack11l11_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧಖ"), help=bstack11l11_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩಗ"))
  bstack111111ll1_opy_ = parser.parse_args()
  try:
    bstack11ll11ll11_opy_ = bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨಘ")
    if bstack111111ll1_opy_.framework and bstack111111ll1_opy_.framework not in (bstack11l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬಙ"), bstack11l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧಚ")):
      bstack11ll11ll11_opy_ = bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ಛ")
    bstack1ll1ll11ll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll11ll11_opy_)
    bstack11ll1111_opy_ = open(bstack1ll1ll11ll_opy_, bstack11l11_opy_ (u"ࠨࡴࠪಜ"))
    bstack1l1ll11lll_opy_ = bstack11ll1111_opy_.read()
    bstack11ll1111_opy_.close()
    if bstack111111ll1_opy_.username:
      bstack1l1ll11lll_opy_ = bstack1l1ll11lll_opy_.replace(bstack11l11_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩಝ"), bstack111111ll1_opy_.username)
    if bstack111111ll1_opy_.key:
      bstack1l1ll11lll_opy_ = bstack1l1ll11lll_opy_.replace(bstack11l11_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬಞ"), bstack111111ll1_opy_.key)
    if bstack111111ll1_opy_.framework:
      bstack1l1ll11lll_opy_ = bstack1l1ll11lll_opy_.replace(bstack11l11_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬಟ"), bstack111111ll1_opy_.framework)
    file_name = bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨಠ")
    file_path = os.path.abspath(file_name)
    bstack111llll11_opy_ = open(file_path, bstack11l11_opy_ (u"࠭ࡷࠨಡ"))
    bstack111llll11_opy_.write(bstack1l1ll11lll_opy_)
    bstack111llll11_opy_.close()
    logger.info(bstack1ll1ll1lll_opy_)
    try:
      os.environ[bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩಢ")] = bstack111111ll1_opy_.framework if bstack111111ll1_opy_.framework != None else bstack11l11_opy_ (u"ࠣࠤಣ")
      config = yaml.safe_load(bstack1l1ll11lll_opy_)
      config[bstack11l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩತ")] = bstack11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩಥ")
      bstack1l11l111_opy_(bstack1lll11l11l_opy_, config)
    except Exception as e:
      logger.debug(bstack1111l11l1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lll1ll11l_opy_.format(str(e)))
def bstack1l11l111_opy_(bstack11lll11l1l_opy_, config, bstack1llll11ll_opy_={}):
  global bstack11111ll11_opy_
  global bstack11l11111l_opy_
  global bstack1111ll1l1_opy_
  if not config:
    return
  bstack11lllllll1_opy_ = bstack1111llll1_opy_ if not bstack11111ll11_opy_ else (
    bstack1ll1lll11l_opy_ if bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨದ") in config else (
        bstack1l11ll11_opy_ if config.get(bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩಧ")) else bstack1l111ll111_opy_
    )
)
  bstack1lll1111ll_opy_ = False
  bstack1llll11l1l_opy_ = False
  if bstack11111ll11_opy_ is True:
      if bstack11l11_opy_ (u"࠭ࡡࡱࡲࠪನ") in config:
          bstack1lll1111ll_opy_ = True
      else:
          bstack1llll11l1l_opy_ = True
  bstack1l111111_opy_ = bstack1l1l111l1l_opy_.bstack1l11ll11l1_opy_(config, bstack11l11111l_opy_)
  data = {
    bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ಩"): config[bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪಪ")],
    bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬಫ"): config[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ಬ")],
    bstack11l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨಭ"): bstack11lll11l1l_opy_,
    bstack11l11_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩಮ"): os.environ.get(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಯ"), bstack11l11111l_opy_),
    bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩರ"): bstack1111l11ll_opy_,
    bstack11l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮ࠪಱ"): bstack1ll1l11ll_opy_(),
    bstack11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬಲ"): {
      bstack11l11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨಳ"): str(config[bstack11l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ಴")]) if bstack11l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬವ") in config else bstack11l11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢಶ"),
      bstack11l11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡘࡨࡶࡸ࡯࡯࡯ࠩಷ"): sys.version,
      bstack11l11_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪಸ"): bstack111l11ll_opy_(os.getenv(bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦಹ"), bstack11l11_opy_ (u"ࠥࠦ಺"))),
      bstack11l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭಻"): bstack11l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ಼ࠬ"),
      bstack11l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧಽ"): bstack11lllllll1_opy_,
      bstack11l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬಾ"): bstack1l111111_opy_,
      bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧಿ"): os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧೀ")],
      bstack11l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ು"): bstack1llll11111_opy_(os.environ.get(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ೂ"), bstack11l11111l_opy_)),
      bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨೃ"): config[bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩೄ")] if config[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೅")] else bstack11l11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤೆ"),
      bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫೇ"): str(config[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬೈ")]) if bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭೉") in config else bstack11l11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨೊ"),
      bstack11l11_opy_ (u"࠭࡯ࡴࠩೋ"): sys.platform,
      bstack11l11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩೌ"): socket.gethostname(),
      bstack11l11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦ್ࠪ"): bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ೎"))
    }
  }
  if not bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ೏")) is None:
    data[bstack11l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ೐")][bstack11l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨ೑")] = {
      bstack11l11_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭೒"): bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ೓"),
      bstack11l11_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ೔"): bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩೕ")),
      bstack11l11_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩೖ"): bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ೗"))
    }
  if bstack11lll11l1l_opy_ == bstack1ll1l1l1ll_opy_:
    data[bstack11l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ೘")][bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫ೙")] = bstack1l11l1ll1l_opy_(config)
    data[bstack11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ೚")][bstack11l11_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭೛")] = percy.bstack11l1l1ll_opy_
    data[bstack11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ೜")][bstack11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩೝ")] = percy.bstack1ll1llll1_opy_
  update(data[bstack11l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧೞ")], bstack1llll11ll_opy_)
  try:
    response = bstack1lllll1l1_opy_(bstack11l11_opy_ (u"ࠬࡖࡏࡔࡖࠪ೟"), bstack1ll11l111_opy_(bstack1ll1llll_opy_), data, {
      bstack11l11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫೠ"): (config[bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩೡ")], config[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫೢ")])
    })
    if response:
      logger.debug(bstack1ll1l111ll_opy_.format(bstack11lll11l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l11l1lll1_opy_.format(str(e)))
def bstack111l11ll_opy_(framework):
  return bstack11l11_opy_ (u"ࠤࡾࢁ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨೣ").format(str(framework), __version__) if framework else bstack11l11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦ೤").format(
    __version__)
def bstack11ll1ll11_opy_():
  global CONFIG
  global bstack1ll1111111_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1l1l111l_opy_()
    logger.debug(bstack11ll1l1l1_opy_.format(str(CONFIG)))
    bstack1ll1111111_opy_ = bstack11llll1ll1_opy_.bstack11lll1lll1_opy_(CONFIG, bstack1ll1111111_opy_)
    bstack11lll1llll_opy_()
  except Exception as e:
    logger.error(bstack11l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠣ೥") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1lll1ll1_opy_
  atexit.register(bstack11ll1l111l_opy_)
  signal.signal(signal.SIGINT, bstack1ll11ll11l_opy_)
  signal.signal(signal.SIGTERM, bstack1ll11ll11l_opy_)
def bstack1lll1ll1_opy_(exctype, value, traceback):
  global bstack1llll111_opy_
  try:
    for driver in bstack1llll111_opy_:
      bstack1ll1ll1l11_opy_(driver, bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ೦"), bstack11l11_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ೧") + str(value))
  except Exception:
    pass
  bstack1llll111l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1llll111l_opy_(message=bstack11l11_opy_ (u"ࠧࠨ೨"), bstack11lll1l1l1_opy_ = False):
  global CONFIG
  bstack111ll111l_opy_ = bstack11l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡆࡺࡦࡩࡵࡺࡩࡰࡰࠪ೩") if bstack11lll1l1l1_opy_ else bstack11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ೪")
  try:
    if message:
      bstack1llll11ll_opy_ = {
        bstack111ll111l_opy_ : str(message)
      }
      bstack1l11l111_opy_(bstack1ll1l1l1ll_opy_, CONFIG, bstack1llll11ll_opy_)
    else:
      bstack1l11l111_opy_(bstack1ll1l1l1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1111l1ll_opy_.format(str(e)))
def bstack1ll11l1l1_opy_(bstack11ll11l1l1_opy_, size):
  bstack1lll1l1ll1_opy_ = []
  while len(bstack11ll11l1l1_opy_) > size:
    bstack1111l111l_opy_ = bstack11ll11l1l1_opy_[:size]
    bstack1lll1l1ll1_opy_.append(bstack1111l111l_opy_)
    bstack11ll11l1l1_opy_ = bstack11ll11l1l1_opy_[size:]
  bstack1lll1l1ll1_opy_.append(bstack11ll11l1l1_opy_)
  return bstack1lll1l1ll1_opy_
def bstack11l1l1lll_opy_(args):
  if bstack11l11_opy_ (u"ࠪ࠱ࡲ࠭೫") in args and bstack11l11_opy_ (u"ࠫࡵࡪࡢࠨ೬") in args:
    return True
  return False
def run_on_browserstack(bstack1l1lll11ll_opy_=None, bstack111l1llll_opy_=None, bstack111l111l1_opy_=False):
  global CONFIG
  global bstack1ll1111lll_opy_
  global bstack11l1l1l1_opy_
  global bstack11l11111l_opy_
  global bstack1111ll1l1_opy_
  bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠬ࠭೭")
  bstack1l11l11ll_opy_(bstack1l11l1llll_opy_, logger)
  if bstack1l1lll11ll_opy_ and isinstance(bstack1l1lll11ll_opy_, str):
    bstack1l1lll11ll_opy_ = eval(bstack1l1lll11ll_opy_)
  if bstack1l1lll11ll_opy_:
    CONFIG = bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭೮")]
    bstack1ll1111lll_opy_ = bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ೯")]
    bstack11l1l1l1_opy_ = bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ೰")]
    bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫೱ"), bstack11l1l1l1_opy_)
    bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪೲ")
  bstack1111ll1l1_opy_.bstack1ll11l1l11_opy_(bstack11l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ೳ"), uuid4().__str__())
  logger.debug(bstack11l11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ࠽ࠨ೴") + bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ೵")))
  if not bstack111l111l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l11l11111_opy_)
      return
    if sys.argv[1] == bstack11l11_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ೶") or sys.argv[1] == bstack11l11_opy_ (u"ࠨ࠯ࡹࠫ೷"):
      logger.info(bstack11l11_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩ೸").format(__version__))
      return
    if sys.argv[1] == bstack11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ೹"):
      bstack1l1l1111l1_opy_()
      return
  args = sys.argv
  bstack11ll1ll11_opy_()
  global bstack11ll111l_opy_
  global bstack111111l1l_opy_
  global bstack1l11ll1lll_opy_
  global bstack1l11l1l111_opy_
  global bstack11ll11l111_opy_
  global bstack111lll1l1_opy_
  global bstack1l1111ll1l_opy_
  global bstack1l1ll11l_opy_
  global bstack11ll111ll_opy_
  global bstack1llll1ll1_opy_
  global bstack1llll1llll_opy_
  bstack111111l1l_opy_ = len(CONFIG.get(bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ೺"), []))
  if not bstack11ll1l1ll_opy_:
    if args[1] == bstack11l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ೻") or args[1] == bstack11l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ೼"):
      bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ೽")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ೾"):
      bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ೿")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩഀ"):
      bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪഁ")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ം"):
      bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧഃ")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧഄ"):
      bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨഅ")
      args = args[2:]
    elif args[1] == bstack11l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩആ"):
      bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪഇ")
      args = args[2:]
    else:
      if not bstack11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഈ") in CONFIG or str(CONFIG[bstack11l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨഉ")]).lower() in [bstack11l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ഊ"), bstack11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨഋ")]:
        bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഌ")
        args = args[1:]
      elif str(CONFIG[bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ഍")]).lower() == bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩഎ"):
        bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪഏ")
        args = args[1:]
      elif str(CONFIG[bstack11l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨഐ")]).lower() == bstack11l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ഑"):
        bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ഒ")
        args = args[1:]
      elif str(CONFIG[bstack11l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫഓ")]).lower() == bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഔ"):
        bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪക")
        args = args[1:]
      elif str(CONFIG[bstack11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഖ")]).lower() == bstack11l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬഗ"):
        bstack11ll1l1ll_opy_ = bstack11l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ഘ")
        args = args[1:]
      else:
        os.environ[bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩങ")] = bstack11ll1l1ll_opy_
        bstack111111ll_opy_(bstack11111l1l_opy_)
  os.environ[bstack11l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩച")] = bstack11ll1l1ll_opy_
  bstack11l11111l_opy_ = bstack11ll1l1ll_opy_
  global bstack1111l1ll1_opy_
  global bstack1ll1lllll_opy_
  if bstack1l1lll11ll_opy_:
    try:
      os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫഛ")] = bstack11ll1l1ll_opy_
      bstack1l11l111_opy_(bstack1ll111111l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11lll1l11_opy_.format(str(e)))
  global bstack11ll1ll11l_opy_
  global bstack111l1l1l1_opy_
  global bstack1l1l11l1ll_opy_
  global bstack11l11llll_opy_
  global bstack111ll1l11_opy_
  global bstack1ll11111_opy_
  global bstack1lll11ll11_opy_
  global bstack11ll11ll_opy_
  global bstack1l1lll1ll1_opy_
  global bstack1l111111ll_opy_
  global bstack111llll1_opy_
  global bstack1llll11ll1_opy_
  global bstack1l1ll111l1_opy_
  global bstack11lllll11l_opy_
  global bstack1l11l11ll1_opy_
  global bstack11ll11l1l_opy_
  global bstack1llll1111l_opy_
  global bstack1l1l11l11_opy_
  global bstack1l1l1l11l_opy_
  global bstack11lll1l1ll_opy_
  global bstack1lll111l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll1ll11l_opy_ = webdriver.Remote.__init__
    bstack111l1l1l1_opy_ = WebDriver.quit
    bstack1llll11ll1_opy_ = WebDriver.close
    bstack1l11l11ll1_opy_ = WebDriver.get
    bstack1lll111l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1111l1ll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l1l11ll_opy_
    bstack1ll1lllll_opy_ = bstack1l1l11ll_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l11l1ll1_opy_
    from QWeb.keywords import browser
    bstack1l11l1ll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l11l11l1l_opy_(CONFIG) and bstack1l11111lll_opy_():
    if bstack1111ll1l_opy_() < version.parse(bstack1lll11llll_opy_):
      logger.error(bstack1ll11111l1_opy_.format(bstack1111ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11ll11l1l_opy_ = RemoteConnection._1lll11111l_opy_
      except Exception as e:
        logger.error(bstack11111111_opy_.format(str(e)))
  if not CONFIG.get(bstack11l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬജ"), False) and not bstack1l1lll11ll_opy_:
    logger.info(bstack1l1ll11l1l_opy_)
  if bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨഝ") in CONFIG and str(CONFIG[bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩഞ")]).lower() != bstack11l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬട"):
    bstack1ll1lll11_opy_()
  elif bstack11ll1l1ll_opy_ != bstack11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഠ") or (bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഡ") and not bstack1l1lll11ll_opy_):
    bstack1l111ll1l_opy_()
  if (bstack11ll1l1ll_opy_ in [bstack11l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨഢ"), bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩണ"), bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬത")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack111lll1l_opy_
        bstack1ll11111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll1l1l1l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack111ll1l11_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11llll11l1_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll1l1l1l1_opy_)
    if bstack11ll1l1ll_opy_ != bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ഥ"):
      bstack1l1ll1llll_opy_()
    bstack1l1l11l1ll_opy_ = Output.start_test
    bstack11l11llll_opy_ = Output.end_test
    bstack1lll11ll11_opy_ = TestStatus.__init__
    bstack1l1lll1ll1_opy_ = pabot._run
    bstack1l111111ll_opy_ = QueueItem.__init__
    bstack111llll1_opy_ = pabot._create_command_for_execution
    bstack1l1l1l11l_opy_ = pabot._report_results
  if bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ദ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1l1l111l_opy_)
    bstack1l1ll111l1_opy_ = Runner.run_hook
    bstack11lllll11l_opy_ = Step.run
  if bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧധ"):
    try:
      from _pytest.config import Config
      bstack1llll1111l_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1l11l11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l1lllll_opy_)
    try:
      from pytest_bdd import reporting
      bstack11lll1l1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩന"))
  try:
    framework_name = bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨഩ") if bstack11ll1l1ll_opy_ in [bstack11l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩപ"), bstack11l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪഫ"), bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ബ")] else bstack1111111l1_opy_(bstack11ll1l1ll_opy_)
    bstack1ll11l1l_opy_ = {
      bstack11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧഭ"): bstack11l11_opy_ (u"ࠧࡼ࠲ࢀ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭മ").format(framework_name) if bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨയ") and bstack1111llll_opy_() else framework_name,
      bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ര"): bstack1llll11111_opy_(framework_name),
      bstack11l11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨറ"): __version__,
      bstack11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬല"): bstack11ll1l1ll_opy_
    }
    if bstack11ll1l1ll_opy_ in bstack1ll1l11l_opy_:
      if bstack11111ll11_opy_ and bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬള") in CONFIG and CONFIG[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ഴ")] == True:
        if bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧവ") in CONFIG:
          os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩശ")] = os.getenv(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪഷ"), json.dumps(CONFIG[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪസ")]))
          CONFIG[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫഹ")].pop(bstack11l11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪഺ"), None)
          CONFIG[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ഻࠭")].pop(bstack11l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩ഼ࠬ"), None)
        bstack1ll11l1l_opy_[bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨഽ")] = {
          bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧാ"): bstack11l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬി"),
          bstack11l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬീ"): str(bstack1111ll1l_opy_())
        }
    if bstack11ll1l1ll_opy_ not in [bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ു")]:
      bstack1lll1l11l1_opy_ = bstack1l11ll1l_opy_.launch(CONFIG, bstack1ll11l1l_opy_)
  except Exception as e:
    logger.debug(bstack11l1111ll_opy_.format(bstack11l11_opy_ (u"࠭ࡔࡦࡵࡷࡌࡺࡨࠧൂ"), str(e)))
  if bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧൃ"):
    bstack1l11ll1lll_opy_ = True
    if bstack1l1lll11ll_opy_ and bstack111l111l1_opy_:
      bstack111lll1l1_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬൄ"), {}).get(bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൅"))
      bstack111l11ll1_opy_(bstack1l1l1l11l1_opy_)
    elif bstack1l1lll11ll_opy_:
      bstack111lll1l1_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧെ"), {}).get(bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭േ"))
      global bstack1llll111_opy_
      try:
        if bstack11l1l1lll_opy_(bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨൈ")]) and multiprocessing.current_process().name == bstack11l11_opy_ (u"࠭࠰ࠨ൉"):
          bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪൊ")].remove(bstack11l11_opy_ (u"ࠨ࠯ࡰࠫോ"))
          bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬൌ")].remove(bstack11l11_opy_ (u"ࠪࡴࡩࡨ്ࠧ"))
          bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧൎ")] = bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൏")][0]
          with open(bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ൐")], bstack11l11_opy_ (u"ࠧࡳࠩ൑")) as f:
            bstack11ll1l111_opy_ = f.read()
          bstack1ll1111ll1_opy_ = bstack11l11_opy_ (u"ࠣࠤࠥࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡦ࡮ࠤ࡮ࡳࡰࡰࡴࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫࠻ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࠬࢀࢃࠩ࠼ࠢࡩࡶࡴࡳࠠࡱࡦࡥࠤ࡮ࡳࡰࡰࡴࡷࠤࡕࡪࡢ࠼ࠢࡲ࡫ࡤࡪࡢࠡ࠿ࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡦࡨࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰ࠮ࡳࡦ࡮ࡩ࠰ࠥࡧࡲࡨ࠮ࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࠽ࠡ࠲ࠬ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡷࡿ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࠥࡃࠠࡴࡶࡵࠬ࡮ࡴࡴࠩࡣࡵ࡫࠮࠱࠱࠱ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧࡻࡧࡪࡶࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡦࡹࠠࡦ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࡯ࡨࡡࡧࡦ࠭ࡹࡥ࡭ࡨ࠯ࡥࡷ࡭ࠬࡵࡧࡰࡴࡴࡸࡡࡳࡻࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬ࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨࠨࠪ࠰ࡶࡩࡹࡥࡴࡳࡣࡦࡩ࠭࠯࡜࡯ࠤࠥࠦ൒").format(str(bstack1l1lll11ll_opy_))
          bstack11l111l11_opy_ = bstack1ll1111ll1_opy_ + bstack11ll1l111_opy_
          bstack1lll1ll1ll_opy_ = bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ൓")] + bstack11l11_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡹ࡫࡭ࡱ࠰ࡳࡽࠬൔ")
          with open(bstack1lll1ll1ll_opy_, bstack11l11_opy_ (u"ࠫࡼ࠭ൕ")):
            pass
          with open(bstack1lll1ll1ll_opy_, bstack11l11_opy_ (u"ࠧࡽࠫࠣൖ")) as f:
            f.write(bstack11l111l11_opy_)
          import subprocess
          bstack11lll111l_opy_ = subprocess.run([bstack11l11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨൗ"), bstack1lll1ll1ll_opy_])
          if os.path.exists(bstack1lll1ll1ll_opy_):
            os.unlink(bstack1lll1ll1ll_opy_)
          os._exit(bstack11lll111l_opy_.returncode)
        else:
          if bstack11l1l1lll_opy_(bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൘")]):
            bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ൙")].remove(bstack11l11_opy_ (u"ࠩ࠰ࡱࠬ൚"))
            bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭൛")].remove(bstack11l11_opy_ (u"ࠫࡵࡪࡢࠨ൜"))
            bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൝")] = bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ൞")][0]
          bstack111l11ll1_opy_(bstack1l1l1l11l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪൟ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11l11_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪൠ")] = bstack11l11_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫൡ")
          mod_globals[bstack11l11_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬൢ")] = os.path.abspath(bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧൣ")])
          exec(open(bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൤")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l11_opy_ (u"࠭ࡃࡢࡷࡪ࡬ࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂ࠭൥").format(str(e)))
          for driver in bstack1llll111_opy_:
            bstack111l1llll_opy_.append({
              bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ൦"): bstack1l1lll11ll_opy_[bstack11l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ൧")],
              bstack11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ൨"): str(e),
              bstack11l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ൩"): multiprocessing.current_process().name
            })
            bstack1ll1ll1l11_opy_(driver, bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ൪"), bstack11l11_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ൫") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1llll111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l1l1l1_opy_, CONFIG, logger)
      bstack111lll11_opy_()
      bstack1lll11l1ll_opy_()
      bstack11lll11ll1_opy_ = {
        bstack11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ൬"): args[0],
        bstack11l11_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ൭"): CONFIG,
        bstack11l11_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ൮"): bstack1ll1111lll_opy_,
        bstack11l11_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ൯"): bstack11l1l1l1_opy_
      }
      percy.bstack1ll1ll1111_opy_()
      if bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭൰") in CONFIG:
        bstack1ll11l1ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1ll11l11_opy_ = manager.list()
        if bstack11l1l1lll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ൱")]):
            if index == 0:
              bstack11lll11ll1_opy_[bstack11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൲")] = args
            bstack1ll11l1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11lll11ll1_opy_, bstack1l1ll11l11_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ൳")]):
            bstack1ll11l1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11lll11ll1_opy_, bstack1l1ll11l11_opy_)))
        for t in bstack1ll11l1ll_opy_:
          t.start()
        for t in bstack1ll11l1ll_opy_:
          t.join()
        bstack1l1ll11l_opy_ = list(bstack1l1ll11l11_opy_)
      else:
        if bstack11l1l1lll_opy_(args):
          bstack11lll11ll1_opy_[bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൴")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11lll11ll1_opy_,))
          test.start()
          test.join()
        else:
          bstack111l11ll1_opy_(bstack1l1l1l11l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l11_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪ൵")] = bstack11l11_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫ൶")
          mod_globals[bstack11l11_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬ൷")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ൸") or bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ൹"):
    percy.init(bstack11l1l1l1_opy_, CONFIG, logger)
    percy.bstack1ll1ll1111_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll1l1l1l1_opy_)
    bstack111lll11_opy_()
    bstack111l11ll1_opy_(bstack111l1l1ll_opy_)
    if bstack11111ll11_opy_:
      bstack1l11lll11l_opy_(bstack111l1l1ll_opy_, args)
      if bstack11l11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫൺ") in args:
        i = args.index(bstack11l11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬൻ"))
        args.pop(i)
        args.pop(i)
      if bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫർ") not in CONFIG:
        CONFIG[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬൽ")] = [{}]
        bstack111111l1l_opy_ = 1
      if bstack11ll111l_opy_ == 0:
        bstack11ll111l_opy_ = 1
      args.insert(0, str(bstack11ll111l_opy_))
      args.insert(0, str(bstack11l11_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨൾ")))
    if bstack1l11ll1l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1llll111ll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1lll11l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11l11_opy_ (u"ࠦࡗࡕࡂࡐࡖࡢࡓࡕ࡚ࡉࡐࡐࡖࠦൿ"),
        ).parse_args(bstack1llll111ll_opy_)
        bstack11ll1ll1l1_opy_ = args.index(bstack1llll111ll_opy_[0]) if len(bstack1llll111ll_opy_) > 0 else len(args)
        args.insert(bstack11ll1ll1l1_opy_, str(bstack11l11_opy_ (u"ࠬ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠩ඀")))
        args.insert(bstack11ll1ll1l1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡲࡰࡤࡲࡸࡤࡲࡩࡴࡶࡨࡲࡪࡸ࠮ࡱࡻࠪඁ"))))
        if bstack1ll1l1l11_opy_(os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬං"))) and str(os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬඃ"), bstack11l11_opy_ (u"ࠩࡱࡹࡱࡲࠧ඄"))) != bstack11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨඅ"):
          for bstack11111l11_opy_ in bstack1lll11l1_opy_:
            args.remove(bstack11111l11_opy_)
          bstack11l1l11ll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨආ")).split(bstack11l11_opy_ (u"ࠬ࠲ࠧඇ"))
          for bstack1ll111lll_opy_ in bstack11l1l11ll_opy_:
            args.append(bstack1ll111lll_opy_)
      except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡺࡴࡢࡥ࡫࡭ࡳ࡭ࠠ࡭࡫ࡶࡸࡪࡴࡥࡳࠢࡩࡳࡷࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࠤඈ").format(e))
    pabot.main(args)
  elif bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨඉ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll1l1l1l1_opy_)
    for a in args:
      if bstack11l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧඊ") in a:
        bstack11ll11l111_opy_ = int(a.split(bstack11l11_opy_ (u"ࠩ࠽ࠫඋ"))[1])
      if bstack11l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧඌ") in a:
        bstack111lll1l1_opy_ = str(a.split(bstack11l11_opy_ (u"ࠫ࠿࠭ඍ"))[1])
      if bstack11l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬඎ") in a:
        bstack1l1111ll1l_opy_ = str(a.split(bstack11l11_opy_ (u"࠭࠺ࠨඏ"))[1])
    bstack1ll1lll111_opy_ = None
    if bstack11l11_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ඐ") in args:
      i = args.index(bstack11l11_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧඑ"))
      args.pop(i)
      bstack1ll1lll111_opy_ = args.pop(i)
    if bstack1ll1lll111_opy_ is not None:
      global bstack11llll11ll_opy_
      bstack11llll11ll_opy_ = bstack1ll1lll111_opy_
    bstack111l11ll1_opy_(bstack111l1l1ll_opy_)
    run_cli(args)
    if bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ඒ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll1ll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111l1llll_opy_.append(bstack1ll1ll1ll_opy_)
  elif bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඓ"):
    percy.init(bstack11l1l1l1_opy_, CONFIG, logger)
    percy.bstack1ll1ll1111_opy_()
    bstack1ll111l1l_opy_ = bstack11l11ll1l_opy_(args, logger, CONFIG, bstack11111ll11_opy_)
    bstack1ll111l1l_opy_.bstack1ll11ll1_opy_()
    bstack111lll11_opy_()
    bstack1l11l1l111_opy_ = True
    bstack1llll1ll1_opy_ = bstack1ll111l1l_opy_.bstack1l111l1lll_opy_()
    bstack1ll111l1l_opy_.bstack11lll11ll1_opy_(bstack1l1lll1l11_opy_)
    bstack1l11ll111_opy_ = bstack1ll111l1l_opy_.bstack1ll1111l1l_opy_(bstack1111lll1_opy_, {
      bstack11l11_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬඔ"): bstack1ll1111lll_opy_,
      bstack11l11_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧඕ"): bstack11l1l1l1_opy_,
      bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩඖ"): bstack11111ll11_opy_
    })
    try:
      bstack1l1111ll1_opy_, bstack111l111ll_opy_ = map(list, zip(*bstack1l11ll111_opy_))
      bstack11ll111ll_opy_ = bstack1l1111ll1_opy_[0]
      for status_code in bstack111l111ll_opy_:
        if status_code != 0:
          bstack1llll1llll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡧࡵࡶࡴࡸࡳࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠱ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠻ࠢࡾࢁࠧ඗").format(str(e)))
  elif bstack11ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ඘"):
    try:
      from behave.__main__ import main as bstack1lll11l111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1l1l111l_opy_)
    bstack111lll11_opy_()
    bstack1l11l1l111_opy_ = True
    bstack1llllllll1_opy_ = 1
    if bstack11l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ඙") in CONFIG:
      bstack1llllllll1_opy_ = CONFIG[bstack11l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪක")]
    if bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧඛ") in CONFIG:
      bstack1ll1lll1l1_opy_ = int(bstack1llllllll1_opy_) * int(len(CONFIG[bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨග")]))
    else:
      bstack1ll1lll1l1_opy_ = int(bstack1llllllll1_opy_)
    config = Configuration(args)
    bstack1l111lllll_opy_ = config.paths
    if len(bstack1l111lllll_opy_) == 0:
      import glob
      pattern = bstack11l11_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬඝ")
      bstack11ll111l1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11ll111l1l_opy_)
      config = Configuration(args)
      bstack1l111lllll_opy_ = config.paths
    bstack11ll11l11l_opy_ = [os.path.normpath(item) for item in bstack1l111lllll_opy_]
    bstack1l1llll111_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1111111l_opy_ = [item for item in bstack1l1llll111_opy_ if item not in bstack11ll11l11l_opy_]
    import platform as pf
    if pf.system().lower() == bstack11l11_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨඞ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11ll11l11l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1llllll111_opy_)))
                    for bstack1llllll111_opy_ in bstack11ll11l11l_opy_]
    bstack1ll1l11l11_opy_ = []
    for spec in bstack11ll11l11l_opy_:
      bstack1ll1l11ll1_opy_ = []
      bstack1ll1l11ll1_opy_ += bstack1l1111111l_opy_
      bstack1ll1l11ll1_opy_.append(spec)
      bstack1ll1l11l11_opy_.append(bstack1ll1l11ll1_opy_)
    execution_items = []
    for bstack1ll1l11ll1_opy_ in bstack1ll1l11l11_opy_:
      if bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫඟ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬච")]):
          item = {}
          item[bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࠧඡ")] = bstack11l11_opy_ (u"ࠫࠥ࠭ජ").join(bstack1ll1l11ll1_opy_)
          item[bstack11l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫඣ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11l11_opy_ (u"࠭ࡡࡳࡩࠪඤ")] = bstack11l11_opy_ (u"ࠧࠡࠩඥ").join(bstack1ll1l11ll1_opy_)
        item[bstack11l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧඦ")] = 0
        execution_items.append(item)
    bstack1l1l11111l_opy_ = bstack1ll11l1l1_opy_(execution_items, bstack1ll1lll1l1_opy_)
    for execution_item in bstack1l1l11111l_opy_:
      bstack1ll11l1ll_opy_ = []
      for item in execution_item:
        bstack1ll11l1ll_opy_.append(bstack11ll1ll111_opy_(name=str(item[bstack11l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨට")]),
                                             target=bstack1l11ll1l1l_opy_,
                                             args=(item[bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࠧඨ")],)))
      for t in bstack1ll11l1ll_opy_:
        t.start()
      for t in bstack1ll11l1ll_opy_:
        t.join()
  else:
    bstack111111ll_opy_(bstack11111l1l_opy_)
  if not bstack1l1lll11ll_opy_:
    bstack11l111ll_opy_()
    if(bstack11ll1l1ll_opy_ in [bstack11l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫඩ"), bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬඪ")]):
      bstack1llllllll_opy_()
  bstack11llll1ll1_opy_.bstack11llll1111_opy_()
def browserstack_initialize(bstack11l1l1111_opy_=None):
  run_on_browserstack(bstack11l1l1111_opy_, None, True)
@measure(event_name=EVENTS.bstack11lll1111l_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack11l111ll_opy_():
  global CONFIG
  global bstack11l11111l_opy_
  global bstack1llll1llll_opy_
  global bstack1ll11lll1l_opy_
  global bstack1111ll1l1_opy_
  bstack1l11ll1l_opy_.stop()
  bstack1l111l1l_opy_.bstack1ll1l1ll1l_opy_()
  if bstack11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪණ") in CONFIG and str(CONFIG[bstack11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫඬ")]).lower() != bstack11l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧත"):
    bstack1ll1111l1_opy_, bstack111lll11l_opy_ = bstack11lll111l1_opy_()
  else:
    bstack1ll1111l1_opy_, bstack111lll11l_opy_ = get_build_link()
  bstack1lll1l1l1_opy_(bstack1ll1111l1_opy_)
  if bstack1ll1111l1_opy_ is not None and bstack1ll11llll1_opy_() != -1:
    sessions = bstack1ll1l111l1_opy_(bstack1ll1111l1_opy_)
    bstack1ll111lll1_opy_(sessions, bstack111lll11l_opy_)
  if bstack11l11111l_opy_ == bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩථ") and bstack1llll1llll_opy_ != 0:
    sys.exit(bstack1llll1llll_opy_)
  if bstack11l11111l_opy_ == bstack11l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪද") and bstack1ll11lll1l_opy_ != 0:
    sys.exit(bstack1ll11lll1l_opy_)
def bstack1lll1l1l1_opy_(new_id):
    global bstack1111l11ll_opy_
    bstack1111l11ll_opy_ = new_id
def bstack1111111l1_opy_(bstack1llllll1l_opy_):
  if bstack1llllll1l_opy_:
    return bstack1llllll1l_opy_.capitalize()
  else:
    return bstack11l11_opy_ (u"ࠫࠬධ")
@measure(event_name=EVENTS.bstack11l1l111_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1l11llllll_opy_(bstack11l11111_opy_):
  if bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪන") in bstack11l11111_opy_ and bstack11l11111_opy_[bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ඲")] != bstack11l11_opy_ (u"ࠧࠨඳ"):
    return bstack11l11111_opy_[bstack11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ප")]
  else:
    bstack111lll111_opy_ = bstack11l11_opy_ (u"ࠤࠥඵ")
    if bstack11l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪබ") in bstack11l11111_opy_ and bstack11l11111_opy_[bstack11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫභ")] != None:
      bstack111lll111_opy_ += bstack11l11111_opy_[bstack11l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬම")] + bstack11l11_opy_ (u"ࠨࠬࠡࠤඹ")
      if bstack11l11111_opy_[bstack11l11_opy_ (u"ࠧࡰࡵࠪය")] == bstack11l11_opy_ (u"ࠣ࡫ࡲࡷࠧර"):
        bstack111lll111_opy_ += bstack11l11_opy_ (u"ࠤ࡬ࡓࡘࠦࠢ඼")
      bstack111lll111_opy_ += (bstack11l11111_opy_[bstack11l11_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧල")] or bstack11l11_opy_ (u"ࠫࠬ඾"))
      return bstack111lll111_opy_
    else:
      bstack111lll111_opy_ += bstack1111111l1_opy_(bstack11l11111_opy_[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭඿")]) + bstack11l11_opy_ (u"ࠨࠠࠣව") + (
              bstack11l11111_opy_[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩශ")] or bstack11l11_opy_ (u"ࠨࠩෂ")) + bstack11l11_opy_ (u"ࠤ࠯ࠤࠧස")
      if bstack11l11111_opy_[bstack11l11_opy_ (u"ࠪࡳࡸ࠭හ")] == bstack11l11_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧළ"):
        bstack111lll111_opy_ += bstack11l11_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥෆ")
      bstack111lll111_opy_ += bstack11l11111_opy_[bstack11l11_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ෇")] or bstack11l11_opy_ (u"ࠧࠨ෈")
      return bstack111lll111_opy_
@measure(event_name=EVENTS.bstack1lllllllll_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack11ll111l1_opy_(bstack1111l1l1l_opy_):
  if bstack1111l1l1l_opy_ == bstack11l11_opy_ (u"ࠣࡦࡲࡲࡪࠨ෉"):
    return bstack11l11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂ්ࠬ")
  elif bstack1111l1l1l_opy_ == bstack11l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ෋"):
    return bstack11l11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ෌")
  elif bstack1111l1l1l_opy_ == bstack11l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ෍"):
    return bstack11l11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭෎")
  elif bstack1111l1l1l_opy_ == bstack11l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨා"):
    return bstack11l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪැ")
  elif bstack1111l1l1l_opy_ == bstack11l11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥෑ"):
    return bstack11l11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨි")
  elif bstack1111l1l1l_opy_ == bstack11l11_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧී"):
    return bstack11l11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ු")
  else:
    return bstack11l11_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪ෕") + bstack1111111l1_opy_(
      bstack1111l1l1l_opy_) + bstack11l11_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ූ")
def bstack11l1l1l11_opy_(session):
  return bstack11l11_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨ෗").format(
    session[bstack11l11_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ෘ")], bstack1l11llllll_opy_(session), bstack11ll111l1_opy_(session[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩෙ")]),
    bstack11ll111l1_opy_(session[bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫේ")]),
    bstack1111111l1_opy_(session[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ෛ")] or session[bstack11l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ො")] or bstack11l11_opy_ (u"ࠧࠨෝ")) + bstack11l11_opy_ (u"ࠣࠢࠥෞ") + (session[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫෟ")] or bstack11l11_opy_ (u"ࠪࠫ෠")),
    session[bstack11l11_opy_ (u"ࠫࡴࡹࠧ෡")] + bstack11l11_opy_ (u"ࠧࠦࠢ෢") + session[bstack11l11_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ෣")], session[bstack11l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ෤")] or bstack11l11_opy_ (u"ࠨࠩ෥"),
    session[bstack11l11_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭෦")] if session[bstack11l11_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧ෧")] else bstack11l11_opy_ (u"ࠫࠬ෨"))
@measure(event_name=EVENTS.bstack1ll1ll111_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def bstack1ll111lll1_opy_(sessions, bstack111lll11l_opy_):
  try:
    bstack11l1lll11_opy_ = bstack11l11_opy_ (u"ࠧࠨ෩")
    if not os.path.exists(bstack11l11lll_opy_):
      os.mkdir(bstack11l11lll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l11_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ෪")), bstack11l11_opy_ (u"ࠧࡳࠩ෫")) as f:
      bstack11l1lll11_opy_ = f.read()
    bstack11l1lll11_opy_ = bstack11l1lll11_opy_.replace(bstack11l11_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬ෬"), str(len(sessions)))
    bstack11l1lll11_opy_ = bstack11l1lll11_opy_.replace(bstack11l11_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩ෭"), bstack111lll11l_opy_)
    bstack11l1lll11_opy_ = bstack11l1lll11_opy_.replace(bstack11l11_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫ෮"),
                                              sessions[0].get(bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨ෯")) if sessions[0] else bstack11l11_opy_ (u"ࠬ࠭෰"))
    with open(os.path.join(bstack11l11lll_opy_, bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪ෱")), bstack11l11_opy_ (u"ࠧࡸࠩෲ")) as stream:
      stream.write(bstack11l1lll11_opy_.split(bstack11l11_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬෳ"))[0])
      for session in sessions:
        stream.write(bstack11l1l1l11_opy_(session))
      stream.write(bstack11l1lll11_opy_.split(bstack11l11_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭෴"))[1])
    logger.info(bstack11l11_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭෵").format(bstack11l11lll_opy_));
  except Exception as e:
    logger.debug(bstack11l1l11l_opy_.format(str(e)))
def bstack1ll1l111l1_opy_(bstack1ll1111l1_opy_):
  global CONFIG
  try:
    host = bstack11l11_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧ෶") if bstack11l11_opy_ (u"ࠬࡧࡰࡱࠩ෷") in CONFIG else bstack11l11_opy_ (u"࠭ࡡࡱ࡫ࠪ෸")
    user = CONFIG[bstack11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ෹")]
    key = CONFIG[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ෺")]
    bstack1l1l1ll1l1_opy_ = bstack11l11_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ෻") if bstack11l11_opy_ (u"ࠪࡥࡵࡶࠧ෼") in CONFIG else (bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ෽") if CONFIG.get(bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ෾")) else bstack11l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ෿"))
    url = bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬ฀").format(user, key, host, bstack1l1l1ll1l1_opy_,
                                                                                bstack1ll1111l1_opy_)
    headers = {
      bstack11l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧก"): bstack11l11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬข"),
    }
    proxies = bstack1ll1ll1l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨฃ")], response.json()))
  except Exception as e:
    logger.debug(bstack1lll1l1l1l_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1l11lll111_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def get_build_link():
  global CONFIG
  global bstack1111l11ll_opy_
  try:
    if bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧค") in CONFIG:
      host = bstack11l11_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨฅ") if bstack11l11_opy_ (u"࠭ࡡࡱࡲࠪฆ") in CONFIG else bstack11l11_opy_ (u"ࠧࡢࡲ࡬ࠫง")
      user = CONFIG[bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪจ")]
      key = CONFIG[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬฉ")]
      bstack1l1l1ll1l1_opy_ = bstack11l11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩช") if bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨซ") in CONFIG else bstack11l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧฌ")
      url = bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭ญ").format(user, key, host, bstack1l1l1ll1l1_opy_)
      headers = {
        bstack11l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ฎ"): bstack11l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫฏ"),
      }
      if bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫฐ") in CONFIG:
        params = {bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨฑ"): CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧฒ")], bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨณ"): CONFIG[bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨด")]}
      else:
        params = {bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬต"): CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫถ")]}
      proxies = bstack1ll1ll1l1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11ll1lll1l_opy_ = response.json()[0][bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬท")]
        if bstack11ll1lll1l_opy_:
          bstack111lll11l_opy_ = bstack11ll1lll1l_opy_[bstack11l11_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧธ")].split(bstack11l11_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪน"))[0] + bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭บ") + bstack11ll1lll1l_opy_[
            bstack11l11_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩป")]
          logger.info(bstack1l1ll1ll_opy_.format(bstack111lll11l_opy_))
          bstack1111l11ll_opy_ = bstack11ll1lll1l_opy_[bstack11l11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪผ")]
          bstack1lll1lll1l_opy_ = CONFIG[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫฝ")]
          if bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫพ") in CONFIG:
            bstack1lll1lll1l_opy_ += bstack11l11_opy_ (u"ࠪࠤࠬฟ") + CONFIG[bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ภ")]
          if bstack1lll1lll1l_opy_ != bstack11ll1lll1l_opy_[bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪม")]:
            logger.debug(bstack11ll1lll_opy_.format(bstack11ll1lll1l_opy_[bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫย")], bstack1lll1lll1l_opy_))
          return [bstack11ll1lll1l_opy_[bstack11l11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪร")], bstack111lll11l_opy_]
    else:
      logger.warn(bstack1l111l1ll_opy_)
  except Exception as e:
    logger.debug(bstack1l1ll1l1l1_opy_.format(str(e)))
  return [None, None]
def bstack1111ll11_opy_(url, bstack11llll1ll_opy_=False):
  global CONFIG
  global bstack11l11l1l_opy_
  if not bstack11l11l1l_opy_:
    hostname = bstack1l111l111l_opy_(url)
    is_private = bstack1llll11l_opy_(hostname)
    if (bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬฤ") in CONFIG and not bstack1ll1l1l11_opy_(CONFIG[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ล")])) and (is_private or bstack11llll1ll_opy_):
      bstack11l11l1l_opy_ = hostname
def bstack1l111l111l_opy_(url):
  return urlparse(url).hostname
def bstack1llll11l_opy_(hostname):
  for bstack1lll111ll1_opy_ in bstack11l11ll1_opy_:
    regex = re.compile(bstack1lll111ll1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1ll11111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack11l1111l_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11ll11l111_opy_
  bstack1ll1lll1l_opy_ = not (bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧฦ"), None) and bstack11l1l11l1_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪว"), None))
  bstack1l1l111ll_opy_ = getattr(driver, bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬศ"), None) != True
  if not bstack1lll11ll_opy_.bstack1l11111111_opy_(CONFIG, bstack11ll11l111_opy_) or (bstack1l1l111ll_opy_ and bstack1ll1lll1l_opy_):
    logger.warning(bstack11l11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤษ"))
    return {}
  try:
    logger.debug(bstack11l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫส"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack11lllll1ll_opy_.bstack1l11lll11_opy_)
    return results
  except Exception:
    logger.error(bstack11l11_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥห"))
    return {}
@measure(event_name=EVENTS.bstack11l111ll1_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11ll11l111_opy_
  bstack1ll1lll1l_opy_ = not (bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ฬ"), None) and bstack11l1l11l1_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩอ"), None))
  bstack1l1l111ll_opy_ = getattr(driver, bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫฮ"), None) != True
  if not bstack1lll11ll_opy_.bstack1l11111111_opy_(CONFIG, bstack11ll11l111_opy_) or (bstack1l1l111ll_opy_ and bstack1ll1lll1l_opy_):
    logger.warning(bstack11l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤฯ"))
    return {}
  try:
    logger.debug(bstack11l11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫะ"))
    logger.debug(perform_scan(driver))
    bstack11lllll111_opy_ = driver.execute_async_script(bstack11lllll1ll_opy_.bstack1lll11l1l_opy_)
    return bstack11lllll111_opy_
  except Exception:
    logger.error(bstack11l11_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣั"))
    return {}
@measure(event_name=EVENTS.bstack1l1l11111_opy_, stage=STAGE.SINGLE, bstack111lll111_opy_=bstack1l1l1ll1_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11ll11l111_opy_
  bstack1ll1lll1l_opy_ = not (bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬา"), None) and bstack11l1l11l1_opy_(
          threading.current_thread(), bstack11l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨำ"), None))
  bstack1l1l111ll_opy_ = getattr(driver, bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪิ"), None) != True
  if not bstack1lll11ll_opy_.bstack1l11111111_opy_(CONFIG, bstack11ll11l111_opy_) or (bstack1l1l111ll_opy_ and bstack1ll1lll1l_opy_):
    logger.warning(bstack11l11_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨี"))
    return {}
  try:
    bstack1l1ll1lll_opy_ = driver.execute_async_script(bstack11lllll1ll_opy_.perform_scan, {bstack11l11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬึ"): kwargs.get(bstack11l11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧื"), None) or bstack11l11_opy_ (u"ࠧࠨุ")})
    return bstack1l1ll1lll_opy_
  except Exception:
    logger.error(bstack11l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ูࠢ"))
    return {}
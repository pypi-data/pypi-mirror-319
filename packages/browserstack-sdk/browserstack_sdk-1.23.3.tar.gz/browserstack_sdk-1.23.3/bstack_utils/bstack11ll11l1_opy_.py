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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111111l1l1_opy_, bstack1l1l1ll11l_opy_, bstack1ll111111l_opy_, bstack1ll1ll111_opy_, \
    bstack1llllll1l11_opy_
from bstack_utils.measure import measure
def bstack11ll11llll_opy_(bstack1ll11l11l1l_opy_):
    for driver in bstack1ll11l11l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1llll_opy_, stage=STAGE.SINGLE)
def bstack1ll11lllll_opy_(driver, status, reason=bstack1l11_opy_ (u"ࠧࠨᛣ")):
    bstack111l11ll1_opy_ = Config.bstack11ll111lll_opy_()
    if bstack111l11ll1_opy_.bstack111ll11l1l_opy_():
        return
    bstack1l1ll111l1_opy_ = bstack11lll11l1_opy_(bstack1l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᛤ"), bstack1l11_opy_ (u"ࠩࠪᛥ"), status, reason, bstack1l11_opy_ (u"ࠪࠫᛦ"), bstack1l11_opy_ (u"ࠫࠬᛧ"))
    driver.execute_script(bstack1l1ll111l1_opy_)
@measure(event_name=EVENTS.bstack1ll1llll_opy_, stage=STAGE.SINGLE)
def bstack1l1l1l111_opy_(page, status, reason=bstack1l11_opy_ (u"ࠬ࠭ᛨ")):
    try:
        if page is None:
            return
        bstack111l11ll1_opy_ = Config.bstack11ll111lll_opy_()
        if bstack111l11ll1_opy_.bstack111ll11l1l_opy_():
            return
        bstack1l1ll111l1_opy_ = bstack11lll11l1_opy_(bstack1l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᛩ"), bstack1l11_opy_ (u"ࠧࠨᛪ"), status, reason, bstack1l11_opy_ (u"ࠨࠩ᛫"), bstack1l11_opy_ (u"ࠩࠪ᛬"))
        page.evaluate(bstack1l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ᛭"), bstack1l1ll111l1_opy_)
    except Exception as e:
        print(bstack1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᛮ"), e)
def bstack11lll11l1_opy_(type, name, status, reason, bstack1l11l111ll_opy_, bstack1l1ll1l1l1_opy_):
    bstack1l1l1llll_opy_ = {
        bstack1l11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᛯ"): type,
        bstack1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᛰ"): {}
    }
    if type == bstack1l11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᛱ"):
        bstack1l1l1llll_opy_[bstack1l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᛲ")][bstack1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᛳ")] = bstack1l11l111ll_opy_
        bstack1l1l1llll_opy_[bstack1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᛴ")][bstack1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩᛵ")] = json.dumps(str(bstack1l1ll1l1l1_opy_))
    if type == bstack1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᛶ"):
        bstack1l1l1llll_opy_[bstack1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᛷ")][bstack1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᛸ")] = name
    if type == bstack1l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ᛹"):
        bstack1l1l1llll_opy_[bstack1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᛺")][bstack1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ᛻")] = status
        if status == bstack1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᛼") and str(reason) != bstack1l11_opy_ (u"ࠧࠨ᛽"):
            bstack1l1l1llll_opy_[bstack1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ᛾")][bstack1l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ᛿")] = json.dumps(str(reason))
    bstack11l1lll1_opy_ = bstack1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᜀ").format(json.dumps(bstack1l1l1llll_opy_))
    return bstack11l1lll1_opy_
def bstack11ll1l1l1_opy_(url, config, logger, bstack1l1l1111ll_opy_=False):
    hostname = bstack1l1l1ll11l_opy_(url)
    is_private = bstack1ll1ll111_opy_(hostname)
    try:
        if is_private or bstack1l1l1111ll_opy_:
            file_path = bstack111111l1l1_opy_(bstack1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᜁ"), bstack1l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᜂ"), logger)
            if os.environ.get(bstack1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᜃ")) and eval(
                    os.environ.get(bstack1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᜄ"))):
                return
            if (bstack1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᜅ") in config and not config[bstack1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᜆ")]):
                os.environ[bstack1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᜇ")] = str(True)
                bstack1ll11l111ll_opy_ = {bstack1l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᜈ"): hostname}
                bstack1llllll1l11_opy_(bstack1l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᜉ"), bstack1l11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᜊ"), bstack1ll11l111ll_opy_, logger)
    except Exception as e:
        pass
def bstack11ll1l11ll_opy_(caps, bstack1ll11l11l11_opy_):
    if bstack1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᜋ") in caps:
        caps[bstack1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᜌ")][bstack1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᜍ")] = True
        if bstack1ll11l11l11_opy_:
            caps[bstack1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᜎ")][bstack1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᜏ")] = bstack1ll11l11l11_opy_
    else:
        caps[bstack1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᜐ")] = True
        if bstack1ll11l11l11_opy_:
            caps[bstack1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᜑ")] = bstack1ll11l11l11_opy_
def bstack1ll11llllll_opy_(bstack11l111llll_opy_):
    bstack1ll11l111l1_opy_ = bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᜒ"), bstack1l11_opy_ (u"࠭ࠧᜓ"))
    if bstack1ll11l111l1_opy_ == bstack1l11_opy_ (u"ࠧࠨ᜔") or bstack1ll11l111l1_opy_ == bstack1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥ᜕ࠩ"):
        threading.current_thread().testStatus = bstack11l111llll_opy_
    else:
        if bstack11l111llll_opy_ == bstack1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᜖"):
            threading.current_thread().testStatus = bstack11l111llll_opy_
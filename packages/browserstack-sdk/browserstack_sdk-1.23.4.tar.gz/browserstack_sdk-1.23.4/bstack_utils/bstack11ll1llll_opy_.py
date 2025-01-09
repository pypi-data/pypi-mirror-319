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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1lllll1lll1_opy_, bstack1l111l111l_opy_, bstack11l1l11l1_opy_, bstack1llll11l_opy_, \
    bstack1llll11111l_opy_
from bstack_utils.measure import measure
def bstack11ll1l111l_opy_(bstack1ll11l11l11_opy_):
    for driver in bstack1ll11l11l11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lllllllll_opy_, stage=STAGE.SINGLE)
def bstack1ll1ll1l11_opy_(driver, status, reason=bstack11l11_opy_ (u"ࠧࠨᛣ")):
    bstack1111ll1l1_opy_ = Config.bstack1llll1lll_opy_()
    if bstack1111ll1l1_opy_.bstack111ll11ll1_opy_():
        return
    bstack1l111llll1_opy_ = bstack1lllllll11_opy_(bstack11l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᛤ"), bstack11l11_opy_ (u"ࠩࠪᛥ"), status, reason, bstack11l11_opy_ (u"ࠪࠫᛦ"), bstack11l11_opy_ (u"ࠫࠬᛧ"))
    driver.execute_script(bstack1l111llll1_opy_)
@measure(event_name=EVENTS.bstack1lllllllll_opy_, stage=STAGE.SINGLE)
def bstack11111lll1_opy_(page, status, reason=bstack11l11_opy_ (u"ࠬ࠭ᛨ")):
    try:
        if page is None:
            return
        bstack1111ll1l1_opy_ = Config.bstack1llll1lll_opy_()
        if bstack1111ll1l1_opy_.bstack111ll11ll1_opy_():
            return
        bstack1l111llll1_opy_ = bstack1lllllll11_opy_(bstack11l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᛩ"), bstack11l11_opy_ (u"ࠧࠨᛪ"), status, reason, bstack11l11_opy_ (u"ࠨࠩ᛫"), bstack11l11_opy_ (u"ࠩࠪ᛬"))
        page.evaluate(bstack11l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ᛭"), bstack1l111llll1_opy_)
    except Exception as e:
        print(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᛮ"), e)
def bstack1lllllll11_opy_(type, name, status, reason, bstack11ll11lll_opy_, bstack1l1111ll11_opy_):
    bstack1111111l_opy_ = {
        bstack11l11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᛯ"): type,
        bstack11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᛰ"): {}
    }
    if type == bstack11l11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᛱ"):
        bstack1111111l_opy_[bstack11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᛲ")][bstack11l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᛳ")] = bstack11ll11lll_opy_
        bstack1111111l_opy_[bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᛴ")][bstack11l11_opy_ (u"ࠫࡩࡧࡴࡢࠩᛵ")] = json.dumps(str(bstack1l1111ll11_opy_))
    if type == bstack11l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᛶ"):
        bstack1111111l_opy_[bstack11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᛷ")][bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᛸ")] = name
    if type == bstack11l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ᛹"):
        bstack1111111l_opy_[bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᛺")][bstack11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ᛻")] = status
        if status == bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᛼") and str(reason) != bstack11l11_opy_ (u"ࠧࠨ᛽"):
            bstack1111111l_opy_[bstack11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ᛾")][bstack11l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ᛿")] = json.dumps(str(reason))
    bstack11llllllll_opy_ = bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᜀ").format(json.dumps(bstack1111111l_opy_))
    return bstack11llllllll_opy_
def bstack1111ll11_opy_(url, config, logger, bstack11llll1ll_opy_=False):
    hostname = bstack1l111l111l_opy_(url)
    is_private = bstack1llll11l_opy_(hostname)
    try:
        if is_private or bstack11llll1ll_opy_:
            file_path = bstack1lllll1lll1_opy_(bstack11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᜁ"), bstack11l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᜂ"), logger)
            if os.environ.get(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᜃ")) and eval(
                    os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᜄ"))):
                return
            if (bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᜅ") in config and not config[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᜆ")]):
                os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᜇ")] = str(True)
                bstack1ll11l111ll_opy_ = {bstack11l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᜈ"): hostname}
                bstack1llll11111l_opy_(bstack11l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᜉ"), bstack11l11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᜊ"), bstack1ll11l111ll_opy_, logger)
    except Exception as e:
        pass
def bstack1l11l111l_opy_(caps, bstack1ll11l111l1_opy_):
    if bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᜋ") in caps:
        caps[bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᜌ")][bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᜍ")] = True
        if bstack1ll11l111l1_opy_:
            caps[bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᜎ")][bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᜏ")] = bstack1ll11l111l1_opy_
    else:
        caps[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᜐ")] = True
        if bstack1ll11l111l1_opy_:
            caps[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᜑ")] = bstack1ll11l111l1_opy_
def bstack1ll11lll111_opy_(bstack111lllllll_opy_):
    bstack1ll11l11l1l_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᜒ"), bstack11l11_opy_ (u"࠭ࠧᜓ"))
    if bstack1ll11l11l1l_opy_ == bstack11l11_opy_ (u"ࠧࠨ᜔") or bstack1ll11l11l1l_opy_ == bstack11l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥ᜕ࠩ"):
        threading.current_thread().testStatus = bstack111lllllll_opy_
    else:
        if bstack111lllllll_opy_ == bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᜖"):
            threading.current_thread().testStatus = bstack111lllllll_opy_
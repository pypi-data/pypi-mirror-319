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
import re
from bstack_utils.bstack11ll11l1_opy_ import bstack1ll11llllll_opy_
def bstack1ll11llll11_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᚮ")):
        return bstack1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᚯ")
    elif fixture_name.startswith(bstack1l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᚰ")):
        return bstack1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᚱ")
    elif fixture_name.startswith(bstack1l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᚲ")):
        return bstack1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᚳ")
    elif fixture_name.startswith(bstack1l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᚴ")):
        return bstack1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᚵ")
def bstack1ll11ll1lll_opy_(fixture_name):
    return bool(re.match(bstack1l11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᚶ"), fixture_name))
def bstack1ll1l1111l1_opy_(fixture_name):
    return bool(re.match(bstack1l11_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᚷ"), fixture_name))
def bstack1ll11lllll1_opy_(fixture_name):
    return bool(re.match(bstack1l11_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᚸ"), fixture_name))
def bstack1ll11ll1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᚹ")):
        return bstack1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᚺ"), bstack1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᚻ")
    elif fixture_name.startswith(bstack1l11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᚼ")):
        return bstack1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᚽ"), bstack1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᚾ")
    elif fixture_name.startswith(bstack1l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᚿ")):
        return bstack1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᛀ"), bstack1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᛁ")
    elif fixture_name.startswith(bstack1l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᛂ")):
        return bstack1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᛃ"), bstack1l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᛄ")
    return None, None
def bstack1ll11lll1ll_opy_(hook_name):
    if hook_name in [bstack1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᛅ"), bstack1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᛆ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll11lll111_opy_(hook_name):
    if hook_name in [bstack1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᛇ"), bstack1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᛈ")]:
        return bstack1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᛉ")
    elif hook_name in [bstack1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᛊ"), bstack1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᛋ")]:
        return bstack1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᛌ")
    elif hook_name in [bstack1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᛍ"), bstack1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᛎ")]:
        return bstack1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᛏ")
    elif hook_name in [bstack1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᛐ"), bstack1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᛑ")]:
        return bstack1l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᛒ")
    return hook_name
def bstack1ll1l1111ll_opy_(node, scenario):
    if hasattr(node, bstack1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᛓ")):
        parts = node.nodeid.rsplit(bstack1l11_opy_ (u"ࠨ࡛ࠣᛔ"))
        params = parts[-1]
        return bstack1l11_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᛕ").format(scenario.name, params)
    return scenario.name
def bstack1ll11lll1l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l11_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᛖ")):
            examples = list(node.callspec.params[bstack1l11_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᛗ")].values())
        return examples
    except:
        return []
def bstack1ll1l111111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll1l11111l_opy_(report):
    try:
        status = bstack1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᛘ")
        if report.passed or (report.failed and hasattr(report, bstack1l11_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᛙ"))):
            status = bstack1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᛚ")
        elif report.skipped:
            status = bstack1l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᛛ")
        bstack1ll11llllll_opy_(status)
    except:
        pass
def bstack11111l111_opy_(status):
    try:
        bstack1ll11lll11l_opy_ = bstack1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᛜ")
        if status == bstack1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᛝ"):
            bstack1ll11lll11l_opy_ = bstack1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᛞ")
        elif status == bstack1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᛟ"):
            bstack1ll11lll11l_opy_ = bstack1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᛠ")
        bstack1ll11llllll_opy_(bstack1ll11lll11l_opy_)
    except:
        pass
def bstack1ll11llll1l_opy_(item=None, report=None, summary=None, extra=None):
    return
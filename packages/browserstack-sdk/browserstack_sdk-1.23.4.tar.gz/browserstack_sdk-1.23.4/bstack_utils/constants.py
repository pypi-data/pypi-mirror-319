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
import re
from enum import Enum
bstack1l11lllll1_opy_ = {
  bstack11l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ႁ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩႂ"),
  bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩႃ"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪႄ"),
  bstack11l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫႅ"): bstack11l11_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ႆ"),
  bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪႇ"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫႈ"),
  bstack11l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪႉ"): bstack11l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧႊ"),
  bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪႋ"): bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧႌ"),
  bstack11l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ႍࠧ"): bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨႎ"),
  bstack11l11_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪႏ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪ႐"),
  bstack11l11_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫ႑"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧ႒"),
  bstack11l11_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭႓"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭႔"),
  bstack11l11_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧ႕"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧ႖"),
  bstack11l11_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫ႗"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫ႘"),
  bstack11l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭႙"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ႚ"),
  bstack11l11_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩႛ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩႜ"),
  bstack11l11_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩႝ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩ႞"),
  bstack11l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨ႟"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨႠ"),
  bstack11l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪႡ"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫႢ"),
  bstack11l11_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩႣ"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩႤ"),
  bstack11l11_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪႥ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪႦ"),
  bstack11l11_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧႧ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧႨ"),
  bstack11l11_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫႩ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫႪ"),
  bstack11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭Ⴋ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭Ⴌ"),
  bstack11l11_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬႭ"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬႮ"),
  bstack11l11_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩႯ"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩႰ"),
  bstack11l11_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫႱ"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫႲ"),
  bstack11l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨႳ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨႴ"),
  bstack11l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫႵ"): bstack11l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨႶ"),
  bstack11l11_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭Ⴗ"): bstack11l11_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨႸ"),
  bstack11l11_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫႹ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬႺ"),
  bstack11l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭Ⴛ"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭Ⴜ"),
  bstack11l11_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩႽ"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩႾ"),
  bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩႿ"): bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬჀ"),
  bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧჁ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧჂ"),
  bstack11l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧჃ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧჄ"),
  bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫჅ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ჆"),
  bstack11l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭Ⴧ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭჈"),
  bstack11l11_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩ჉"): bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡥ࡯ࡣࡥࡰࡪ࡙ࡩ࡮ࠩ჊"),
  bstack11l11_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬ჋"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬ჌"),
  bstack11l11_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨჍ"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨ჎"),
  bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ჏"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨა"),
  bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩბ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩგ")
}
bstack11111ll11l_opy_ = [
  bstack11l11_opy_ (u"ࠩࡲࡷࠬდ"),
  bstack11l11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ე"),
  bstack11l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ვ"),
  bstack11l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪზ"),
  bstack11l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪთ"),
  bstack11l11_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫი"),
  bstack11l11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨკ"),
]
bstack1l11lll1ll_opy_ = {
  bstack11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫლ"): [bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫმ"), bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡐࡄࡑࡊ࠭ნ")],
  bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨო"): bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩპ"),
  bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪჟ"): bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠫრ"),
  bstack11l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧს"): bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠨტ"),
  bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭უ"): bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧფ"),
  bstack11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ქ"): bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡔࡡࡓࡉࡗࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨღ"),
  bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬყ"): bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧშ"),
  bstack11l11_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧჩ"): bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨც"),
  bstack11l11_opy_ (u"ࠬࡧࡰࡱࠩძ"): [bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࡡࡌࡈࠬწ"), bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࠪჭ")],
  bstack11l11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪხ"): bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡒࡏࡈࡎࡈ࡚ࡊࡒࠧჯ"),
  bstack11l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧჰ"): bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧჱ"),
  bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩჲ"): bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠪჳ"),
  bstack11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫჴ"): bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡗࡕࡆࡔ࡙ࡃࡂࡎࡈࠫჵ")
}
bstack111l1l11_opy_ = {
  bstack11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫჶ"): [bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬჷ"), bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬჸ")],
  bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨჹ"): [bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩჺ"), bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ჻")],
  bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫჼ"): bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫჽ"),
  bstack11l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨჾ"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨჿ"),
  bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᄀ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᄁ"),
  bstack11l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᄂ"): [bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫᄃ"), bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᄄ")],
  bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᄅ"): bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᄆ"),
  bstack11l11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᄇ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᄈ"),
  bstack11l11_opy_ (u"ࠧࡢࡲࡳࠫᄉ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫᄊ"),
  bstack11l11_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᄋ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᄌ"),
  bstack11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᄍ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᄎ")
}
bstack111l1lll_opy_ = {
  bstack11l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᄏ"): bstack11l11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᄐ"),
  bstack11l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᄑ"): [bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᄒ"), bstack11l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᄓ")],
  bstack11l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᄔ"): bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᄕ"),
  bstack11l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᄖ"): bstack11l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᄗ"),
  bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᄘ"): [bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᄙ"), bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᄚ")],
  bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᄛ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᄜ"),
  bstack11l11_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪᄝ"): bstack11l11_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬᄞ"),
  bstack11l11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᄟ"): [bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᄠ"), bstack11l11_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᄡ")],
  bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪᄢ"): [bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ᄣ"), bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭ᄤ")]
}
bstack1ll1llllll_opy_ = [
  bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ᄥ"),
  bstack11l11_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫᄦ"),
  bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨᄧ"),
  bstack11l11_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶࠪᄨ"),
  bstack11l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭ᄩ"),
  bstack11l11_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻࠪᄪ"),
  bstack11l11_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩᄫ"),
  bstack11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᄬ"),
  bstack11l11_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᄭ"),
  bstack11l11_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᄮ"),
  bstack11l11_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᄯ"),
  bstack11l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬᄰ"),
]
bstack1l111l1l11_opy_ = [
  bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᄱ"),
  bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪᄲ"),
  bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᄳ"),
  bstack11l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᄴ"),
  bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᄵ"),
  bstack11l11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᄶ"),
  bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᄷ"),
  bstack11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᄸ"),
  bstack11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᄹ"),
  bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬᄺ"),
  bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᄻ"),
  bstack11l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᄼ"),
  bstack11l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡗࡥ࡬࠭ᄽ"),
  bstack11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᄾ"),
  bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᄿ"),
  bstack11l11_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪᅀ"),
  bstack11l11_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠶࠭ᅁ"),
  bstack11l11_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠸ࠧᅂ"),
  bstack11l11_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠳ࠨᅃ"),
  bstack11l11_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠵ࠩᅄ"),
  bstack11l11_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠷ࠪᅅ"),
  bstack11l11_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠹ࠫᅆ"),
  bstack11l11_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠻ࠬᅇ"),
  bstack11l11_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠽࠭ᅈ"),
  bstack11l11_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠿ࠧᅉ"),
  bstack11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᅊ"),
  bstack11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᅋ"),
  bstack11l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᅌ"),
  bstack11l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᅍ"),
  bstack11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᅎ"),
  bstack11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫᅏ")
]
bstack11111l1lll_opy_ = [
  bstack11l11_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ᅐ"),
  bstack11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᅑ"),
  bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᅒ"),
  bstack11l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᅓ"),
  bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫᅔ"),
  bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᅕ"),
  bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩᅖ"),
  bstack11l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᅗ"),
  bstack11l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᅘ"),
  bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᅙ"),
  bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᅚ"),
  bstack11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᅛ"),
  bstack11l11_opy_ (u"࠭࡯ࡴࠩᅜ"),
  bstack11l11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᅝ"),
  bstack11l11_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧᅞ"),
  bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫᅟ"),
  bstack11l11_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪᅠ"),
  bstack11l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ᅡ"),
  bstack11l11_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ᅢ"),
  bstack11l11_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪᅣ"),
  bstack11l11_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬᅤ"),
  bstack11l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬᅥ"),
  bstack11l11_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨᅦ"),
  bstack11l11_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧᅧ"),
  bstack11l11_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬᅨ"),
  bstack11l11_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᅩ"),
  bstack11l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᅪ"),
  bstack11l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨᅫ"),
  bstack11l11_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᅬ"),
  bstack11l11_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ᅭ"),
  bstack11l11_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬᅮ"),
  bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᅯ"),
  bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬᅰ"),
  bstack11l11_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬᅱ"),
  bstack11l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᅲ"),
  bstack11l11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᅳ"),
  bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᅴ"),
  bstack11l11_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪࠫᅵ"),
  bstack11l11_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵࠪᅶ"),
  bstack11l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴࠩᅷ"),
  bstack11l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨᅸ"),
  bstack11l11_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩᅹ"),
  bstack11l11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧᅺ"),
  bstack11l11_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧᅻ"),
  bstack11l11_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨᅼ"),
  bstack11l11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩᅽ"),
  bstack11l11_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪᅾ"),
  bstack11l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᅿ"),
  bstack11l11_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫᆀ"),
  bstack11l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪᆁ"),
  bstack11l11_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪᆂ"),
  bstack11l11_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫᆃ"),
  bstack11l11_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬᆄ"),
  bstack11l11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫᆅ"),
  bstack11l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫᆆ"),
  bstack11l11_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧᆇ"),
  bstack11l11_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪᆈ"),
  bstack11l11_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧᆉ"),
  bstack11l11_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨᆊ"),
  bstack11l11_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬᆋ"),
  bstack11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬᆌ"),
  bstack11l11_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࠧᆍ"),
  bstack11l11_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧᆎ"),
  bstack11l11_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨᆏ"),
  bstack11l11_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨᆐ"),
  bstack11l11_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪᆑ"),
  bstack11l11_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᆒ"),
  bstack11l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨᆓ"),
  bstack11l11_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࠪᆔ"),
  bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ᆕ"),
  bstack11l11_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࠫᆖ"),
  bstack11l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ᆗ"),
  bstack11l11_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪᆘ"),
  bstack11l11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬᆙ"),
  bstack11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᆚ"),
  bstack11l11_opy_ (u"࠭ࡩࡦࠩᆛ"),
  bstack11l11_opy_ (u"ࠧࡦࡦࡪࡩࠬᆜ"),
  bstack11l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᆝ"),
  bstack11l11_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨᆞ"),
  bstack11l11_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬᆟ"),
  bstack11l11_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬᆠ"),
  bstack11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫᆡ"),
  bstack11l11_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩᆢ"),
  bstack11l11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪᆣ"),
  bstack11l11_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬᆤ"),
  bstack11l11_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩᆥ"),
  bstack11l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᆦ"),
  bstack11l11_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ᆧ"),
  bstack11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ᆨ"),
  bstack11l11_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᆩ"),
  bstack11l11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧᆪ"),
  bstack11l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩᆫ"),
  bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᆬ"),
  bstack11l11_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨᆭ"),
  bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᆮ"),
  bstack11l11_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩᆯ"),
  bstack11l11_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬᆰ"),
  bstack11l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫᆱ"),
  bstack11l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫᆲ"),
  bstack11l11_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ᆳ"),
  bstack11l11_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨᆴ"),
  bstack11l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ᆵ"),
  bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᆶ"),
  bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨᆷ"),
  bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᆸ"),
  bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᆹ"),
  bstack11l11_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬᆺ"),
  bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩᆻ"),
  bstack11l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭ᆼ"),
  bstack11l11_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨᆽ")
]
bstack11lll1ll1_opy_ = {
  bstack11l11_opy_ (u"࠭ࡶࠨᆾ"): bstack11l11_opy_ (u"ࠧࡷࠩᆿ"),
  bstack11l11_opy_ (u"ࠨࡨࠪᇀ"): bstack11l11_opy_ (u"ࠩࡩࠫᇁ"),
  bstack11l11_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩᇂ"): bstack11l11_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪᇃ"),
  bstack11l11_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᇄ"): bstack11l11_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬᇅ"),
  bstack11l11_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫᇆ"): bstack11l11_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬᇇ"),
  bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬᇈ"): bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ᇉ"),
  bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧᇊ"): bstack11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨᇋ"),
  bstack11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᇌ"): bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᇍ"),
  bstack11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᇎ"): bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᇏ"),
  bstack11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫᇐ"): bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬᇑ"),
  bstack11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ᇒ"): bstack11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᇓ"),
  bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᇔ"): bstack11l11_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᇕ"),
  bstack11l11_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᇖ"): bstack11l11_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᇗ"),
  bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᇘ"): bstack11l11_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᇙ"),
  bstack11l11_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᇚ"): bstack11l11_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᇛ"),
  bstack11l11_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬᇜ"): bstack11l11_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ᇝ"),
  bstack11l11_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫᇞ"): bstack11l11_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᇟ"),
  bstack11l11_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᇠ"): bstack11l11_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᇡ"),
  bstack11l11_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᇢ"): bstack11l11_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᇣ"),
  bstack11l11_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪᇤ"): bstack11l11_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫᇥ"),
  bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᇦ"): bstack11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᇧ"),
  bstack11l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨᇨ"): bstack11l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࠨᇩ")
}
bstack1111l11l1l_opy_ = bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡪ࡭ࡹ࡮ࡵࡣ࠰ࡦࡳࡲ࠵ࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪ࠱ࡵࡩࡱ࡫ࡡࡴࡧࡶ࠳ࡱࡧࡴࡦࡵࡷ࠳ࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᇪ")
bstack11111ll1l1_opy_ = bstack11l11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠱࡫ࡩࡦࡲࡴࡩࡥ࡫ࡩࡨࡱࠢᇫ")
bstack1lllllll1_opy_ = bstack11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡪࡪࡳ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡸ࡫࡮ࡥࡡࡶࡨࡰࡥࡥࡷࡧࡱࡸࡸࠨᇬ")
bstack1llll111l1_opy_ = bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡽࡤ࠰ࡪࡸࡦࠬᇭ")
bstack1lll111111_opy_ = bstack11l11_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠨᇮ")
bstack1l1l1ll111_opy_ = bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯࡯ࡧࡻࡸࡤ࡮ࡵࡣࡵࠪᇯ")
bstack1111l1111l_opy_ = {
  bstack11l11_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩᇰ"): 50,
  bstack11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᇱ"): 40,
  bstack11l11_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᇲ"): 30,
  bstack11l11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᇳ"): 20,
  bstack11l11_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᇴ"): 10
}
bstack1l1lllll1l_opy_ = bstack1111l1111l_opy_[bstack11l11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᇵ")]
bstack1l1l1l11l1_opy_ = bstack11l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᇶ")
bstack111l1l1ll_opy_ = bstack11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᇷ")
bstack1111l1ll_opy_ = bstack11l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᇸ")
bstack1l11l11l11_opy_ = bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᇹ")
bstack1l1lllll_opy_ = bstack11l11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡦࡴࡤࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡴࡦࡩ࡫ࡢࡩࡨࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡠࠨᇺ")
bstack11111llll1_opy_ = [bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᇻ"), bstack11l11_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᇼ")]
bstack1111l11l11_opy_ = [bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᇽ"), bstack11l11_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᇾ")]
bstack1ll1l1lll_opy_ = re.compile(bstack11l11_opy_ (u"ࠨࡠ࡞ࡠࡡࡽ࠭࡞࠭࠽࠲࠯ࠪࠧᇿ"))
bstack1l11ll1l1_opy_ = [
  bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪሀ"),
  bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬሁ"),
  bstack11l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨሂ"),
  bstack11l11_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩሃ"),
  bstack11l11_opy_ (u"࠭ࡡࡱࡲࠪሄ"),
  bstack11l11_opy_ (u"ࠧࡶࡦ࡬ࡨࠬህ"),
  bstack11l11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪሆ"),
  bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩሇ"),
  bstack11l11_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨለ"),
  bstack11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩሉ"),
  bstack11l11_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭ሊ"), bstack11l11_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩላ"),
  bstack11l11_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪሌ"),
  bstack11l11_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧል"),
  bstack11l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ሎ"),
  bstack11l11_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭ሏ"),
  bstack11l11_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬሐ"),
  bstack11l11_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪሑ"), bstack11l11_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪሒ"), bstack11l11_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩሓ"), bstack11l11_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩሔ"), bstack11l11_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫሕ"),
  bstack11l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨሖ"),
  bstack11l11_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨሗ"),
  bstack11l11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧመ"), bstack11l11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪሙ"),
  bstack11l11_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬሚ"),
  bstack11l11_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩማ"),
  bstack11l11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨሜ"),
  bstack11l11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫም"),
  bstack11l11_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩሞ"),
  bstack11l11_opy_ (u"ࠬࡧࡶࡥࠩሟ"), bstack11l11_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩሠ"), bstack11l11_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩሡ"), bstack11l11_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩሢ"),
  bstack11l11_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧሣ"), bstack11l11_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩሤ"), bstack11l11_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧሥ"),
  bstack11l11_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧሦ"), bstack11l11_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫሧ"),
  bstack11l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩረ"), bstack11l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫሩ"), bstack11l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧሪ"), bstack11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬራ"), bstack11l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨሬ"),
  bstack11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨር"), bstack11l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪሮ"),
  bstack11l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩሯ"),
  bstack11l11_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ሰ"),
  bstack11l11_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨሱ"), bstack11l11_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫሲ"), bstack11l11_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩሳ"), bstack11l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨሴ"),
  bstack11l11_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫስ"),
  bstack11l11_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩሶ"), bstack11l11_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨሷ"),
  bstack11l11_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩሸ"),
  bstack11l11_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬሹ"),
  bstack11l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭ሺ"),
  bstack11l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬሻ"),
  bstack11l11_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧሼ"),
  bstack11l11_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ሽ"),
  bstack11l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩሾ"),
  bstack11l11_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨሿ"),
  bstack11l11_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧቀ"),
  bstack11l11_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨቁ"),
  bstack11l11_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ቂ"),
  bstack11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬቃ"),
  bstack11l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫቄ"),
  bstack11l11_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨቅ"),
  bstack11l11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧቆ"),
  bstack11l11_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧቇ"),
  bstack11l11_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫቈ"),
  bstack11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩ቉"), bstack11l11_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪቊ"), bstack11l11_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪቋ"),
  bstack11l11_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬቌ"),
  bstack11l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ቍ"),
  bstack11l11_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬ቎"),
  bstack11l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭቏"),
  bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩቐ"),
  bstack11l11_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪቑ"),
  bstack11l11_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪቒ"), bstack11l11_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧቓ"), bstack11l11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬቔ"),
  bstack11l11_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪቕ"),
  bstack11l11_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬቖ"),
  bstack11l11_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧ቗"),
  bstack11l11_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ቘ"),
  bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪ቙"), bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧቚ"),
  bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬቛ"), bstack11l11_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧቜ"),
  bstack11l11_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫቝ"),
  bstack11l11_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ቞"),
  bstack11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ቟"), bstack11l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫበ"), bstack11l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬቡ"), bstack11l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩቢ"),
  bstack11l11_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪባ"),
  bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬቤ"),
  bstack11l11_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨብ"),
  bstack11l11_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭ቦ"),
  bstack11l11_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪࠫቧ"),
  bstack11l11_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪቨ"),
  bstack11l11_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪቩ"), bstack11l11_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫቪ"),
  bstack11l11_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧቫ"),
  bstack11l11_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬቬ"),
  bstack11l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧቭ"),
  bstack11l11_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧቮ"),
  bstack11l11_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪቯ"),
  bstack11l11_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬተ"),
  bstack11l11_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫቱ"),
  bstack11l11_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬቲ"),
  bstack11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬታ"),
  bstack11l11_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫቴ"),
  bstack11l11_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬት"),
  bstack11l11_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧቶ"),
  bstack11l11_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨቷ"),
  bstack11l11_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩࠬቸ"),
  bstack11l11_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ቹ"),
  bstack11l11_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨቺ"),
  bstack11l11_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧቻ"),
  bstack11l11_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨቼ"),
  bstack11l11_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬች"),
  bstack11l11_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨቾ"),
  bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭ቿ"),
  bstack11l11_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧኀ"), bstack11l11_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬኁ"),
  bstack11l11_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪኂ"), bstack11l11_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨኃ"),
  bstack11l11_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭ኄ"),
  bstack11l11_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬኅ"),
  bstack11l11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬኆ"),
  bstack11l11_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨኇ"), bstack11l11_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨኈ"),
  bstack11l11_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ኉"),
  bstack11l11_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬኊ"),
  bstack11l11_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨኋ"),
  bstack11l11_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪኌ"),
  bstack11l11_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬኍ"),
  bstack11l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧ኎"),
  bstack11l11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ኏"),
  bstack11l11_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬነ"),
  bstack11l11_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩኑ"),
  bstack11l11_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧኒ"), bstack11l11_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭ና"),
  bstack11l11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪኔ"),
  bstack11l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡎࡪࡌࡰࡥࡤࡸࡴࡸࡁࡶࡶࡲࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠧን")
]
bstack1l11111l1_opy_ = bstack11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡺࡶ࡬ࡰࡣࡧࠫኖ")
bstack1lll1lll_opy_ = [bstack11l11_opy_ (u"࠭࠮ࡢࡲ࡮ࠫኗ"), bstack11l11_opy_ (u"ࠧ࠯ࡣࡤࡦࠬኘ"), bstack11l11_opy_ (u"ࠨ࠰࡬ࡴࡦ࠭ኙ")]
bstack1ll11l11l1_opy_ = [bstack11l11_opy_ (u"ࠩ࡬ࡨࠬኚ"), bstack11l11_opy_ (u"ࠪࡴࡦࡺࡨࠨኛ"), bstack11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧኜ"), bstack11l11_opy_ (u"ࠬࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࠫኝ")]
bstack1lll1l11ll_opy_ = {
  bstack11l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ኞ"): bstack11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬኟ"),
  bstack11l11_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩአ"): bstack11l11_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧኡ"),
  bstack11l11_opy_ (u"ࠪࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨኢ"): bstack11l11_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬኣ"),
  bstack11l11_opy_ (u"ࠬ࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨኤ"): bstack11l11_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬእ"),
  bstack11l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡶ࡬ࡳࡳࡹࠧኦ"): bstack11l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩኧ")
}
bstack1l11llll11_opy_ = [
  bstack11l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧከ"),
  bstack11l11_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨኩ"),
  bstack11l11_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬኪ"),
  bstack11l11_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫካ"),
  bstack11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧኬ"),
]
bstack11lllll1l1_opy_ = bstack1l111l1l11_opy_ + bstack11111l1lll_opy_ + bstack1l11ll1l1_opy_
bstack11l11ll1_opy_ = [
  bstack11l11_opy_ (u"ࠧ࡟࡮ࡲࡧࡦࡲࡨࡰࡵࡷࠨࠬክ"),
  bstack11l11_opy_ (u"ࠨࡠࡥࡷ࠲ࡲ࡯ࡤࡣ࡯࠲ࡨࡵ࡭ࠥࠩኮ"),
  bstack11l11_opy_ (u"ࠩࡡ࠵࠷࠽࠮ࠨኯ"),
  bstack11l11_opy_ (u"ࠪࡢ࠶࠶࠮ࠨኰ"),
  bstack11l11_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠴࡟࠻࠳࠹࡞࠰ࠪ኱"),
  bstack11l11_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠶ࡠ࠶࠭࠺࡟࠱ࠫኲ"),
  bstack11l11_opy_ (u"࠭࡞࠲࠹࠵࠲࠸ࡡ࠰࠮࠳ࡠ࠲ࠬኳ"),
  bstack11l11_opy_ (u"ࠧ࡟࠳࠼࠶࠳࠷࠶࠹࠰ࠪኴ")
]
bstack11111ll111_opy_ = bstack11l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩኵ")
bstack1ll1llll_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡨࡺࡪࡴࡴࠨ኶")
bstack1l111ll111_opy_ = [ bstack11l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ኷") ]
bstack1ll1lll11l_opy_ = [ bstack11l11_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪኸ") ]
bstack1l11ll11_opy_ = [bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩኹ")]
bstack1111llll1_opy_ = [ bstack11l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ኺ") ]
bstack1lll11l11l_opy_ = bstack11l11_opy_ (u"ࠧࡔࡆࡎࡗࡪࡺࡵࡱࠩኻ")
bstack1ll111111l_opy_ = bstack11l11_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠫኼ")
bstack1ll1l1l1ll_opy_ = bstack11l11_opy_ (u"ࠩࡖࡈࡐ࡚ࡥࡴࡶࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱ࠭ኽ")
bstack1lll11llll_opy_ = bstack11l11_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࠩኾ")
bstack1l111l1l1l_opy_ = [
  bstack11l11_opy_ (u"ࠫࡊࡘࡒࡠࡈࡄࡍࡑࡋࡄࠨ኿"),
  bstack11l11_opy_ (u"ࠬࡋࡒࡓࡡࡗࡍࡒࡋࡄࡠࡑࡘࡘࠬዀ"),
  bstack11l11_opy_ (u"࠭ࡅࡓࡔࡢࡆࡑࡕࡃࡌࡇࡇࡣࡇ࡟࡟ࡄࡎࡌࡉࡓ࡚ࠧ዁"),
  bstack11l11_opy_ (u"ࠧࡆࡔࡕࡣࡓࡋࡔࡘࡑࡕࡏࡤࡉࡈࡂࡐࡊࡉࡉ࠭ዂ"),
  bstack11l11_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡈࡘࡤࡔࡏࡕࡡࡆࡓࡓࡔࡅࡄࡖࡈࡈࠬዃ"),
  bstack11l11_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡇࡑࡕࡓࡆࡆࠪዄ"),
  bstack11l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡓࡆࡖࠪዅ"),
  bstack11l11_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡘࡅࡇࡗࡖࡉࡉ࠭዆"),
  bstack11l11_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡁࡃࡑࡕࡘࡊࡊࠧ዇"),
  bstack11l11_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧወ"),
  bstack11l11_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨዉ"),
  bstack11l11_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡉࡏࡘࡄࡐࡎࡊࠧዊ"),
  bstack11l11_opy_ (u"ࠩࡈࡖࡗࡥࡁࡅࡆࡕࡉࡘ࡙࡟ࡖࡐࡕࡉࡆࡉࡈࡂࡄࡏࡉࠬዋ"),
  bstack11l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡗࡑࡒࡊࡒ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫዌ"),
  bstack11l11_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤ࡚ࡉࡎࡇࡇࡣࡔ࡛ࡔࠨው"),
  bstack11l11_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬዎ"),
  bstack11l11_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡔࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡈࡐࡕࡗࡣ࡚ࡔࡒࡆࡃࡆࡌࡆࡈࡌࡆࠩዏ"),
  bstack11l11_opy_ (u"ࠧࡆࡔࡕࡣࡕࡘࡏ࡙࡛ࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧዐ"),
  bstack11l11_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡒࡔ࡚࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࠩዑ"),
  bstack11l11_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡗࡋࡓࡐࡎࡘࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨዒ"),
  bstack11l11_opy_ (u"ࠪࡉࡗࡘ࡟ࡎࡃࡑࡈࡆ࡚ࡏࡓ࡛ࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩዓ"),
]
bstack11l11lll_opy_ = bstack11l11_opy_ (u"ࠫ࠳࠵ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡧࡲࡵ࡫ࡩࡥࡨࡺࡳ࠰ࠩዔ")
bstack1l11l1llll_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠬࢄࠧዕ")), bstack11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ዖ"), bstack11l11_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭዗"))
bstack111l1111l1_opy_ = bstack11l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡰࡪࠩዘ")
bstack111111llll_opy_ = [ bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩዙ"), bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩዚ"), bstack11l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪዛ"), bstack11l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬዜ")]
bstack1ll1l11l_opy_ = [ bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ዝ"), bstack11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ዞ"), bstack11l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧዟ"), bstack11l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩዠ") ]
bstack111lll1l11_opy_ = {
  bstack11l11_opy_ (u"ࠪࡔࡆ࡙ࡓࠨዡ"): bstack11l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫዢ"),
  bstack11l11_opy_ (u"ࠬࡌࡁࡊࡎࠪዣ"): bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ዤ"),
  bstack11l11_opy_ (u"ࠧࡔࡍࡌࡔࠬዥ"): bstack11l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩዦ")
}
bstack1l1ll1l1ll_opy_ = [
  bstack11l11_opy_ (u"ࠤࡪࡩࡹࠨዧ"),
  bstack11l11_opy_ (u"ࠥ࡫ࡴࡈࡡࡤ࡭ࠥየ"),
  bstack11l11_opy_ (u"ࠦ࡬ࡵࡆࡰࡴࡺࡥࡷࡪࠢዩ"),
  bstack11l11_opy_ (u"ࠧࡸࡥࡧࡴࡨࡷ࡭ࠨዪ"),
  bstack11l11_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧያ"),
  bstack11l11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦዬ"),
  bstack11l11_opy_ (u"ࠣࡵࡸࡦࡲ࡯ࡴࡆ࡮ࡨࡱࡪࡴࡴࠣይ"),
  bstack11l11_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨዮ"),
  bstack11l11_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨዯ"),
  bstack11l11_opy_ (u"ࠦࡨࡲࡥࡢࡴࡈࡰࡪࡳࡥ࡯ࡶࠥደ"),
  bstack11l11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࡸࠨዱ"),
  bstack11l11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹࠨዲ"),
  bstack11l11_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡂࡵࡼࡲࡨ࡙ࡣࡳ࡫ࡳࡸࠧዳ"),
  bstack11l11_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢዴ"),
  bstack11l11_opy_ (u"ࠤࡴࡹ࡮ࡺࠢድ"),
  bstack11l11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡘࡴࡻࡣࡩࡃࡦࡸ࡮ࡵ࡮ࠣዶ"),
  bstack11l11_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡒࡻ࡬ࡵ࡫ࡗࡳࡺࡩࡨࠣዷ"),
  bstack11l11_opy_ (u"ࠧࡹࡨࡢ࡭ࡨࠦዸ"),
  bstack11l11_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࡆࡶࡰࠣዹ")
]
bstack11111l11ll_opy_ = [
  bstack11l11_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨዺ"),
  bstack11l11_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧዻ"),
  bstack11l11_opy_ (u"ࠤࡤࡹࡹࡵࠢዼ"),
  bstack11l11_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥዽ"),
  bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨዾ")
]
bstack1l11ll1ll_opy_ = {
  bstack11l11_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦዿ"): [bstack11l11_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧጀ")],
  bstack11l11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦጁ"): [bstack11l11_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧጂ")],
  bstack11l11_opy_ (u"ࠤࡤࡹࡹࡵࠢጃ"): [bstack11l11_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢጄ"), bstack11l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢጅ"), bstack11l11_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤጆ"), bstack11l11_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧጇ")],
  bstack11l11_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢገ"): [bstack11l11_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣጉ")],
  bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦጊ"): [bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧጋ")],
}
bstack1111l111ll_opy_ = {
  bstack11l11_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥጌ"): bstack11l11_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦግ"),
  bstack11l11_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥጎ"): bstack11l11_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦጏ"),
  bstack11l11_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧጐ"): bstack11l11_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦ጑"),
  bstack11l11_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨጒ"): bstack11l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨጓ"),
  bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢጔ"): bstack11l11_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣጕ")
}
bstack111lll1ll1_opy_ = {
  bstack11l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ጖"): bstack11l11_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡔࡧࡷࡹࡵ࠭጗"),
  bstack11l11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬጘ"): bstack11l11_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡗࡩࡦࡸࡤࡰࡹࡱࠫጙ"),
  bstack11l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩጚ"): bstack11l11_opy_ (u"࡚ࠬࡥࡴࡶࠣࡗࡪࡺࡵࡱࠩጛ"),
  bstack11l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪጜ"): bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸ࡚ࠥࡥࡢࡴࡧࡳࡼࡴࠧጝ")
}
bstack111111lll1_opy_ = 65536
bstack11111l1ll1_opy_ = bstack11l11_opy_ (u"ࠨ࠰࠱࠲ࡠ࡚ࡒࡖࡐࡆࡅ࡙ࡋࡄ࡞ࠩጞ")
bstack11111l1l1l_opy_ = [
      bstack11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫጟ"), bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ጠ"), bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧጡ"), bstack11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩጢ"), bstack11l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨጣ"),
      bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪጤ"), bstack11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫጥ"), bstack11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪጦ"), bstack11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫጧ"),
      bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬጨ"), bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧጩ"), bstack11l11_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩጪ")
    ]
bstack11111l11l1_opy_= {
  bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫጫ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬጬ"),
  bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ጭ"): bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧጮ"),
  bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪጯ"): bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩጰ"),
  bstack11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ጱ"): bstack11l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧጲ"),
  bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫጳ"): bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬጴ"),
  bstack11l11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬጵ"): bstack11l11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ጶ"),
  bstack11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨጷ"): bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩጸ"),
  bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫጹ"): bstack11l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬጺ"),
  bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬጻ"): bstack11l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ጼ"),
  bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩጽ"): bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪጾ"),
  bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪጿ"): bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫፀ"),
  bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬፁ"): bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ፂ"),
  bstack11l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬፃ"): bstack11l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ፄ"),
  bstack11l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩፅ"): bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨፆ"),
  bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩፇ"): bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪፈ"),
  bstack11l11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ፉ"): bstack11l11_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧፊ"),
  bstack11l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪፋ"): bstack11l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫፌ"),
  bstack11l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬፍ"): bstack11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ፎ"),
  bstack11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫፏ"): bstack11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬፐ"),
  bstack11l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬፑ"): bstack11l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ፒ"),
  bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬፓ"): bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ፔ"),
  bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧፕ"): bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨፖ"),
  bstack11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ፗ"): bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧፘ"),
  bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨፙ"): bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩፚ"),
  bstack11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭፛"): bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧ፜")
}
bstack11111lll11_opy_ = [bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ፝"), bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ፞")]
bstack1lllll11ll_opy_ = bstack11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠳ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠲ࡺ࠶࠵ࡧࡳ࡫ࡧࡷ࠴ࠨ፟")
bstack1l1lll1l1l_opy_ = bstack11l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴࡭ࡲࡪࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡢࡵ࡫ࡦࡴࡧࡲࡥ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࠥ፠")
bstack1lll1111l_opy_ = bstack11l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠮ࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩ࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳࠨ፡")
class EVENTS(Enum):
  bstack11111l1111_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡳ࠶࠷ࡹ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪ።")
  bstack11lll1111l_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡥࡢࡰࡸࡴࠬ፣") # final bstack11111l111l_opy_
  bstack11111lll1l_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥ࡯ࡦ࡯ࡳ࡬ࡹࠧ፤")
  bstack1llllll11_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽ࡴࡷ࡯࡮ࡵ࠯ࡥࡹ࡮ࡲࡤ࡭࡫ࡱ࡯ࠬ፥")
  bstack1l11lll111_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮ࠫ፦")
  bstack1111l11ll1_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹ࡮ࡵࡣࠩ፧")
  bstack11111lllll_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡦࡲࡻࡳࡲ࡯ࡢࡦࠪ፨")
  bstack11lll1l1_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫࠺ࡩࡷࡥ࠱ࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠨ፩")
  bstack1111lll1l1_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡶࡥࡻ࡫࠭ࡳࡧࡶࡹࡱࡺࡳࠨ፪")
  bstack1l1l11111_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡴࡪࡸࡦࡰࡴࡰࡷࡨࡧ࡮ࠨ፫")
  bstack1l11l1l11l_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻࡮ࡲࡧࡦࡲࠧ፬")
  bstack1l1l1ll1ll_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡡࡱࡲ࠰ࡹࡵࡲ࡯ࡢࡦࠪ፭")
  bstack1ll1ll111_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡧ࡮࠳ࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠩ፮")
  bstack11l111ll1_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭፯")
  bstack11l1111l_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡩࡨࡸ࠲ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠲ࡸࡥࡴࡷ࡯ࡸࡸ࠭፰")
  bstack1111l111l1_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻࠪ፱")
  SDK_PERCY_SCREENSHOT = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ፲")
  bstack1lllllllll_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡶࡸࡦࡺࡵࡴࠩ፳")
  bstack1l1ll1ll11_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼࡫ࡹࡧ࠳࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠪ፴")
  bstack1111l11111_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡵࡳࡽࡿ࠭ࡴࡧࡷࡹࡵ࠭፵")
  bstack1ll111ll_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡶࡩࡹࡻࡰࠨ፶")
  bstack1111l1l111_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡶࡲࡦࡶࡳࡩࡱࡷࠫ፷") # not bstack11111ll1ll_opy_ in python
  bstack1ll1l1llll_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡶࡻࡩࡵࠩ፸") # used in bstack1111l11lll_opy_
  bstack11llll11l_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿࡭ࡥࡵࠩ፹") # used in bstack1111l11lll_opy_
  bstack111l111l_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡨࡰࡱ࡮ࠫ፺")
  bstack11l1l111_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠨ፻")
  bstack111l11l1_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽ࡷࡪࡹࡳࡪࡱࡱ࠱ࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠨ፼") #
  bstack1llll1ll_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡥࡴ࡬ࡺࡪࡸ࠭ࡵࡣ࡮ࡩࡘࡩࡲࡦࡧࡱࡗ࡭ࡵࡴࠨ፽")
  bstack1ll11llll_opy_ = bstack11l11_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺ࠼ࡤࡹࡹࡵ࠭ࡤࡣࡳࡸࡺࡸࡥࠨ፾")
  bstack1l111ll1l1_opy_ = bstack11l11_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸࡥ࠮ࡶࡨࡷࡹ࠭፿")
  bstack1l1l1ll11_opy_ = bstack11l11_opy_ (u"ࠨࡵࡧ࡯࠿ࡶ࡯ࡴࡶ࠰ࡸࡪࡹࡴࠨᎀ")
  bstack11l1ll11l_opy_ = bstack11l11_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡳࡧ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫᎁ")
  bstack1l11l111ll_opy_ = bstack11l11_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᎂ")
  bstack11111l1l11_opy_ = bstack11l11_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴ࠳ࡣࡢࡲࡷࡹࡷ࡫ࠧᎃ")
  bstack1111l1l11l_opy_ = bstack11l11_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾࡮ࡪ࡬ࡦ࠯ࡷ࡭ࡲ࡫࡯ࡶࡶࠪᎄ")
class STAGE(Enum):
  bstack11lll1ll_opy_ = bstack11l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬᎅ")
  END = bstack11l11_opy_ (u"ࠧࡦࡰࡧࠫᎆ")
  SINGLE = bstack11l11_opy_ (u"ࠨࡵ࡬ࡲ࡬ࡲࡥࠨᎇ")
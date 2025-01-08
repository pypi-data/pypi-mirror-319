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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll11ll111_opy_
bstack111l11ll1_opy_ = Config.bstack11ll111lll_opy_()
def bstack1ll1l111lll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll1l111ll1_opy_(bstack1ll1l111l11_opy_, bstack1ll1l11l11l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1l111l11_opy_):
        with open(bstack1ll1l111l11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll1l111lll_opy_(bstack1ll1l111l11_opy_):
        pac = get_pac(url=bstack1ll1l111l11_opy_)
    else:
        raise Exception(bstack1l11_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧᚈ").format(bstack1ll1l111l11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l11_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤᚉ"), 80))
        bstack1ll1l111l1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1l111l1l_opy_ = bstack1l11_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪᚊ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1l11l11l_opy_, bstack1ll1l111l1l_opy_)
    return proxy_url
def bstack1l1lllll1_opy_(config):
    return bstack1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᚋ") in config or bstack1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᚌ") in config
def bstack11l1l1l1l_opy_(config):
    if not bstack1l1lllll1_opy_(config):
        return
    if config.get(bstack1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᚍ")):
        return config.get(bstack1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᚎ"))
    if config.get(bstack1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᚏ")):
        return config.get(bstack1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᚐ"))
def bstack11111l1l_opy_(config, bstack1ll1l11l11l_opy_):
    proxy = bstack11l1l1l1l_opy_(config)
    proxies = {}
    if config.get(bstack1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᚑ")) or config.get(bstack1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᚒ")):
        if proxy.endswith(bstack1l11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᚓ")):
            proxies = bstack11ll111l1_opy_(proxy, bstack1ll1l11l11l_opy_)
        else:
            proxies = {
                bstack1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᚔ"): proxy
            }
    bstack111l11ll1_opy_.bstack1l1l1l1ll_opy_(bstack1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᚕ"), proxies)
    return proxies
def bstack11ll111l1_opy_(bstack1ll1l111l11_opy_, bstack1ll1l11l11l_opy_):
    proxies = {}
    global bstack1ll1l11l111_opy_
    if bstack1l11_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪᚖ") in globals():
        return bstack1ll1l11l111_opy_
    try:
        proxy = bstack1ll1l111ll1_opy_(bstack1ll1l111l11_opy_, bstack1ll1l11l11l_opy_)
        if bstack1l11_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣᚗ") in proxy:
            proxies = {}
        elif bstack1l11_opy_ (u"ࠤࡋࡘ࡙ࡖࠢᚘ") in proxy or bstack1l11_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤᚙ") in proxy or bstack1l11_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥᚚ") in proxy:
            bstack1ll1l11l1l1_opy_ = proxy.split(bstack1l11_opy_ (u"ࠧࠦࠢ᚛"))
            if bstack1l11_opy_ (u"ࠨ࠺࠰࠱ࠥ᚜") in bstack1l11_opy_ (u"ࠢࠣ᚝").join(bstack1ll1l11l1l1_opy_[1:]):
                proxies = {
                    bstack1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ᚞"): bstack1l11_opy_ (u"ࠤࠥ᚟").join(bstack1ll1l11l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᚠ"): str(bstack1ll1l11l1l1_opy_[0]).lower() + bstack1l11_opy_ (u"ࠦ࠿࠵࠯ࠣᚡ") + bstack1l11_opy_ (u"ࠧࠨᚢ").join(bstack1ll1l11l1l1_opy_[1:])
                }
        elif bstack1l11_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧᚣ") in proxy:
            bstack1ll1l11l1l1_opy_ = proxy.split(bstack1l11_opy_ (u"ࠢࠡࠤᚤ"))
            if bstack1l11_opy_ (u"ࠣ࠼࠲࠳ࠧᚥ") in bstack1l11_opy_ (u"ࠤࠥᚦ").join(bstack1ll1l11l1l1_opy_[1:]):
                proxies = {
                    bstack1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᚧ"): bstack1l11_opy_ (u"ࠦࠧᚨ").join(bstack1ll1l11l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᚩ"): bstack1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᚪ") + bstack1l11_opy_ (u"ࠢࠣᚫ").join(bstack1ll1l11l1l1_opy_[1:])
                }
        else:
            proxies = {
                bstack1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᚬ"): proxy
            }
    except Exception as e:
        print(bstack1l11_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᚭ"), bstack1lll11ll111_opy_.format(bstack1ll1l111l11_opy_, str(e)))
    bstack1ll1l11l111_opy_ = proxies
    return proxies
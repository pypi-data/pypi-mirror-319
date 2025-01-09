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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111l1ll1l1_opy_, bstack1111llll11_opy_, bstack1lllll1l1_opy_, bstack11l11ll1ll_opy_, bstack1111111ll1_opy_, bstack1llll1l1l11_opy_, bstack1lllll1l111_opy_, bstack1ll1l1l11l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll11ll1l11_opy_ import bstack1ll11ll11l1_opy_
import bstack_utils.bstack1l1ll111ll_opy_ as bstack1l1l111l1l_opy_
from bstack_utils.bstack11l1l11l11_opy_ import bstack1l111l1l_opy_
import bstack_utils.bstack111lll111l_opy_ as bstack1lll11ll_opy_
from bstack_utils.bstack11lllll1ll_opy_ import bstack11lllll1ll_opy_
from bstack_utils.bstack11l1l1l1l1_opy_ import bstack111lllll11_opy_
bstack1l1lllll1l1_opy_ = bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ᝖")
logger = logging.getLogger(__name__)
class bstack1l11ll1l_opy_:
    bstack1ll11ll1l11_opy_ = None
    bs_config = None
    bstack1ll11l1l_opy_ = None
    @classmethod
    @bstack11l11ll1ll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1111l11ll1_opy_, stage=STAGE.SINGLE)
    def launch(cls, bs_config, bstack1ll11l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack1ll11l1l_opy_ = bstack1ll11l1l_opy_
        try:
            cls.bstack1l1llll1ll1_opy_()
            bstack1111lll11l_opy_ = bstack111l1ll1l1_opy_(bs_config)
            bstack111l111l11_opy_ = bstack1111llll11_opy_(bs_config)
            data = bstack1l1l111l1l_opy_.bstack1ll1111l1ll_opy_(bs_config, bstack1ll11l1l_opy_)
            config = {
                bstack11l11_opy_ (u"ࠫࡦࡻࡴࡩࠩ᝗"): (bstack1111lll11l_opy_, bstack111l111l11_opy_),
                bstack11l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭᝘"): cls.default_headers()
            }
            response = bstack1lllll1l1_opy_(bstack11l11_opy_ (u"࠭ࡐࡐࡕࡗࠫ᝙"), cls.request_url(bstack11l11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠸࠯ࡣࡷ࡬ࡰࡩࡹࠧ᝚")), data, config)
            if response.status_code != 200:
                bstack1l1llll111l_opy_ = response.json()
                if bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ᝛")] == False:
                    cls.bstack1ll1111l111_opy_(bstack1l1llll111l_opy_)
                    return
                cls.bstack1ll11111l11_opy_(bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᝜")])
                cls.bstack1l1llll1l11_opy_(bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᝝")])
                return None
            bstack1ll11111ll1_opy_ = cls.bstack1l1llllll1l_opy_(response)
            return bstack1ll11111ll1_opy_
        except Exception as error:
            logger.error(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤ᝞").format(str(error)))
            return None
    @classmethod
    @bstack11l11ll1ll_opy_(class_method=True)
    def stop(cls, bstack1ll111111ll_opy_=None):
        if not bstack1l111l1l_opy_.on() and not bstack1lll11ll_opy_.on():
            return
        if os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᝟")) == bstack11l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᝠ") or os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᝡ")) == bstack11l11_opy_ (u"ࠣࡰࡸࡰࡱࠨᝢ"):
            logger.error(bstack11l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᝣ"))
            return {
                bstack11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᝤ"): bstack11l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᝥ"),
                bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᝦ"): bstack11l11_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫᝧ")
            }
        try:
            cls.bstack1ll11ll1l11_opy_.shutdown()
            data = {
                bstack11l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᝨ"): bstack1ll1l1l11l_opy_()
            }
            if not bstack1ll111111ll_opy_ is None:
                data[bstack11l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬᝩ")] = [{
                    bstack11l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᝪ"): bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨᝫ"),
                    bstack11l11_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫᝬ"): bstack1ll111111ll_opy_
                }]
            config = {
                bstack11l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭᝭"): cls.default_headers()
            }
            bstack111111l11l_opy_ = bstack11l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧᝮ").format(os.environ[bstack11l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧᝯ")])
            bstack1ll1111l11l_opy_ = cls.request_url(bstack111111l11l_opy_)
            response = bstack1lllll1l1_opy_(bstack11l11_opy_ (u"ࠨࡒࡘࡘࠬᝰ"), bstack1ll1111l11l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l11_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣ᝱"))
        except Exception as error:
            logger.error(bstack11l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾࠿ࠦࠢᝲ") + str(error))
            return {
                bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᝳ"): bstack11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᝴"),
                bstack11l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᝵"): str(error)
            }
    @classmethod
    @bstack11l11ll1ll_opy_(class_method=True)
    def bstack1l1llllll1l_opy_(cls, response):
        bstack1l1llll111l_opy_ = response.json()
        bstack1ll11111ll1_opy_ = {}
        if bstack1l1llll111l_opy_.get(bstack11l11_opy_ (u"ࠧ࡫ࡹࡷࠫ᝶")) is None:
            os.environ[bstack11l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ᝷")] = bstack11l11_opy_ (u"ࠩࡱࡹࡱࡲࠧ᝸")
        else:
            os.environ[bstack11l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ᝹")] = bstack1l1llll111l_opy_.get(bstack11l11_opy_ (u"ࠫ࡯ࡽࡴࠨ᝺"), bstack11l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ᝻"))
        os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᝼")] = bstack1l1llll111l_opy_.get(bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ᝽"), bstack11l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭᝾"))
        if bstack1l111l1l_opy_.bstack1ll1111111l_opy_(cls.bs_config, cls.bstack1ll11l1l_opy_.get(bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ᝿"), bstack11l11_opy_ (u"ࠪࠫក"))) is True:
            bstack1ll11111lll_opy_, bstack1l11l11l_opy_, bstack1l1llll1lll_opy_ = cls.bstack1ll11111111_opy_(bstack1l1llll111l_opy_)
            if bstack1ll11111lll_opy_ != None and bstack1l11l11l_opy_ != None:
                bstack1ll11111ll1_opy_[bstack11l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫខ")] = {
                    bstack11l11_opy_ (u"ࠬࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠨគ"): bstack1ll11111lll_opy_,
                    bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨឃ"): bstack1l11l11l_opy_,
                    bstack11l11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫង"): bstack1l1llll1lll_opy_
                }
            else:
                bstack1ll11111ll1_opy_[bstack11l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨច")] = {}
        else:
            bstack1ll11111ll1_opy_[bstack11l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩឆ")] = {}
        if bstack1lll11ll_opy_.bstack111l1l1111_opy_(cls.bs_config) is True:
            bstack1l1llll1l1l_opy_, bstack1l11l11l_opy_ = cls.bstack1l1llllllll_opy_(bstack1l1llll111l_opy_)
            if bstack1l1llll1l1l_opy_ != None and bstack1l11l11l_opy_ != None:
                bstack1ll11111ll1_opy_[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪជ")] = {
                    bstack11l11_opy_ (u"ࠫࡦࡻࡴࡩࡡࡷࡳࡰ࡫࡮ࠨឈ"): bstack1l1llll1l1l_opy_,
                    bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧញ"): bstack1l11l11l_opy_,
                }
            else:
                bstack1ll11111ll1_opy_[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ដ")] = {}
        else:
            bstack1ll11111ll1_opy_[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧឋ")] = {}
        if bstack1ll11111ll1_opy_[bstack11l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨឌ")].get(bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫឍ")) != None or bstack1ll11111ll1_opy_[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪណ")].get(bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ត")) != None:
            cls.bstack1ll1111ll1l_opy_(bstack1l1llll111l_opy_.get(bstack11l11_opy_ (u"ࠬࡰࡷࡵࠩថ")), bstack1l1llll111l_opy_.get(bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨទ")))
        return bstack1ll11111ll1_opy_
    @classmethod
    def bstack1ll11111111_opy_(cls, bstack1l1llll111l_opy_):
        if bstack1l1llll111l_opy_.get(bstack11l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧធ")) == None:
            cls.bstack1ll11111l11_opy_()
            return [None, None, None]
        if bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨន")][bstack11l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪប")] != True:
            cls.bstack1ll11111l11_opy_(bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪផ")])
            return [None, None, None]
        logger.debug(bstack11l11_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨព"))
        os.environ[bstack11l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫភ")] = bstack11l11_opy_ (u"࠭ࡴࡳࡷࡨࠫម")
        if bstack1l1llll111l_opy_.get(bstack11l11_opy_ (u"ࠧ࡫ࡹࡷࠫយ")):
            os.environ[bstack11l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩរ")] = bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠩ࡭ࡻࡹ࠭ល")]
            os.environ[bstack11l11_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧវ")] = json.dumps({
                bstack11l11_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ឝ"): bstack111l1ll1l1_opy_(cls.bs_config),
                bstack11l11_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧឞ"): bstack1111llll11_opy_(cls.bs_config)
            })
        if bstack1l1llll111l_opy_.get(bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨស")):
            os.environ[bstack11l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ហ")] = bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪឡ")]
        if bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩអ")].get(bstack11l11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫឣ"), {}).get(bstack11l11_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨឤ")):
            os.environ[bstack11l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ឥ")] = str(bstack1l1llll111l_opy_[bstack11l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ឦ")][bstack11l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨឧ")][bstack11l11_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬឨ")])
        return [bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠩ࡭ࡻࡹ࠭ឩ")], bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬឪ")], os.environ[bstack11l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬឫ")]]
    @classmethod
    def bstack1l1llllllll_opy_(cls, bstack1l1llll111l_opy_):
        if bstack1l1llll111l_opy_.get(bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬឬ")) == None:
            cls.bstack1l1llll1l11_opy_()
            return [None, None]
        if bstack1l1llll111l_opy_[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ឭ")][bstack11l11_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨឮ")] != True:
            cls.bstack1l1llll1l11_opy_(bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨឯ")])
            return [None, None]
        if bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩឰ")].get(bstack11l11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫឱ")):
            logger.debug(bstack11l11_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨឲ"))
            parsed = json.loads(os.getenv(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ឳ"), bstack11l11_opy_ (u"࠭ࡻࡾࠩ឴")))
            capabilities = bstack1l1l111l1l_opy_.bstack1l1llll11l1_opy_(bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ឵")][bstack11l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩា")][bstack11l11_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨិ")], bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨី"), bstack11l11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪឹ"))
            bstack1l1llll1l1l_opy_ = capabilities[bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪឺ")]
            os.environ[bstack11l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫុ")] = bstack1l1llll1l1l_opy_
            parsed[bstack11l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨូ")] = capabilities[bstack11l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩួ")]
            os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪើ")] = json.dumps(parsed)
            scripts = bstack1l1l111l1l_opy_.bstack1l1llll11l1_opy_(bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪឿ")][bstack11l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬៀ")][bstack11l11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭េ")], bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫែ"), bstack11l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨៃ"))
            bstack11lllll1ll_opy_.bstack111l111111_opy_(scripts)
            commands = bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨោ")][bstack11l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪៅ")][bstack11l11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫំ")].get(bstack11l11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ះ"))
            bstack11lllll1ll_opy_.bstack111l1l1lll_opy_(commands)
            bstack11lllll1ll_opy_.store()
        return [bstack1l1llll1l1l_opy_, bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧៈ")]]
    @classmethod
    def bstack1ll11111l11_opy_(cls, response=None):
        os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ៉")] = bstack11l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ៊")
        os.environ[bstack11l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ់")] = bstack11l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ៌")
        os.environ[bstack11l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ៍")] = bstack11l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ៎")
        os.environ[bstack11l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭៏")] = bstack11l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ័")
        os.environ[bstack11l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭៑")] = bstack11l11_opy_ (u"ࠣࡰࡸࡰࡱࠨ្")
        os.environ[bstack11l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ៓")] = bstack11l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ។")
        cls.bstack1ll1111l111_opy_(response, bstack11l11_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦ៕"))
        return [None, None, None]
    @classmethod
    def bstack1l1llll1l11_opy_(cls, response=None):
        os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ៖")] = bstack11l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫៗ")
        os.environ[bstack11l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ៘")] = bstack11l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭៙")
        os.environ[bstack11l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ៚")] = bstack11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ៛")
        cls.bstack1ll1111l111_opy_(response, bstack11l11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦៜ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1111ll1l_opy_(cls, bstack1ll11111l1l_opy_, bstack1l11l11l_opy_):
        os.environ[bstack11l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭៝")] = bstack1ll11111l1l_opy_
        os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ៞")] = bstack1l11l11l_opy_
    @classmethod
    def bstack1ll1111l111_opy_(cls, response=None, product=bstack11l11_opy_ (u"ࠢࠣ៟")):
        if response == None:
            logger.error(product + bstack11l11_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥ០"))
        for error in response[bstack11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ១")]:
            bstack1llll1l1ll1_opy_ = error[bstack11l11_opy_ (u"ࠪ࡯ࡪࡿࠧ២")]
            error_message = error[bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ៣")]
            if error_message:
                if bstack1llll1l1ll1_opy_ == bstack11l11_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦ៤"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l11_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢ៥") + product + bstack11l11_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ៦"))
    @classmethod
    def bstack1l1llll1ll1_opy_(cls):
        if cls.bstack1ll11ll1l11_opy_ is not None:
            return
        cls.bstack1ll11ll1l11_opy_ = bstack1ll11ll11l1_opy_(cls.bstack1l1lllllll1_opy_)
        cls.bstack1ll11ll1l11_opy_.start()
    @classmethod
    def bstack111llll1l1_opy_(cls):
        if cls.bstack1ll11ll1l11_opy_ is None:
            return
        cls.bstack1ll11ll1l11_opy_.shutdown()
    @classmethod
    @bstack11l11ll1ll_opy_(class_method=True)
    def bstack1l1lllllll1_opy_(cls, bstack11l11111ll_opy_, bstack1l1lllll11l_opy_=bstack11l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ៧")):
        config = {
            bstack11l11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ៨"): cls.default_headers()
        }
        response = bstack1lllll1l1_opy_(bstack11l11_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ៩"), cls.request_url(bstack1l1lllll11l_opy_), bstack11l11111ll_opy_, config)
        bstack111l11llll_opy_ = response.json()
    @classmethod
    def bstack1lllll1111_opy_(cls, bstack11l11111ll_opy_, bstack1l1lllll11l_opy_=bstack11l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ៪")):
        if not bstack1l1l111l1l_opy_.bstack1l1llllll11_opy_(bstack11l11111ll_opy_[bstack11l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ៫")]):
            return
        bstack1l111111_opy_ = bstack1l1l111l1l_opy_.bstack1ll111111l1_opy_(bstack11l11111ll_opy_[bstack11l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ៬")], bstack11l11111ll_opy_.get(bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ៭")))
        if bstack1l111111_opy_ != None:
            if bstack11l11111ll_opy_.get(bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ៮")) != None:
                bstack11l11111ll_opy_[bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ៯")][bstack11l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ៰")] = bstack1l111111_opy_
            else:
                bstack11l11111ll_opy_[bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ៱")] = bstack1l111111_opy_
        if bstack1l1lllll11l_opy_ == bstack11l11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ៲"):
            cls.bstack1l1llll1ll1_opy_()
            cls.bstack1ll11ll1l11_opy_.add(bstack11l11111ll_opy_)
        elif bstack1l1lllll11l_opy_ == bstack11l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ៳"):
            cls.bstack1l1lllllll1_opy_([bstack11l11111ll_opy_], bstack1l1lllll11l_opy_)
    @classmethod
    @bstack11l11ll1ll_opy_(class_method=True)
    def bstack1ll11l11ll_opy_(cls, bstack11l111llll_opy_):
        bstack1l1llll11ll_opy_ = []
        for log in bstack11l111llll_opy_:
            bstack1l1lllll1ll_opy_ = {
                bstack11l11_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ៴"): bstack11l11_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪ៵"),
                bstack11l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ៶"): log[bstack11l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ៷")],
                bstack11l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ៸"): log[bstack11l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ៹")],
                bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭៺"): {},
                bstack11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៻"): log[bstack11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ៼")],
            }
            if bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ៽") in log:
                bstack1l1lllll1ll_opy_[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ៾")] = log[bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៿")]
            elif bstack11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᠀") in log:
                bstack1l1lllll1ll_opy_[bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᠁")] = log[bstack11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᠂")]
            bstack1l1llll11ll_opy_.append(bstack1l1lllll1ll_opy_)
        cls.bstack1lllll1111_opy_({
            bstack11l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᠃"): bstack11l11_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭᠄"),
            bstack11l11_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ᠅"): bstack1l1llll11ll_opy_
        })
    @classmethod
    @bstack11l11ll1ll_opy_(class_method=True)
    def bstack1ll1111l1l1_opy_(cls, steps):
        bstack1ll1111ll11_opy_ = []
        for step in steps:
            bstack1l1llll1111_opy_ = {
                bstack11l11_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ᠆"): bstack11l11_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨ᠇"),
                bstack11l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ᠈"): step[bstack11l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭᠉")],
                bstack11l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ᠊"): step[bstack11l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ᠋")],
                bstack11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᠌"): step[bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᠍")],
                bstack11l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ᠎"): step[bstack11l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ᠏")]
            }
            if bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᠐") in step:
                bstack1l1llll1111_opy_[bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᠑")] = step[bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᠒")]
            elif bstack11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᠓") in step:
                bstack1l1llll1111_opy_[bstack11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᠔")] = step[bstack11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᠕")]
            bstack1ll1111ll11_opy_.append(bstack1l1llll1111_opy_)
        cls.bstack1lllll1111_opy_({
            bstack11l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ᠖"): bstack11l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ᠗"),
            bstack11l11_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭᠘"): bstack1ll1111ll11_opy_
        })
    @classmethod
    @bstack11l11ll1ll_opy_(class_method=True)
    def bstack1ll1l1l1l_opy_(cls, screenshot):
        cls.bstack1lllll1111_opy_({
            bstack11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᠙"): bstack11l11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ᠚"),
            bstack11l11_opy_ (u"ࠫࡱࡵࡧࡴࠩ᠛"): [{
                bstack11l11_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ᠜"): bstack11l11_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨ᠝"),
                bstack11l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᠞"): datetime.datetime.utcnow().isoformat() + bstack11l11_opy_ (u"ࠨ࡜ࠪ᠟"),
                bstack11l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᠠ"): screenshot[bstack11l11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᠡ")],
                bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᠢ"): screenshot[bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᠣ")]
            }]
        }, bstack1l1lllll11l_opy_=bstack11l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᠤ"))
    @classmethod
    @bstack11l11ll1ll_opy_(class_method=True)
    def bstack11111l11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1lllll1111_opy_({
            bstack11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᠥ"): bstack11l11_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᠦ"),
            bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᠧ"): {
                bstack11l11_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᠨ"): cls.current_test_uuid(),
                bstack11l11_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥᠩ"): cls.bstack11l1ll1ll1_opy_(driver)
            }
        })
    @classmethod
    def bstack11l1ll11ll_opy_(cls, event: str, bstack11l11111ll_opy_: bstack111lllll11_opy_):
        bstack111llll1ll_opy_ = {
            bstack11l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᠪ"): event,
            bstack11l11111ll_opy_.bstack11l11l111l_opy_(): bstack11l11111ll_opy_.bstack11l111ll1l_opy_(event)
        }
        cls.bstack1lllll1111_opy_(bstack111llll1ll_opy_)
        result = getattr(bstack11l11111ll_opy_, bstack11l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᠫ"), None)
        if event == bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᠬ"):
            threading.current_thread().bstackTestMeta = {bstack11l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᠭ"): bstack11l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᠮ")}
        elif event == bstack11l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᠯ"):
            threading.current_thread().bstackTestMeta = {bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᠰ"): getattr(result, bstack11l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᠱ"), bstack11l11_opy_ (u"࠭ࠧᠲ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᠳ"), None) is None or os.environ[bstack11l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᠴ")] == bstack11l11_opy_ (u"ࠤࡱࡹࡱࡲࠢᠵ")) and (os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᠶ"), None) is None or os.environ[bstack11l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᠷ")] == bstack11l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᠸ")):
            return False
        return True
    @staticmethod
    def bstack1l1lllll111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11ll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᠹ"): bstack11l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᠺ"),
            bstack11l11_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫᠻ"): bstack11l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᠼ")
        }
        if os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᠽ"), None):
            headers[bstack11l11_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᠾ")] = bstack11l11_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨᠿ").format(os.environ[bstack11l11_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠢᡀ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11l11_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᡁ").format(bstack1l1lllll1l1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᡂ"), None)
    @staticmethod
    def bstack11l1ll1ll1_opy_(driver):
        return {
            bstack1111111ll1_opy_(): bstack1llll1l1l11_opy_(driver)
        }
    @staticmethod
    def bstack1ll1111lll1_opy_(exception_info, report):
        return [{bstack11l11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᡃ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111l1llll1_opy_(typename):
        if bstack11l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᡄ") in typename:
            return bstack11l11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᡅ")
        return bstack11l11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᡆ")
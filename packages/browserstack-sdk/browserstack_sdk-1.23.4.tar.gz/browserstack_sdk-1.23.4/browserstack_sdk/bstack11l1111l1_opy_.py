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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11l1l1l1l1_opy_ import bstack11l1l1lll1_opy_, bstack11l1ll1lll_opy_
from bstack_utils.bstack11l1l11l11_opy_ import bstack1l111l1l_opy_
from bstack_utils.helper import bstack11l1l11l1_opy_, bstack1ll1l1l11l_opy_, Result
from bstack_utils.bstack11l1lll111_opy_ import bstack1l11ll1l_opy_
from bstack_utils.capture import bstack11l1ll111l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11l1111l1_opy_:
    def __init__(self):
        self.bstack11l1l11lll_opy_ = bstack11l1ll111l_opy_(self.bstack11l1ll1111_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l1ll1111_opy_(log):
        if not (log[bstack11l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๡")] and log[bstack11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ๢")].strip()):
            return
        active = bstack1l111l1l_opy_.bstack11l1llll1l_opy_()
        log = {
            bstack11l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ๣"): log[bstack11l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ๤")],
            bstack11l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭๥"): bstack1ll1l1l11l_opy_(),
            bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ๦"): log[bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭๧")],
        }
        if active:
            if active[bstack11l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ๨")] == bstack11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ๩"):
                log[bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ๪")] = active[bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ๫")]
            elif active[bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ๬")] == bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ๭"):
                log[bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ๮")] = active[bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭๯")]
        bstack1l11ll1l_opy_.bstack1ll11l11ll_opy_([log])
    def start_test(self, attrs):
        bstack11l1ll1l1l_opy_ = uuid4().__str__()
        self.tests[bstack11l1ll1l1l_opy_] = {}
        self.bstack11l1l11lll_opy_.start()
        driver = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭๰"), None)
        bstack11l1l1l1l1_opy_ = bstack11l1ll1lll_opy_(
            name=attrs.scenario.name,
            uuid=bstack11l1ll1l1l_opy_,
            bstack11l1l111ll_opy_=bstack1ll1l1l11l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack11l11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤ๱"),
            framework=bstack11l11_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩ๲"),
            scope=[attrs.feature.name],
            bstack11l1lll11l_opy_=bstack1l11ll1l_opy_.bstack11l1ll1ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11l1ll1l1l_opy_][bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭๳")] = bstack11l1l1l1l1_opy_
        threading.current_thread().current_test_uuid = bstack11l1ll1l1l_opy_
        bstack1l11ll1l_opy_.bstack11l1ll11ll_opy_(bstack11l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ๴"), bstack11l1l1l1l1_opy_)
    def end_test(self, attrs):
        bstack11l1l1ll11_opy_ = {
            bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ๵"): attrs.feature.name,
            bstack11l11_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ๶"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11l1l1l1l1_opy_ = self.tests[current_test_uuid][bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ๷")]
        meta = {
            bstack11l11_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤ๸"): bstack11l1l1ll11_opy_,
            bstack11l11_opy_ (u"ࠤࡶࡸࡪࡶࡳࠣ๹"): bstack11l1l1l1l1_opy_.meta.get(bstack11l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ๺"), []),
            bstack11l11_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ๻"): {
                bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ๼"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11l1l1l1l1_opy_.bstack11l1ll1l11_opy_(meta)
        bstack11l1l1l1l1_opy_.bstack11l1ll11l1_opy_(bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ๽"), []))
        bstack11l1lll1ll_opy_, exception = self._11l1l1l11l_opy_(attrs)
        bstack11l1lll1l1_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1l1l111_opy_=[bstack11l1lll1ll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ๾")].stop(time=bstack1ll1l1l11l_opy_(), duration=int(attrs.duration)*1000, result=bstack11l1lll1l1_opy_)
        bstack1l11ll1l_opy_.bstack11l1ll11ll_opy_(bstack11l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ๿"), self.tests[threading.current_thread().current_test_uuid][bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ຀")])
    def bstack11lll1l1l_opy_(self, attrs):
        bstack11l1l1l1ll_opy_ = {
            bstack11l11_opy_ (u"ࠪ࡭ࡩ࠭ກ"): uuid4().__str__(),
            bstack11l11_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬຂ"): attrs.keyword,
            bstack11l11_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ຃"): [],
            bstack11l11_opy_ (u"࠭ࡴࡦࡺࡷࠫຄ"): attrs.name,
            bstack11l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ຅"): bstack1ll1l1l11l_opy_(),
            bstack11l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨຆ"): bstack11l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪງ"),
            bstack11l11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨຈ"): bstack11l11_opy_ (u"ࠫࠬຉ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨຊ")].add_step(bstack11l1l1l1ll_opy_)
        threading.current_thread().current_step_uuid = bstack11l1l1l1ll_opy_[bstack11l11_opy_ (u"࠭ࡩࡥࠩ຋")]
    def bstack1l11l1lll_opy_(self, attrs):
        current_test_id = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫຌ"), None)
        current_step_uuid = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬຍ"), None)
        bstack11l1lll1ll_opy_, exception = self._11l1l1l11l_opy_(attrs)
        bstack11l1lll1l1_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1l1l111_opy_=[bstack11l1lll1ll_opy_])
        self.tests[current_test_id][bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຎ")].bstack11l1l11ll1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11l1lll1l1_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1ll11ll1ll_opy_(self, name, attrs):
        try:
            bstack11l1llll11_opy_ = uuid4().__str__()
            self.tests[bstack11l1llll11_opy_] = {}
            self.bstack11l1l11lll_opy_.start()
            scopes = []
            driver = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩຏ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩຐ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l1llll11_opy_)
            if name in [bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤຑ"), bstack11l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤຒ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣຓ"), bstack11l11_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣດ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11l11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪຕ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11l1l1lll1_opy_(
                name=name,
                uuid=bstack11l1llll11_opy_,
                bstack11l1l111ll_opy_=bstack1ll1l1l11l_opy_(),
                file_path=file_path,
                framework=bstack11l11_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥຖ"),
                bstack11l1lll11l_opy_=bstack1l11ll1l_opy_.bstack11l1ll1ll1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧທ"),
                hook_type=name
            )
            self.tests[bstack11l1llll11_opy_][bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣຘ")] = hook_data
            current_test_id = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥນ"), None)
            if current_test_id:
                hook_data.bstack11l1l11l1l_opy_(current_test_id)
            if name == bstack11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦບ"):
                threading.current_thread().before_all_hook_uuid = bstack11l1llll11_opy_
            threading.current_thread().current_hook_uuid = bstack11l1llll11_opy_
            bstack1l11ll1l_opy_.bstack11l1ll11ll_opy_(bstack11l11_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤປ"), hook_data)
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣຜ"), name, e)
    def bstack1l1lll11l_opy_(self, attrs):
        bstack11l1l111l1_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧຝ"), None)
        hook_data = self.tests[bstack11l1l111l1_opy_][bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧພ")]
        status = bstack11l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧຟ")
        exception = None
        bstack11l1lll1ll_opy_ = None
        if hook_data.name == bstack11l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤຠ"):
            self.bstack11l1l11lll_opy_.reset()
            bstack11l1l1llll_opy_ = self.tests[bstack11l1l11l1_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧມ"), None)][bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫຢ")].result.result
            if bstack11l1l1llll_opy_ == bstack11l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤຣ"):
                if attrs.hook_failures == 1:
                    status = bstack11l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ຤")
                elif attrs.hook_failures == 2:
                    status = bstack11l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦລ")
            elif attrs.bstack11l1l1ll1l_opy_:
                status = bstack11l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ຦")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪວ") and attrs.hook_failures == 1:
                status = bstack11l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢຨ")
            elif hasattr(attrs, bstack11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨຩ")) and attrs.error_message:
                status = bstack11l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤສ")
            bstack11l1lll1ll_opy_, exception = self._11l1l1l11l_opy_(attrs)
        bstack11l1lll1l1_opy_ = Result(result=status, exception=exception, bstack11l1l1l111_opy_=[bstack11l1lll1ll_opy_])
        hook_data.stop(time=bstack1ll1l1l11l_opy_(), duration=0, result=bstack11l1lll1l1_opy_)
        bstack1l11ll1l_opy_.bstack11l1ll11ll_opy_(bstack11l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬຫ"), self.tests[bstack11l1l111l1_opy_][bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧຬ")])
        threading.current_thread().current_hook_uuid = None
    def _11l1l1l11l_opy_(self, attrs):
        try:
            import traceback
            bstack1ll1lll1ll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l1lll1ll_opy_ = bstack1ll1lll1ll_opy_[-1] if bstack1ll1lll1ll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤອ"))
            bstack11l1lll1ll_opy_ = None
            exception = None
        return bstack11l1lll1ll_opy_, exception
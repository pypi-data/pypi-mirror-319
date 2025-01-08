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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111lll11ll_opy_ import RobotHandler
from bstack_utils.capture import bstack11l1llll1l_opy_
from bstack_utils.bstack11l1l1lll1_opy_ import bstack11l111l11l_opy_, bstack11l1lll1l1_opy_, bstack11l1lll111_opy_
from bstack_utils.bstack11l1ll1111_opy_ import bstack111lll111_opy_
from bstack_utils.bstack11l1l1l111_opy_ import bstack1lll1lllll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll111111l_opy_, bstack11ll1111l1_opy_, Result, \
    bstack11l11llll1_opy_, bstack11l11ll11l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪຮ"): [],
        bstack1l11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ຯ"): [],
        bstack1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬະ"): []
    }
    bstack11l1111l1l_opy_ = []
    bstack11l11l111l_opy_ = []
    @staticmethod
    def bstack11l1ll1l11_opy_(log):
        if not (log[bstack1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪັ")] and log[bstack1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫາ")].strip()):
            return
        active = bstack111lll111_opy_.bstack11l1l111ll_opy_()
        log = {
            bstack1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪຳ"): log[bstack1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫິ")],
            bstack1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩີ"): bstack11l11ll11l_opy_().isoformat() + bstack1l11_opy_ (u"࡛ࠧࠩຶ"),
            bstack1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩື"): log[bstack1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧຸࠪ")],
        }
        if active:
            if active[bstack1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨູ")] == bstack1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬຺ࠩ"):
                log[bstack1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬົ")] = active[bstack1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ຼ")]
            elif active[bstack1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬຽ")] == bstack1l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭຾"):
                log[bstack1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ຿")] = active[bstack1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪເ")]
        bstack1lll1lllll_opy_.bstack11111ll11_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11l1l1111l_opy_ = None
        self._111lllll1l_opy_ = None
        self._11l11l11ll_opy_ = OrderedDict()
        self.bstack11l1ll1lll_opy_ = bstack11l1llll1l_opy_(self.bstack11l1ll1l11_opy_)
    @bstack11l11llll1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11l11lllll_opy_()
        if not self._11l11l11ll_opy_.get(attrs.get(bstack1l11_opy_ (u"ࠫ࡮ࡪࠧແ")), None):
            self._11l11l11ll_opy_[attrs.get(bstack1l11_opy_ (u"ࠬ࡯ࡤࠨໂ"))] = {}
        bstack11l11l1ll1_opy_ = bstack11l1lll111_opy_(
                bstack11l11l1111_opy_=attrs.get(bstack1l11_opy_ (u"࠭ࡩࡥࠩໃ")),
                name=name,
                bstack11l1llll11_opy_=bstack11ll1111l1_opy_(),
                file_path=os.path.relpath(attrs[bstack1l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧໄ")], start=os.getcwd()) if attrs.get(bstack1l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ໅")) != bstack1l11_opy_ (u"ࠩࠪໆ") else bstack1l11_opy_ (u"ࠪࠫ໇"),
                framework=bstack1l11_opy_ (u"ࠫࡗࡵࡢࡰࡶ່ࠪ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l11_opy_ (u"ࠬ࡯ࡤࠨ້"), None)
        self._11l11l11ll_opy_[attrs.get(bstack1l11_opy_ (u"࠭ࡩࡥ໊ࠩ"))][bstack1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣ໋ࠪ")] = bstack11l11l1ll1_opy_
    @bstack11l11llll1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111lllll11_opy_()
        self._111lll1ll1_opy_(messages)
        for bstack11l111l111_opy_ in self.bstack11l1111l1l_opy_:
            bstack11l111l111_opy_[bstack1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ໌")][bstack1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨໍ")].extend(self.store[bstack1l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ໎")])
            bstack1lll1lllll_opy_.bstack1llllll111_opy_(bstack11l111l111_opy_)
        self.bstack11l1111l1l_opy_ = []
        self.store[bstack1l11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ໏")] = []
    @bstack11l11llll1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l1ll1lll_opy_.start()
        if not self._11l11l11ll_opy_.get(attrs.get(bstack1l11_opy_ (u"ࠬ࡯ࡤࠨ໐")), None):
            self._11l11l11ll_opy_[attrs.get(bstack1l11_opy_ (u"࠭ࡩࡥࠩ໑"))] = {}
        driver = bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭໒"), None)
        bstack11l1l1lll1_opy_ = bstack11l1lll111_opy_(
            bstack11l11l1111_opy_=attrs.get(bstack1l11_opy_ (u"ࠨ࡫ࡧࠫ໓")),
            name=name,
            bstack11l1llll11_opy_=bstack11ll1111l1_opy_(),
            file_path=os.path.relpath(attrs[bstack1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ໔")], start=os.getcwd()),
            scope=RobotHandler.bstack11l1111ll1_opy_(attrs.get(bstack1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ໕"), None)),
            framework=bstack1l11_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ໖"),
            tags=attrs[bstack1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪ໗")],
            hooks=self.store[bstack1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ໘")],
            bstack11l1l11ll1_opy_=bstack1lll1lllll_opy_.bstack11l1l1l1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l11_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤ໙").format(bstack1l11_opy_ (u"ࠣࠢࠥ໚").join(attrs[bstack1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ໛")]), name) if attrs[bstack1l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨໜ")] else name
        )
        self._11l11l11ll_opy_[attrs.get(bstack1l11_opy_ (u"ࠫ࡮ࡪࠧໝ"))][bstack1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨໞ")] = bstack11l1l1lll1_opy_
        threading.current_thread().current_test_uuid = bstack11l1l1lll1_opy_.bstack11l111111l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l11_opy_ (u"࠭ࡩࡥࠩໟ"), None)
        self.bstack11l1lll11l_opy_(bstack1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ໠"), bstack11l1l1lll1_opy_)
    @bstack11l11llll1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l1ll1lll_opy_.reset()
        bstack11l111llll_opy_ = bstack11l111ll11_opy_.get(attrs.get(bstack1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ໡")), bstack1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ໢"))
        self._11l11l11ll_opy_[attrs.get(bstack1l11_opy_ (u"ࠪ࡭ࡩ࠭໣"))][bstack1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໤")].stop(time=bstack11ll1111l1_opy_(), duration=int(attrs.get(bstack1l11_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪ໥"), bstack1l11_opy_ (u"࠭࠰ࠨ໦"))), result=Result(result=bstack11l111llll_opy_, exception=attrs.get(bstack1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໧")), bstack11l1lll1ll_opy_=[attrs.get(bstack1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໨"))]))
        self.bstack11l1lll11l_opy_(bstack1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ໩"), self._11l11l11ll_opy_[attrs.get(bstack1l11_opy_ (u"ࠪ࡭ࡩ࠭໪"))][bstack1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໫")], True)
        self.store[bstack1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ໬")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11l11llll1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11l11lllll_opy_()
        current_test_id = bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ໭"), None)
        bstack11l11l1l11_opy_ = current_test_id if bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩ໮"), None) else bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ໯"), None)
        if attrs.get(bstack1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ໰"), bstack1l11_opy_ (u"ࠪࠫ໱")).lower() in [bstack1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ໲"), bstack1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ໳")]:
            hook_type = bstack111lll1l1l_opy_(attrs.get(bstack1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ໴")), bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ໵"), None))
            hook_name = bstack1l11_opy_ (u"ࠨࡽࢀࠫ໶").format(attrs.get(bstack1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ໷"), bstack1l11_opy_ (u"ࠪࠫ໸")))
            if hook_type in [bstack1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ໹"), bstack1l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨ໺")]:
                hook_name = bstack1l11_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧ໻").format(bstack11l11111ll_opy_.get(hook_type), attrs.get(bstack1l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ໼"), bstack1l11_opy_ (u"ࠨࠩ໽")))
            bstack11l11111l1_opy_ = bstack11l1lll1l1_opy_(
                bstack11l11l1111_opy_=bstack11l11l1l11_opy_ + bstack1l11_opy_ (u"ࠩ࠰ࠫ໾") + attrs.get(bstack1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ໿"), bstack1l11_opy_ (u"ࠫࠬༀ")).lower(),
                name=hook_name,
                bstack11l1llll11_opy_=bstack11ll1111l1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ༁")), start=os.getcwd()),
                framework=bstack1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬ༂"),
                tags=attrs[bstack1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬ༃")],
                scope=RobotHandler.bstack11l1111ll1_opy_(attrs.get(bstack1l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ༄"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11l11111l1_opy_.bstack11l111111l_opy_()
            threading.current_thread().current_hook_id = bstack11l11l1l11_opy_ + bstack1l11_opy_ (u"ࠩ࠰ࠫ༅") + attrs.get(bstack1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ༆"), bstack1l11_opy_ (u"ࠫࠬ༇")).lower()
            self.store[bstack1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ༈")] = [bstack11l11111l1_opy_.bstack11l111111l_opy_()]
            if bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ༉"), None):
                self.store[bstack1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ༊")].append(bstack11l11111l1_opy_.bstack11l111111l_opy_())
            else:
                self.store[bstack1l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ་")].append(bstack11l11111l1_opy_.bstack11l111111l_opy_())
            if bstack11l11l1l11_opy_:
                self._11l11l11ll_opy_[bstack11l11l1l11_opy_ + bstack1l11_opy_ (u"ࠩ࠰ࠫ༌") + attrs.get(bstack1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ།"), bstack1l11_opy_ (u"ࠫࠬ༎")).lower()] = { bstack1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ༏"): bstack11l11111l1_opy_ }
            bstack1lll1lllll_opy_.bstack11l1lll11l_opy_(bstack1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ༐"), bstack11l11111l1_opy_)
        else:
            bstack11l1l1l1l1_opy_ = {
                bstack1l11_opy_ (u"ࠧࡪࡦࠪ༑"): uuid4().__str__(),
                bstack1l11_opy_ (u"ࠨࡶࡨࡼࡹ࠭༒"): bstack1l11_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ༓").format(attrs.get(bstack1l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ༔")), attrs.get(bstack1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩ༕"), bstack1l11_opy_ (u"ࠬ࠭༖"))) if attrs.get(bstack1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫ༗"), []) else attrs.get(bstack1l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫༘ࠧ")),
                bstack1l11_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨ༙"): attrs.get(bstack1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ༚"), []),
                bstack1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ༛"): bstack11ll1111l1_opy_(),
                bstack1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ༜"): bstack1l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭༝"),
                bstack1l11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ༞"): attrs.get(bstack1l11_opy_ (u"ࠧࡥࡱࡦࠫ༟"), bstack1l11_opy_ (u"ࠨࠩ༠"))
            }
            if attrs.get(bstack1l11_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪ༡"), bstack1l11_opy_ (u"ࠪࠫ༢")) != bstack1l11_opy_ (u"ࠫࠬ༣"):
                bstack11l1l1l1l1_opy_[bstack1l11_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭༤")] = attrs.get(bstack1l11_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ༥"))
            if not self.bstack11l11l111l_opy_:
                self._11l11l11ll_opy_[self._111llll1l1_opy_()][bstack1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ༦")].add_step(bstack11l1l1l1l1_opy_)
                threading.current_thread().current_step_uuid = bstack11l1l1l1l1_opy_[bstack1l11_opy_ (u"ࠨ࡫ࡧࠫ༧")]
            self.bstack11l11l111l_opy_.append(bstack11l1l1l1l1_opy_)
    @bstack11l11llll1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111lllll11_opy_()
        self._111lll1ll1_opy_(messages)
        current_test_id = bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ༨"), None)
        bstack11l11l1l11_opy_ = current_test_id if current_test_id else bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭༩"), None)
        bstack11l1111lll_opy_ = bstack11l111ll11_opy_.get(attrs.get(bstack1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ༪")), bstack1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭༫"))
        bstack11l11lll1l_opy_ = attrs.get(bstack1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༬"))
        if bstack11l1111lll_opy_ != bstack1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ༭") and not attrs.get(bstack1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༮")) and self._11l1l1111l_opy_:
            bstack11l11lll1l_opy_ = self._11l1l1111l_opy_
        bstack11l1l1llll_opy_ = Result(result=bstack11l1111lll_opy_, exception=bstack11l11lll1l_opy_, bstack11l1lll1ll_opy_=[bstack11l11lll1l_opy_])
        if attrs.get(bstack1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ༯"), bstack1l11_opy_ (u"ࠪࠫ༰")).lower() in [bstack1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ༱"), bstack1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ༲")]:
            bstack11l11l1l11_opy_ = current_test_id if current_test_id else bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ༳"), None)
            if bstack11l11l1l11_opy_:
                bstack11l1ll1ll1_opy_ = bstack11l11l1l11_opy_ + bstack1l11_opy_ (u"ࠢ࠮ࠤ༴") + attrs.get(bstack1l11_opy_ (u"ࠨࡶࡼࡴࡪ༵࠭"), bstack1l11_opy_ (u"ࠩࠪ༶")).lower()
                self._11l11l11ll_opy_[bstack11l1ll1ll1_opy_][bstack1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ༷࠭")].stop(time=bstack11ll1111l1_opy_(), duration=int(attrs.get(bstack1l11_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ༸"), bstack1l11_opy_ (u"ࠬ࠶༹ࠧ"))), result=bstack11l1l1llll_opy_)
                bstack1lll1lllll_opy_.bstack11l1lll11l_opy_(bstack1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ༺"), self._11l11l11ll_opy_[bstack11l1ll1ll1_opy_][bstack1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ༻")])
        else:
            bstack11l11l1l11_opy_ = current_test_id if current_test_id else bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪ༼"), None)
            if bstack11l11l1l11_opy_ and len(self.bstack11l11l111l_opy_) == 1:
                current_step_uuid = bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭༽"), None)
                self._11l11l11ll_opy_[bstack11l11l1l11_opy_][bstack1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༾")].bstack11l1ll1l1l_opy_(current_step_uuid, duration=int(attrs.get(bstack1l11_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ༿"), bstack1l11_opy_ (u"ࠬ࠶ࠧཀ"))), result=bstack11l1l1llll_opy_)
            else:
                self.bstack11l11l1l1l_opy_(attrs)
            self.bstack11l11l111l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l11_opy_ (u"࠭ࡨࡵ࡯࡯ࠫཁ"), bstack1l11_opy_ (u"ࠧ࡯ࡱࠪག")) == bstack1l11_opy_ (u"ࠨࡻࡨࡷࠬགྷ"):
                return
            self.messages.push(message)
            bstack11l11ll1l1_opy_ = []
            if bstack111lll111_opy_.bstack11l1l111ll_opy_():
                bstack11l11ll1l1_opy_.append({
                    bstack1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬང"): bstack11ll1111l1_opy_(),
                    bstack1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཅ"): message.get(bstack1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཆ")),
                    bstack1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫཇ"): message.get(bstack1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ཈")),
                    **bstack111lll111_opy_.bstack11l1l111ll_opy_()
                })
                if len(bstack11l11ll1l1_opy_) > 0:
                    bstack1lll1lllll_opy_.bstack11111ll11_opy_(bstack11l11ll1l1_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1lll1lllll_opy_.bstack11l111l1ll_opy_()
    def bstack11l11l1l1l_opy_(self, bstack111llll11l_opy_):
        if not bstack111lll111_opy_.bstack11l1l111ll_opy_():
            return
        kwname = bstack1l11_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ཉ").format(bstack111llll11l_opy_.get(bstack1l11_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨཊ")), bstack111llll11l_opy_.get(bstack1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧཋ"), bstack1l11_opy_ (u"ࠪࠫཌ"))) if bstack111llll11l_opy_.get(bstack1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩཌྷ"), []) else bstack111llll11l_opy_.get(bstack1l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬཎ"))
        error_message = bstack1l11_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧཏ").format(kwname, bstack111llll11l_opy_.get(bstack1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧཐ")), str(bstack111llll11l_opy_.get(bstack1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩད"))))
        bstack11l11lll11_opy_ = bstack1l11_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣདྷ").format(kwname, bstack111llll11l_opy_.get(bstack1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪན")))
        bstack11l11ll1ll_opy_ = error_message if bstack111llll11l_opy_.get(bstack1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཔ")) else bstack11l11lll11_opy_
        bstack111lll1lll_opy_ = {
            bstack1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨཕ"): self.bstack11l11l111l_opy_[-1].get(bstack1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪབ"), bstack11ll1111l1_opy_()),
            bstack1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨབྷ"): bstack11l11ll1ll_opy_,
            bstack1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧམ"): bstack1l11_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨཙ") if bstack111llll11l_opy_.get(bstack1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪཚ")) == bstack1l11_opy_ (u"ࠫࡋࡇࡉࡍࠩཛ") else bstack1l11_opy_ (u"ࠬࡏࡎࡇࡑࠪཛྷ"),
            **bstack111lll111_opy_.bstack11l1l111ll_opy_()
        }
        bstack1lll1lllll_opy_.bstack11111ll11_opy_([bstack111lll1lll_opy_])
    def _111llll1l1_opy_(self):
        for bstack11l11l1111_opy_ in reversed(self._11l11l11ll_opy_):
            bstack111llllll1_opy_ = bstack11l11l1111_opy_
            data = self._11l11l11ll_opy_[bstack11l11l1111_opy_][bstack1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཝ")]
            if isinstance(data, bstack11l1lll1l1_opy_):
                if not bstack1l11_opy_ (u"ࠧࡆࡃࡆࡌࠬཞ") in data.bstack11l1l11111_opy_():
                    return bstack111llllll1_opy_
            else:
                return bstack111llllll1_opy_
    def _111lll1ll1_opy_(self, messages):
        try:
            bstack11l11l11l1_opy_ = BuiltIn().get_variable_value(bstack1l11_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢཟ")) in (bstack111lll11l1_opy_.DEBUG, bstack111lll11l1_opy_.TRACE)
            for message, bstack111llll1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪའ"))
                level = message.get(bstack1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩཡ"))
                if level == bstack111lll11l1_opy_.FAIL:
                    self._11l1l1111l_opy_ = name or self._11l1l1111l_opy_
                    self._111lllll1l_opy_ = bstack111llll1ll_opy_.get(bstack1l11_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧར")) if bstack11l11l11l1_opy_ and bstack111llll1ll_opy_ else self._111lllll1l_opy_
        except:
            pass
    @classmethod
    def bstack11l1lll11l_opy_(self, event: str, bstack11l111lll1_opy_: bstack11l111l11l_opy_, bstack111lll1l11_opy_=False):
        if event == bstack1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧལ"):
            bstack11l111lll1_opy_.set(hooks=self.store[bstack1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪཤ")])
        if event == bstack1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨཥ"):
            event = bstack1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪས")
        if bstack111lll1l11_opy_:
            bstack11l11l1lll_opy_ = {
                bstack1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ཧ"): event,
                bstack11l111lll1_opy_.bstack111llll111_opy_(): bstack11l111lll1_opy_.bstack111lllllll_opy_(event)
            }
            self.bstack11l1111l1l_opy_.append(bstack11l11l1lll_opy_)
        else:
            bstack1lll1lllll_opy_.bstack11l1lll11l_opy_(event, bstack11l111lll1_opy_)
class Messages:
    def __init__(self):
        self._11l1111l11_opy_ = []
    def bstack11l11lllll_opy_(self):
        self._11l1111l11_opy_.append([])
    def bstack111lllll11_opy_(self):
        return self._11l1111l11_opy_.pop() if self._11l1111l11_opy_ else list()
    def push(self, message):
        self._11l1111l11_opy_[-1].append(message) if self._11l1111l11_opy_ else self._11l1111l11_opy_.append([message])
class bstack111lll11l1_opy_:
    FAIL = bstack1l11_opy_ (u"ࠪࡊࡆࡏࡌࠨཨ")
    ERROR = bstack1l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪཀྵ")
    WARNING = bstack1l11_opy_ (u"ࠬ࡝ࡁࡓࡐࠪཪ")
    bstack11l111ll1l_opy_ = bstack1l11_opy_ (u"࠭ࡉࡏࡈࡒࠫཫ")
    DEBUG = bstack1l11_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭ཬ")
    TRACE = bstack1l11_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧ཭")
    bstack11l1111111_opy_ = [FAIL, ERROR]
def bstack11l11ll111_opy_(bstack11l111l1l1_opy_):
    if not bstack11l111l1l1_opy_:
        return None
    if bstack11l111l1l1_opy_.get(bstack1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ཮"), None):
        return getattr(bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭཯")], bstack1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ཰"), None)
    return bstack11l111l1l1_opy_.get(bstack1l11_opy_ (u"ࠬࡻࡵࡪࡦཱࠪ"), None)
def bstack111lll1l1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴིࠬ"), bstack1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ཱིࠩ")]:
        return
    if hook_type.lower() == bstack1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶུࠧ"):
        if current_test_uuid is None:
            return bstack1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑཱུ࠭")
        else:
            return bstack1l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨྲྀ")
    elif hook_type.lower() == bstack1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ཷ"):
        if current_test_uuid is None:
            return bstack1l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨླྀ")
        else:
            return bstack1l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪཹ")
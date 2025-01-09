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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11111111ll_opy_
from browserstack_sdk.bstack1l1l111ll1_opy_ import bstack11l11ll1l_opy_
def _1lll1l1ll1l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lll1l1l1ll_opy_:
    def __init__(self, handler):
        self._1lll1ll11l1_opy_ = {}
        self._1lll1l1llll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l11ll1l_opy_.version()
        if bstack11111111ll_opy_(pytest_version, bstack11l11_opy_ (u"ࠦ࠽࠴࠱࠯࠳ࠥᕦ")) >= 0:
            self._1lll1ll11l1_opy_[bstack11l11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᕧ")] = Module._register_setup_function_fixture
            self._1lll1ll11l1_opy_[bstack11l11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᕨ")] = Module._register_setup_module_fixture
            self._1lll1ll11l1_opy_[bstack11l11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᕩ")] = Class._register_setup_class_fixture
            self._1lll1ll11l1_opy_[bstack11l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᕪ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1lll1l1l111_opy_(bstack11l11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᕫ"))
            Module._register_setup_module_fixture = self.bstack1lll1l1l111_opy_(bstack11l11_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᕬ"))
            Class._register_setup_class_fixture = self.bstack1lll1l1l111_opy_(bstack11l11_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᕭ"))
            Class._register_setup_method_fixture = self.bstack1lll1l1l111_opy_(bstack11l11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᕮ"))
        else:
            self._1lll1ll11l1_opy_[bstack11l11_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᕯ")] = Module._inject_setup_function_fixture
            self._1lll1ll11l1_opy_[bstack11l11_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᕰ")] = Module._inject_setup_module_fixture
            self._1lll1ll11l1_opy_[bstack11l11_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᕱ")] = Class._inject_setup_class_fixture
            self._1lll1ll11l1_opy_[bstack11l11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᕲ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1lll1l1l111_opy_(bstack11l11_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᕳ"))
            Module._inject_setup_module_fixture = self.bstack1lll1l1l111_opy_(bstack11l11_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᕴ"))
            Class._inject_setup_class_fixture = self.bstack1lll1l1l111_opy_(bstack11l11_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᕵ"))
            Class._inject_setup_method_fixture = self.bstack1lll1l1l111_opy_(bstack11l11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᕶ"))
    def bstack1lll1l1lll1_opy_(self, bstack1lll1l11lll_opy_, hook_type):
        bstack1lll1ll11ll_opy_ = id(bstack1lll1l11lll_opy_.__class__)
        if (bstack1lll1ll11ll_opy_, hook_type) in self._1lll1l1llll_opy_:
            return
        meth = getattr(bstack1lll1l11lll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1lll1l1llll_opy_[(bstack1lll1ll11ll_opy_, hook_type)] = meth
            setattr(bstack1lll1l11lll_opy_, hook_type, self.bstack1lll1l1l11l_opy_(hook_type, bstack1lll1ll11ll_opy_))
    def bstack1lll1ll1lll_opy_(self, instance, bstack1lll1ll1111_opy_):
        if bstack1lll1ll1111_opy_ == bstack11l11_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᕷ"):
            self.bstack1lll1l1lll1_opy_(instance.obj, bstack11l11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᕸ"))
            self.bstack1lll1l1lll1_opy_(instance.obj, bstack11l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᕹ"))
        if bstack1lll1ll1111_opy_ == bstack11l11_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᕺ"):
            self.bstack1lll1l1lll1_opy_(instance.obj, bstack11l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥᕻ"))
            self.bstack1lll1l1lll1_opy_(instance.obj, bstack11l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢᕼ"))
        if bstack1lll1ll1111_opy_ == bstack11l11_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᕽ"):
            self.bstack1lll1l1lll1_opy_(instance.obj, bstack11l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧᕾ"))
            self.bstack1lll1l1lll1_opy_(instance.obj, bstack11l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤᕿ"))
        if bstack1lll1ll1111_opy_ == bstack11l11_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᖀ"):
            self.bstack1lll1l1lll1_opy_(instance.obj, bstack11l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤᖁ"))
            self.bstack1lll1l1lll1_opy_(instance.obj, bstack11l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨᖂ"))
    @staticmethod
    def bstack1lll1ll1l11_opy_(hook_type, func, args):
        if hook_type in [bstack11l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᖃ"), bstack11l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᖄ")]:
            _1lll1l1ll1l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1lll1l1l11l_opy_(self, hook_type, bstack1lll1ll11ll_opy_):
        def bstack1lll1ll1l1l_opy_(arg=None):
            self.handler(hook_type, bstack11l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᖅ"))
            result = None
            try:
                bstack1lll1l1ll11_opy_ = self._1lll1l1llll_opy_[(bstack1lll1ll11ll_opy_, hook_type)]
                self.bstack1lll1ll1l11_opy_(hook_type, bstack1lll1l1ll11_opy_, (arg,))
                result = Result(result=bstack11l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᖆ"))
            except Exception as e:
                result = Result(result=bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᖇ"), exception=e)
                self.handler(hook_type, bstack11l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᖈ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᖉ"), result)
        def bstack1lll1ll1ll1_opy_(this, arg=None):
            self.handler(hook_type, bstack11l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᖊ"))
            result = None
            exception = None
            try:
                self.bstack1lll1ll1l11_opy_(hook_type, self._1lll1l1llll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᖋ"))
            except Exception as e:
                result = Result(result=bstack11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᖌ"), exception=e)
                self.handler(hook_type, bstack11l11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᖍ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᖎ"), result)
        if hook_type in [bstack11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᖏ"), bstack11l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᖐ")]:
            return bstack1lll1ll1ll1_opy_
        return bstack1lll1ll1l1l_opy_
    def bstack1lll1l1l111_opy_(self, bstack1lll1ll1111_opy_):
        def bstack1lll1l1l1l1_opy_(this, *args, **kwargs):
            self.bstack1lll1ll1lll_opy_(this, bstack1lll1ll1111_opy_)
            self._1lll1ll11l1_opy_[bstack1lll1ll1111_opy_](this, *args, **kwargs)
        return bstack1lll1l1l1l1_opy_
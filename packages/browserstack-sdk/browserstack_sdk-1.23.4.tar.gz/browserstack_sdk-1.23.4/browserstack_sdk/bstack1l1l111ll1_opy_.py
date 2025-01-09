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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack111lll111l_opy_ as bstack1lll11ll_opy_
from browserstack_sdk.bstack1ll1111l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1lllll_opy_
class bstack11l11ll1l_opy_:
    def __init__(self, args, logger, bstack111ll11lll_opy_, bstack111ll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack111ll11lll_opy_ = bstack111ll11lll_opy_
        self.bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11ll11l11l_opy_ = []
        self.bstack111ll1lll1_opy_ = None
        self.bstack1ll1l11l11_opy_ = []
        self.bstack111ll111l1_opy_ = self.bstack1l111l1lll_opy_()
        self.bstack1llllllll1_opy_ = -1
    def bstack11lll11ll1_opy_(self, bstack111ll1111l_opy_):
        self.parse_args()
        self.bstack111lll1111_opy_()
        self.bstack111ll11111_opy_(bstack111ll1111l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111ll1llll_opy_():
        import importlib
        if getattr(importlib, bstack11l11_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶེࠬ"), False):
            bstack111ll11l11_opy_ = importlib.find_loader(bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ཻࠪ"))
        else:
            bstack111ll11l11_opy_ = importlib.util.find_spec(bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰོࠫ"))
    def bstack111ll1ll11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1llllllll1_opy_ = -1
        if self.bstack111ll11l1l_opy_ and bstack11l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ཽࠪ") in self.bstack111ll11lll_opy_:
            self.bstack1llllllll1_opy_ = int(self.bstack111ll11lll_opy_[bstack11l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫཾ")])
        try:
            bstack111ll1l111_opy_ = [bstack11l11_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧཿ"), bstack11l11_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴྀࠩ"), bstack11l11_opy_ (u"ࠧ࠮ࡲཱྀࠪ")]
            if self.bstack1llllllll1_opy_ >= 0:
                bstack111ll1l111_opy_.extend([bstack11l11_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩྂ"), bstack11l11_opy_ (u"ࠩ࠰ࡲࠬྃ")])
            for arg in bstack111ll1l111_opy_:
                self.bstack111ll1ll11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111lll1111_opy_(self):
        bstack111ll1lll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111ll1lll1_opy_ = bstack111ll1lll1_opy_
        return bstack111ll1lll1_opy_
    def bstack1ll11ll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111ll1llll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1lllll_opy_)
    def bstack111ll11111_opy_(self, bstack111ll1111l_opy_):
        bstack1111ll1l1_opy_ = Config.bstack1llll1lll_opy_()
        if bstack111ll1111l_opy_:
            self.bstack111ll1lll1_opy_.append(bstack11l11_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫྄ࠧ"))
            self.bstack111ll1lll1_opy_.append(bstack11l11_opy_ (u"࡙ࠫࡸࡵࡦࠩ྅"))
        if bstack1111ll1l1_opy_.bstack111ll11ll1_opy_():
            self.bstack111ll1lll1_opy_.append(bstack11l11_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ྆"))
            self.bstack111ll1lll1_opy_.append(bstack11l11_opy_ (u"࠭ࡔࡳࡷࡨࠫ྇"))
        self.bstack111ll1lll1_opy_.append(bstack11l11_opy_ (u"ࠧ࠮ࡲࠪྈ"))
        self.bstack111ll1lll1_opy_.append(bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ྉ"))
        self.bstack111ll1lll1_opy_.append(bstack11l11_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫྊ"))
        self.bstack111ll1lll1_opy_.append(bstack11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪྋ"))
        if self.bstack1llllllll1_opy_ > 1:
            self.bstack111ll1lll1_opy_.append(bstack11l11_opy_ (u"ࠫ࠲ࡴࠧྌ"))
            self.bstack111ll1lll1_opy_.append(str(self.bstack1llllllll1_opy_))
    def bstack111ll1l1ll_opy_(self):
        bstack1ll1l11l11_opy_ = []
        for spec in self.bstack11ll11l11l_opy_:
            bstack1ll1l11ll1_opy_ = [spec]
            bstack1ll1l11ll1_opy_ += self.bstack111ll1lll1_opy_
            bstack1ll1l11l11_opy_.append(bstack1ll1l11ll1_opy_)
        self.bstack1ll1l11l11_opy_ = bstack1ll1l11l11_opy_
        return bstack1ll1l11l11_opy_
    def bstack1l111l1lll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111ll111l1_opy_ = True
            return True
        except Exception as e:
            self.bstack111ll111l1_opy_ = False
        return self.bstack111ll111l1_opy_
    def bstack1ll1111l1l_opy_(self, bstack111ll1l1l1_opy_, bstack11lll11ll1_opy_):
        bstack11lll11ll1_opy_[bstack11l11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬྍ")] = self.bstack111ll11lll_opy_
        multiprocessing.set_start_method(bstack11l11_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬྎ"))
        bstack1ll11l1ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1ll11l11_opy_ = manager.list()
        if bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪྏ") in self.bstack111ll11lll_opy_:
            for index, platform in enumerate(self.bstack111ll11lll_opy_[bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫྐ")]):
                bstack1ll11l1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111ll1l1l1_opy_,
                                                            args=(self.bstack111ll1lll1_opy_, bstack11lll11ll1_opy_, bstack1l1ll11l11_opy_)))
            bstack111ll111ll_opy_ = len(self.bstack111ll11lll_opy_[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬྑ")])
        else:
            bstack1ll11l1ll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111ll1l1l1_opy_,
                                                        args=(self.bstack111ll1lll1_opy_, bstack11lll11ll1_opy_, bstack1l1ll11l11_opy_)))
            bstack111ll111ll_opy_ = 1
        i = 0
        for t in bstack1ll11l1ll_opy_:
            os.environ[bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪྒ")] = str(i)
            if bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧྒྷ") in self.bstack111ll11lll_opy_:
                os.environ[bstack11l11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ྔ")] = json.dumps(self.bstack111ll11lll_opy_[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩྕ")][i % bstack111ll111ll_opy_])
            i += 1
            t.start()
        for t in bstack1ll11l1ll_opy_:
            t.join()
        return list(bstack1l1ll11l11_opy_)
    @staticmethod
    def bstack1ll1l111_opy_(driver, bstack111ll1ll1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫྖ"), None)
        if item and getattr(item, bstack11l11_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࠪྗ"), None) and not getattr(item, bstack11l11_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡳࡵࡥࡤࡰࡰࡨࠫ྘"), False):
            logger.info(
                bstack11l11_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠤྙ"))
            bstack111ll1l11l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1lll11ll_opy_.bstack1ll1ll1l1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
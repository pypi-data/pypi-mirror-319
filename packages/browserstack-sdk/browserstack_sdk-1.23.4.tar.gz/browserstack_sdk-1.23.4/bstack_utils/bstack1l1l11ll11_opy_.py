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
class bstack1ll11lll11_opy_:
    def __init__(self, handler):
        self._1ll11l1l11l_opy_ = None
        self.handler = handler
        self._1ll11l11lll_opy_ = self.bstack1ll11l1l111_opy_()
        self.patch()
    def patch(self):
        self._1ll11l1l11l_opy_ = self._1ll11l11lll_opy_.execute
        self._1ll11l11lll_opy_.execute = self.bstack1ll11l11ll1_opy_()
    def bstack1ll11l11ll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᛡ"), driver_command, None, this, args)
            response = self._1ll11l1l11l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᛢ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11l11lll_opy_.execute = self._1ll11l1l11l_opy_
    @staticmethod
    def bstack1ll11l1l111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
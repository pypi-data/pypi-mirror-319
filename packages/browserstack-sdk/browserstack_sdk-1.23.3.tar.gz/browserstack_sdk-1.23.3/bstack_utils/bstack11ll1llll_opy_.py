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
class bstack1l1l1ll111_opy_:
    def __init__(self, handler):
        self._1ll11l1l111_opy_ = None
        self.handler = handler
        self._1ll11l11lll_opy_ = self.bstack1ll11l11ll1_opy_()
        self.patch()
    def patch(self):
        self._1ll11l1l111_opy_ = self._1ll11l11lll_opy_.execute
        self._1ll11l11lll_opy_.execute = self.bstack1ll11l1l11l_opy_()
    def bstack1ll11l1l11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᛡ"), driver_command, None, this, args)
            response = self._1ll11l1l111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᛢ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11l11lll_opy_.execute = self._1ll11l1l111_opy_
    @staticmethod
    def bstack1ll11l11ll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
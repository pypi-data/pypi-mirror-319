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
from collections import deque
from bstack_utils.constants import *
class bstack1lllll1lll_opy_:
    def __init__(self):
        self._1ll1l1lll11_opy_ = deque()
        self._1ll1l1l11ll_opy_ = {}
        self._1ll1l1l1l1l_opy_ = False
    def bstack1ll1l1l111l_opy_(self, test_name, bstack1ll1l1l1lll_opy_):
        bstack1ll1l1llll1_opy_ = self._1ll1l1l11ll_opy_.get(test_name, {})
        return bstack1ll1l1llll1_opy_.get(bstack1ll1l1l1lll_opy_, 0)
    def bstack1ll1l1ll111_opy_(self, test_name, bstack1ll1l1l1lll_opy_):
        bstack1ll1l1lll1l_opy_ = self.bstack1ll1l1l111l_opy_(test_name, bstack1ll1l1l1lll_opy_)
        self.bstack1ll1l1l1l11_opy_(test_name, bstack1ll1l1l1lll_opy_)
        return bstack1ll1l1lll1l_opy_
    def bstack1ll1l1l1l11_opy_(self, test_name, bstack1ll1l1l1lll_opy_):
        if test_name not in self._1ll1l1l11ll_opy_:
            self._1ll1l1l11ll_opy_[test_name] = {}
        bstack1ll1l1llll1_opy_ = self._1ll1l1l11ll_opy_[test_name]
        bstack1ll1l1lll1l_opy_ = bstack1ll1l1llll1_opy_.get(bstack1ll1l1l1lll_opy_, 0)
        bstack1ll1l1llll1_opy_[bstack1ll1l1l1lll_opy_] = bstack1ll1l1lll1l_opy_ + 1
    def bstack1l1111l111_opy_(self, bstack1ll1l1ll1ll_opy_, bstack1ll1l1l11l1_opy_):
        bstack1ll1l1ll1l1_opy_ = self.bstack1ll1l1ll111_opy_(bstack1ll1l1ll1ll_opy_, bstack1ll1l1l11l1_opy_)
        event_name = bstack1111l111ll_opy_[bstack1ll1l1l11l1_opy_]
        bstack1ll1l1l1ll1_opy_ = bstack11l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢᙸ").format(bstack1ll1l1ll1ll_opy_, event_name, bstack1ll1l1ll1l1_opy_)
        self._1ll1l1lll11_opy_.append(bstack1ll1l1l1ll1_opy_)
    def bstack11ll1l1l_opy_(self):
        return len(self._1ll1l1lll11_opy_) == 0
    def bstack1l1llll1ll_opy_(self):
        bstack1ll1l1ll11l_opy_ = self._1ll1l1lll11_opy_.popleft()
        return bstack1ll1l1ll11l_opy_
    def capturing(self):
        return self._1ll1l1l1l1l_opy_
    def bstack1l1111ll_opy_(self):
        self._1ll1l1l1l1l_opy_ = True
    def bstack11ll1111ll_opy_(self):
        self._1ll1l1l1l1l_opy_ = False
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
import builtins
import logging
class bstack11l1llll1l_opy_:
    def __init__(self, handler):
        self._1111ll1111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1111l1llll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩၳ"), bstack1l11_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫၴ"), bstack1l11_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧၵ"), bstack1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ၶ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1111l1ll1l_opy_
        self._1111ll111l_opy_()
    def _1111l1ll1l_opy_(self, *args, **kwargs):
        self._1111ll1111_opy_(*args, **kwargs)
        message = bstack1l11_opy_ (u"ࠨࠢࠪၷ").join(map(str, args)) + bstack1l11_opy_ (u"ࠩ࡟ࡲࠬၸ")
        self._log_message(bstack1l11_opy_ (u"ࠪࡍࡓࡌࡏࠨၹ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪၺ"): level, bstack1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ၻ"): msg})
    def _1111ll111l_opy_(self):
        for level, bstack1111l1ll11_opy_ in self._1111l1llll_opy_.items():
            setattr(logging, level, self._1111l1lll1_opy_(level, bstack1111l1ll11_opy_))
    def _1111l1lll1_opy_(self, level, bstack1111l1ll11_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1111l1ll11_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1111ll1111_opy_
        for level, bstack1111l1ll11_opy_ in self._1111l1llll_opy_.items():
            setattr(logging, level, bstack1111l1ll11_opy_)
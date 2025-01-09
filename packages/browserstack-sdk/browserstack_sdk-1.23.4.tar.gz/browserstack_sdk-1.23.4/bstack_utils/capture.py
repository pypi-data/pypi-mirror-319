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
import builtins
import logging
class bstack11l1ll111l_opy_:
    def __init__(self, handler):
        self._1111ll111l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1111l1llll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩၳ"), bstack11l11_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫၴ"), bstack11l11_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧၵ"), bstack11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ၶ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1111l1ll1l_opy_
        self._1111l1lll1_opy_()
    def _1111l1ll1l_opy_(self, *args, **kwargs):
        self._1111ll111l_opy_(*args, **kwargs)
        message = bstack11l11_opy_ (u"ࠨࠢࠪၷ").join(map(str, args)) + bstack11l11_opy_ (u"ࠩ࡟ࡲࠬၸ")
        self._log_message(bstack11l11_opy_ (u"ࠪࡍࡓࡌࡏࠨၹ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪၺ"): level, bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ၻ"): msg})
    def _1111l1lll1_opy_(self):
        for level, bstack1111ll1111_opy_ in self._1111l1llll_opy_.items():
            setattr(logging, level, self._1111l1ll11_opy_(level, bstack1111ll1111_opy_))
    def _1111l1ll11_opy_(self, level, bstack1111ll1111_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1111ll1111_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1111ll111l_opy_
        for level, bstack1111ll1111_opy_ in self._1111l1llll_opy_.items():
            setattr(logging, level, bstack1111ll1111_opy_)
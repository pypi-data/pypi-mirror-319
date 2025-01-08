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
class RobotHandler():
    def __init__(self, args, logger, bstack111lll111l_opy_, bstack111ll11111_opy_):
        self.args = args
        self.logger = logger
        self.bstack111lll111l_opy_ = bstack111lll111l_opy_
        self.bstack111ll11111_opy_ = bstack111ll11111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l1111ll1_opy_(bstack111l1llll1_opy_):
        bstack111l1lllll_opy_ = []
        if bstack111l1llll1_opy_:
            tokens = str(os.path.basename(bstack111l1llll1_opy_)).split(bstack1l11_opy_ (u"ࠦࡤࠨྚ"))
            camelcase_name = bstack1l11_opy_ (u"ࠧࠦࠢྛ").join(t.title() for t in tokens)
            suite_name, bstack111l1lll11_opy_ = os.path.splitext(camelcase_name)
            bstack111l1lllll_opy_.append(suite_name)
        return bstack111l1lllll_opy_
    @staticmethod
    def bstack111l1lll1l_opy_(typename):
        if bstack1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤྜ") in typename:
            return bstack1l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣྜྷ")
        return bstack1l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤྞ")
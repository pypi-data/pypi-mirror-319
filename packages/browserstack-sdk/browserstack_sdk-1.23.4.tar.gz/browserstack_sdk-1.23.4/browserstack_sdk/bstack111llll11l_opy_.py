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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack111ll11lll_opy_, bstack111ll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack111ll11lll_opy_ = bstack111ll11lll_opy_
        self.bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l11l1l11_opy_(bstack111l1lllll_opy_):
        bstack111l1lll11_opy_ = []
        if bstack111l1lllll_opy_:
            tokens = str(os.path.basename(bstack111l1lllll_opy_)).split(bstack11l11_opy_ (u"ࠦࡤࠨྚ"))
            camelcase_name = bstack11l11_opy_ (u"ࠧࠦࠢྛ").join(t.title() for t in tokens)
            suite_name, bstack111l1lll1l_opy_ = os.path.splitext(camelcase_name)
            bstack111l1lll11_opy_.append(suite_name)
        return bstack111l1lll11_opy_
    @staticmethod
    def bstack111l1llll1_opy_(typename):
        if bstack11l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤྜ") in typename:
            return bstack11l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣྜྷ")
        return bstack11l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤྞ")
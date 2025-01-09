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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11llll1ll1_opy_ import get_logger
from bstack_utils.bstack1111l1l11_opy_ import bstack111l1l1l1l_opy_
bstack1111l1l11_opy_ = bstack111l1l1l1l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack111lll111_opy_: Optional[str] = None):
    bstack11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡈࡪࡩ࡯ࡳࡣࡷࡳࡷࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡴࡩࡧࠣࡷࡹࡧࡲࡵࠢࡷ࡭ࡲ࡫ࠠࡰࡨࠣࡥࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠍࠤࠥࠦࠠࡢ࡮ࡲࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᖹ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack111l1l11l1_opy_: str = bstack1111l1l11_opy_.bstack111l1l1l11_opy_(label)
            start_mark: str = label + bstack11l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᖺ")
            end_mark: str = label + bstack11l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᖻ")
            result = None
            try:
                if stage.value == STAGE.bstack11lll1ll_opy_.value:
                    bstack1111l1l11_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1111l1l11_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack111lll111_opy_)
                elif stage.value == STAGE.SINGLE.value:
                    start_mark: str = bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᖼ")
                    end_mark: str = bstack111l1l11l1_opy_ + bstack11l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᖽ")
                    bstack1111l1l11_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1111l1l11_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack111lll111_opy_)
            except Exception as e:
                bstack1111l1l11_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack111lll111_opy_)
            return result
        return wrapper
    return decorator
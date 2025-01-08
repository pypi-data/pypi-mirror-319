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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11l111l1_opy_ import get_logger
from bstack_utils.bstack11ll1lllll_opy_ import bstack111l1111l1_opy_
bstack11ll1lllll_opy_ = bstack111l1111l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11l111lll_opy_: Optional[str] = None):
    bstack1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡈࡪࡩ࡯ࡳࡣࡷࡳࡷࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡴࡩࡧࠣࡷࡹࡧࡲࡵࠢࡷ࡭ࡲ࡫ࠠࡰࡨࠣࡥࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠍࠤࠥࠦࠠࡢ࡮ࡲࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᖹ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack111l111l11_opy_: str = bstack11ll1lllll_opy_.bstack111l1111ll_opy_(label)
            start_mark: str = label + bstack1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᖺ")
            end_mark: str = label + bstack1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᖻ")
            result = None
            try:
                if stage.value == STAGE.bstack1lllll11l_opy_.value:
                    bstack11ll1lllll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11ll1lllll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11l111lll_opy_)
                elif stage.value == STAGE.SINGLE.value:
                    start_mark: str = bstack111l111l11_opy_ + bstack1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᖼ")
                    end_mark: str = bstack111l111l11_opy_ + bstack1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᖽ")
                    bstack11ll1lllll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11ll1lllll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11l111lll_opy_)
            except Exception as e:
                bstack11ll1lllll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11l111lll_opy_)
            return result
        return wrapper
    return decorator
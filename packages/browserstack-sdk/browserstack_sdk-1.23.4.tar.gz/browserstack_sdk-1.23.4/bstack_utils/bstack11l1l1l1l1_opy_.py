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
from uuid import uuid4
from bstack_utils.helper import bstack1ll1l1l11l_opy_, bstack1llll1ll111_opy_
from bstack_utils.bstack11l1llll1_opy_ import bstack1ll11lll1ll_opy_
class bstack111lllll11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11l1l111ll_opy_=None, framework=None, tags=[], scope=[], bstack1ll111l1lll_opy_=None, bstack1ll111ll111_opy_=True, bstack1ll111lllll_opy_=None, bstack11lll11l1l_opy_=None, result=None, duration=None, bstack11l1l1111l_opy_=None, meta={}):
        self.bstack11l1l1111l_opy_ = bstack11l1l1111l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll111ll111_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11l1l111ll_opy_ = bstack11l1l111ll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll111l1lll_opy_ = bstack1ll111l1lll_opy_
        self.bstack1ll111lllll_opy_ = bstack1ll111lllll_opy_
        self.bstack11lll11l1l_opy_ = bstack11lll11l1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack11l11ll111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l1ll1l11_opy_(self, meta):
        self.meta = meta
    def bstack11l1ll11l1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll111ll11l_opy_(self):
        bstack1ll111l1l11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭᜗"): bstack1ll111l1l11_opy_,
            bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭᜘"): bstack1ll111l1l11_opy_,
            bstack11l11_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ᜙"): bstack1ll111l1l11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l11_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢ᜚") + key)
            setattr(self, key, val)
    def bstack1ll11l11111_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᜛"): self.name,
            bstack11l11_opy_ (u"ࠨࡤࡲࡨࡾ࠭᜜"): {
                bstack11l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ᜝"): bstack11l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ᜞"),
                bstack11l11_opy_ (u"ࠫࡨࡵࡤࡦࠩᜟ"): self.code
            },
            bstack11l11_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᜠ"): self.scope,
            bstack11l11_opy_ (u"࠭ࡴࡢࡩࡶࠫᜡ"): self.tags,
            bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᜢ"): self.framework,
            bstack11l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᜣ"): self.bstack11l1l111ll_opy_
        }
    def bstack1ll111llll1_opy_(self):
        return {
         bstack11l11_opy_ (u"ࠩࡰࡩࡹࡧࠧᜤ"): self.meta
        }
    def bstack1ll111lll1l_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᜥ"): {
                bstack11l11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᜦ"): self.bstack1ll111l1lll_opy_
            }
        }
    def bstack1ll11l1111l_opy_(self, bstack1ll111lll11_opy_, details):
        step = next(filter(lambda st: st[bstack11l11_opy_ (u"ࠬ࡯ࡤࠨᜧ")] == bstack1ll111lll11_opy_, self.meta[bstack11l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᜨ")]), None)
        step.update(details)
    def bstack11lll1l1l_opy_(self, bstack1ll111lll11_opy_):
        step = next(filter(lambda st: st[bstack11l11_opy_ (u"ࠧࡪࡦࠪᜩ")] == bstack1ll111lll11_opy_, self.meta[bstack11l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᜪ")]), None)
        step.update({
            bstack11l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᜫ"): bstack1ll1l1l11l_opy_()
        })
    def bstack11l1l11ll1_opy_(self, bstack1ll111lll11_opy_, result, duration=None):
        bstack1ll111lllll_opy_ = bstack1ll1l1l11l_opy_()
        if bstack1ll111lll11_opy_ is not None and self.meta.get(bstack11l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᜬ")):
            step = next(filter(lambda st: st[bstack11l11_opy_ (u"ࠫ࡮ࡪࠧᜭ")] == bstack1ll111lll11_opy_, self.meta[bstack11l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᜮ")]), None)
            step.update({
                bstack11l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᜯ"): bstack1ll111lllll_opy_,
                bstack11l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᜰ"): duration if duration else bstack1llll1ll111_opy_(step[bstack11l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᜱ")], bstack1ll111lllll_opy_),
                bstack11l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᜲ"): result.result,
                bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᜳ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll111l1111_opy_):
        if self.meta.get(bstack11l11_opy_ (u"ࠫࡸࡺࡥࡱࡵ᜴ࠪ")):
            self.meta[bstack11l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᜵")].append(bstack1ll111l1111_opy_)
        else:
            self.meta[bstack11l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ᜶")] = [ bstack1ll111l1111_opy_ ]
    def bstack1ll111l111l_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᜷"): self.bstack11l11ll111_opy_(),
            **self.bstack1ll11l11111_opy_(),
            **self.bstack1ll111ll11l_opy_(),
            **self.bstack1ll111llll1_opy_()
        }
    def bstack1ll111l11ll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᜸"): self.bstack1ll111lllll_opy_,
            bstack11l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ᜹"): self.duration,
            bstack11l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᜺"): self.result.result
        }
        if data[bstack11l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᜻")] == bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᜼"):
            data[bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ᜽")] = self.result.bstack111l1llll1_opy_()
            data[bstack11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ᜾")] = [{bstack11l11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ᜿"): self.result.bstack1lllll1111l_opy_()}]
        return data
    def bstack1ll111ll1ll_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᝀ"): self.bstack11l11ll111_opy_(),
            **self.bstack1ll11l11111_opy_(),
            **self.bstack1ll111ll11l_opy_(),
            **self.bstack1ll111l11ll_opy_(),
            **self.bstack1ll111llll1_opy_()
        }
    def bstack11l111ll1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l11_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᝁ") in event:
            return self.bstack1ll111l111l_opy_()
        elif bstack11l11_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᝂ") in event:
            return self.bstack1ll111ll1ll_opy_()
    def bstack11l11l111l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll111lllll_opy_ = time if time else bstack1ll1l1l11l_opy_()
        self.duration = duration if duration else bstack1llll1ll111_opy_(self.bstack11l1l111ll_opy_, self.bstack1ll111lllll_opy_)
        if result:
            self.result = result
class bstack11l1ll1lll_opy_(bstack111lllll11_opy_):
    def __init__(self, hooks=[], bstack11l1lll11l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l1lll11l_opy_ = bstack11l1lll11l_opy_
        super().__init__(*args, **kwargs, bstack11lll11l1l_opy_=bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࠪᝃ"))
    @classmethod
    def bstack1ll111l1ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l11_opy_ (u"࠭ࡩࡥࠩᝄ"): id(step),
                bstack11l11_opy_ (u"ࠧࡵࡧࡻࡸࠬᝅ"): step.name,
                bstack11l11_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᝆ"): step.keyword,
            })
        return bstack11l1ll1lll_opy_(
            **kwargs,
            meta={
                bstack11l11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᝇ"): {
                    bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᝈ"): feature.name,
                    bstack11l11_opy_ (u"ࠫࡵࡧࡴࡩࠩᝉ"): feature.filename,
                    bstack11l11_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᝊ"): feature.description
                },
                bstack11l11_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᝋ"): {
                    bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᝌ"): scenario.name
                },
                bstack11l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᝍ"): steps,
                bstack11l11_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᝎ"): bstack1ll11lll1ll_opy_(test)
            }
        )
    def bstack1ll111ll1l1_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᝏ"): self.hooks
        }
    def bstack1ll111l11l1_opy_(self):
        if self.bstack11l1lll11l_opy_:
            return {
                bstack11l11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᝐ"): self.bstack11l1lll11l_opy_
            }
        return {}
    def bstack1ll111ll1ll_opy_(self):
        return {
            **super().bstack1ll111ll1ll_opy_(),
            **self.bstack1ll111ll1l1_opy_()
        }
    def bstack1ll111l111l_opy_(self):
        return {
            **super().bstack1ll111l111l_opy_(),
            **self.bstack1ll111l11l1_opy_()
        }
    def bstack11l11l111l_opy_(self):
        return bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᝑ")
class bstack11l1l1lll1_opy_(bstack111lllll11_opy_):
    def __init__(self, hook_type, *args,bstack11l1lll11l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll111l1l1l_opy_ = None
        self.bstack11l1lll11l_opy_ = bstack11l1lll11l_opy_
        super().__init__(*args, **kwargs, bstack11lll11l1l_opy_=bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᝒ"))
    def bstack111lll1l1l_opy_(self):
        return self.hook_type
    def bstack1ll1111llll_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᝓ"): self.hook_type
        }
    def bstack1ll111ll1ll_opy_(self):
        return {
            **super().bstack1ll111ll1ll_opy_(),
            **self.bstack1ll1111llll_opy_()
        }
    def bstack1ll111l111l_opy_(self):
        return {
            **super().bstack1ll111l111l_opy_(),
            bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭᝔"): self.bstack1ll111l1l1l_opy_,
            **self.bstack1ll1111llll_opy_()
        }
    def bstack11l11l111l_opy_(self):
        return bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ᝕")
    def bstack11l1l11l1l_opy_(self, bstack1ll111l1l1l_opy_):
        self.bstack1ll111l1l1l_opy_ = bstack1ll111l1l1l_opy_
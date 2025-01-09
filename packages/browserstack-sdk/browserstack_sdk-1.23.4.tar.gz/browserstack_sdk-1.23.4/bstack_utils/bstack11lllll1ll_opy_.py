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
import json
class bstack1111ll1l11_opy_(object):
  bstack1l1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠩࢁࠫၕ")), bstack11l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪၖ"))
  bstack1111ll1lll_opy_ = os.path.join(bstack1l1lll1lll_opy_, bstack11l11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫၗ"))
  bstack1111ll11ll_opy_ = None
  perform_scan = None
  bstack1l11lll11_opy_ = None
  bstack1lll11l1l_opy_ = None
  bstack111l1l11ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l11_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧၘ")):
      cls.instance = super(bstack1111ll1l11_opy_, cls).__new__(cls)
      cls.instance.bstack1111ll1l1l_opy_()
    return cls.instance
  def bstack1111ll1l1l_opy_(self):
    try:
      with open(self.bstack1111ll1lll_opy_, bstack11l11_opy_ (u"࠭ࡲࠨၙ")) as bstack11ll11ll1_opy_:
        bstack1111ll1ll1_opy_ = bstack11ll11ll1_opy_.read()
        data = json.loads(bstack1111ll1ll1_opy_)
        if bstack11l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩၚ") in data:
          self.bstack111l1l1lll_opy_(data[bstack11l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪၛ")])
        if bstack11l11_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪၜ") in data:
          self.bstack111l111111_opy_(data[bstack11l11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫၝ")])
    except:
      pass
  def bstack111l111111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11l11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩၞ")]
      self.bstack1l11lll11_opy_ = scripts[bstack11l11_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩၟ")]
      self.bstack1lll11l1l_opy_ = scripts[bstack11l11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪၠ")]
      self.bstack111l1l11ll_opy_ = scripts[bstack11l11_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬၡ")]
  def bstack111l1l1lll_opy_(self, bstack1111ll11ll_opy_):
    if bstack1111ll11ll_opy_ != None and len(bstack1111ll11ll_opy_) != 0:
      self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
  def store(self):
    try:
      with open(self.bstack1111ll1lll_opy_, bstack11l11_opy_ (u"ࠨࡹࠪၢ")) as file:
        json.dump({
          bstack11l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦၣ"): self.bstack1111ll11ll_opy_,
          bstack11l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦၤ"): {
            bstack11l11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤၥ"): self.perform_scan,
            bstack11l11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤၦ"): self.bstack1l11lll11_opy_,
            bstack11l11_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥၧ"): self.bstack1lll11l1l_opy_,
            bstack11l11_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧၨ"): self.bstack111l1l11ll_opy_
          }
        }, file)
    except:
      pass
  def bstack111ll1l1l_opy_(self, bstack1111ll11l1_opy_):
    try:
      return any(command.get(bstack11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ၩ")) == bstack1111ll11l1_opy_ for command in self.bstack1111ll11ll_opy_)
    except:
      return False
bstack11lllll1ll_opy_ = bstack1111ll1l11_opy_()
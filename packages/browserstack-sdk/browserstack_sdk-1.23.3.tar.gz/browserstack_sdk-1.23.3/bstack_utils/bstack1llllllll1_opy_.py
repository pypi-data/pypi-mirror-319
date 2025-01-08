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
import json
class bstack1111ll11ll_opy_(object):
  bstack11llllllll_opy_ = os.path.join(os.path.expanduser(bstack1l11_opy_ (u"ࠩࢁࠫၕ")), bstack1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪၖ"))
  bstack1111ll11l1_opy_ = os.path.join(bstack11llllllll_opy_, bstack1l11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫၗ"))
  bstack1111ll1ll1_opy_ = None
  perform_scan = None
  bstack1l1111l11l_opy_ = None
  bstack1l1l111ll1_opy_ = None
  bstack111l1l1ll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l11_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧၘ")):
      cls.instance = super(bstack1111ll11ll_opy_, cls).__new__(cls)
      cls.instance.bstack1111ll1l11_opy_()
    return cls.instance
  def bstack1111ll1l11_opy_(self):
    try:
      with open(self.bstack1111ll11l1_opy_, bstack1l11_opy_ (u"࠭ࡲࠨၙ")) as bstack1llllll1ll_opy_:
        bstack1111ll1lll_opy_ = bstack1llllll1ll_opy_.read()
        data = json.loads(bstack1111ll1lll_opy_)
        if bstack1l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩၚ") in data:
          self.bstack1111llll1l_opy_(data[bstack1l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪၛ")])
        if bstack1l11_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪၜ") in data:
          self.bstack111l111111_opy_(data[bstack1l11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫၝ")])
    except:
      pass
  def bstack111l111111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1l11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩၞ")]
      self.bstack1l1111l11l_opy_ = scripts[bstack1l11_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩၟ")]
      self.bstack1l1l111ll1_opy_ = scripts[bstack1l11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪၠ")]
      self.bstack111l1l1ll1_opy_ = scripts[bstack1l11_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬၡ")]
  def bstack1111llll1l_opy_(self, bstack1111ll1ll1_opy_):
    if bstack1111ll1ll1_opy_ != None and len(bstack1111ll1ll1_opy_) != 0:
      self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
  def store(self):
    try:
      with open(self.bstack1111ll11l1_opy_, bstack1l11_opy_ (u"ࠨࡹࠪၢ")) as file:
        json.dump({
          bstack1l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦၣ"): self.bstack1111ll1ll1_opy_,
          bstack1l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦၤ"): {
            bstack1l11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤၥ"): self.perform_scan,
            bstack1l11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤၦ"): self.bstack1l1111l11l_opy_,
            bstack1l11_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥၧ"): self.bstack1l1l111ll1_opy_,
            bstack1l11_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧၨ"): self.bstack111l1l1ll1_opy_
          }
        }, file)
    except:
      pass
  def bstack1ll1lll1l_opy_(self, bstack1111ll1l1l_opy_):
    try:
      return any(command.get(bstack1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ၩ")) == bstack1111ll1l1l_opy_ for command in self.bstack1111ll1ll1_opy_)
    except:
      return False
bstack1llllllll1_opy_ = bstack1111ll11ll_opy_()
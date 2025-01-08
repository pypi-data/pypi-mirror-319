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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l11ll1l11_opy_, bstack1l11ll111_opy_
from bstack_utils.measure import measure
class bstack1lllll11ll_opy_:
  working_dir = os.getcwd()
  bstack11lll1ll1_opy_ = False
  config = {}
  binary_path = bstack1l11_opy_ (u"ࠩࠪᘅ")
  bstack1lll1111lll_opy_ = bstack1l11_opy_ (u"ࠪࠫᘆ")
  bstack1111lll1_opy_ = False
  bstack1ll1ll1l1ll_opy_ = None
  bstack1lll11l111l_opy_ = {}
  bstack1ll1ll1llll_opy_ = 300
  bstack1ll1ll1ll11_opy_ = False
  logger = None
  bstack1lll111l1ll_opy_ = False
  bstack1ll1l1l1_opy_ = False
  bstack11l1l111l_opy_ = None
  bstack1ll1l1lllll_opy_ = bstack1l11_opy_ (u"ࠫࠬᘇ")
  bstack1ll1llllll1_opy_ = {
    bstack1l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᘈ") : 1,
    bstack1l11_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᘉ") : 2,
    bstack1l11_opy_ (u"ࠧࡦࡦࡪࡩࠬᘊ") : 3,
    bstack1l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᘋ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1ll1lll11ll_opy_(self):
    bstack1lll1111l1l_opy_ = bstack1l11_opy_ (u"ࠩࠪᘌ")
    bstack1ll1ll11111_opy_ = sys.platform
    bstack1ll1ll11l1l_opy_ = bstack1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᘍ")
    if re.match(bstack1l11_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᘎ"), bstack1ll1ll11111_opy_) != None:
      bstack1lll1111l1l_opy_ = bstack1111l11l11_opy_ + bstack1l11_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᘏ")
      self.bstack1ll1l1lllll_opy_ = bstack1l11_opy_ (u"࠭࡭ࡢࡥࠪᘐ")
    elif re.match(bstack1l11_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧᘑ"), bstack1ll1ll11111_opy_) != None:
      bstack1lll1111l1l_opy_ = bstack1111l11l11_opy_ + bstack1l11_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤᘒ")
      bstack1ll1ll11l1l_opy_ = bstack1l11_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧᘓ")
      self.bstack1ll1l1lllll_opy_ = bstack1l11_opy_ (u"ࠪࡻ࡮ࡴࠧᘔ")
    else:
      bstack1lll1111l1l_opy_ = bstack1111l11l11_opy_ + bstack1l11_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᘕ")
      self.bstack1ll1l1lllll_opy_ = bstack1l11_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᘖ")
    return bstack1lll1111l1l_opy_, bstack1ll1ll11l1l_opy_
  def bstack1ll1lll1l1l_opy_(self):
    try:
      bstack1ll1ll11ll1_opy_ = [os.path.join(expanduser(bstack1l11_opy_ (u"ࠨࡾࠣᘗ")), bstack1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᘘ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1ll1ll11ll1_opy_:
        if(self.bstack1ll1llll1ll_opy_(path)):
          return path
      raise bstack1l11_opy_ (u"ࠣࡗࡱࡥࡱࡨࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᘙ")
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᘚ").format(e))
  def bstack1ll1llll1ll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  @measure(event_name=EVENTS.bstack1111l11111_opy_, stage=STAGE.SINGLE)
  def bstack1ll1ll1lll1_opy_(self, bstack1lll1111l1l_opy_, bstack1ll1ll11l1l_opy_):
    try:
      bstack1lll11l1111_opy_ = self.bstack1ll1lll1l1l_opy_()
      bstack1lll111ll11_opy_ = os.path.join(bstack1lll11l1111_opy_, bstack1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭ᘛ"))
      bstack1lll111lll1_opy_ = os.path.join(bstack1lll11l1111_opy_, bstack1ll1ll11l1l_opy_)
      if os.path.exists(bstack1lll111lll1_opy_):
        self.logger.info(bstack1l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᘜ").format(bstack1lll111lll1_opy_))
        return bstack1lll111lll1_opy_
      if os.path.exists(bstack1lll111ll11_opy_):
        self.logger.info(bstack1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥᘝ").format(bstack1lll111ll11_opy_))
        return self.bstack1lll111111l_opy_(bstack1lll111ll11_opy_, bstack1ll1ll11l1l_opy_)
      self.logger.info(bstack1l11_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦᘞ").format(bstack1lll1111l1l_opy_))
      response = bstack1l11ll111_opy_(bstack1l11_opy_ (u"ࠧࡈࡇࡗࠫᘟ"), bstack1lll1111l1l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1lll111ll11_opy_, bstack1l11_opy_ (u"ࠨࡹࡥࠫᘠ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l11_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢᘡ").format(bstack1lll111ll11_opy_))
        return self.bstack1lll111111l_opy_(bstack1lll111ll11_opy_, bstack1ll1ll11l1l_opy_)
      else:
        raise(bstack1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨᘢ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧᘣ").format(e))
  def bstack1lll111l111_opy_(self, bstack1lll1111l1l_opy_, bstack1ll1ll11l1l_opy_):
    try:
      retry = 2
      bstack1lll111lll1_opy_ = None
      bstack1ll1ll1ll1l_opy_ = False
      while retry > 0:
        bstack1lll111lll1_opy_ = self.bstack1ll1ll1lll1_opy_(bstack1lll1111l1l_opy_, bstack1ll1ll11l1l_opy_)
        bstack1ll1ll1ll1l_opy_ = self.bstack1ll1ll1l1l1_opy_(bstack1lll1111l1l_opy_, bstack1ll1ll11l1l_opy_, bstack1lll111lll1_opy_)
        if bstack1ll1ll1ll1l_opy_:
          break
        retry -= 1
      return bstack1lll111lll1_opy_, bstack1ll1ll1ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤᘤ").format(e))
    return bstack1lll111lll1_opy_, False
  def bstack1ll1ll1l1l1_opy_(self, bstack1lll1111l1l_opy_, bstack1ll1ll11l1l_opy_, bstack1lll111lll1_opy_, bstack1lll1111111_opy_ = 0):
    if bstack1lll1111111_opy_ > 1:
      return False
    if bstack1lll111lll1_opy_ == None or os.path.exists(bstack1lll111lll1_opy_) == False:
      self.logger.warn(bstack1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᘥ"))
      return False
    bstack1ll1lllll11_opy_ = bstack1l11_opy_ (u"ࠢ࡟࠰࠭ࡄࡵ࡫ࡲࡤࡻ࡟࠳ࡨࡲࡩࠡ࡞ࡧ࠲ࡡࡪࠫ࠯࡞ࡧ࠯ࠧᘦ")
    command = bstack1l11_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧᘧ").format(bstack1lll111lll1_opy_)
    bstack1ll1ll11l11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1ll1lllll11_opy_, bstack1ll1ll11l11_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣᘨ"))
      return False
  def bstack1lll111111l_opy_(self, bstack1lll111ll11_opy_, bstack1ll1ll11l1l_opy_):
    try:
      working_dir = os.path.dirname(bstack1lll111ll11_opy_)
      shutil.unpack_archive(bstack1lll111ll11_opy_, working_dir)
      bstack1lll111lll1_opy_ = os.path.join(working_dir, bstack1ll1ll11l1l_opy_)
      os.chmod(bstack1lll111lll1_opy_, 0o755)
      return bstack1lll111lll1_opy_
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᘩ"))
  def bstack1ll1ll11lll_opy_(self):
    try:
      bstack1ll1llll1l1_opy_ = self.config.get(bstack1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᘪ"))
      bstack1ll1ll11lll_opy_ = bstack1ll1llll1l1_opy_ or (bstack1ll1llll1l1_opy_ is None and self.bstack11lll1ll1_opy_)
      if not bstack1ll1ll11lll_opy_ or self.config.get(bstack1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᘫ"), None) not in bstack11111l11l1_opy_:
        return False
      self.bstack1111lll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᘬ").format(e))
  def bstack1ll1ll111ll_opy_(self):
    try:
      bstack1ll1ll111ll_opy_ = self.bstack1lll1111l11_opy_
      return bstack1ll1ll111ll_opy_
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺࠢࡦࡥࡵࡺࡵࡳࡧࠣࡱࡴࡪࡥ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᘭ").format(e))
  def init(self, bstack11lll1ll1_opy_, config, logger):
    self.bstack11lll1ll1_opy_ = bstack11lll1ll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1ll1ll11lll_opy_():
      return
    self.bstack1lll11l111l_opy_ = config.get(bstack1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᘮ"), {})
    self.bstack1lll1111l11_opy_ = config.get(bstack1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᘯ"))
    try:
      bstack1lll1111l1l_opy_, bstack1ll1ll11l1l_opy_ = self.bstack1ll1lll11ll_opy_()
      bstack1lll111lll1_opy_, bstack1ll1ll1ll1l_opy_ = self.bstack1lll111l111_opy_(bstack1lll1111l1l_opy_, bstack1ll1ll11l1l_opy_)
      if bstack1ll1ll1ll1l_opy_:
        self.binary_path = bstack1lll111lll1_opy_
        thread = Thread(target=self.bstack1ll1lll11l1_opy_)
        thread.start()
      else:
        self.bstack1lll111l1ll_opy_ = True
        self.logger.error(bstack1l11_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢᘰ").format(bstack1lll111lll1_opy_))
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᘱ").format(e))
  def bstack1ll1ll1l11l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l11_opy_ (u"ࠬࡲ࡯ࡨࠩᘲ"), bstack1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩᘳ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l11_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦᘴ").format(logfile))
      self.bstack1lll1111lll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᘵ").format(e))
  @measure(event_name=EVENTS.bstack11111ll111_opy_, stage=STAGE.SINGLE)
  def bstack1ll1lll11l1_opy_(self):
    bstack1ll1lll1ll1_opy_ = self.bstack1ll1lll1l11_opy_()
    if bstack1ll1lll1ll1_opy_ == None:
      self.bstack1lll111l1ll_opy_ = True
      self.logger.error(bstack1l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧᘶ"))
      return False
    command_args = [bstack1l11_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦᘷ") if self.bstack11lll1ll1_opy_ else bstack1l11_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨᘸ")]
    bstack1ll1ll1111l_opy_ = self.bstack1lll11111l1_opy_()
    if bstack1ll1ll1111l_opy_ != None:
      command_args.append(bstack1l11_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦᘹ").format(bstack1ll1ll1111l_opy_))
    env = os.environ.copy()
    env[bstack1l11_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦᘺ")] = bstack1ll1lll1ll1_opy_
    env[bstack1l11_opy_ (u"ࠢࡕࡊࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠢᘻ")] = os.environ.get(bstack1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᘼ"), bstack1l11_opy_ (u"ࠩࠪᘽ"))
    bstack1ll1ll111l1_opy_ = [self.binary_path]
    self.bstack1ll1ll1l11l_opy_()
    self.bstack1ll1ll1l1ll_opy_ = self.bstack1lll11l11ll_opy_(bstack1ll1ll111l1_opy_ + command_args, env)
    self.logger.debug(bstack1l11_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦᘾ"))
    bstack1lll1111111_opy_ = 0
    while self.bstack1ll1ll1l1ll_opy_.poll() == None:
      bstack1ll1llll11l_opy_ = self.bstack1lll111llll_opy_()
      if bstack1ll1llll11l_opy_:
        self.logger.debug(bstack1l11_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢᘿ"))
        self.bstack1ll1ll1ll11_opy_ = True
        return True
      bstack1lll1111111_opy_ += 1
      self.logger.debug(bstack1l11_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣᙀ").format(bstack1lll1111111_opy_))
      time.sleep(2)
    self.logger.error(bstack1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦᙁ").format(bstack1lll1111111_opy_))
    self.bstack1lll111l1ll_opy_ = True
    return False
  def bstack1lll111llll_opy_(self, bstack1lll1111111_opy_ = 0):
    if bstack1lll1111111_opy_ > 10:
      return False
    try:
      bstack1ll1lllll1l_opy_ = os.environ.get(bstack1l11_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧᙂ"), bstack1l11_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩᙃ"))
      bstack1lll111ll1l_opy_ = bstack1ll1lllll1l_opy_ + bstack11111l1ll1_opy_
      response = requests.get(bstack1lll111ll1l_opy_)
      data = response.json()
      self.bstack11l1l111l_opy_ = data.get(bstack1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨᙄ"), {}).get(bstack1l11_opy_ (u"ࠪ࡭ࡩ࠭ᙅ"), None)
      return True
    except:
      self.logger.debug(bstack1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡪࡨࡥࡱࡺࡨࠡࡥ࡫ࡩࡨࡱࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤᙆ"))
      return False
  def bstack1ll1lll1l11_opy_(self):
    bstack1ll1ll1l111_opy_ = bstack1l11_opy_ (u"ࠬࡧࡰࡱࠩᙇ") if self.bstack11lll1ll1_opy_ else bstack1l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᙈ")
    bstack1lll111l1l1_opy_ = bstack1l11_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥᙉ") if self.config.get(bstack1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᙊ")) is None else True
    bstack1lllll1l1ll_opy_ = bstack1l11_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠧࡲࡨࡶࡨࡿ࠽ࡼࡿࠥᙋ").format(self.config[bstack1l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᙌ")], bstack1ll1ll1l111_opy_, bstack1lll111l1l1_opy_)
    if self.bstack1lll1111l11_opy_:
      bstack1lllll1l1ll_opy_ += bstack1l11_opy_ (u"ࠦࠫࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࡀࡿࢂࠨᙍ").format(self.bstack1lll1111l11_opy_)
    uri = bstack1l11ll1l11_opy_(bstack1lllll1l1ll_opy_)
    try:
      response = bstack1l11ll111_opy_(bstack1l11_opy_ (u"ࠬࡍࡅࡕࠩᙎ"), uri, {}, {bstack1l11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᙏ"): (self.config[bstack1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᙐ")], self.config[bstack1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᙑ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1111lll1_opy_ = data.get(bstack1l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᙒ"))
        self.bstack1lll1111l11_opy_ = data.get(bstack1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥࠨᙓ"))
        os.environ[bstack1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᙔ")] = str(self.bstack1111lll1_opy_)
        os.environ[bstack1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩᙕ")] = str(self.bstack1lll1111l11_opy_)
        if bstack1lll111l1l1_opy_ == bstack1l11_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤᙖ") and str(self.bstack1111lll1_opy_).lower() == bstack1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᙗ"):
          self.bstack1ll1l1l1_opy_ = True
        if bstack1l11_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᙘ") in data:
          return data[bstack1l11_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣᙙ")]
        else:
          raise bstack1l11_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪᙚ").format(data)
      else:
        raise bstack1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦᙛ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨᙜ").format(e))
  def bstack1lll11111l1_opy_(self):
    bstack1lll1111ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤᙝ"))
    try:
      if bstack1l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᙞ") not in self.bstack1lll11l111l_opy_:
        self.bstack1lll11l111l_opy_[bstack1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᙟ")] = 2
      with open(bstack1lll1111ll1_opy_, bstack1l11_opy_ (u"ࠩࡺࠫᙠ")) as fp:
        json.dump(self.bstack1lll11l111l_opy_, fp)
      return bstack1lll1111ll1_opy_
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᙡ").format(e))
  def bstack1lll11l11ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1ll1l1lllll_opy_ == bstack1l11_opy_ (u"ࠫࡼ࡯࡮ࠨᙢ"):
        bstack1ll1lllllll_opy_ = [bstack1l11_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭ᙣ"), bstack1l11_opy_ (u"࠭࠯ࡤࠩᙤ")]
        cmd = bstack1ll1lllllll_opy_ + cmd
      cmd = bstack1l11_opy_ (u"ࠧࠡࠩᙥ").join(cmd)
      self.logger.debug(bstack1l11_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧᙦ").format(cmd))
      with open(self.bstack1lll1111lll_opy_, bstack1l11_opy_ (u"ࠤࡤࠦᙧ")) as bstack1ll1lll1111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1ll1lll1111_opy_, text=True, stderr=bstack1ll1lll1111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lll111l1ll_opy_ = True
      self.logger.error(bstack1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᙨ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1ll1ll1ll11_opy_:
        self.logger.info(bstack1l11_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧᙩ"))
        cmd = [self.binary_path, bstack1l11_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣᙪ")]
        self.bstack1lll11l11ll_opy_(cmd)
        self.bstack1ll1ll1ll11_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᙫ").format(cmd, e))
  def bstack1111l1l1_opy_(self):
    if not self.bstack1111lll1_opy_:
      return
    try:
      bstack1lll111l11l_opy_ = 0
      while not self.bstack1ll1ll1ll11_opy_ and bstack1lll111l11l_opy_ < self.bstack1ll1ll1llll_opy_:
        if self.bstack1lll111l1ll_opy_:
          self.logger.info(bstack1l11_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧᙬ"))
          return
        time.sleep(1)
        bstack1lll111l11l_opy_ += 1
      os.environ[bstack1l11_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧ᙭")] = str(self.bstack1ll1llll111_opy_())
      self.logger.info(bstack1l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥ᙮"))
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᙯ").format(e))
  def bstack1ll1llll111_opy_(self):
    if self.bstack11lll1ll1_opy_:
      return
    try:
      bstack1lll11111ll_opy_ = [platform[bstack1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᙰ")].lower() for platform in self.config.get(bstack1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᙱ"), [])]
      bstack1ll1lll1lll_opy_ = sys.maxsize
      bstack1ll1lll111l_opy_ = bstack1l11_opy_ (u"࠭ࠧᙲ")
      for browser in bstack1lll11111ll_opy_:
        if browser in self.bstack1ll1llllll1_opy_:
          bstack1lll11l11l1_opy_ = self.bstack1ll1llllll1_opy_[browser]
        if bstack1lll11l11l1_opy_ < bstack1ll1lll1lll_opy_:
          bstack1ll1lll1lll_opy_ = bstack1lll11l11l1_opy_
          bstack1ll1lll111l_opy_ = browser
      return bstack1ll1lll111l_opy_
    except Exception as e:
      self.logger.error(bstack1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᙳ").format(e))
  @classmethod
  def bstack11ll11ll1l_opy_(self):
    return os.getenv(bstack1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ᙴ"), bstack1l11_opy_ (u"ࠩࡉࡥࡱࡹࡥࠨᙵ")).lower()
  @classmethod
  def bstack1l1lll1111_opy_(self):
    return os.getenv(bstack1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧᙶ"), bstack1l11_opy_ (u"ࠫࠬᙷ"))
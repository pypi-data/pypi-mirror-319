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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack1111l1111l_opy_, bstack11111l1l1l_opy_
import tempfile
import json
bstack1lll1l11ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧᖑ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11l11_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᖒ"),
      datefmt=bstack11l11_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩᖓ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll11lll11_opy_():
  global bstack1lll1l11ll1_opy_
  if os.path.exists(bstack1lll1l11ll1_opy_):
    os.remove(bstack1lll1l11ll1_opy_)
def bstack11llll1111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11lll1lll1_opy_(config, log_level):
  bstack1lll11lll1l_opy_ = log_level
  if bstack11l11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᖔ") in config and config[bstack11l11_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᖕ")] in bstack1111l1111l_opy_:
    bstack1lll11lll1l_opy_ = bstack1111l1111l_opy_[config[bstack11l11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᖖ")]]
  if config.get(bstack11l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᖗ"), False):
    logging.getLogger().setLevel(bstack1lll11lll1l_opy_)
    return bstack1lll11lll1l_opy_
  global bstack1lll1l11ll1_opy_
  bstack11llll1111_opy_()
  bstack1lll1l11l1l_opy_ = logging.Formatter(
    fmt=bstack11l11_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᖘ"),
    datefmt=bstack11l11_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨᖙ")
  )
  bstack1lll11lllll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll1l11ll1_opy_)
  file_handler.setFormatter(bstack1lll1l11l1l_opy_)
  bstack1lll11lllll_opy_.setFormatter(bstack1lll1l11l1l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll11lllll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩᖚ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll11lllll_opy_.setLevel(bstack1lll11lll1l_opy_)
  logging.getLogger().addHandler(bstack1lll11lllll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll11lll1l_opy_
def bstack1lll11llll1_opy_(config):
  try:
    bstack1lll1l11111_opy_ = set(bstack11111l1l1l_opy_)
    bstack1lll1l111ll_opy_ = bstack11l11_opy_ (u"ࠨࠩᖛ")
    with open(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬᖜ")) as bstack1lll1l11l11_opy_:
      bstack1lll11ll11l_opy_ = bstack1lll1l11l11_opy_.read()
      bstack1lll1l111ll_opy_ = re.sub(bstack11l11_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃࠨ࠴ࠪࠥ࡞ࡱࠫᖝ"), bstack11l11_opy_ (u"ࠫࠬᖞ"), bstack1lll11ll11l_opy_, flags=re.M)
      bstack1lll1l111ll_opy_ = re.sub(
        bstack11l11_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠨࠨᖟ") + bstack11l11_opy_ (u"࠭ࡼࠨᖠ").join(bstack1lll1l11111_opy_) + bstack11l11_opy_ (u"ࠧࠪ࠰࠭ࠨࠬᖡ"),
        bstack11l11_opy_ (u"ࡳࠩ࡟࠶࠿࡛ࠦࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᖢ"),
        bstack1lll1l111ll_opy_, flags=re.M | re.I
      )
    def bstack1lll11ll1ll_opy_(dic):
      bstack1lll11ll1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll1l11111_opy_:
          bstack1lll11ll1l1_opy_[key] = bstack11l11_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ᖣ")
        else:
          if isinstance(value, dict):
            bstack1lll11ll1l1_opy_[key] = bstack1lll11ll1ll_opy_(value)
          else:
            bstack1lll11ll1l1_opy_[key] = value
      return bstack1lll11ll1l1_opy_
    bstack1lll11ll1l1_opy_ = bstack1lll11ll1ll_opy_(config)
    return {
      bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ᖤ"): bstack1lll1l111ll_opy_,
      bstack11l11_opy_ (u"ࠫ࡫࡯࡮ࡢ࡮ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᖥ"): json.dumps(bstack1lll11ll1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll11l11ll_opy_(config):
  global bstack1lll1l11ll1_opy_
  try:
    if config.get(bstack11l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᖦ"), False):
      return
    uuid = os.getenv(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᖧ"))
    if not uuid or uuid == bstack11l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᖨ"):
      return
    bstack1lll1l111l1_opy_ = [bstack11l11_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫᖩ"), bstack11l11_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪᖪ"), bstack11l11_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫᖫ"), bstack1lll1l11ll1_opy_]
    bstack11llll1111_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪᖬ") + uuid + bstack11l11_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭ᖭ"))
    with tarfile.open(output_file, bstack11l11_opy_ (u"ࠨࡷ࠻ࡩࡽࠦᖮ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll1l111l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll11llll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll1l1111l_opy_ = data.encode()
        tarinfo.size = len(bstack1lll1l1111l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll1l1111l_opy_))
    bstack1ll11lll_opy_ = MultipartEncoder(
      fields= {
        bstack11l11_opy_ (u"ࠧࡥࡣࡷࡥࠬᖯ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11l11_opy_ (u"ࠨࡴࡥࠫᖰ")), bstack11l11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧᖱ")),
        bstack11l11_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᖲ"): uuid
      }
    )
    response = requests.post(
      bstack11l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨᖳ"),
      data=bstack1ll11lll_opy_,
      headers={bstack11l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᖴ"): bstack1ll11lll_opy_.content_type},
      auth=(config[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᖵ")], config[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᖶ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧᖷ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨᖸ") + str(e))
  finally:
    try:
      bstack1lll11lll11_opy_()
    except:
      pass
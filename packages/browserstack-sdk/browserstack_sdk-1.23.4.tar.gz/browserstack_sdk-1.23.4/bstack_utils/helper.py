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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11111ll111_opy_, bstack11l11ll1_opy_, bstack1lll111111_opy_, bstack1llll111l1_opy_,
                                    bstack111111lll1_opy_, bstack11111l1ll1_opy_, bstack11111l1l1l_opy_, bstack11111l11l1_opy_)
from bstack_utils.messages import bstack1ll111l1l1_opy_, bstack11111111_opy_
from bstack_utils.proxy import bstack1ll1ll1l1_opy_, bstack1l1ll1ll1l_opy_
bstack1111ll1l1_opy_ = Config.bstack1llll1lll_opy_()
logger = logging.getLogger(__name__)
def bstack111l1ll1l1_opy_(config):
    return config[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᎌ")]
def bstack1111llll11_opy_(config):
    return config[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᎍ")]
def bstack1ll111l1ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1llllll1l11_opy_(obj):
    values = []
    bstack1llll111l1l_opy_ = re.compile(bstack11l11_opy_ (u"ࡳࠤࡡࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࡝ࡦ࠮ࠨࠧᎎ"), re.I)
    for key in obj.keys():
        if bstack1llll111l1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1lllll11l1l_opy_(config):
    tags = []
    tags.extend(bstack1llllll1l11_opy_(os.environ))
    tags.extend(bstack1llllll1l11_opy_(config))
    return tags
def bstack1lllll11l11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1llll1llll1_opy_(bstack1lllllll1ll_opy_):
    if not bstack1lllllll1ll_opy_:
        return bstack11l11_opy_ (u"ࠩࠪᎏ")
    return bstack11l11_opy_ (u"ࠥࡿࢂࠦࠨࡼࡿࠬࠦ᎐").format(bstack1lllllll1ll_opy_.name, bstack1lllllll1ll_opy_.email)
def bstack111l1l111l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1lll1lll111_opy_ = repo.common_dir
        info = {
            bstack11l11_opy_ (u"ࠦࡸ࡮ࡡࠣ᎑"): repo.head.commit.hexsha,
            bstack11l11_opy_ (u"ࠧࡹࡨࡰࡴࡷࡣࡸ࡮ࡡࠣ᎒"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l11_opy_ (u"ࠨࡢࡳࡣࡱࡧ࡭ࠨ᎓"): repo.active_branch.name,
            bstack11l11_opy_ (u"ࠢࡵࡣࡪࠦ᎔"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࠦ᎕"): bstack1llll1llll1_opy_(repo.head.commit.committer),
            bstack11l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࡤࡪࡡࡵࡧࠥ᎖"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l11_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࠥ᎗"): bstack1llll1llll1_opy_(repo.head.commit.author),
            bstack11l11_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡣࡩࡧࡴࡦࠤ᎘"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᎙"): repo.head.commit.message,
            bstack11l11_opy_ (u"ࠨࡲࡰࡱࡷࠦ᎚"): repo.git.rev_parse(bstack11l11_opy_ (u"ࠢ࠮࠯ࡶ࡬ࡴࡽ࠭ࡵࡱࡳࡰࡪࡼࡥ࡭ࠤ᎛")),
            bstack11l11_opy_ (u"ࠣࡥࡲࡱࡲࡵ࡮ࡠࡩ࡬ࡸࡤࡪࡩࡳࠤ᎜"): bstack1lll1lll111_opy_,
            bstack11l11_opy_ (u"ࠤࡺࡳࡷࡱࡴࡳࡧࡨࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ᎝"): subprocess.check_output([bstack11l11_opy_ (u"ࠥ࡫࡮ࡺࠢ᎞"), bstack11l11_opy_ (u"ࠦࡷ࡫ࡶ࠮ࡲࡤࡶࡸ࡫ࠢ᎟"), bstack11l11_opy_ (u"ࠧ࠳࠭ࡨ࡫ࡷ࠱ࡨࡵ࡭࡮ࡱࡱ࠱ࡩ࡯ࡲࠣᎠ")]).strip().decode(
                bstack11l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᎡ")),
            bstack11l11_opy_ (u"ࠢ࡭ࡣࡶࡸࡤࡺࡡࡨࠤᎢ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡴࡡࡶ࡭ࡳࡩࡥࡠ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᎣ"): repo.git.rev_list(
                bstack11l11_opy_ (u"ࠤࡾࢁ࠳࠴ࡻࡾࠤᎤ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1llllll111l_opy_ = []
        for remote in remotes:
            bstack1llll1l1l1l_opy_ = {
                bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᎥ"): remote.name,
                bstack11l11_opy_ (u"ࠦࡺࡸ࡬ࠣᎦ"): remote.url,
            }
            bstack1llllll111l_opy_.append(bstack1llll1l1l1l_opy_)
        bstack1lll1llll11_opy_ = {
            bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᎧ"): bstack11l11_opy_ (u"ࠨࡧࡪࡶࠥᎨ"),
            **info,
            bstack11l11_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫ࡳࠣᎩ"): bstack1llllll111l_opy_
        }
        bstack1lll1llll11_opy_ = bstack1llll1ll1ll_opy_(bstack1lll1llll11_opy_)
        return bstack1lll1llll11_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᎪ").format(err))
        return {}
def bstack1llll1ll1ll_opy_(bstack1lll1llll11_opy_):
    bstack1llll11l1l1_opy_ = bstack1lllll11ll1_opy_(bstack1lll1llll11_opy_)
    if bstack1llll11l1l1_opy_ and bstack1llll11l1l1_opy_ > bstack111111lll1_opy_:
        bstack111111111l_opy_ = bstack1llll11l1l1_opy_ - bstack111111lll1_opy_
        bstack111111ll11_opy_ = bstack1lllll1l11l_opy_(bstack1lll1llll11_opy_[bstack11l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᎫ")], bstack111111111l_opy_)
        bstack1lll1llll11_opy_[bstack11l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᎬ")] = bstack111111ll11_opy_
        logger.info(bstack11l11_opy_ (u"࡙ࠦ࡮ࡥࠡࡥࡲࡱࡲ࡯ࡴࠡࡪࡤࡷࠥࡨࡥࡦࡰࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩ࠴ࠠࡔ࡫ࡽࡩࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࠡࡣࡩࡸࡪࡸࠠࡵࡴࡸࡲࡨࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡼࡿࠣࡏࡇࠨᎭ")
                    .format(bstack1lllll11ll1_opy_(bstack1lll1llll11_opy_) / 1024))
    return bstack1lll1llll11_opy_
def bstack1lllll11ll1_opy_(bstack1l11l1l1l_opy_):
    try:
        if bstack1l11l1l1l_opy_:
            bstack1lllllll11l_opy_ = json.dumps(bstack1l11l1l1l_opy_)
            bstack1llll1l111l_opy_ = sys.getsizeof(bstack1lllllll11l_opy_)
            return bstack1llll1l111l_opy_
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡨࡧ࡬ࡤࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡎࡘࡕࡎࠡࡱࡥ࡮ࡪࡩࡴ࠻ࠢࡾࢁࠧᎮ").format(e))
    return -1
def bstack1lllll1l11l_opy_(field, bstack1llll1lll1l_opy_):
    try:
        bstack1llll1l1lll_opy_ = len(bytes(bstack11111l1ll1_opy_, bstack11l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᎯ")))
        bstack1llll11l11l_opy_ = bytes(field, bstack11l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭Ꮀ"))
        bstack1lll1lll11l_opy_ = len(bstack1llll11l11l_opy_)
        bstack1lll1llllll_opy_ = ceil(bstack1lll1lll11l_opy_ - bstack1llll1lll1l_opy_ - bstack1llll1l1lll_opy_)
        if bstack1lll1llllll_opy_ > 0:
            bstack1llll1111ll_opy_ = bstack1llll11l11l_opy_[:bstack1lll1llllll_opy_].decode(bstack11l11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᎱ"), errors=bstack11l11_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࠩᎲ")) + bstack11111l1ll1_opy_
            return bstack1llll1111ll_opy_
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩࡦ࡮ࡧ࠰ࠥࡴ࡯ࡵࡪ࡬ࡲ࡬ࠦࡷࡢࡵࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩࠦࡨࡦࡴࡨ࠾ࠥࢁࡽࠣᎳ").format(e))
    return field
def bstack1111lllll_opy_():
    env = os.environ
    if (bstack11l11_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᎴ") in env and len(env[bstack11l11_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᎵ")]) > 0) or (
            bstack11l11_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᎶ") in env and len(env[bstack11l11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᎷ")]) > 0):
        return {
            bstack11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᎸ"): bstack11l11_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥᎹ"),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᎺ"): env.get(bstack11l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᎻ")),
            bstack11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᎼ"): env.get(bstack11l11_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣᎽ")),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᎾ"): env.get(bstack11l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᎿ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠤࡆࡍࠧᏀ")) == bstack11l11_opy_ (u"ࠥࡸࡷࡻࡥࠣᏁ") and bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨᏂ"))):
        return {
            bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏃ"): bstack11l11_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣᏄ"),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏅ"): env.get(bstack11l11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᏆ")),
            bstack11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏇ"): env.get(bstack11l11_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢᏈ")),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏉ"): env.get(bstack11l11_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣᏊ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠨࡃࡊࠤᏋ")) == bstack11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᏌ") and bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣᏍ"))):
        return {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᏎ"): bstack11l11_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨᏏ"),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᏐ"): env.get(bstack11l11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧᏑ")),
            bstack11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᏒ"): env.get(bstack11l11_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᏓ")),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᏔ"): env.get(bstack11l11_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᏕ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠥࡇࡎࠨᏖ")) == bstack11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᏗ") and env.get(bstack11l11_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᏘ")) == bstack11l11_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᏙ"):
        return {
            bstack11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᏚ"): bstack11l11_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᏛ"),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᏜ"): None,
            bstack11l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏝ"): None,
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏞ"): None
        }
    if env.get(bstack11l11_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᏟ")) and env.get(bstack11l11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᏠ")):
        return {
            bstack11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᏡ"): bstack11l11_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦᏢ"),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᏣ"): env.get(bstack11l11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣᏤ")),
            bstack11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᏥ"): None,
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏦ"): env.get(bstack11l11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᏧ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠢࡄࡋࠥᏨ")) == bstack11l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᏩ") and bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣᏪ"))):
        return {
            bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᏫ"): bstack11l11_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥᏬ"),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏭ"): env.get(bstack11l11_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤᏮ")),
            bstack11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᏯ"): None,
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᏰ"): env.get(bstack11l11_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᏱ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠥࡇࡎࠨᏲ")) == bstack11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᏳ") and bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᏴ"))):
        return {
            bstack11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᏵ"): bstack11l11_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥ᏶"),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᏷"): env.get(bstack11l11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᏸ")),
            bstack11l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏹ"): env.get(bstack11l11_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᏺ")),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏻ"): env.get(bstack11l11_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤᏼ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠢࡄࡋࠥᏽ")) == bstack11l11_opy_ (u"ࠣࡶࡵࡹࡪࠨ᏾") and bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧ᏿"))):
        return {
            bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᐀"): bstack11l11_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦᐁ"),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᐂ"): env.get(bstack11l11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥᐃ")),
            bstack11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᐄ"): env.get(bstack11l11_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᐅ")),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᐆ"): env.get(bstack11l11_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨᐇ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠦࡈࡏࠢᐈ")) == bstack11l11_opy_ (u"ࠧࡺࡲࡶࡧࠥᐉ") and bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤᐊ"))):
        return {
            bstack11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐋ"): bstack11l11_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦᐌ"),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐍ"): env.get(bstack11l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᐎ")),
            bstack11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᐏ"): env.get(bstack11l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢᐐ")) or env.get(bstack11l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᐑ")),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᐒ"): env.get(bstack11l11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᐓ"))
        }
    if bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᐔ"))):
        return {
            bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᐕ"): bstack11l11_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦᐖ"),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᐗ"): bstack11l11_opy_ (u"ࠨࡻࡾࡽࢀࠦᐘ").format(env.get(bstack11l11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᐙ")), env.get(bstack11l11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨᐚ"))),
            bstack11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᐛ"): env.get(bstack11l11_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤᐜ")),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᐝ"): env.get(bstack11l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᐞ"))
        }
    if bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣᐟ"))):
        return {
            bstack11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐠ"): bstack11l11_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥᐡ"),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐢ"): bstack11l11_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤᐣ").format(env.get(bstack11l11_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪᐤ")), env.get(bstack11l11_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ᐥ")), env.get(bstack11l11_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧᐦ")), env.get(bstack11l11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫᐧ"))),
            bstack11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᐨ"): env.get(bstack11l11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᐩ")),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᐪ"): env.get(bstack11l11_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᐫ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨᐬ")) and env.get(bstack11l11_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᐭ")):
        return {
            bstack11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐮ"): bstack11l11_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥᐯ"),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐰ"): bstack11l11_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨᐱ").format(env.get(bstack11l11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᐲ")), env.get(bstack11l11_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪᐳ")), env.get(bstack11l11_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ᐴ"))),
            bstack11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᐵ"): env.get(bstack11l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᐶ")),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᐷ"): env.get(bstack11l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᐸ"))
        }
    if any([env.get(bstack11l11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᐹ")), env.get(bstack11l11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᐺ")), env.get(bstack11l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᐻ"))]):
        return {
            bstack11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐼ"): bstack11l11_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣᐽ"),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐾ"): env.get(bstack11l11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᐿ")),
            bstack11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᑀ"): env.get(bstack11l11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᑁ")),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᑂ"): env.get(bstack11l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᑃ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᑄ")):
        return {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᑅ"): bstack11l11_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥᑆ"),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᑇ"): env.get(bstack11l11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢᑈ")),
            bstack11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᑉ"): env.get(bstack11l11_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨᑊ")),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᑋ"): env.get(bstack11l11_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᑌ"))
        }
    if env.get(bstack11l11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦᑍ")) or env.get(bstack11l11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᑎ")):
        return {
            bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᑏ"): bstack11l11_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢᑐ"),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᑑ"): env.get(bstack11l11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᑒ")),
            bstack11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᑓ"): bstack11l11_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥᑔ") if env.get(bstack11l11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᑕ")) else None,
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᑖ"): env.get(bstack11l11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦᑗ"))
        }
    if any([env.get(bstack11l11_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧᑘ")), env.get(bstack11l11_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᑙ")), env.get(bstack11l11_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᑚ"))]):
        return {
            bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᑛ"): bstack11l11_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥᑜ"),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᑝ"): None,
            bstack11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᑞ"): env.get(bstack11l11_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦᑟ")),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᑠ"): env.get(bstack11l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᑡ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨᑢ")):
        return {
            bstack11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᑣ"): bstack11l11_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣᑤ"),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᑥ"): env.get(bstack11l11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᑦ")),
            bstack11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᑧ"): bstack11l11_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥᑨ").format(env.get(bstack11l11_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭ᑩ"))) if env.get(bstack11l11_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᑪ")) else None,
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᑫ"): env.get(bstack11l11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᑬ"))
        }
    if bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣᑭ"))):
        return {
            bstack11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᑮ"): bstack11l11_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥᑯ"),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᑰ"): env.get(bstack11l11_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣᑱ")),
            bstack11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᑲ"): env.get(bstack11l11_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤᑳ")),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᑴ"): env.get(bstack11l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᑵ"))
        }
    if bstack1ll1l1l11_opy_(env.get(bstack11l11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥᑶ"))):
        return {
            bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᑷ"): bstack11l11_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧᑸ"),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᑹ"): bstack11l11_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢᑺ").format(env.get(bstack11l11_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫᑻ")), env.get(bstack11l11_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬᑼ")), env.get(bstack11l11_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩᑽ"))),
            bstack11l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᑾ"): env.get(bstack11l11_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨᑿ")),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᒀ"): env.get(bstack11l11_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨᒁ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠢࡄࡋࠥᒂ")) == bstack11l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᒃ") and env.get(bstack11l11_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤᒄ")) == bstack11l11_opy_ (u"ࠥ࠵ࠧᒅ"):
        return {
            bstack11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᒆ"): bstack11l11_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧᒇ"),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᒈ"): bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥᒉ").format(env.get(bstack11l11_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬᒊ"))),
            bstack11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᒋ"): None,
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᒌ"): None,
        }
    if env.get(bstack11l11_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢᒍ")):
        return {
            bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᒎ"): bstack11l11_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣᒏ"),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᒐ"): None,
            bstack11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᒑ"): env.get(bstack11l11_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥᒒ")),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᒓ"): env.get(bstack11l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᒔ"))
        }
    if any([env.get(bstack11l11_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣᒕ")), env.get(bstack11l11_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨᒖ")), env.get(bstack11l11_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧᒗ")), env.get(bstack11l11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤᒘ"))]):
        return {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᒙ"): bstack11l11_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨᒚ"),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᒛ"): None,
            bstack11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᒜ"): env.get(bstack11l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᒝ")) or None,
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᒞ"): env.get(bstack11l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᒟ"), 0)
        }
    if env.get(bstack11l11_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᒠ")):
        return {
            bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᒡ"): bstack11l11_opy_ (u"ࠦࡌࡵࡃࡅࠤᒢ"),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᒣ"): None,
            bstack11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᒤ"): env.get(bstack11l11_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᒥ")),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᒦ"): env.get(bstack11l11_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣᒧ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᒨ")):
        return {
            bstack11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᒩ"): bstack11l11_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣᒪ"),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᒫ"): env.get(bstack11l11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᒬ")),
            bstack11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᒭ"): env.get(bstack11l11_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᒮ")),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᒯ"): env.get(bstack11l11_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᒰ"))
        }
    return {bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᒱ"): None}
def get_host_info():
    return {
        bstack11l11_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣᒲ"): platform.node(),
        bstack11l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤᒳ"): platform.system(),
        bstack11l11_opy_ (u"ࠣࡶࡼࡴࡪࠨᒴ"): platform.machine(),
        bstack11l11_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥᒵ"): platform.version(),
        bstack11l11_opy_ (u"ࠥࡥࡷࡩࡨࠣᒶ"): platform.architecture()[0]
    }
def bstack1l11111lll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1111111ll1_opy_():
    if bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬᒷ")):
        return bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᒸ")
    return bstack11l11_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬᒹ")
def bstack1llll1l1l11_opy_(driver):
    info = {
        bstack11l11_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᒺ"): driver.capabilities,
        bstack11l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬᒻ"): driver.session_id,
        bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᒼ"): driver.capabilities.get(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᒽ"), None),
        bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᒾ"): driver.capabilities.get(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᒿ"), None),
        bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨᓀ"): driver.capabilities.get(bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᓁ"), None),
    }
    if bstack1111111ll1_opy_() == bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᓂ"):
        if bstack11lllll1_opy_():
            info[bstack11l11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᓃ")] = bstack11l11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩᓄ")
        elif driver.capabilities.get(bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᓅ"), {}).get(bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᓆ"), False):
            info[bstack11l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᓇ")] = bstack11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᓈ")
        else:
            info[bstack11l11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᓉ")] = bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᓊ")
    return info
def bstack11lllll1_opy_():
    if bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᓋ")):
        return True
    if bstack1ll1l1l11_opy_(os.environ.get(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᓌ"), None)):
        return True
    return False
def bstack1lllll1l1_opy_(bstack1llll1lll11_opy_, url, data, config):
    headers = config.get(bstack11l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᓍ"), None)
    proxies = bstack1ll1ll1l1_opy_(config, url)
    auth = config.get(bstack11l11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᓎ"), None)
    response = requests.request(
            bstack1llll1lll11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll11l1l1_opy_(bstack11ll11l1l1_opy_, size):
    bstack1lll1l1ll1_opy_ = []
    while len(bstack11ll11l1l1_opy_) > size:
        bstack1111l111l_opy_ = bstack11ll11l1l1_opy_[:size]
        bstack1lll1l1ll1_opy_.append(bstack1111l111l_opy_)
        bstack11ll11l1l1_opy_ = bstack11ll11l1l1_opy_[size:]
    bstack1lll1l1ll1_opy_.append(bstack11ll11l1l1_opy_)
    return bstack1lll1l1ll1_opy_
def bstack1lllll1l111_opy_(message, bstack1lll1llll1l_opy_=False):
    os.write(1, bytes(message, bstack11l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᓏ")))
    os.write(1, bytes(bstack11l11_opy_ (u"ࠨ࡞ࡱࠫᓐ"), bstack11l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᓑ")))
    if bstack1lll1llll1l_opy_:
        with open(bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩᓒ") + os.environ[bstack11l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᓓ")] + bstack11l11_opy_ (u"ࠬ࠴࡬ࡰࡩࠪᓔ"), bstack11l11_opy_ (u"࠭ࡡࠨᓕ")) as f:
            f.write(message + bstack11l11_opy_ (u"ࠧ࡝ࡰࠪᓖ"))
def bstack1lllll1l1l1_opy_():
    return os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᓗ")].lower() == bstack11l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᓘ")
def bstack1ll11l111_opy_(bstack111111l11l_opy_):
    return bstack11l11_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᓙ").format(bstack11111ll111_opy_, bstack111111l11l_opy_)
def bstack1ll1l1l11l_opy_():
    return bstack11l1111111_opy_().replace(tzinfo=None).isoformat() + bstack11l11_opy_ (u"ࠫ࡟࠭ᓚ")
def bstack1llll1ll111_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l11_opy_ (u"ࠬࡠࠧᓛ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l11_opy_ (u"࡚࠭ࠨᓜ")))).total_seconds() * 1000
def bstack111111l1ll_opy_(timestamp):
    return bstack1lllll11111_opy_(timestamp).isoformat() + bstack11l11_opy_ (u"࡛ࠧࠩᓝ")
def bstack1llllllll1l_opy_(bstack1111111l11_opy_):
    date_format = bstack11l11_opy_ (u"ࠨࠧ࡜ࠩࡲࠫࡤࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫࠭ᓞ")
    bstack1llllll11l1_opy_ = datetime.datetime.strptime(bstack1111111l11_opy_, date_format)
    return bstack1llllll11l1_opy_.isoformat() + bstack11l11_opy_ (u"ࠩ࡝ࠫᓟ")
def bstack1llllll1lll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᓠ")
    else:
        return bstack11l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᓡ")
def bstack1ll1l1l11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l11_opy_ (u"ࠬࡺࡲࡶࡧࠪᓢ")
def bstack1llll11l111_opy_(val):
    return val.__str__().lower() == bstack11l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᓣ")
def bstack11l11ll1ll_opy_(bstack1llll1l1ll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1llll1l1ll1_opy_ as e:
                print(bstack11l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᓤ").format(func.__name__, bstack1llll1l1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1lllll1ll11_opy_(bstack1llll111l11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1llll111l11_opy_(cls, *args, **kwargs)
            except bstack1llll1l1ll1_opy_ as e:
                print(bstack11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣᓥ").format(bstack1llll111l11_opy_.__name__, bstack1llll1l1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1lllll1ll11_opy_
    else:
        return decorator
def bstack1l1l11l1l1_opy_(bstack111ll11lll_opy_):
    if bstack11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᓦ") in bstack111ll11lll_opy_ and bstack1llll11l111_opy_(bstack111ll11lll_opy_[bstack11l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᓧ")]):
        return False
    if bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᓨ") in bstack111ll11lll_opy_ and bstack1llll11l111_opy_(bstack111ll11lll_opy_[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᓩ")]):
        return False
    return True
def bstack1111llll_opy_():
    try:
        from pytest_bdd import reporting
        bstack1lllll1llll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨᓪ"), None)
        return bstack1lllll1llll_opy_ is None or bstack1lllll1llll_opy_ == bstack11l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᓫ")
    except Exception as e:
        return False
def bstack11l11l111_opy_(hub_url, CONFIG):
    if bstack1111ll1l_opy_() <= version.parse(bstack11l11_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨᓬ")):
        if hub_url != bstack11l11_opy_ (u"ࠩࠪᓭ"):
            return bstack11l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᓮ") + hub_url + bstack11l11_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᓯ")
        return bstack1lll111111_opy_
    if hub_url != bstack11l11_opy_ (u"ࠬ࠭ᓰ"):
        return bstack11l11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᓱ") + hub_url + bstack11l11_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣᓲ")
    return bstack1llll111l1_opy_
def bstack1111111111_opy_():
    return isinstance(os.getenv(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧᓳ")), str)
def bstack1l111l111l_opy_(url):
    return urlparse(url).hostname
def bstack1llll11l_opy_(hostname):
    for bstack1lll111ll1_opy_ in bstack11l11ll1_opy_:
        regex = re.compile(bstack1lll111ll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1lllll1lll1_opy_(bstack1llllll1111_opy_, file_name, logger):
    bstack1l1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠩࢁࠫᓴ")), bstack1llllll1111_opy_)
    try:
        if not os.path.exists(bstack1l1lll1lll_opy_):
            os.makedirs(bstack1l1lll1lll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠪࢂࠬᓵ")), bstack1llllll1111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l11_opy_ (u"ࠫࡼ࠭ᓶ")):
                pass
            with open(file_path, bstack11l11_opy_ (u"ࠧࡽࠫࠣᓷ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll111l1l1_opy_.format(str(e)))
def bstack1llll11111l_opy_(file_name, key, value, logger):
    file_path = bstack1lllll1lll1_opy_(bstack11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᓸ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1lllll1_opy_ = json.load(open(file_path, bstack11l11_opy_ (u"ࠧࡳࡤࠪᓹ")))
        else:
            bstack1ll1lllll1_opy_ = {}
        bstack1ll1lllll1_opy_[key] = value
        with open(file_path, bstack11l11_opy_ (u"ࠣࡹ࠮ࠦᓺ")) as outfile:
            json.dump(bstack1ll1lllll1_opy_, outfile)
def bstack1lll11111_opy_(file_name, logger):
    file_path = bstack1lllll1lll1_opy_(bstack11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᓻ"), file_name, logger)
    bstack1ll1lllll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l11_opy_ (u"ࠪࡶࠬᓼ")) as bstack11ll11ll1_opy_:
            bstack1ll1lllll1_opy_ = json.load(bstack11ll11ll1_opy_)
    return bstack1ll1lllll1_opy_
def bstack1l11l11ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨᓽ") + file_path + bstack11l11_opy_ (u"ࠬࠦࠧᓾ") + str(e))
def bstack1111ll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l11_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣᓿ")
def bstack11llllll_opy_(config):
    if bstack11l11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᔀ") in config:
        del (config[bstack11l11_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᔁ")])
        return False
    if bstack1111ll1l_opy_() < version.parse(bstack11l11_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨᔂ")):
        return False
    if bstack1111ll1l_opy_() >= version.parse(bstack11l11_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩᔃ")):
        return True
    if bstack11l11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᔄ") in config and config[bstack11l11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᔅ")] is False:
        return False
    else:
        return True
def bstack1l111ll1_opy_(args_list, bstack1lllll111l1_opy_):
    index = -1
    for value in bstack1lllll111l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l1l1l111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l1l1l111_opy_ = bstack11l1l1l111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᔆ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᔇ"), exception=exception)
    def bstack111l1llll1_opy_(self):
        if self.result != bstack11l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᔈ"):
            return None
        if isinstance(self.exception_type, str) and bstack11l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᔉ") in self.exception_type:
            return bstack11l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᔊ")
        return bstack11l11_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᔋ")
    def bstack1lllll1111l_opy_(self):
        if self.result != bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᔌ"):
            return None
        if self.bstack11l1l1l111_opy_:
            return self.bstack11l1l1l111_opy_
        return bstack111111l1l1_opy_(self.exception)
def bstack111111l1l1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1lllll1l1ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11l1l11l1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11llll1l1_opy_(config, logger):
    try:
        import playwright
        bstack1llll1111l1_opy_ = playwright.__file__
        bstack1llllll1l1l_opy_ = os.path.split(bstack1llll1111l1_opy_)
        bstack1llll11ll1l_opy_ = bstack1llllll1l1l_opy_[0] + bstack11l11_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩᔍ")
        os.environ[bstack11l11_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪᔎ")] = bstack1l1ll1ll1l_opy_(config)
        with open(bstack1llll11ll1l_opy_, bstack11l11_opy_ (u"ࠨࡴࠪᔏ")) as f:
            bstack11ll1l111_opy_ = f.read()
            bstack111111ll1l_opy_ = bstack11l11_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨᔐ")
            bstack1111111l1l_opy_ = bstack11ll1l111_opy_.find(bstack111111ll1l_opy_)
            if bstack1111111l1l_opy_ == -1:
              process = subprocess.Popen(bstack11l11_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢᔑ"), shell=True, cwd=bstack1llllll1l1l_opy_[0])
              process.wait()
              bstack1llll111ll1_opy_ = bstack11l11_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫᔒ")
              bstack1lll1lll1l1_opy_ = bstack11l11_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤᔓ")
              bstack1llll1ll11l_opy_ = bstack11ll1l111_opy_.replace(bstack1llll111ll1_opy_, bstack1lll1lll1l1_opy_)
              with open(bstack1llll11ll1l_opy_, bstack11l11_opy_ (u"࠭ࡷࠨᔔ")) as f:
                f.write(bstack1llll1ll11l_opy_)
    except Exception as e:
        logger.error(bstack11111111_opy_.format(str(e)))
def bstack1ll1l11ll_opy_():
  try:
    bstack1llll11l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᔕ"))
    bstack1lll1lll1ll_opy_ = []
    if os.path.exists(bstack1llll11l1ll_opy_):
      with open(bstack1llll11l1ll_opy_) as f:
        bstack1lll1lll1ll_opy_ = json.load(f)
      os.remove(bstack1llll11l1ll_opy_)
    return bstack1lll1lll1ll_opy_
  except:
    pass
  return []
def bstack1llllll11l_opy_(bstack1ll1ll111l_opy_):
  try:
    bstack1lll1lll1ll_opy_ = []
    bstack1llll11l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᔖ"))
    if os.path.exists(bstack1llll11l1ll_opy_):
      with open(bstack1llll11l1ll_opy_) as f:
        bstack1lll1lll1ll_opy_ = json.load(f)
    bstack1lll1lll1ll_opy_.append(bstack1ll1ll111l_opy_)
    with open(bstack1llll11l1ll_opy_, bstack11l11_opy_ (u"ࠩࡺࠫᔗ")) as f:
        json.dump(bstack1lll1lll1ll_opy_, f)
  except:
    pass
def bstack1l1l1ll11l_opy_(logger, bstack1lllll1ll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ᔘ"), bstack11l11_opy_ (u"ࠫࠬᔙ"))
    if test_name == bstack11l11_opy_ (u"ࠬ࠭ᔚ"):
        test_name = threading.current_thread().__dict__.get(bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬᔛ"), bstack11l11_opy_ (u"ࠧࠨᔜ"))
    bstack1lllllll1l1_opy_ = bstack11l11_opy_ (u"ࠨ࠮ࠣࠫᔝ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1lllll1ll1l_opy_:
        bstack1l1l1l1ll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᔞ"), bstack11l11_opy_ (u"ࠪ࠴ࠬᔟ"))
        bstack1l11111l11_opy_ = {bstack11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᔠ"): test_name, bstack11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᔡ"): bstack1lllllll1l1_opy_, bstack11l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᔢ"): bstack1l1l1l1ll_opy_}
        bstack1llllllll11_opy_ = []
        bstack1llll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ᔣ"))
        if os.path.exists(bstack1llll1l1111_opy_):
            with open(bstack1llll1l1111_opy_) as f:
                bstack1llllllll11_opy_ = json.load(f)
        bstack1llllllll11_opy_.append(bstack1l11111l11_opy_)
        with open(bstack1llll1l1111_opy_, bstack11l11_opy_ (u"ࠨࡹࠪᔤ")) as f:
            json.dump(bstack1llllllll11_opy_, f)
    else:
        bstack1l11111l11_opy_ = {bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᔥ"): test_name, bstack11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᔦ"): bstack1lllllll1l1_opy_, bstack11l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᔧ"): str(multiprocessing.current_process().name)}
        if bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩᔨ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l11111l11_opy_)
  except Exception as e:
      logger.warn(bstack11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᔩ").format(e))
def bstack1l111lll1_opy_(error_message, test_name, index, logger):
  try:
    bstack11111111l1_opy_ = []
    bstack1l11111l11_opy_ = {bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᔪ"): test_name, bstack11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᔫ"): error_message, bstack11l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᔬ"): index}
    bstack1lllll11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᔭ"))
    if os.path.exists(bstack1lllll11lll_opy_):
        with open(bstack1lllll11lll_opy_) as f:
            bstack11111111l1_opy_ = json.load(f)
    bstack11111111l1_opy_.append(bstack1l11111l11_opy_)
    with open(bstack1lllll11lll_opy_, bstack11l11_opy_ (u"ࠫࡼ࠭ᔮ")) as f:
        json.dump(bstack11111111l1_opy_, f)
  except Exception as e:
    logger.warn(bstack11l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᔯ").format(e))
def bstack11lll11l1_opy_(bstack1l11l11lll_opy_, name, logger):
  try:
    bstack1l11111l11_opy_ = {bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᔰ"): name, bstack11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᔱ"): bstack1l11l11lll_opy_, bstack11l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᔲ"): str(threading.current_thread()._name)}
    return bstack1l11111l11_opy_
  except Exception as e:
    logger.warn(bstack11l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᔳ").format(e))
  return
def bstack1llll1l11ll_opy_():
    return platform.system() == bstack11l11_opy_ (u"࡛ࠪ࡮ࡴࡤࡰࡹࡶࠫᔴ")
def bstack11l111111_opy_(bstack1111111lll_opy_, config, logger):
    bstack1llll11ll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111111lll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫࡯ࡸࡪࡸࠠࡤࡱࡱࡪ࡮࡭ࠠ࡬ࡧࡼࡷࠥࡨࡹࠡࡴࡨ࡫ࡪࡾࠠ࡮ࡣࡷࡧ࡭ࡀࠠࡼࡿࠥᔵ").format(e))
    return bstack1llll11ll11_opy_
def bstack11111111ll_opy_(bstack1llll1l11l1_opy_, bstack1lll1lllll1_opy_):
    bstack1llll11lll1_opy_ = version.parse(bstack1llll1l11l1_opy_)
    bstack1llll1ll1l1_opy_ = version.parse(bstack1lll1lllll1_opy_)
    if bstack1llll11lll1_opy_ > bstack1llll1ll1l1_opy_:
        return 1
    elif bstack1llll11lll1_opy_ < bstack1llll1ll1l1_opy_:
        return -1
    else:
        return 0
def bstack11l1111111_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1lllll11111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll111lll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111ll111_opy_(options, framework, bstack1l111111_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11l11_opy_ (u"ࠬ࡭ࡥࡵࠩᔶ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1lll11lll_opy_ = caps.get(bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᔷ"))
    bstack111111l111_opy_ = True
    bstack1l1ll1l1_opy_ = os.environ[bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᔸ")]
    if bstack1llll11l111_opy_(caps.get(bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧᔹ"))) or bstack1llll11l111_opy_(caps.get(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩᔺ"))):
        bstack111111l111_opy_ = False
    if bstack11llllll_opy_({bstack11l11_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥᔻ"): bstack111111l111_opy_}):
        bstack1lll11lll_opy_ = bstack1lll11lll_opy_ or {}
        bstack1lll11lll_opy_[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᔼ")] = bstack1llll111lll_opy_(framework)
        bstack1lll11lll_opy_[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᔽ")] = bstack1lllll1l1l1_opy_()
        bstack1lll11lll_opy_[bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᔾ")] = bstack1l1ll1l1_opy_
        bstack1lll11lll_opy_[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᔿ")] = bstack1l111111_opy_
        if getattr(options, bstack11l11_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩᕀ"), None):
            options.set_capability(bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᕁ"), bstack1lll11lll_opy_)
        else:
            options[bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᕂ")] = bstack1lll11lll_opy_
    else:
        if getattr(options, bstack11l11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᕃ"), None):
            options.set_capability(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᕄ"), bstack1llll111lll_opy_(framework))
            options.set_capability(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᕅ"), bstack1lllll1l1l1_opy_())
            options.set_capability(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᕆ"), bstack1l1ll1l1_opy_)
            options.set_capability(bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᕇ"), bstack1l111111_opy_)
        else:
            options[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᕈ")] = bstack1llll111lll_opy_(framework)
            options[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᕉ")] = bstack1lllll1l1l1_opy_()
            options[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᕊ")] = bstack1l1ll1l1_opy_
            options[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᕋ")] = bstack1l111111_opy_
    return options
def bstack1llll1lllll_opy_(bstack1llllll11ll_opy_, framework):
    bstack1l111111_opy_ = bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣᕌ"))
    if bstack1llllll11ll_opy_ and len(bstack1llllll11ll_opy_.split(bstack11l11_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᕍ"))) > 1:
        ws_url = bstack1llllll11ll_opy_.split(bstack11l11_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᕎ"))[0]
        if bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᕏ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1lllll111ll_opy_ = json.loads(urllib.parse.unquote(bstack1llllll11ll_opy_.split(bstack11l11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᕐ"))[1]))
            bstack1lllll111ll_opy_ = bstack1lllll111ll_opy_ or {}
            bstack1l1ll1l1_opy_ = os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᕑ")]
            bstack1lllll111ll_opy_[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᕒ")] = str(framework) + str(__version__)
            bstack1lllll111ll_opy_[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᕓ")] = bstack1lllll1l1l1_opy_()
            bstack1lllll111ll_opy_[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᕔ")] = bstack1l1ll1l1_opy_
            bstack1lllll111ll_opy_[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᕕ")] = bstack1l111111_opy_
            bstack1llllll11ll_opy_ = bstack1llllll11ll_opy_.split(bstack11l11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᕖ"))[0] + bstack11l11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᕗ") + urllib.parse.quote(json.dumps(bstack1lllll111ll_opy_))
    return bstack1llllll11ll_opy_
def bstack1l1l11ll_opy_():
    global bstack1ll1lllll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll1lllll_opy_ = BrowserType.connect
    return bstack1ll1lllll_opy_
def bstack1l1l1l1l1_opy_(framework_name):
    global bstack1l11111l1l_opy_
    bstack1l11111l1l_opy_ = framework_name
    return framework_name
def bstack1ll11l1ll1_opy_(self, *args, **kwargs):
    global bstack1ll1lllll_opy_
    try:
        global bstack1l11111l1l_opy_
        if bstack11l11_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᕘ") in kwargs:
            kwargs[bstack11l11_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᕙ")] = bstack1llll1lllll_opy_(
                kwargs.get(bstack11l11_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᕚ"), None),
                bstack1l11111l1l_opy_
            )
    except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢᕛ").format(str(e)))
    return bstack1ll1lllll_opy_(self, *args, **kwargs)
def bstack1llllllllll_opy_(bstack1llll111111_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll1ll1l1_opy_(bstack1llll111111_opy_, bstack11l11_opy_ (u"ࠣࠤᕜ"))
        if proxies and proxies.get(bstack11l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᕝ")):
            parsed_url = urlparse(proxies.get(bstack11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᕞ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᕟ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨᕠ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11l11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᕡ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᕢ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l11l1ll1l_opy_(bstack1llll111111_opy_):
    bstack1llllll1ll1_opy_ = {
        bstack11111l11l1_opy_[bstack1lllllllll1_opy_]: bstack1llll111111_opy_[bstack1lllllllll1_opy_]
        for bstack1lllllllll1_opy_ in bstack1llll111111_opy_
        if bstack1lllllllll1_opy_ in bstack11111l11l1_opy_
    }
    bstack1llllll1ll1_opy_[bstack11l11_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣᕣ")] = bstack1llllllllll_opy_(bstack1llll111111_opy_, bstack1111ll1l1_opy_.get_property(bstack11l11_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤᕤ")))
    bstack1llll11llll_opy_ = [element.lower() for element in bstack11111l1l1l_opy_]
    bstack1lllllll111_opy_(bstack1llllll1ll1_opy_, bstack1llll11llll_opy_)
    return bstack1llllll1ll1_opy_
def bstack1lllllll111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11l11_opy_ (u"ࠥ࠮࠯࠰ࠪࠣᕥ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1lllllll111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1lllllll111_opy_(item, keys)
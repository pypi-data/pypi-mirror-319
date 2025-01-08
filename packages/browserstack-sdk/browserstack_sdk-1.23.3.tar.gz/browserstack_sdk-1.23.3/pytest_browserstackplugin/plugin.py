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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11ll1lllll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack111ll1ll_opy_, bstack1ll1l1l1l_opy_, update, bstack1l1l1111l_opy_,
                                       bstack1l1111111_opy_, bstack1ll1l1lll_opy_, bstack11111ll1l_opy_, bstack1l1llllll_opy_,
                                       bstack1lll11111l_opy_, bstack1l111l1l11_opy_, bstack11ll1llll1_opy_, bstack1llll1l1l_opy_,
                                       bstack1111ll1ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll1l111l_opy_)
from browserstack_sdk.bstack11111l11_opy_ import bstack1l1l11l1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11l111l1_opy_
from bstack_utils.capture import bstack11l1llll1l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l111111ll_opy_, bstack11llllll1l_opy_, bstack1l1llll11l_opy_, \
    bstack11l1ll1l1_opy_
from bstack_utils.helper import bstack1ll111111l_opy_, bstack1lllll1l11l_opy_, bstack11l11ll11l_opy_, bstack1l1lll11ll_opy_, bstack1llll1llll1_opy_, bstack11ll1111l1_opy_, \
    bstack111111ll1l_opy_, \
    bstack1lllll11111_opy_, bstack11ll1111_opy_, bstack1l11l1l1ll_opy_, bstack1llllll111l_opy_, bstack1l11l11111_opy_, Notset, \
    bstack11ll1l1l11_opy_, bstack1lllll11l11_opy_, bstack1llll1l1111_opy_, Result, bstack1llllll1lll_opy_, bstack1llll1l1l11_opy_, bstack11l11llll1_opy_, \
    bstack1lll1ll1ll_opy_, bstack1ll11l1111_opy_, bstack1l1llll1l1_opy_, bstack1llllll11ll_opy_
from bstack_utils.bstack1lll1ll1lll_opy_ import bstack1lll1ll11l1_opy_
from bstack_utils.messages import bstack11l111111_opy_, bstack1ll11ll11_opy_, bstack1l1111ll1_opy_, bstack1lll11l11l_opy_, bstack1l11111l1_opy_, \
    bstack1111ll11_opy_, bstack111l1l111_opy_, bstack11l1llll1_opy_, bstack1l11l11ll_opy_, bstack1ll11l1l11_opy_, \
    bstack1lll11l1_opy_, bstack1l1l11l11l_opy_
from bstack_utils.proxy import bstack11l1l1l1l_opy_, bstack11ll111l1_opy_
from bstack_utils.bstack1l1llll1l_opy_ import bstack1ll11llll1l_opy_, bstack1ll11lll1ll_opy_, bstack1ll11lll111_opy_, bstack1ll1l1111l1_opy_, \
    bstack1ll11lllll1_opy_, bstack1ll1l1111ll_opy_, bstack1ll1l111111_opy_, bstack11111l111_opy_, bstack1ll1l11111l_opy_
from bstack_utils.bstack11ll1llll_opy_ import bstack1l1l1ll111_opy_
from bstack_utils.bstack11ll11l1_opy_ import bstack11lll11l1_opy_, bstack11ll1l1l1_opy_, bstack11ll1l11ll_opy_, \
    bstack1ll11lllll_opy_, bstack1l1l1l111_opy_
from bstack_utils.bstack11l1l1lll1_opy_ import bstack11l1lll111_opy_
from bstack_utils.bstack11l1ll1111_opy_ import bstack111lll111_opy_
import bstack_utils.bstack111ll11l11_opy_ as bstack1l1l11llll_opy_
from bstack_utils.bstack11l1l1l111_opy_ import bstack1lll1lllll_opy_
from bstack_utils.bstack1llllllll1_opy_ import bstack1llllllll1_opy_
from browserstack_sdk.__init__ import bstack11l11ll1l_opy_
bstack1l1l11111_opy_ = None
bstack1l1llll1_opy_ = None
bstack11lllll11_opy_ = None
bstack1ll1l1ll1_opy_ = None
bstack11lllll1ll_opy_ = None
bstack111l11ll_opy_ = None
bstack11lll11111_opy_ = None
bstack1l111ll11l_opy_ = None
bstack1llll1l1l1_opy_ = None
bstack11ll1lll1l_opy_ = None
bstack1lll11ll11_opy_ = None
bstack1l11ll1l_opy_ = None
bstack11111lll_opy_ = None
bstack1ll1l11l1_opy_ = bstack1l11_opy_ (u"ࠩࠪᢥ")
CONFIG = {}
bstack111ll1ll1_opy_ = False
bstack11ll11l11l_opy_ = bstack1l11_opy_ (u"ࠪࠫᢦ")
bstack1lll11lll1_opy_ = bstack1l11_opy_ (u"ࠫࠬᢧ")
bstack1lllll1l1_opy_ = False
bstack11ll1l1lll_opy_ = []
bstack11111ll1_opy_ = bstack1l111111ll_opy_
bstack1l1ll1ll1l1_opy_ = bstack1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᢨ")
bstack111ll111_opy_ = {}
bstack1lll1llll_opy_ = None
bstack1l1l11l1l_opy_ = False
logger = bstack11l111l1_opy_.get_logger(__name__, bstack11111ll1_opy_)
store = {
    bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦᢩࠪ"): []
}
bstack1l1ll1l1111_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l11l11ll_opy_ = {}
current_test_uuid = None
def bstack11ll111l11_opy_(page, bstack11lll1111l_opy_):
    try:
        page.evaluate(bstack1l11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᢪ"),
                      bstack1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ᢫") + json.dumps(
                          bstack11lll1111l_opy_) + bstack1l11_opy_ (u"ࠤࢀࢁࠧ᢬"))
    except Exception as e:
        print(bstack1l11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣ᢭"), e)
def bstack11lll111_opy_(page, message, level):
    try:
        page.evaluate(bstack1l11_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ᢮"), bstack1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ᢯") + json.dumps(
            message) + bstack1l11_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩᢰ") + json.dumps(level) + bstack1l11_opy_ (u"ࠧࡾࡿࠪᢱ"))
    except Exception as e:
        print(bstack1l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᢲ"), e)
def pytest_configure(config):
    bstack111l11ll1_opy_ = Config.bstack11ll111lll_opy_()
    config.args = bstack111lll111_opy_.bstack1l1lll11111_opy_(config.args)
    bstack111l11ll1_opy_.bstack1l1111l11_opy_(bstack1l1llll1l1_opy_(config.getoption(bstack1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᢳ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1l1ll1l1l11_opy_ = item.config.getoption(bstack1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᢴ"))
    plugins = item.config.getoption(bstack1l11_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧᢵ"))
    report = outcome.get_result()
    bstack1l1ll11l111_opy_(item, call, report)
    if bstack1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥᢶ") not in plugins or bstack1l11l11111_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l11_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢᢷ"), None)
    page = getattr(item, bstack1l11_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨᢸ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1l1ll1l11ll_opy_(item, report, summary, bstack1l1ll1l1l11_opy_)
    if (page is not None):
        bstack1l1ll11l1l1_opy_(item, report, summary, bstack1l1ll1l1l11_opy_)
def bstack1l1ll1l11ll_opy_(item, report, summary, bstack1l1ll1l1l11_opy_):
    if report.when == bstack1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᢹ") and report.skipped:
        bstack1ll1l11111l_opy_(report)
    if report.when in [bstack1l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᢺ"), bstack1l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᢻ")]:
        return
    if not bstack1llll1llll1_opy_():
        return
    try:
        if (str(bstack1l1ll1l1l11_opy_).lower() != bstack1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩᢼ")):
            item._driver.execute_script(
                bstack1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪᢽ") + json.dumps(
                    report.nodeid) + bstack1l11_opy_ (u"࠭ࡽࡾࠩᢾ"))
        os.environ[bstack1l11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᢿ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣᣀ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᣁ")))
    bstack1ll11111_opy_ = bstack1l11_opy_ (u"ࠥࠦᣂ")
    bstack1ll1l11111l_opy_(report)
    if not passed:
        try:
            bstack1ll11111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᣃ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll11111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l11_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᣄ")))
        bstack1ll11111_opy_ = bstack1l11_opy_ (u"ࠨࠢᣅ")
        if not passed:
            try:
                bstack1ll11111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᣆ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll11111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬᣇ")
                    + json.dumps(bstack1l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥᣈ"))
                    + bstack1l11_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᣉ")
                )
            else:
                item._driver.execute_script(
                    bstack1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᣊ")
                    + json.dumps(str(bstack1ll11111_opy_))
                    + bstack1l11_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᣋ")
                )
        except Exception as e:
            summary.append(bstack1l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦᣌ").format(e))
def bstack1l1ll11ll11_opy_(test_name, error_message):
    try:
        bstack1l1ll1l1lll_opy_ = []
        bstack1l111111_opy_ = os.environ.get(bstack1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᣍ"), bstack1l11_opy_ (u"ࠨ࠲ࠪᣎ"))
        bstack1l11lll11_opy_ = {bstack1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᣏ"): test_name, bstack1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᣐ"): error_message, bstack1l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᣑ"): bstack1l111111_opy_}
        bstack1l1ll11ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᣒ"))
        if os.path.exists(bstack1l1ll11ll1l_opy_):
            with open(bstack1l1ll11ll1l_opy_) as f:
                bstack1l1ll1l1lll_opy_ = json.load(f)
        bstack1l1ll1l1lll_opy_.append(bstack1l11lll11_opy_)
        with open(bstack1l1ll11ll1l_opy_, bstack1l11_opy_ (u"࠭ࡷࠨᣓ")) as f:
            json.dump(bstack1l1ll1l1lll_opy_, f)
    except Exception as e:
        logger.debug(bstack1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬᣔ") + str(e))
def bstack1l1ll11l1l1_opy_(item, report, summary, bstack1l1ll1l1l11_opy_):
    if report.when in [bstack1l11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᣕ"), bstack1l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᣖ")]:
        return
    if (str(bstack1l1ll1l1l11_opy_).lower() != bstack1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨᣗ")):
        bstack11ll111l11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l11_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᣘ")))
    bstack1ll11111_opy_ = bstack1l11_opy_ (u"ࠧࠨᣙ")
    bstack1ll1l11111l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll11111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᣚ").format(e)
                )
        try:
            if passed:
                bstack1l1l1l111_opy_(getattr(item, bstack1l11_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᣛ"), None), bstack1l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᣜ"))
            else:
                error_message = bstack1l11_opy_ (u"ࠩࠪᣝ")
                if bstack1ll11111_opy_:
                    bstack11lll111_opy_(item._page, str(bstack1ll11111_opy_), bstack1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᣞ"))
                    bstack1l1l1l111_opy_(getattr(item, bstack1l11_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᣟ"), None), bstack1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᣠ"), str(bstack1ll11111_opy_))
                    error_message = str(bstack1ll11111_opy_)
                else:
                    bstack1l1l1l111_opy_(getattr(item, bstack1l11_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᣡ"), None), bstack1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᣢ"))
                bstack1l1ll11ll11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᣣ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1l11_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᣤ"), default=bstack1l11_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᣥ"), help=bstack1l11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᣦ"))
    parser.addoption(bstack1l11_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᣧ"), default=bstack1l11_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᣨ"), help=bstack1l11_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᣩ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l11_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥᣪ"), action=bstack1l11_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣᣫ"), default=bstack1l11_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥᣬ"),
                         help=bstack1l11_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᣭ"))
def bstack11l1ll1l11_opy_(log):
    if not (log[bstack1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᣮ")] and log[bstack1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᣯ")].strip()):
        return
    active = bstack11l1l111ll_opy_()
    log = {
        bstack1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᣰ"): log[bstack1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᣱ")],
        bstack1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᣲ"): bstack11l11ll11l_opy_().isoformat() + bstack1l11_opy_ (u"ࠪ࡞ࠬᣳ"),
        bstack1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᣴ"): log[bstack1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᣵ")],
    }
    if active:
        if active[bstack1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ᣶")] == bstack1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ᣷"):
            log[bstack1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᣸")] = active[bstack1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᣹")]
        elif active[bstack1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ᣺")] == bstack1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ᣻"):
            log[bstack1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᣼")] = active[bstack1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᣽")]
    bstack1lll1lllll_opy_.bstack11111ll11_opy_([log])
def bstack11l1l111ll_opy_():
    if len(store[bstack1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ᣾")]) > 0 and store[bstack1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ᣿")][-1]:
        return {
            bstack1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᤀ"): bstack1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᤁ"),
            bstack1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᤂ"): store[bstack1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᤃ")][-1]
        }
    if store.get(bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᤄ"), None):
        return {
            bstack1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬᤅ"): bstack1l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᤆ"),
            bstack1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᤇ"): store[bstack1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᤈ")]
        }
    return None
bstack11l1ll1lll_opy_ = bstack11l1llll1l_opy_(bstack11l1ll1l11_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        item._1l1ll1lll11_opy_ = True
        bstack111llll1_opy_ = bstack1l1l11llll_opy_.bstack1lll1l1l1_opy_(bstack1lllll11111_opy_(item.own_markers))
        item._a11y_test_case = bstack111llll1_opy_
        if bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᤉ"), None):
            driver = getattr(item, bstack1l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᤊ"), None)
            item._a11y_started = bstack1l1l11llll_opy_.bstack1llll1llll_opy_(driver, bstack111llll1_opy_)
        if not bstack1lll1lllll_opy_.on() or bstack1l1ll1ll1l1_opy_ != bstack1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᤋ"):
            return
        global current_test_uuid, bstack11l1ll1lll_opy_
        bstack11l1ll1lll_opy_.start()
        bstack11l111l1l1_opy_ = {
            bstack1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᤌ"): uuid4().__str__(),
            bstack1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᤍ"): bstack11l11ll11l_opy_().isoformat() + bstack1l11_opy_ (u"ࠩ࡝ࠫᤎ")
        }
        current_test_uuid = bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᤏ")]
        store[bstack1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᤐ")] = bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪᤑ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l11l11ll_opy_[item.nodeid] = {**_11l11l11ll_opy_[item.nodeid], **bstack11l111l1l1_opy_}
        bstack1l1ll1ll111_opy_(item, _11l11l11ll_opy_[item.nodeid], bstack1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᤒ"))
    except Exception as err:
        print(bstack1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩᤓ"), str(err))
def pytest_runtest_setup(item):
    global bstack1l1ll1l1111_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1llllll111l_opy_():
        atexit.register(bstack11ll11llll_opy_)
        if not bstack1l1ll1l1111_opy_:
            try:
                bstack1l1ll11lll1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1llllll11ll_opy_():
                    bstack1l1ll11lll1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1l1ll11lll1_opy_:
                    signal.signal(s, bstack1l1ll111111_opy_)
                bstack1l1ll1l1111_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤᤔ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll11llll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᤕ")
    try:
        if not bstack1lll1lllll_opy_.on():
            return
        bstack11l1ll1lll_opy_.start()
        uuid = uuid4().__str__()
        bstack11l111l1l1_opy_ = {
            bstack1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᤖ"): uuid,
            bstack1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᤗ"): bstack11l11ll11l_opy_().isoformat() + bstack1l11_opy_ (u"ࠬࡠࠧᤘ"),
            bstack1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫᤙ"): bstack1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᤚ"),
            bstack1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᤛ"): bstack1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᤜ"),
            bstack1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᤝ"): bstack1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᤞ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᤟")] = item
        store[bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᤠ")] = [uuid]
        if not _11l11l11ll_opy_.get(item.nodeid, None):
            _11l11l11ll_opy_[item.nodeid] = {bstack1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᤡ"): [], bstack1l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᤢ"): []}
        _11l11l11ll_opy_[item.nodeid][bstack1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᤣ")].append(bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᤤ")])
        _11l11l11ll_opy_[item.nodeid + bstack1l11_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫᤥ")] = bstack11l111l1l1_opy_
        bstack1l1ll11llll_opy_(item, bstack11l111l1l1_opy_, bstack1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᤦ"))
    except Exception as err:
        print(bstack1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᤧ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack111ll111_opy_
        bstack1l111111_opy_ = 0
        if bstack1lllll1l1_opy_ is True:
            bstack1l111111_opy_ = int(os.environ.get(bstack1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᤨ")))
        if bstack1lllll11ll_opy_.bstack11ll11ll1l_opy_() == bstack1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᤩ"):
            if bstack1lllll11ll_opy_.bstack1l1lll1111_opy_() == bstack1l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᤪ"):
                bstack1l1ll1111l1_opy_ = bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᤫ"), None)
                bstack1lll1l11_opy_ = bstack1l1ll1111l1_opy_ + bstack1l11_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ᤬")
                driver = getattr(item, bstack1l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭᤭"), None)
                bstack1l1l111lll_opy_ = getattr(item, bstack1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᤮"), None)
                bstack1l11l1l1_opy_ = getattr(item, bstack1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᤯"), None)
                PercySDK.screenshot(driver, bstack1lll1l11_opy_, bstack1l1l111lll_opy_=bstack1l1l111lll_opy_, bstack1l11l1l1_opy_=bstack1l11l1l1_opy_, bstack11lll1l1l_opy_=bstack1l111111_opy_)
        if getattr(item, bstack1l11_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨᤰ"), False):
            bstack1l1l11l1_opy_.bstack1ll1l111ll_opy_(getattr(item, bstack1l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᤱ"), None), bstack111ll111_opy_, logger, item)
        if not bstack1lll1lllll_opy_.on():
            return
        bstack11l111l1l1_opy_ = {
            bstack1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᤲ"): uuid4().__str__(),
            bstack1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᤳ"): bstack11l11ll11l_opy_().isoformat() + bstack1l11_opy_ (u"ࠬࡠࠧᤴ"),
            bstack1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫᤵ"): bstack1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᤶ"),
            bstack1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᤷ"): bstack1l11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᤸ"),
            bstack1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ᤹࠭"): bstack1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭᤺")
        }
        _11l11l11ll_opy_[item.nodeid + bstack1l11_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ᤻")] = bstack11l111l1l1_opy_
        bstack1l1ll11llll_opy_(item, bstack11l111l1l1_opy_, bstack1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ᤼"))
    except Exception as err:
        print(bstack1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭᤽"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1lll1lllll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1ll1l1111l1_opy_(fixturedef.argname):
        store[bstack1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ᤾")] = request.node
    elif bstack1ll11lllll1_opy_(fixturedef.argname):
        store[bstack1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ᤿")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ᥀"): fixturedef.argname,
            bstack1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᥁"): bstack111111ll1l_opy_(outcome),
            bstack1l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ᥂"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᥃")]
        if not _11l11l11ll_opy_.get(current_test_item.nodeid, None):
            _11l11l11ll_opy_[current_test_item.nodeid] = {bstack1l11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ᥄"): []}
        _11l11l11ll_opy_[current_test_item.nodeid][bstack1l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ᥅")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ᥆"), str(err))
if bstack1l11l11111_opy_() and bstack1lll1lllll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11l11l11ll_opy_[request.node.nodeid][bstack1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭᥇")].bstack1ll11llll1_opy_(id(step))
        except Exception as err:
            print(bstack1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩ᥈"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11l11l11ll_opy_[request.node.nodeid][bstack1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ᥉")].bstack11l1ll1l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ᥊"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11l1l1lll1_opy_: bstack11l1lll111_opy_ = _11l11l11ll_opy_[request.node.nodeid][bstack1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ᥋")]
            bstack11l1l1lll1_opy_.bstack11l1ll1l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ᥌"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1l1ll1ll1l1_opy_
        try:
            if not bstack1lll1lllll_opy_.on() or bstack1l1ll1ll1l1_opy_ != bstack1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭᥍"):
                return
            global bstack11l1ll1lll_opy_
            bstack11l1ll1lll_opy_.start()
            driver = bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ᥎"), None)
            if not _11l11l11ll_opy_.get(request.node.nodeid, None):
                _11l11l11ll_opy_[request.node.nodeid] = {}
            bstack11l1l1lll1_opy_ = bstack11l1lll111_opy_.bstack1ll111l1lll_opy_(
                scenario, feature, request.node,
                name=bstack1ll1l1111ll_opy_(request.node, scenario),
                bstack11l1llll11_opy_=bstack11ll1111l1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭᥏"),
                tags=bstack1ll1l111111_opy_(feature, scenario),
                bstack11l1l11ll1_opy_=bstack1lll1lllll_opy_.bstack11l1l1l1ll_opy_(driver) if driver and driver.session_id else {}
            )
            _11l11l11ll_opy_[request.node.nodeid][bstack1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᥐ")] = bstack11l1l1lll1_opy_
            bstack1l1ll111ll1_opy_(bstack11l1l1lll1_opy_.uuid)
            bstack1lll1lllll_opy_.bstack11l1lll11l_opy_(bstack1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᥑ"), bstack11l1l1lll1_opy_)
        except Exception as err:
            print(bstack1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩᥒ"), str(err))
def bstack1l1ll1111ll_opy_(bstack11l1l1ll1l_opy_):
    if bstack11l1l1ll1l_opy_ in store[bstack1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᥓ")]:
        store[bstack1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᥔ")].remove(bstack11l1l1ll1l_opy_)
def bstack1l1ll111ll1_opy_(bstack11l1ll111l_opy_):
    store[bstack1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᥕ")] = bstack11l1ll111l_opy_
    threading.current_thread().current_test_uuid = bstack11l1ll111l_opy_
@bstack1lll1lllll_opy_.bstack1l1llll11l1_opy_
def bstack1l1ll11l111_opy_(item, call, report):
    global bstack1l1ll1ll1l1_opy_
    bstack1l1lll1l1l_opy_ = bstack11ll1111l1_opy_()
    if hasattr(report, bstack1l11_opy_ (u"ࠫࡸࡺ࡯ࡱࠩᥖ")):
        bstack1l1lll1l1l_opy_ = bstack1llllll1lll_opy_(report.stop)
    elif hasattr(report, bstack1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫᥗ")):
        bstack1l1lll1l1l_opy_ = bstack1llllll1lll_opy_(report.start)
    try:
        if getattr(report, bstack1l11_opy_ (u"࠭ࡷࡩࡧࡱࠫᥘ"), bstack1l11_opy_ (u"ࠧࠨᥙ")) == bstack1l11_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᥚ"):
            bstack11l1ll1lll_opy_.reset()
        if getattr(report, bstack1l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᥛ"), bstack1l11_opy_ (u"ࠪࠫᥜ")) == bstack1l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᥝ"):
            if bstack1l1ll1ll1l1_opy_ == bstack1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᥞ"):
                _11l11l11ll_opy_[item.nodeid][bstack1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᥟ")] = bstack1l1lll1l1l_opy_
                bstack1l1ll1ll111_opy_(item, _11l11l11ll_opy_[item.nodeid], bstack1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᥠ"), report, call)
                store[bstack1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᥡ")] = None
            elif bstack1l1ll1ll1l1_opy_ == bstack1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᥢ"):
                bstack11l1l1lll1_opy_ = _11l11l11ll_opy_[item.nodeid][bstack1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᥣ")]
                bstack11l1l1lll1_opy_.set(hooks=_11l11l11ll_opy_[item.nodeid].get(bstack1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᥤ"), []))
                exception, bstack11l1lll1ll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l1lll1ll_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l11_opy_ (u"ࠬࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠫᥥ"), bstack1l11_opy_ (u"࠭ࠧᥦ"))]
                bstack11l1l1lll1_opy_.stop(time=bstack1l1lll1l1l_opy_, result=Result(result=getattr(report, bstack1l11_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨᥧ"), bstack1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᥨ")), exception=exception, bstack11l1lll1ll_opy_=bstack11l1lll1ll_opy_))
                bstack1lll1lllll_opy_.bstack11l1lll11l_opy_(bstack1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᥩ"), _11l11l11ll_opy_[item.nodeid][bstack1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᥪ")])
        elif getattr(report, bstack1l11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᥫ"), bstack1l11_opy_ (u"ࠬ࠭ᥬ")) in [bstack1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᥭ"), bstack1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ᥮")]:
            bstack11l1ll1ll1_opy_ = item.nodeid + bstack1l11_opy_ (u"ࠨ࠯ࠪ᥯") + getattr(report, bstack1l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᥰ"), bstack1l11_opy_ (u"ࠪࠫᥱ"))
            if getattr(report, bstack1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᥲ"), False):
                hook_type = bstack1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᥳ") if getattr(report, bstack1l11_opy_ (u"࠭ࡷࡩࡧࡱࠫᥴ"), bstack1l11_opy_ (u"ࠧࠨ᥵")) == bstack1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ᥶") else bstack1l11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭᥷")
                _11l11l11ll_opy_[bstack11l1ll1ll1_opy_] = {
                    bstack1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᥸"): uuid4().__str__(),
                    bstack1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᥹"): bstack1l1lll1l1l_opy_,
                    bstack1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ᥺"): hook_type
                }
            _11l11l11ll_opy_[bstack11l1ll1ll1_opy_][bstack1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᥻")] = bstack1l1lll1l1l_opy_
            bstack1l1ll1111ll_opy_(_11l11l11ll_opy_[bstack11l1ll1ll1_opy_][bstack1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᥼")])
            bstack1l1ll11llll_opy_(item, _11l11l11ll_opy_[bstack11l1ll1ll1_opy_], bstack1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᥽"), report, call)
            if getattr(report, bstack1l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ᥾"), bstack1l11_opy_ (u"ࠪࠫ᥿")) == bstack1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᦀ"):
                if getattr(report, bstack1l11_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ᦁ"), bstack1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᦂ")) == bstack1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᦃ"):
                    bstack11l111l1l1_opy_ = {
                        bstack1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᦄ"): uuid4().__str__(),
                        bstack1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᦅ"): bstack11ll1111l1_opy_(),
                        bstack1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᦆ"): bstack11ll1111l1_opy_()
                    }
                    _11l11l11ll_opy_[item.nodeid] = {**_11l11l11ll_opy_[item.nodeid], **bstack11l111l1l1_opy_}
                    bstack1l1ll1ll111_opy_(item, _11l11l11ll_opy_[item.nodeid], bstack1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᦇ"))
                    bstack1l1ll1ll111_opy_(item, _11l11l11ll_opy_[item.nodeid], bstack1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᦈ"), report, call)
    except Exception as err:
        print(bstack1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫᦉ"), str(err))
def bstack1l1ll1lll1l_opy_(test, bstack11l111l1l1_opy_, result=None, call=None, bstack11ll11111l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l1l1lll1_opy_ = {
        bstack1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᦊ"): bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᦋ")],
        bstack1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᦌ"): bstack1l11_opy_ (u"ࠪࡸࡪࡹࡴࠨᦍ"),
        bstack1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᦎ"): test.name,
        bstack1l11_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᦏ"): {
            bstack1l11_opy_ (u"࠭࡬ࡢࡰࡪࠫᦐ"): bstack1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᦑ"),
            bstack1l11_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᦒ"): inspect.getsource(test.obj)
        },
        bstack1l11_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᦓ"): test.name,
        bstack1l11_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᦔ"): test.name,
        bstack1l11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᦕ"): bstack111lll111_opy_.bstack11l1111ll1_opy_(test),
        bstack1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᦖ"): file_path,
        bstack1l11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᦗ"): file_path,
        bstack1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᦘ"): bstack1l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᦙ"),
        bstack1l11_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᦚ"): file_path,
        bstack1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᦛ"): bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᦜ")],
        bstack1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᦝ"): bstack1l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᦞ"),
        bstack1l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᦟ"): {
            bstack1l11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᦠ"): test.nodeid
        },
        bstack1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᦡ"): bstack1lllll11111_opy_(test.own_markers)
    }
    if bstack11ll11111l_opy_ in [bstack1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᦢ"), bstack1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᦣ")]:
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠬࡳࡥࡵࡣࠪᦤ")] = {
            bstack1l11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᦥ"): bstack11l111l1l1_opy_.get(bstack1l11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᦦ"), [])
        }
    if bstack11ll11111l_opy_ == bstack1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᦧ"):
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᦨ")] = bstack1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᦩ")
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᦪ")] = bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᦫ")]
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᦬")] = bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᦭")]
    if result:
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᦮")] = result.outcome
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ᦯")] = result.duration * 1000
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᦰ")] = bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᦱ")]
        if result.failed:
            bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᦲ")] = bstack1lll1lllll_opy_.bstack111l1lll1l_opy_(call.excinfo.typename)
            bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᦳ")] = bstack1lll1lllll_opy_.bstack1ll11111ll1_opy_(call.excinfo, result)
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᦴ")] = bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᦵ")]
    if outcome:
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᦶ")] = bstack111111ll1l_opy_(outcome)
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᦷ")] = 0
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᦸ")] = bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᦹ")]
        if bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᦺ")] == bstack1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᦻ"):
            bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᦼ")] = bstack1l11_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᦽ")  # bstack1l1ll1l1l1l_opy_
            bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᦾ")] = [{bstack1l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᦿ"): [bstack1l11_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᧀ")]}]
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᧁ")] = bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᧂ")]
    return bstack11l1l1lll1_opy_
def bstack1l1ll1ll11l_opy_(test, bstack11l11111l1_opy_, bstack11ll11111l_opy_, result, call, outcome, bstack1l1ll11111l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11l11111l1_opy_[bstack1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᧃ")]
    hook_name = bstack11l11111l1_opy_[bstack1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᧄ")]
    hook_data = {
        bstack1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᧅ"): bstack11l11111l1_opy_[bstack1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᧆ")],
        bstack1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᧇ"): bstack1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᧈ"),
        bstack1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᧉ"): bstack1l11_opy_ (u"ࠨࡽࢀࠫ᧊").format(bstack1ll11lll1ll_opy_(hook_name)),
        bstack1l11_opy_ (u"ࠩࡥࡳࡩࡿࠧ᧋"): {
            bstack1l11_opy_ (u"ࠪࡰࡦࡴࡧࠨ᧌"): bstack1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ᧍"),
            bstack1l11_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ᧎"): None
        },
        bstack1l11_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ᧏"): test.name,
        bstack1l11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ᧐"): bstack111lll111_opy_.bstack11l1111ll1_opy_(test, hook_name),
        bstack1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ᧑"): file_path,
        bstack1l11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ᧒"): file_path,
        bstack1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᧓"): bstack1l11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ᧔"),
        bstack1l11_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ᧕"): file_path,
        bstack1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᧖"): bstack11l11111l1_opy_[bstack1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᧗")],
        bstack1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ᧘"): bstack1l11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ᧙") if bstack1l1ll1ll1l1_opy_ == bstack1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ᧚") else bstack1l11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ᧛"),
        bstack1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ᧜"): hook_type
    }
    bstack1ll111l1l11_opy_ = bstack11l11ll111_opy_(_11l11l11ll_opy_.get(test.nodeid, None))
    if bstack1ll111l1l11_opy_:
        hook_data[bstack1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ᧝")] = bstack1ll111l1l11_opy_
    if result:
        hook_data[bstack1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᧞")] = result.outcome
        hook_data[bstack1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ᧟")] = result.duration * 1000
        hook_data[bstack1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᧠")] = bstack11l11111l1_opy_[bstack1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᧡")]
        if result.failed:
            hook_data[bstack1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ᧢")] = bstack1lll1lllll_opy_.bstack111l1lll1l_opy_(call.excinfo.typename)
            hook_data[bstack1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭᧣")] = bstack1lll1lllll_opy_.bstack1ll11111ll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᧤")] = bstack111111ll1l_opy_(outcome)
        hook_data[bstack1l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ᧥")] = 100
        hook_data[bstack1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᧦")] = bstack11l11111l1_opy_[bstack1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᧧")]
        if hook_data[bstack1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᧨")] == bstack1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᧩"):
            hook_data[bstack1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ᧪")] = bstack1l11_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ᧫")  # bstack1l1ll1l1l1l_opy_
            hook_data[bstack1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ᧬")] = [{bstack1l11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ᧭"): [bstack1l11_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭᧮")]}]
    if bstack1l1ll11111l_opy_:
        hook_data[bstack1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᧯")] = bstack1l1ll11111l_opy_.result
        hook_data[bstack1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ᧰")] = bstack1lllll11l11_opy_(bstack11l11111l1_opy_[bstack1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ᧱")], bstack11l11111l1_opy_[bstack1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᧲")])
        hook_data[bstack1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᧳")] = bstack11l11111l1_opy_[bstack1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᧴")]
        if hook_data[bstack1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᧵")] == bstack1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᧶"):
            hook_data[bstack1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ᧷")] = bstack1lll1lllll_opy_.bstack111l1lll1l_opy_(bstack1l1ll11111l_opy_.exception_type)
            hook_data[bstack1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭᧸")] = [{bstack1l11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ᧹"): bstack1llll1l1111_opy_(bstack1l1ll11111l_opy_.exception)}]
    return hook_data
def bstack1l1ll1ll111_opy_(test, bstack11l111l1l1_opy_, bstack11ll11111l_opy_, result=None, call=None, outcome=None):
    bstack11l1l1lll1_opy_ = bstack1l1ll1lll1l_opy_(test, bstack11l111l1l1_opy_, result, call, bstack11ll11111l_opy_, outcome)
    driver = getattr(test, bstack1l11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ᧺"), None)
    if bstack11ll11111l_opy_ == bstack1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ᧻") and driver:
        bstack11l1l1lll1_opy_[bstack1l11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ᧼")] = bstack1lll1lllll_opy_.bstack11l1l1l1ll_opy_(driver)
    if bstack11ll11111l_opy_ == bstack1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ᧽"):
        bstack11ll11111l_opy_ = bstack1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭᧾")
    bstack11l11l1lll_opy_ = {
        bstack1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ᧿"): bstack11ll11111l_opy_,
        bstack1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᨀ"): bstack11l1l1lll1_opy_
    }
    bstack1lll1lllll_opy_.bstack1llllll111_opy_(bstack11l11l1lll_opy_)
    if bstack11ll11111l_opy_ == bstack1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᨁ"):
        threading.current_thread().bstackTestMeta = {bstack1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᨂ"): bstack1l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᨃ")}
    elif bstack11ll11111l_opy_ == bstack1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᨄ"):
        threading.current_thread().bstackTestMeta = {bstack1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᨅ"): getattr(result, bstack1l11_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ᨆ"), bstack1l11_opy_ (u"࠭ࠧᨇ"))}
def bstack1l1ll11llll_opy_(test, bstack11l111l1l1_opy_, bstack11ll11111l_opy_, result=None, call=None, outcome=None, bstack1l1ll11111l_opy_=None):
    hook_data = bstack1l1ll1ll11l_opy_(test, bstack11l111l1l1_opy_, bstack11ll11111l_opy_, result, call, outcome, bstack1l1ll11111l_opy_)
    bstack11l11l1lll_opy_ = {
        bstack1l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᨈ"): bstack11ll11111l_opy_,
        bstack1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᨉ"): hook_data
    }
    bstack1lll1lllll_opy_.bstack1llllll111_opy_(bstack11l11l1lll_opy_)
def bstack11l11ll111_opy_(bstack11l111l1l1_opy_):
    if not bstack11l111l1l1_opy_:
        return None
    if bstack11l111l1l1_opy_.get(bstack1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᨊ"), None):
        return getattr(bstack11l111l1l1_opy_[bstack1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᨋ")], bstack1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᨌ"), None)
    return bstack11l111l1l1_opy_.get(bstack1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪᨍ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1lll1lllll_opy_.on():
            return
        places = [bstack1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᨎ"), bstack1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᨏ"), bstack1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᨐ")]
        bstack11l11ll1l1_opy_ = []
        for bstack1l1ll1ll1ll_opy_ in places:
            records = caplog.get_records(bstack1l1ll1ll1ll_opy_)
            bstack1l1ll1l11l1_opy_ = bstack1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᨑ") if bstack1l1ll1ll1ll_opy_ == bstack1l11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᨒ") else bstack1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᨓ")
            bstack1l1ll111lll_opy_ = request.node.nodeid + (bstack1l11_opy_ (u"ࠬ࠭ᨔ") if bstack1l1ll1ll1ll_opy_ == bstack1l11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᨕ") else bstack1l11_opy_ (u"ࠧ࠮ࠩᨖ") + bstack1l1ll1ll1ll_opy_)
            bstack11l1ll111l_opy_ = bstack11l11ll111_opy_(_11l11l11ll_opy_.get(bstack1l1ll111lll_opy_, None))
            if not bstack11l1ll111l_opy_:
                continue
            for record in records:
                if bstack1llll1l1l11_opy_(record.message):
                    continue
                bstack11l11ll1l1_opy_.append({
                    bstack1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᨗ"): bstack1lllll1l11l_opy_(record.created).isoformat() + bstack1l11_opy_ (u"ࠩ࡝ᨘࠫ"),
                    bstack1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᨙ"): record.levelname,
                    bstack1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᨚ"): record.message,
                    bstack1l1ll1l11l1_opy_: bstack11l1ll111l_opy_
                })
        if len(bstack11l11ll1l1_opy_) > 0:
            bstack1lll1lllll_opy_.bstack11111ll11_opy_(bstack11l11ll1l1_opy_)
    except Exception as err:
        print(bstack1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩᨛ"), str(err))
def bstack1l1llll111_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1l11l1l_opy_
    bstack1llll1l1ll_opy_ = bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ᨜"), None) and bstack1ll111111l_opy_(
            threading.current_thread(), bstack1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭᨝"), None)
    bstack111l1111l_opy_ = getattr(driver, bstack1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ᨞"), None) != None and getattr(driver, bstack1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ᨟"), None) == True
    if sequence == bstack1l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᨠ") and driver != None:
      if not bstack1l1l11l1l_opy_ and bstack1llll1llll1_opy_() and bstack1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᨡ") in CONFIG and CONFIG[bstack1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨢ")] == True and bstack1llllllll1_opy_.bstack1ll1lll1l_opy_(driver_command) and (bstack111l1111l_opy_ or bstack1llll1l1ll_opy_) and not bstack1ll1l111l_opy_(args):
        try:
          bstack1l1l11l1l_opy_ = True
          logger.debug(bstack1l11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨᨣ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬᨤ").format(str(err)))
        bstack1l1l11l1l_opy_ = False
    if sequence == bstack1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᨥ"):
        if driver_command == bstack1l11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᨦ"):
            bstack1lll1lllll_opy_.bstack1l1111l1_opy_({
                bstack1l11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᨧ"): response[bstack1l11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪᨨ")],
                bstack1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᨩ"): store[bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᨪ")]
            })
def bstack11ll11llll_opy_():
    global bstack11ll1l1lll_opy_
    bstack11l111l1_opy_.bstack1ll11ll11l_opy_()
    logging.shutdown()
    bstack1lll1lllll_opy_.bstack11l111l1ll_opy_()
    for driver in bstack11ll1l1lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1ll111111_opy_(*args):
    global bstack11ll1l1lll_opy_
    bstack1lll1lllll_opy_.bstack11l111l1ll_opy_()
    for driver in bstack11ll1l1lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll11111_opy_, stage=STAGE.SINGLE, bstack11l111lll_opy_=bstack1lll1llll_opy_)
def bstack1llll1lll1_opy_(self, *args, **kwargs):
    bstack1l1l1lll11_opy_ = bstack1l1l11111_opy_(self, *args, **kwargs)
    bstack1l1l1l1l11_opy_ = getattr(threading.current_thread(), bstack1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨᨫ"), None)
    if bstack1l1l1l1l11_opy_ and bstack1l1l1l1l11_opy_.get(bstack1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᨬ"), bstack1l11_opy_ (u"ࠩࠪᨭ")) == bstack1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᨮ"):
        bstack1lll1lllll_opy_.bstack111l1ll1l_opy_(self)
    return bstack1l1l1lll11_opy_
@measure(event_name=EVENTS.bstack1l1l1l11_opy_, stage=STAGE.bstack1lllll11l_opy_, bstack11l111lll_opy_=bstack1lll1llll_opy_)
def bstack1ll111l1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack111l11ll1_opy_ = Config.bstack11ll111lll_opy_()
    if bstack111l11ll1_opy_.get_property(bstack1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨᨯ")):
        return
    bstack111l11ll1_opy_.bstack1l1l1l1ll_opy_(bstack1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩᨰ"), True)
    global bstack1ll1l11l1_opy_
    global bstack1ll1111l1l_opy_
    bstack1ll1l11l1_opy_ = framework_name
    logger.info(bstack1l1l11l11l_opy_.format(bstack1ll1l11l1_opy_.split(bstack1l11_opy_ (u"࠭࠭ࠨᨱ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1llll1llll1_opy_():
            Service.start = bstack11111ll1l_opy_
            Service.stop = bstack1l1llllll_opy_
            webdriver.Remote.__init__ = bstack1111111ll_opy_
            webdriver.Remote.get = bstack11ll11ll_opy_
            if not isinstance(os.getenv(bstack1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨᨲ")), str):
                return
            WebDriver.close = bstack1lll11111l_opy_
            WebDriver.quit = bstack1lll1l1111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1llll1llll1_opy_() and bstack1lll1lllll_opy_.on():
            webdriver.Remote.__init__ = bstack1llll1lll1_opy_
        bstack1ll1111l1l_opy_ = True
    except Exception as e:
        pass
    bstack11llll11l_opy_()
    if os.environ.get(bstack1l11_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭ᨳ")):
        bstack1ll1111l1l_opy_ = eval(os.environ.get(bstack1l11_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧᨴ")))
    if not bstack1ll1111l1l_opy_:
        bstack11ll1llll1_opy_(bstack1l11_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧᨵ"), bstack1lll11l1_opy_)
    if bstack11ll1ll1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1111l11l1_opy_ = bstack1ll1ll1111_opy_
        except Exception as e:
            logger.error(bstack1111ll11_opy_.format(str(e)))
    if bstack1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᨶ") in str(framework_name).lower():
        if not bstack1llll1llll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1111111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1l1lll_opy_
            Config.getoption = bstack1l1ll1lll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l1llll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1llll111ll_opy_, stage=STAGE.SINGLE, bstack11l111lll_opy_=bstack1lll1llll_opy_)
def bstack1lll1l1111_opy_(self):
    global bstack1ll1l11l1_opy_
    global bstack11lll111ll_opy_
    global bstack1l1llll1_opy_
    try:
        if bstack1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᨷ") in bstack1ll1l11l1_opy_ and self.session_id != None and bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᨸ"), bstack1l11_opy_ (u"ࠧࠨᨹ")) != bstack1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᨺ"):
            bstack11l1l1111_opy_ = bstack1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᨻ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᨼ")
            bstack1ll11l1111_opy_(logger, True)
            if self != None:
                bstack1ll11lllll_opy_(self, bstack11l1l1111_opy_, bstack1l11_opy_ (u"ࠫ࠱ࠦࠧᨽ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᨾ"), None)
        if item is not None and bstack1ll111111l_opy_(threading.current_thread(), bstack1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᨿ"), None):
            bstack1l1l11l1_opy_.bstack1ll1l111ll_opy_(self, bstack111ll111_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l11_opy_ (u"ࠧࠨᩀ")
    except Exception as e:
        logger.debug(bstack1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤᩁ") + str(e))
    bstack1l1llll1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1l1l1lll_opy_, stage=STAGE.SINGLE, bstack11l111lll_opy_=bstack1lll1llll_opy_)
def bstack1111111ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11lll111ll_opy_
    global bstack1lll1llll_opy_
    global bstack1lllll1l1_opy_
    global bstack1ll1l11l1_opy_
    global bstack1l1l11111_opy_
    global bstack11ll1l1lll_opy_
    global bstack11ll11l11l_opy_
    global bstack1lll11lll1_opy_
    global bstack111ll111_opy_
    CONFIG[bstack1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᩂ")] = str(bstack1ll1l11l1_opy_) + str(__version__)
    command_executor = bstack1l11l1l1ll_opy_(bstack11ll11l11l_opy_, CONFIG)
    logger.debug(bstack1lll11l11l_opy_.format(command_executor))
    proxy = bstack1111ll1ll_opy_(CONFIG, proxy)
    bstack1l111111_opy_ = 0
    try:
        if bstack1lllll1l1_opy_ is True:
            bstack1l111111_opy_ = int(os.environ.get(bstack1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᩃ")))
    except:
        bstack1l111111_opy_ = 0
    bstack1l111ll1ll_opy_ = bstack111ll1ll_opy_(CONFIG, bstack1l111111_opy_)
    logger.debug(bstack11l1llll1_opy_.format(str(bstack1l111ll1ll_opy_)))
    bstack111ll111_opy_ = CONFIG.get(bstack1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᩄ"))[bstack1l111111_opy_]
    if bstack1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᩅ") in CONFIG and CONFIG[bstack1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᩆ")]:
        bstack11ll1l11ll_opy_(bstack1l111ll1ll_opy_, bstack1lll11lll1_opy_)
    if bstack1l1l11llll_opy_.bstack11lll1l1ll_opy_(CONFIG, bstack1l111111_opy_) and bstack1l1l11llll_opy_.bstack1l1111l1l_opy_(bstack1l111ll1ll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        bstack1l1l11llll_opy_.set_capabilities(bstack1l111ll1ll_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll111l11_opy_ = bstack1ll1l1l1l_opy_(desired_capabilities)
        bstack1ll111l11_opy_[bstack1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᩇ")] = bstack11ll1l1l11_opy_(CONFIG)
        bstack1111ll11l_opy_ = bstack111ll1ll_opy_(bstack1ll111l11_opy_)
        if bstack1111ll11l_opy_:
            bstack1l111ll1ll_opy_ = update(bstack1111ll11l_opy_, bstack1l111ll1ll_opy_)
        desired_capabilities = None
    if options:
        bstack1l111l1l11_opy_(options, bstack1l111ll1ll_opy_)
    if not options:
        options = bstack1l1l1111l_opy_(bstack1l111ll1ll_opy_)
    if proxy and bstack11ll1111_opy_() >= version.parse(bstack1l11_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᩈ")):
        options.proxy(proxy)
    if options and bstack11ll1111_opy_() >= version.parse(bstack1l11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᩉ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11ll1111_opy_() < version.parse(bstack1l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᩊ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l111ll1ll_opy_)
    logger.info(bstack1l1111ll1_opy_)
    bstack11ll1lllll_opy_.end(EVENTS.bstack1l1l1l11_opy_.value, EVENTS.bstack1l1l1l11_opy_.value + bstack1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᩋ"),
                               EVENTS.bstack1l1l1l11_opy_.value + bstack1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᩌ"), True, None)
    if bstack11ll1111_opy_() >= version.parse(bstack1l11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᩍ")):
        bstack1l1l11111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll1111_opy_() >= version.parse(bstack1l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᩎ")):
        bstack1l1l11111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll1111_opy_() >= version.parse(bstack1l11_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᩏ")):
        bstack1l1l11111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l1l11111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11llll111_opy_ = bstack1l11_opy_ (u"ࠩࠪᩐ")
        if bstack11ll1111_opy_() >= version.parse(bstack1l11_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫᩑ")):
            bstack11llll111_opy_ = self.caps.get(bstack1l11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦᩒ"))
        else:
            bstack11llll111_opy_ = self.capabilities.get(bstack1l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧᩓ"))
        if bstack11llll111_opy_:
            bstack1lll1ll1ll_opy_(bstack11llll111_opy_)
            if bstack11ll1111_opy_() <= version.parse(bstack1l11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ᩔ")):
                self.command_executor._url = bstack1l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᩕ") + bstack11ll11l11l_opy_ + bstack1l11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧᩖ")
            else:
                self.command_executor._url = bstack1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᩗ") + bstack11llll111_opy_ + bstack1l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᩘ")
            logger.debug(bstack1ll11ll11_opy_.format(bstack11llll111_opy_))
        else:
            logger.debug(bstack11l111111_opy_.format(bstack1l11_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧᩙ")))
    except Exception as e:
        logger.debug(bstack11l111111_opy_.format(e))
    bstack11lll111ll_opy_ = self.session_id
    if bstack1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᩚ") in bstack1ll1l11l1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᩛ"), None)
        if item:
            bstack1l1ll111l1l_opy_ = getattr(item, bstack1l11_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬᩜ"), False)
            if not getattr(item, bstack1l11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᩝ"), None) and bstack1l1ll111l1l_opy_:
                setattr(store[bstack1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᩞ")], bstack1l11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ᩟"), self)
        bstack1l1l1l1l11_opy_ = getattr(threading.current_thread(), bstack1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥ᩠ࠬ"), None)
        if bstack1l1l1l1l11_opy_ and bstack1l1l1l1l11_opy_.get(bstack1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᩡ"), bstack1l11_opy_ (u"࠭ࠧᩢ")) == bstack1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᩣ"):
            bstack1lll1lllll_opy_.bstack111l1ll1l_opy_(self)
    bstack11ll1l1lll_opy_.append(self)
    if bstack1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᩤ") in CONFIG and bstack1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᩥ") in CONFIG[bstack1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᩦ")][bstack1l111111_opy_]:
        bstack1lll1llll_opy_ = CONFIG[bstack1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᩧ")][bstack1l111111_opy_][bstack1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᩨ")]
    logger.debug(bstack1ll11l1l11_opy_.format(bstack11lll111ll_opy_))
@measure(event_name=EVENTS.bstack111llllll_opy_, stage=STAGE.SINGLE, bstack11l111lll_opy_=bstack1lll1llll_opy_)
def bstack11ll11ll_opy_(self, url):
    global bstack1llll1l1l1_opy_
    global CONFIG
    try:
        bstack11ll1l1l1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l11l11ll_opy_.format(str(err)))
    try:
        bstack1llll1l1l1_opy_(self, url)
    except Exception as e:
        try:
            bstack11l11l1l1_opy_ = str(e)
            if any(err_msg in bstack11l11l1l1_opy_ for err_msg in bstack1l1llll11l_opy_):
                bstack11ll1l1l1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l11l11ll_opy_.format(str(err)))
        raise e
def bstack1lll1ll11_opy_(item, when):
    global bstack1l11ll1l_opy_
    try:
        bstack1l11ll1l_opy_(item, when)
    except Exception as e:
        pass
def bstack11l1llll_opy_(item, call, rep):
    global bstack11111lll_opy_
    global bstack11ll1l1lll_opy_
    name = bstack1l11_opy_ (u"࠭ࠧᩩ")
    try:
        if rep.when == bstack1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᩪ"):
            bstack11lll111ll_opy_ = threading.current_thread().bstackSessionId
            bstack1l1ll1l1l11_opy_ = item.config.getoption(bstack1l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᩫ"))
            try:
                if (str(bstack1l1ll1l1l11_opy_).lower() != bstack1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᩬ")):
                    name = str(rep.nodeid)
                    bstack1l1ll111l1_opy_ = bstack11lll11l1_opy_(bstack1l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᩭ"), name, bstack1l11_opy_ (u"ࠫࠬᩮ"), bstack1l11_opy_ (u"ࠬ࠭ᩯ"), bstack1l11_opy_ (u"࠭ࠧᩰ"), bstack1l11_opy_ (u"ࠧࠨᩱ"))
                    os.environ[bstack1l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᩲ")] = name
                    for driver in bstack11ll1l1lll_opy_:
                        if bstack11lll111ll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1ll111l1_opy_)
            except Exception as e:
                logger.debug(bstack1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᩳ").format(str(e)))
            try:
                bstack11111l111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᩴ"):
                    status = bstack1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᩵") if rep.outcome.lower() == bstack1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᩶") else bstack1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᩷")
                    reason = bstack1l11_opy_ (u"ࠧࠨ᩸")
                    if status == bstack1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᩹"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ᩺") if status == bstack1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᩻") else bstack1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᩼")
                    data = name + bstack1l11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ᩽") if status == bstack1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᩾") else name + bstack1l11_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤ᩿ࠢࠢࠪ") + reason
                    bstack11111lll1_opy_ = bstack11lll11l1_opy_(bstack1l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ᪀"), bstack1l11_opy_ (u"ࠩࠪ᪁"), bstack1l11_opy_ (u"ࠪࠫ᪂"), bstack1l11_opy_ (u"ࠫࠬ᪃"), level, data)
                    for driver in bstack11ll1l1lll_opy_:
                        if bstack11lll111ll_opy_ == driver.session_id:
                            driver.execute_script(bstack11111lll1_opy_)
            except Exception as e:
                logger.debug(bstack1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ᪄").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ᪅").format(str(e)))
    bstack11111lll_opy_(item, call, rep)
notset = Notset()
def bstack1l1ll1lll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll11ll11_opy_
    if str(name).lower() == bstack1l11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ᪆"):
        return bstack1l11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ᪇")
    else:
        return bstack1lll11ll11_opy_(self, name, default, skip)
def bstack1ll1ll1111_opy_(self):
    global CONFIG
    global bstack11lll11111_opy_
    try:
        proxy = bstack11l1l1l1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ᪈")):
                proxies = bstack11ll111l1_opy_(proxy, bstack1l11l1l1ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1111l1111_opy_ = proxies.popitem()
                    if bstack1l11_opy_ (u"ࠥ࠾࠴࠵ࠢ᪉") in bstack1111l1111_opy_:
                        return bstack1111l1111_opy_
                    else:
                        return bstack1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ᪊") + bstack1111l1111_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤ᪋").format(str(e)))
    return bstack11lll11111_opy_(self)
def bstack11ll1ll1l_opy_():
    return (bstack1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᪌") in CONFIG or bstack1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᪍") in CONFIG) and bstack1l1lll11ll_opy_() and bstack11ll1111_opy_() >= version.parse(
        bstack11llllll1l_opy_)
def bstack1l111ll1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1lll1llll_opy_
    global bstack1lllll1l1_opy_
    global bstack1ll1l11l1_opy_
    CONFIG[bstack1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᪎")] = str(bstack1ll1l11l1_opy_) + str(__version__)
    bstack1l111111_opy_ = 0
    try:
        if bstack1lllll1l1_opy_ is True:
            bstack1l111111_opy_ = int(os.environ.get(bstack1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᪏")))
    except:
        bstack1l111111_opy_ = 0
    CONFIG[bstack1l11_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ᪐")] = True
    bstack1l111ll1ll_opy_ = bstack111ll1ll_opy_(CONFIG, bstack1l111111_opy_)
    logger.debug(bstack11l1llll1_opy_.format(str(bstack1l111ll1ll_opy_)))
    if CONFIG.get(bstack1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ᪑")):
        bstack11ll1l11ll_opy_(bstack1l111ll1ll_opy_, bstack1lll11lll1_opy_)
    if bstack1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᪒") in CONFIG and bstack1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᪓") in CONFIG[bstack1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᪔")][bstack1l111111_opy_]:
        bstack1lll1llll_opy_ = CONFIG[bstack1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᪕")][bstack1l111111_opy_][bstack1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᪖")]
    import urllib
    import json
    if bstack1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ᪗") in CONFIG and str(CONFIG[bstack1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᪘")]).lower() != bstack1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ᪙"):
        bstack1lllll111_opy_ = bstack11l11ll1l_opy_()
        bstack11ll11lll1_opy_ = bstack1lllll111_opy_ + urllib.parse.quote(json.dumps(bstack1l111ll1ll_opy_))
    else:
        bstack11ll11lll1_opy_ = bstack1l11_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ᪚") + urllib.parse.quote(json.dumps(bstack1l111ll1ll_opy_))
    browser = self.connect(bstack11ll11lll1_opy_)
    return browser
def bstack11llll11l_opy_():
    global bstack1ll1111l1l_opy_
    global bstack1ll1l11l1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11lll1lll1_opy_
        if not bstack1llll1llll1_opy_():
            global bstack11ll11l111_opy_
            if not bstack11ll11l111_opy_:
                from bstack_utils.helper import bstack1lll111l1_opy_, bstack111ll1l11_opy_
                bstack11ll11l111_opy_ = bstack1lll111l1_opy_()
                bstack111ll1l11_opy_(bstack1ll1l11l1_opy_)
            BrowserType.connect = bstack11lll1lll1_opy_
            return
        BrowserType.launch = bstack1l111ll1_opy_
        bstack1ll1111l1l_opy_ = True
    except Exception as e:
        pass
def bstack1l1ll11l1ll_opy_():
    global CONFIG
    global bstack111ll1ll1_opy_
    global bstack11ll11l11l_opy_
    global bstack1lll11lll1_opy_
    global bstack1lllll1l1_opy_
    global bstack11111ll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭᪛")))
    bstack111ll1ll1_opy_ = eval(os.environ.get(bstack1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᪜")))
    bstack11ll11l11l_opy_ = os.environ.get(bstack1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ᪝"))
    bstack1llll1l1l_opy_(CONFIG, bstack111ll1ll1_opy_)
    bstack11111ll1_opy_ = bstack11l111l1_opy_.bstack11111l1l1_opy_(CONFIG, bstack11111ll1_opy_)
    global bstack1l1l11111_opy_
    global bstack1l1llll1_opy_
    global bstack11lllll11_opy_
    global bstack1ll1l1ll1_opy_
    global bstack11lllll1ll_opy_
    global bstack111l11ll_opy_
    global bstack1l111ll11l_opy_
    global bstack1llll1l1l1_opy_
    global bstack11lll11111_opy_
    global bstack1lll11ll11_opy_
    global bstack1l11ll1l_opy_
    global bstack11111lll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1l11111_opy_ = webdriver.Remote.__init__
        bstack1l1llll1_opy_ = WebDriver.quit
        bstack1l111ll11l_opy_ = WebDriver.close
        bstack1llll1l1l1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭᪞") in CONFIG or bstack1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ᪟") in CONFIG) and bstack1l1lll11ll_opy_():
        if bstack11ll1111_opy_() < version.parse(bstack11llllll1l_opy_):
            logger.error(bstack111l1l111_opy_.format(bstack11ll1111_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11lll11111_opy_ = RemoteConnection._1111l11l1_opy_
            except Exception as e:
                logger.error(bstack1111ll11_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lll11ll11_opy_ = Config.getoption
        from _pytest import runner
        bstack1l11ll1l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l11111l1_opy_)
    try:
        from pytest_bdd import reporting
        bstack11111lll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l11_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭᪠"))
    bstack1lll11lll1_opy_ = CONFIG.get(bstack1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ᪡"), {}).get(bstack1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᪢"))
    bstack1lllll1l1_opy_ = True
    bstack1ll111l1_opy_(bstack11l1ll1l1_opy_)
if (bstack1llllll111l_opy_()):
    bstack1l1ll11l1ll_opy_()
@bstack11l11llll1_opy_(class_method=False)
def bstack1l1ll1l1ll1_opy_(hook_name, event, bstack1l1l1llllll_opy_=None):
    if hook_name not in [bstack1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ᪣"), bstack1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭᪤"), bstack1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ᪥"), bstack1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭᪦"), bstack1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᪧ"), bstack1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ᪨"), bstack1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭᪩"), bstack1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ᪪")]:
        return
    node = store[bstack1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭᪫")]
    if hook_name in [bstack1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ᪬"), bstack1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭᪭")]:
        node = store[bstack1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ᪮")]
    elif hook_name in [bstack1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ᪯"), bstack1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ᪰")]:
        node = store[bstack1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭᪱")]
    if event == bstack1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ᪲"):
        hook_type = bstack1ll11lll111_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11l11111l1_opy_ = {
            bstack1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᪳"): uuid,
            bstack1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᪴"): bstack11ll1111l1_opy_(),
            bstack1l11_opy_ (u"ࠬࡺࡹࡱࡧ᪵ࠪ"): bstack1l11_opy_ (u"࠭ࡨࡰࡱ࡮᪶ࠫ"),
            bstack1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧ᪷ࠪ"): hook_type,
            bstack1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨ᪸ࠫ"): hook_name
        }
        store[bstack1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ᪹࠭")].append(uuid)
        bstack1l1ll111l11_opy_ = node.nodeid
        if hook_type == bstack1l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ᪺"):
            if not _11l11l11ll_opy_.get(bstack1l1ll111l11_opy_, None):
                _11l11l11ll_opy_[bstack1l1ll111l11_opy_] = {bstack1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ᪻"): []}
            _11l11l11ll_opy_[bstack1l1ll111l11_opy_][bstack1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ᪼")].append(bstack11l11111l1_opy_[bstack1l11_opy_ (u"࠭ࡵࡶ࡫ࡧ᪽ࠫ")])
        _11l11l11ll_opy_[bstack1l1ll111l11_opy_ + bstack1l11_opy_ (u"ࠧ࠮ࠩ᪾") + hook_name] = bstack11l11111l1_opy_
        bstack1l1ll11llll_opy_(node, bstack11l11111l1_opy_, bstack1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥᪿࠩ"))
    elif event == bstack1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᫀ"):
        bstack11l1ll1ll1_opy_ = node.nodeid + bstack1l11_opy_ (u"ࠪ࠱ࠬ᫁") + hook_name
        _11l11l11ll_opy_[bstack11l1ll1ll1_opy_][bstack1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᫂")] = bstack11ll1111l1_opy_()
        bstack1l1ll1111ll_opy_(_11l11l11ll_opy_[bstack11l1ll1ll1_opy_][bstack1l11_opy_ (u"ࠬࡻࡵࡪࡦ᫃ࠪ")])
        bstack1l1ll11llll_opy_(node, _11l11l11ll_opy_[bstack11l1ll1ll1_opy_], bstack1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᫄"), bstack1l1ll11111l_opy_=bstack1l1l1llllll_opy_)
def bstack1l1ll1l111l_opy_():
    global bstack1l1ll1ll1l1_opy_
    if bstack1l11l11111_opy_():
        bstack1l1ll1ll1l1_opy_ = bstack1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ᫅")
    else:
        bstack1l1ll1ll1l1_opy_ = bstack1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᫆")
@bstack1lll1lllll_opy_.bstack1l1llll11l1_opy_
def bstack1l1ll11l11l_opy_():
    bstack1l1ll1l111l_opy_()
    if bstack1l1lll11ll_opy_():
        bstack1l1l1ll111_opy_(bstack1l1llll111_opy_)
    try:
        bstack1lll1ll11l1_opy_(bstack1l1ll1l1ll1_opy_)
    except Exception as e:
        logger.debug(bstack1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ᫇").format(e))
bstack1l1ll11l11l_opy_()
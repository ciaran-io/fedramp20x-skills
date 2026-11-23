"""Unit tests for {module}.py. Every test fixes the run date."""
import copy
from datetime import date

import {module} as m

AS_OF = date({YYYY}, {M}, {D})
SAMPLE = {}  # load the sample inputs here, parsed as the check's run() parses them


def test_sample_passes():
    assert m.static_method(SAMPLE, AS_OF)["status"] == "pass"
    assert m.live_method(SAMPLE, AS_OF)["status"] == "pass"


# One test per "fails when" condition in the design, for example:
def test_live_fails_when_overdue():
    pass

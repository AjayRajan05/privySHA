# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Action enforcement gate — calibrated bands + hard-override ensemble."""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict

from .alignment_bands import (
    calibrate_score,
    has_hard_block_trigger,
    score_to_verdict,
)
from .contracts import MissionContract
from .evaluator import AlignmentEvaluator
from .payload_inspection import is_high_risk_tool, is_mission_local_tool
from .tool_capabilities import get_tool_capabilities
from .types import ActionEvent
from .verdicts import ActionVerdict, Verdict


class ActionGuard:
    """Intercept, normalize, and evaluate actions against the Mission Contract."""

    def __init__(self, evaluator: AlignmentEvaluator) -> None:
        self.evaluator = evaluator
        self._calibrator = None
        self._calibrator_loaded = False

    def _get_calibrator(self) -> Any:
        if not self._calibrator_loaded:
            from .alignment_bands import load_isotonic_calibrator

            self._calibrator = load_isotonic_calibrator()
            self._calibrator_loaded = True
        return self._calibrator

    def normalize_action(self, action_type: str, payload: Dict[str, Any]) -> ActionEvent:
        return ActionEvent(
            action_id=str(uuid.uuid4()),
            action_type=action_type,
            payload=payload,
            timestamp=time.time(),
        )

    def evaluate_action(
        self, action: ActionEvent, contract: MissionContract
    ) -> ActionVerdict:
        raw_score, explanation, triggers = self.evaluator.evaluate(action, contract)
        score = calibrate_score(raw_score, self._get_calibrator())
        verdict = score_to_verdict(score)
        risk_score = 1.0 - score

        # Ensemble hard overrides — independent signals force BLOCK even if
        # calibrated banding would allow a medium aggregate score through.
        if has_hard_block_trigger(triggers, explanation):
            verdict = Verdict.BLOCK
            risk_score = 1.0

        if action.action_type in contract.forbidden_actions:
            verdict = Verdict.BLOCK
            risk_score = 1.0
            explanation = (
                f"Action '{action.action_type}' explicitly forbidden by mission contract."
            )

        if action.action_type == "tool_call":
            tool_name = str(action.payload.get("tool_name", ""))
            if tool_name and (
                contract.local_only or contract.forbid_network_exfiltration
            ):
                caps = get_tool_capabilities(tool_name)
                if (
                    (
                        is_high_risk_tool(tool_name)
                        or caps.network_egress
                        or caps.destructive
                    )
                    and not is_mission_local_tool(tool_name, contract)
                ):
                    verdict = Verdict.BLOCK
                    risk_score = 1.0
                    explanation = (
                        f"High-risk tool '{tool_name}' requires human approval "
                        "before execution."
                    )

            # Resource-scope trigger already in evaluator; belt-and-suspenders:
            if any("resource scope violation" in t.lower() for t in triggers):
                verdict = Verdict.BLOCK
                risk_score = 1.0

        return ActionVerdict(
            verdict=verdict,
            reason=explanation,
            risk_score=risk_score,
            risk_triggers=tuple(triggers),
        )

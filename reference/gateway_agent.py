#!/usr/bin/env python3
"""
TeleHealth Connect - Gateway Agent Reference Solution
Level 3 Practical Exam

This is the instructor reference solution.
"""

from datetime import datetime
from signalwire_agents import AgentBase, SwaigFunctionResult

# Department routing
DEPARTMENTS = {
    "triage": "/patient",
    "scheduling": "/patient",
    "prescriptions": "/patient",
    "billing": "+15551111111",
    "emergency": "+15559999999"
}

OPERATING_HOURS = {
    "weekday": {"open": 8, "close": 20},
    "weekend": {"open": 9, "close": 17}
}


class GatewayAgent(AgentBase):
    def __init__(self):
        super().__init__(
            name="telehealth-gateway",
            route="/gateway"
        )

        self._configure_prompts()
        self._configure_language()
        self._setup_functions()

    def _configure_prompts(self):
        self.prompt_add_section(
            "Role",
            "You are the gateway agent for TeleHealth Connect, a HIPAA-compliant "
            "telehealth service. Route callers to the appropriate department."
        )

        self.prompt_add_section(
            "Services",
            bullets=[
                "Triage - For symptom assessment and medical questions",
                "Scheduling - To book or modify appointments",
                "Prescriptions - For refill requests",
                "Billing - For payment and insurance questions",
                "Emergency - For urgent medical situations"
            ]
        )

        self.prompt_add_section(
            "Important",
            "For life-threatening emergencies, always advise calling 911 first. "
            "Our emergency line is for urgent but non-life-threatening situations."
        )

    def _configure_language(self):
        self.add_language(
            "English",
            "en-US",
            "rime.spore",
            speech_fillers=["Um", "Let me see"],
            function_fillers=["One moment...", "Connecting you now..."]
        )

    def _setup_functions(self):
        @self.tool(
            description="Route call to appropriate department",
            parameters={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "Department to route to",
                        "enum": ["triage", "scheduling", "prescriptions", "billing", "emergency"]
                    }
                },
                "required": ["department"]
            }
        )
        def route_call(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            department = args.get("department", "triage")
            destination = DEPARTMENTS.get(department, DEPARTMENTS["triage"])

            result = SwaigFunctionResult(
                f"I'm transferring you to our {department} department now.",
                post_process=True
            )
            result.swml_transfer(destination, "Goodbye!", final=True)

            return result

        @self.tool(
            description="Get current operating hours",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        def get_hours(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            now = datetime.now()
            is_weekend = now.weekday() >= 5

            if is_weekend:
                hours = OPERATING_HOURS["weekend"]
                day_type = "weekends"
            else:
                hours = OPERATING_HOURS["weekday"]
                day_type = "weekdays"

            current_hour = now.hour
            is_open = hours["open"] <= current_hour < hours["close"]

            if is_open:
                return SwaigFunctionResult(
                    f"We're currently open. Our {day_type} hours are "
                    f"{hours['open']}AM to {hours['close'] - 12}PM. "
                    "How can I help you today?"
                )
            else:
                return SwaigFunctionResult(
                    f"We're currently closed. Our {day_type} hours are "
                    f"{hours['open']}AM to {hours['close'] - 12}PM. "
                    "For emergencies, I can connect you to our after-hours nurse line."
                )

        @self.tool(
            description="Provide emergency guidance",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        def emergency_guidance(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return SwaigFunctionResult(
                "If this is a life-threatening emergency, please hang up and call 911 immediately. "
                "For urgent but non-life-threatening situations, I can connect you to our "
                "on-call nurse. Would you like me to transfer you?"
            )


# Create agent instance
agent = GatewayAgent()

if __name__ == "__main__":
    agent.run()

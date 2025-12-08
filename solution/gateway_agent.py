#!/usr/bin/env python3
"""
TeleHealth Connect - Gateway Agent
Level 3 Practical Exam

Implement your gateway agent here.

Requirements:
1. Route calls to appropriate departments
2. Handle after-hours routing
3. Provide emergency guidance
4. Implement health check

See README.md for full requirements.
"""

from signalwire_agents import AgentBase, SwaigFunctionResult

# Department routing
DEPARTMENTS = {
    "triage": "/patient",
    "scheduling": "/patient",
    "prescriptions": "/patient",
    "billing": "+15551111111",
    "emergency": "+15559999999"
}

# Your implementation here...

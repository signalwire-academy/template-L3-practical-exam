#!/usr/bin/env python3
"""
TeleHealth Connect - Patient Services Agent Reference Solution
Level 3 Practical Exam

This is the instructor reference solution.
"""

from signalwire_agents import AgentBase, SwaigFunctionResult
from signalwire_agents.contexts import ContextBuilder

# Mock patient database
PATIENTS = {
    "M123456": {"name": "John Smith", "dob": "1980-01-15", "tier": "premium"},
    "M234567": {"name": "Jane Doe", "dob": "1975-06-20", "tier": "standard"},
}

# Mock appointment slots
AVAILABLE_SLOTS = {
    "cardiology": ["2024-01-15 9:00", "2024-01-15 14:00", "2024-01-16 10:00"],
    "general": ["2024-01-15 11:00", "2024-01-15 15:00", "2024-01-16 9:00"],
    "dermatology": ["2024-01-17 10:00", "2024-01-17 14:00"]
}

# Urgent symptoms that require escalation
URGENT_SYMPTOMS = ["chest pain", "difficulty breathing", "severe bleeding", "unconscious"]


class PatientAgent(AgentBase):
    def __init__(self):
        super().__init__(
            name="telehealth-patient",
            route="/patient"
        )

        self._configure_prompts()
        self._configure_recording()
        self._configure_language()
        self._setup_contexts()
        self._setup_functions()

    def _configure_prompts(self):
        self.prompt_add_section(
            "Role",
            "You are a patient services agent for TeleHealth Connect. "
            "This call may be recorded for quality purposes. "
            "Always verify patient identity before accessing or discussing PHI."
        )

        self.prompt_add_section(
            "HIPAA Compliance",
            bullets=[
                "Verify identity before discussing any health information",
                "Pause recording when collecting sensitive data",
                "Never log PHI or PII",
                "Escalate urgent symptoms immediately"
            ]
        )

    def _configure_recording(self):
        self.set_params({
            "record_call": True,
            "record_format": "mp3",
            "record_stereo": True
        })

    def _configure_language(self):
        self.add_language(
            "English",
            "en-US",
            "rime.spore",
            speech_fillers=["Um", "Let me check"],
            function_fillers=["One moment please...", "Looking that up..."]
        )

    def _setup_contexts(self):
        # Verification context
        verification = ContextBuilder("verification")
        verification.add_step(
            "system",
            "First, verify the patient's identity using their date of birth "
            "and member ID. Pause recording before collecting this information."
        )
        verification.set_functions(["verify_patient", "secure_input"])
        self.add_context(verification)

        # Triage context
        triage = ContextBuilder("triage")
        triage.add_step(
            "system",
            "Assess the patient's symptoms. If urgent, escalate immediately. "
            "Otherwise, help schedule an appropriate appointment."
        )
        triage.set_functions(["assess_symptoms", "escalate_urgent"])
        self.add_context(triage)

        # Scheduling context
        scheduling = ContextBuilder("scheduling")
        scheduling.add_step(
            "system",
            "Help the patient find and book an appointment with the "
            "appropriate specialist."
        )
        scheduling.set_functions(["check_availability", "book_appointment"])
        self.add_context(scheduling)

        # Prescriptions context
        prescriptions = ContextBuilder("prescriptions")
        prescriptions.add_step(
            "system",
            "Handle prescription refill requests. Verify the medication "
            "and pharmacy information."
        )
        prescriptions.set_functions(["request_refill"])
        self.add_context(prescriptions)

    def _setup_functions(self):
        @self.tool(
            description="Verify patient identity - SECURE function",
            parameters={
                "type": "object",
                "properties": {
                    "dob": {
                        "type": "string",
                        "description": "Patient date of birth (YYYY-MM-DD)"
                    },
                    "member_id": {
                        "type": "string",
                        "description": "Patient member ID"
                    }
                },
                "required": ["dob", "member_id"]
            },
            secure=True
        )
        def verify_patient(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            dob = args.get("dob", "")
            member_id = args.get("member_id", "").upper()

            patient = PATIENTS.get(member_id)
            if patient and patient["dob"] == dob:
                result = SwaigFunctionResult(
                    f"Thank you, {patient['name']}. Your identity has been verified. "
                    "How can I help you today?"
                )
                result.update_global_data({
                    "patient_verified": True,
                    "patient_name": patient["name"],
                    "patient_tier": patient["tier"]
                })
                result.set_context_switch("triage")
                # Resume recording after verification
                result.toggle_record(on=True)
                return result
            else:
                return SwaigFunctionResult(
                    "I couldn't verify your identity with that information. "
                    "Please check your member ID and date of birth and try again."
                )

        @self.tool(
            description="Pause recording for secure input",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        def secure_input(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            result = SwaigFunctionResult(
                "Recording has been paused. You can now share your information securely."
            )
            result.toggle_record(on=False)
            return result

        @self.tool(
            description="Assess patient symptoms",
            parameters={
                "type": "object",
                "properties": {
                    "symptoms": {
                        "type": "string",
                        "description": "Description of symptoms"
                    }
                },
                "required": ["symptoms"]
            }
        )
        def assess_symptoms(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            symptoms = args.get("symptoms", "").lower()

            # Check for urgent symptoms
            for urgent in URGENT_SYMPTOMS:
                if urgent in symptoms:
                    result = SwaigFunctionResult(
                        f"Based on your symptoms ({urgent}), I need to connect you "
                        "with a nurse immediately. Please hold."
                    )
                    result.swml_transfer("+15559999999", final=True)
                    return result

            result = SwaigFunctionResult(
                "Thank you for describing your symptoms. Based on what you've told me, "
                "I can help you schedule an appointment with the appropriate specialist. "
                "What type of doctor would you like to see?"
            )
            result.update_global_data({"symptoms": symptoms})
            result.set_context_switch("scheduling")
            return result

        @self.tool(
            description="Escalate to nurse for urgent symptoms",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        def escalate_urgent(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            result = SwaigFunctionResult(
                "I'm connecting you with an on-call nurse immediately. Please hold."
            )
            result.swml_transfer("+15559999999", final=True)
            return result

        @self.tool(
            description="Check appointment availability",
            parameters={
                "type": "object",
                "properties": {
                    "specialty": {
                        "type": "string",
                        "description": "Medical specialty",
                        "enum": ["cardiology", "general", "dermatology"]
                    },
                    "date": {
                        "type": "string",
                        "description": "Preferred date (YYYY-MM-DD)"
                    }
                },
                "required": ["specialty"]
            }
        )
        def check_availability(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            specialty = args.get("specialty", "general")
            slots = AVAILABLE_SLOTS.get(specialty, [])

            if slots:
                slot_list = ", ".join(slots[:3])
                return SwaigFunctionResult(
                    f"For {specialty}, I have the following available slots: {slot_list}. "
                    "Which one would work best for you?"
                )
            else:
                return SwaigFunctionResult(
                    f"I don't have any {specialty} slots available right now. "
                    "Would you like me to check another specialty or add you to a waitlist?"
                )

        @self.tool(
            description="Book an appointment",
            parameters={
                "type": "object",
                "properties": {
                    "slot_id": {
                        "type": "string",
                        "description": "Selected appointment slot"
                    }
                },
                "required": ["slot_id"]
            }
        )
        def book_appointment(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            slot_id = args.get("slot_id", "")
            raw_data = raw_data or {}
            global_data = raw_data.get("global_data", {})
            patient_name = global_data.get("patient_name", "Patient")

            result = SwaigFunctionResult(
                f"I've booked your appointment for {slot_id}. "
                f"A confirmation will be sent to your registered phone and email. "
                "Is there anything else I can help you with today?"
            )
            result.add_action("send_sms", {
                "to": "+15551234567",
                "body": f"Your TeleHealth appointment is confirmed for {slot_id}."
            })
            return result

        @self.tool(
            description="Request prescription refill",
            parameters={
                "type": "object",
                "properties": {
                    "medication": {
                        "type": "string",
                        "description": "Name of medication"
                    },
                    "pharmacy": {
                        "type": "string",
                        "description": "Preferred pharmacy name"
                    }
                },
                "required": ["medication", "pharmacy"]
            }
        )
        def request_refill(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            medication = args.get("medication", "")
            pharmacy = args.get("pharmacy", "")

            return SwaigFunctionResult(
                f"I've submitted a refill request for {medication} to {pharmacy}. "
                "Your doctor will review it within 24-48 hours. "
                "The pharmacy will contact you when it's ready. "
                "Is there anything else I can help you with?"
            )


# Create agent instance
agent = PatientAgent()

if __name__ == "__main__":
    agent.run()

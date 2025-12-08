# Level 3 Practical Exam: Certified Voice AI Architect

| | |
|--|--|
| **Duration** | 4 hours |
| **Passing Score** | 80 points (70% automated + manual review) |

## Scenario: TeleHealth Connect

Design and implement a production-ready telehealth voice AI system that:

- Triages patient symptoms
- Schedules appointments with specialists
- Provides medication reminders
- Handles prescription refill requests
- Routes to on-call nurses for urgent issues

### Compliance Requirements

- HIPAA-compliant data handling
- No PHI in logs
- Recording consent required
- Identity verification before PHI access

## Requirements

### Part 1: Architecture Design (20 points)

Create `architecture/` directory with:

**1. `overview.md`** - System overview including:
- High-level architecture description
- List of agents and responsibilities
- Integration points
- Data flow description

**2. `diagram.md`** - ASCII or described system diagram showing:
- Agent relationships
- Data flow
- External integrations
- Security boundaries

**3. ADRs (Architecture Decision Records):**
- `adr/001-agent-structure.md` - Agent organization decisions
- `adr/002-hipaa-compliance.md` - HIPAA approach
- `adr/003-knowledge-strategy.md` - Knowledge base design

### Part 2: Gateway Agent (15 points)

Create `solution/gateway_agent.py`:

**Required Functions:**
- `route_call(department)` - Route to appropriate specialist
- `get_hours()` - Return operating hours
- `emergency_guidance()` - Provide emergency info

**Requirements:**
- Clean routing logic
- After-hours handling
- Emergency handling
- Health endpoint
- Authentication

### Part 3: Patient Services Agent (25 points)

Create `solution/patient_agent.py`:

**Required Contexts:**
1. **Verification** - Verify patient identity
2. **Triage** - Assess symptoms
3. **Scheduling** - Book appointments
4. **Prescriptions** - Handle refills

**Required Functions:**

*Verification:*
- `verify_patient(dob, member_id)` - Verify identity (secure)

*Triage:*
- `assess_symptoms(symptoms)` - Initial assessment
- `escalate_urgent()` - Route to nurse

*Scheduling:*
- `check_availability(specialty, date)` - Check availability
- `book_appointment(slot_id)` - Confirm booking

*Prescriptions:*
- `request_refill(medication, pharmacy)` - Submit refill request

### Part 4: Knowledge Integration (10 points)

Create knowledge base content:
- `knowledge/symptoms.md` - Symptom guidance
- `knowledge/medications.md` - Medication info

Integrate search skill in patient agent.

### Part 5: Observability (15 points)

Create `shared/` directory with:

**1. `logging_config.py`** - Structured JSON logging
- Call ID correlation
- Function timing
- PHI exclusion

**2. `metrics.py`** - Prometheus metrics
- Call counters
- Function latency histograms
- Business metrics

**3. `config/alerts.yml`** - Alert rules
- Error rate alert
- Latency alert
- Business metric alerts

### Part 6: Deployment (10 points)

Create `deployment/` directory with:

**1. `Dockerfile`**
- Multi-stage build
- Non-root user
- Health check

**2. `docker-compose.yml`**
- All agents
- Environment configuration
- Health checks

**3. `.env.example`**
- All required variables with comments

### Part 7: Testing & Documentation (5 points)

- `tests/test_verification.py` - Test patient verification
- `README.md` - Setup instructions and API docs

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Test gateway agent
swaig-test solution/gateway_agent.py --dump-swml
swaig-test solution/gateway_agent.py --exec route_call --department "triage"

# Test patient agent
swaig-test solution/patient_agent.py --list-tools
swaig-test solution/patient_agent.py --exec verify_patient \
  --dob "1980-01-15" --member_id "M123456"

# Build Docker
docker build -t telehealth:latest -f deployment/Dockerfile .

# Run with compose
docker-compose -f deployment/docker-compose.yml up
```

## Submission Structure

```
solution/
├── gateway_agent.py
├── patient_agent.py
├── architecture/
│   ├── overview.md
│   ├── diagram.md
│   └── adr/
│       ├── 001-agent-structure.md
│       ├── 002-hipaa-compliance.md
│       └── 003-knowledge-strategy.md
├── knowledge/
│   ├── symptoms.md
│   └── medications.md
├── shared/
│   ├── logging_config.py
│   └── metrics.py
├── config/
│   └── alerts.yml
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
├── tests/
│   └── test_verification.py
└── README.md
```

## Grading Breakdown

| Component | Points | Type |
|-----------|--------|------|
| Gateway agent loads | 5 | Automated |
| Gateway SWML valid | 5 | Automated |
| route_call exists | 5 | Automated |
| Patient agent loads | 5 | Automated |
| Patient SWML valid | 5 | Automated |
| verify_patient exists | 5 | Automated |
| assess_symptoms exists | 5 | Automated |
| book_appointment exists | 5 | Automated |
| Secure function marking | 5 | Automated |
| Multi-context workflow | 5 | Automated |
| Recording control | 5 | Automated |
| route_call works | 5 | Automated |
| verify_patient works | 5 | Automated |
| Transfer capability | 5 | Automated |
| get_hours exists | 5 | Automated |
| request_refill exists | 5 | Automated |
| Architecture docs | 10 | Manual |
| Observability setup | 5 | Manual |
| Deployment config | 5 | Manual |
| **Total** | **100** | |

---

## Certification Complete

Congratulations! You've completed all requirements for the **Certified Voice AI Architect** certification!

---

*SignalWire AI Agents Certification - Level 3 Practical Exam*

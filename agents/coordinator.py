from tools.supabase_client import SupabaseClient
from .greeting import GreetingAgent
from .dm_check import DMCheckAgent
from .renovation_q import RenovationQAgent
from .qualify import QualifyAgent
from .objection import ObjectionAgent
from .faq import FAQAgent
from .appointment import AppointmentAgent
from .prep_remind import PrepRemindAgent
from .followup import FollowUpAgent

class Coordinator:
    def __init__(self):
        self.supabase = SupabaseClient()
        self.agents = {
            "greeting": GreetingAgent(),
            "dm_check": DMCheckAgent(),
            "renovation_q": RenovationQAgent(),
            "qualify": QualifyAgent(),
            "objection": ObjectionAgent(),
            "faq": FAQAgent(),
            "appointment": AppointmentAgent(),
            "prep_remind": PrepRemindAgent(),
            "followup": FollowUpAgent(),
        }

    async def transfer_to_agent(self, intent: str, session_id: str, text: str):
        agent = self.agents.get(intent)
        if not agent:
            raise ValueError(f"Unknown intent: {intent}")
        return await agent.handle(session_id, text)

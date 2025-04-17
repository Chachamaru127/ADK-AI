from tools.supabase_client import SupabaseClient

class FollowUpAgent:
    def __init__(self):
        self.client = SupabaseClient()

    async def handle(self, session_id: str, text: str) -> str:
        return self.client.get_script("followup")

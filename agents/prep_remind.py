from tools.supabase_client import SupabaseClient

class PrepRemindAgent:
    def __init__(self):
        self.client = SupabaseClient()

    async def handle(self, session_id: str, text: str) -> str:
        return self.client.get_script('prep_remind')

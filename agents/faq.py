from tools.supabase_client import SupabaseClient

class FAQAgent:
    def __init__(self):
        self.client = SupabaseClient()

    async def handle(self, session_id: str, text: str) -> str:
        faqs=self.client.search_faq(text); return '\n'.join(faqs)

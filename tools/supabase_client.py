import os
from supabase import create_client, Client
from jinja2 import Template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

class SupabaseClient:
    def __init__(self):
        self.client = supabase

    def get_script(self, name: str) -> str:
        # Fetch script by name
        res = self.client.table("scripts").select("*").eq("name", name).single().execute()
        if res.error:
            raise Exception(f"get_script error: {res.error.message}")
        data = res.data
        content = data.get("content", "")
        variables = data.get("variables") or {}
        # Render with Jinja2
        template = Template(content)
        return template.render(**variables)

    def get_objection(self, objection_type: str, target_type: str) -> str:
        # Fetch top priority objection handler
        res = (
            self.client.table("objection_handlers")
            .select("*")
            .eq("objection_type", objection_type)
            .eq("target_type", target_type)
            .order("priority", {"ascending": True})
            .limit(1)
            .execute()
        )
        if res.error or not res.data:
            return None
        return res.data[0].get("response_content")

    def search_faq(self, query: str, limit: int = 5) -> list:
        # Search FAQ entries by title
        res = (
            self.client.table("knowledge")
            .select("*")
            .ilike("title", f"%{query}%")
            .limit(limit)
            .execute()
        )
        if res.error:
            raise Exception(f"search_faq error: {res.error.message}")
        items = res.data or []
        # Return contents of matching FAQs
        return [item.get("content") for item in items]

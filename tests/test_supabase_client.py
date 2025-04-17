import pytest
from tools.supabase_client import SupabaseClient

@pytest.fixture
def client():
    return SupabaseClient()

def test_get_script(client):
    # TODO: supabase emulator 設定後に実装
    assert hasattr(client, "get_script")

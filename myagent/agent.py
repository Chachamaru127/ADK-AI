from google.adk.agents.llm_agent import LlmAgent

root_agent = LlmAgent(
    model='gemini-1.5-flash',
    name='webui_agent',
    instruction='ユーザーの質問に日本語で丁寧に答えてください。',
) 
from google.adk.agents.llm_agent import LlmAgent

# テキスト用エージェント
root_agent = LlmAgent(
    model='gemini-2.0-flash-live-001',
    name='audio_text_agent',
    instruction='日本語で丁寧に答えてください。'
)

# 音声用エージェント（必要な箇所でimportして使う）
audio_agent = LlmAgent(
    model='gemini-2.0-flash-live-001',
    name='audio_agent',
    instruction='音声会話用のエージェントです。'
)

class RootAgent:
    def __init__(self, audio_agent, text_agent):
        self.audio_agent = audio_agent
        self.text_agent = text_agent

    def __call__(self, *args, **kwargs):
        input_type = kwargs.get('input_type', 'text')
        if input_type == 'audio':
            return self.audio_agent(*args, **kwargs)
        else:
            return self.text_agent(*args, **kwargs) 
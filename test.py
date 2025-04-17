import os
import google.generativeai as genai
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google.auth
from google.auth.exceptions import DefaultCredentialsError

load_dotenv()
print("DEBUG: .env ファイルを読み込みました。")

# --- Google Cloud 認証 ---
# gcloud auth application-default login を実行して認証情報を設定してください
try:
    print("DEBUG: Google Cloud 認証を試みます...")
    credentials, project_id = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    print(f"DEBUG: Google Cloud 認証成功。Project ID: {project_id}")
    if not credentials or not credentials.valid:
        print("認証情報が見つからないか、無効です。'gcloud auth application-default login' を実行してください。")
        # exit() # ここでは終了させずに続行してみる
    else:
        print("DEBUG: Google Cloud 認証情報は有効です。")
except DefaultCredentialsError:
    print("認証情報が見つかりませんでした。'gcloud auth application-default login' を実行してください。")
    # exit() # ここでは終了させずに続行してみる
except Exception as e:
    print(f"DEBUG: Google Cloud 認証中に予期せぬエラー: {e}")
    # exit()

# --- Gemini API キーの設定 ---
# 環境変数 GOOGLE_API_KEY からAPIキーを読み込むか、直接設定してください
api_key = os.getenv("GOOGLE_API_KEY")
print(f"DEBUG: GOOGLE_API_KEY: {api_key[:5]}...{api_key[-5:]}" if api_key else "DEBUG: GOOGLE_API_KEY が見つかりません。") # キーの一部のみ表示

if not api_key:
    print("環境変数 GOOGLE_API_KEY が設定されていません。")
    # ここにあなたのAPIキーを直接入力することもできます
    # api_key = "YOUR_API_KEY"
    # Google Cloud 認証情報からトークンを取得して代替することも検討できます
    # しかし、Gemini APIは通常APIキー認証を推奨します。
    # ここでは Google Cloud 認証情報のトークンを使用してみます。
    # ADKの認証機構と連携させる場合は、より適切な方法があるかもしれません。
    if credentials and hasattr(credentials, 'token'):
         print("警告: GOOGLE_API_KEY が見つかりません。Google Cloud認証情報のトークンを使用します。")
         # これは推奨される方法ではない可能性があります。Gemini APIのドキュメントを確認してください。
         # genai.configure(credentials=credentials) # credentials オブジェクトを直接渡せるか確認
         # 現状の genai ライブラリでは API キーが推奨されています。
         print("Gemini APIを使用するには、APIキーを設定することを強く推奨します。")
         exit() # APIキーがない場合は終了
    else:
        print("APIキーも有効なGoogle Cloud認証トークンも見つかりませんでした。")
        exit()

try:
    print("DEBUG: genai.configure を実行します...")
    genai.configure(api_key=api_key)
    print("DEBUG: genai.configure 成功。")
except Exception as e:
    print(f"DEBUG: genai.configure でエラー: {e}")
    exit()

# --- エージェントの定義 ---
print("DEBUG: GenerativeModel を初期化します...")
model = genai.GenerativeModel('gemini-1.5-flash') # または他の適切なモデル
print("DEBUG: GenerativeModel 初期化成功。")

prompt = "Google ADKについて簡単に教えてください。"

print(f"--- プロンプト ---")
print(prompt)
print(f"-----------------")

# --- モデルの実行 ---
try:
    print("DEBUG: model.generate_content を実行します...")
    response = model.generate_content(prompt)
    print("DEBUG: model.generate_content 成功。")
    print(f"--- モデルの応答 ---")
    print(response.text)
    print(f"--------------------")
except Exception as e:
    print(f"エラーが発生しました: {e}")

print("\nクイックスタート完了！")


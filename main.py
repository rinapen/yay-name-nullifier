import requests
import json
import sys

class YayProfileUpdater:    
    def __init__(self, access_token):
        self.access_token = access_token
        self.jwt_token = None
        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ja",
            "agent": "YayWeb 4.18.2",
            "authorization": f"Bearer {access_token}",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-device-info": "Yay 4.18.2 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36)"
        }
    
    def get_jwt(self):
        try:
            headers = self.base_headers.copy()
            headers.update({
                "baggage": "sentry-environment=production,sentry-public_key=4a55ec61d9f9565a070e92da003d0e97,sentry-trace_id=670e1c66967c4af88b04726637f95b1b,sentry-sample_rate=0.5,sentry-sampled=false",
                "sentry-trace": "670e1c66967c4af88b04726637f95b1b-92d2f1ca3eec4a90-0",
                "x-csrf-token": "0u8YS60hN8EaUkHvEUe5MB4y3sEsT9VSxrGGtaXsfSC6yC6q36Q5YPwr1kbjKtRx7PacUcHqurpJLhEwCoa9qg==",
                "Referer": "https://yay.space/"
            })
            
            response = requests.get("https://yay.space/api/jwt", headers=headers)
            response.raise_for_status()
            
            jwt_data = response.json()
            if 'jwt' in jwt_data:
                self.jwt_token = jwt_data['jwt']
                print(f"JWT取得: {self.jwt_token[:50]}...")
                return self.jwt_token
            else:
                print("JWTがレスポンスにない")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"[errorjwt]: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"[errorjson]: {e}")
            return None
    
    def update_profile(self, nickname="", biography=""):
        if not self.jwt_token:
            print("JWTトークンが取得されていません。先にget_jwt()を実行してください。")
            return False
        
        try:
            headers = self.base_headers.copy()
            headers.update({
                "content-type": "application/json;charset=UTF-8",
                "sec-fetch-site": "same-site",
                "x-app-version": "4.18.2",
                "x-jwt": self.jwt_token,
                "referrer": "https://yay.space/"
            })
            
            body = {
                "nickname": nickname,
                "biography": biography
            }
            
            response = requests.post(
                "https://api.yay.space/v3/users/edit",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            
            print(f"プロフィール更新完了:")
            print(f"  ニックネーム: '{nickname}'")
            print(f"  自己紹介: '{biography}'")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"プロフィール更新エラー: {e}")
            return False
    
    def nullify_name(self):
        return self.update_profile(nickname="\u200B", biography="")


def main():
    if len(sys.argv) != 2:
        print("使用方法: python main.py <アクセストークン>")
        print("例: python main.py 7470bcfbec081b90eda69a108e26946f4bb937688213eb3c8d6e3172dfc06ec5")
        sys.exit(1)
    
    access_token = sys.argv[1]
    
    updater = YayProfileUpdater(access_token)
    
    print("JWTトークンを取得中...")
    if not updater.get_jwt():
        print("JWTトークンの取得に失敗しました")
        sys.exit(1)
    
    print("ユーザー名を空白に設定中...")
    if updater.nullify_name():
        print("ユーザー名の空白化が完了しました！")
    else:
        print("ユーザー名の空白化に失敗しました")
        sys.exit(1)


if __name__ == "__main__":
    main()
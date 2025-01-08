import asyncio
import websockets
import json

class login():
    def __init__(self,username:str,password:any = ""):
        global usernamea
        usernamea = username
        self.username = username
        self.password = str(password)
        
        
    class connect_cloud_tw():
        def __init__(self,projectID:any):
            self.projectID = str(projectID)
        
        def set_var(self,variable:str,value:any):
            self.variable = variable
            self.value = value
            asyncio.run(self._set_cloud_variable())
            
            
        async def _set_cloud_variable(self):
            cloud_var_name = f"☁ {self.variable}"
            new_value = self.value

            uri = f"wss://clouddata.turbowarp.org/"

            async with websockets.connect(uri) as websocket:
                # ハンドシェイクメッセージを送信
                handshake_message = {
                    "method": "handshake",
                    "user": usernamea,
                    "project_id": self.projectID
                }
                await websocket.send(json.dumps(handshake_message))

                # クラウド変数の設定メッセージを送信
                set_variable_message = {
                    "method": "set",
                    "name": cloud_var_name,
                    "value": str(new_value)
                }
                await websocket.send(json.dumps(set_variable_message))

                # サーバーからの応答を待機（応答がない場合もあるため例外処理を追加）
                try:
                    response = await websocket.recv()
                    # print(f"Response: {response}")
                except websockets.exceptions.ConnectionClosedOK:
                    print("Connection closed normally without response.")
                    
        def get_var(self,variable:str):
            project_id = self.projectID  # 取得したいプロジェクトのID
            self.cloud_variable_name = f"☁ {variable}"  # クラウド変数名 (Scratchの仕様上"☁ "が必要)
            asyncio.run(self._get_cloud_variables())
        async def _get_cloud_variables(self):
            url = f"wss://clouddata.turbowarp.org/"
            async with websockets.connect(url) as ws:
                # TurboWarpのクラウド変数のサーバーへ接続要求
                await ws.send(json.dumps({
                    "method": "handshake",
                    "user": usernamea,  # 任意のユーザー名
                    "project_id": self.projectID
                }))
                
                message = await ws.recv()
                data = json.loads(message)
                return data[self.cloud_variable_name]
import random

class DummyDRLPolicy:
    """
    這是一個模擬的 DRL Policy Network (Actor Network)。
    在真實場景中，這會是一個載入預先訓練權重 (如 PPO, SAC) 的 PyTorch/TensorFlow 模型。
    這裡我們用簡單的邏輯與亂數來模擬其根據 State 與 Risk Penalty 輸出的 Action。
    """
    
    def __init__(self, model_name="PPO_Trading_V1"):
        self.model_name = model_name
        # 模擬模型的信心指數基底
        self.base_confidence = 0.7 
        print(f"[DRL System] Loaded DRL Policy Network: {self.model_name}")

    def get_action(self, state_data: dict, risk_penalty_factor: float) -> dict:
        """
        根據當前市場狀態與風險懲罰係數，輸出對應的買賣決策。
        
        Args:
            state_data (dict): 市場狀態，如價格、指標等。
            risk_penalty_factor (float): 0.0 ~ 1.0 的值，越高代表越保守（懲罰高風險動作）。
            
        Returns:
            dict: 包含 action (BUY/SELL/HOLD), proportion (比例), confidence (信心度)
        """
        print(f"  --> [DRL Engine] Running Forward Pass on state... (Risk Penalty: {risk_penalty_factor})")
        
        # 提取狀態特徵 (簡單模擬)
        macd = state_data.get("MACD", "Neutral")
        vix = state_data.get("VIX", "Normal")
        
        # 模擬 Actor Network 經過神經網路推論後的決策邏輯
        action = "HOLD"
        proportion = "0%"
        
        if macd == "Bearish" or vix == "High":
            # 市場狀況差，傾向賣出
            if risk_penalty_factor > 0.6:
                # 高度保守，重倉賣出
                action = "SELL"
                proportion = "50%"
            else:
                # 稍微保守，輕倉賣出
                action = "SELL"
                proportion = "20%"
        elif macd == "Bullish":
            # 市場狀況好，傾向買入
            if risk_penalty_factor > 0.6:
                # 即使市場好，因為風險厭惡，只輕倉買入
                action = "BUY"
                proportion = "10%"
            else:
                # 風險承受度高，重倉買入
                action = "BUY"
                proportion = "40%"
                
        # 模擬預期 Reward 帶來的信心度擾動
        confidence = round(self.base_confidence + random.uniform(-0.1, 0.2), 2)
        
        return {
            "action": action,
            "proportion": proportion,
            "confidence": confidence,
            "model_used": self.model_name
        }

if __name__ == "__main__":
    # 簡單的測試
    drl = DummyDRLPolicy()
    state = {"Price": 120, "MACD": "Bearish", "VIX": "High"}
    print(drl.get_action(state, risk_penalty_factor=0.8))

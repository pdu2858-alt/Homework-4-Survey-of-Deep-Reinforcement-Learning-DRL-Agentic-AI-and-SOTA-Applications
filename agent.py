import time
from tools import fetch_market_state, execute_drl_policy, run_portfolio_simulation

class Memory:
    def __init__(self):
        self.short_term = []
        self.long_term = {"user_risk_profile": "Unknown", "holdings": {"NVDA": 100, "AAPL": 50}}

    def add_context(self, text):
        self.short_term.append(text)
        
    def get_context(self):
        return "\n".join(self.short_term)

class TradingAgent:
    def __init__(self):
        self.memory = Memory()
        print("\n[System Controller] Trading Agent Initialized (LLM Core + ReAct Engine Ready)")

    def process_request(self, user_input: str):
        """
        模擬 LLM 處理使用者輸入並執行 ReAct (Thought-Action-Observation) 流程。
        """
        print(f"\n==================== 新任務啟動 ====================")
        print(f"[User Input]: {user_input}")
        
        # 1. 模擬 LLM 解析意圖與風險
        print("\n[LLM Thought 1]:")
        print("使用者詢問 NVDA 股票，且提到市場波動大、不想承擔風險。")
        print("=> 判斷 ticker='NVDA'")
        print("=> 判斷風險承受度='低'，將 risk_penalty_factor 設為 0.8。")
        print("=> 第一步：需要先獲取目前的市場狀態。")
        
        self.memory.add_context(f"Task: Manage NVDA. Risk: Low (0.8).")
        
        # 2. Action 1: 呼叫抓資料工具
        print("\n[Action 1]: 準備呼叫 `fetch_market_state`")
        time.sleep(1)
        state_data = fetch_market_state(ticker="NVDA", timeframe="1D")
        
        # 3. Observation 1
        print(f"\n[Observation 1]: 市場狀態顯示價格為 {state_data['Price']}，且 MACD 為 {state_data['MACD']}，VIX 為 {state_data['VIX']}。")
        
        # 4. 模擬 LLM 思考下一步
        print("\n[LLM Thought 2]:")
        print("已經取得狀態。市場確實存在風險。現在將狀態與高懲罰係數傳給底層的 DRL Policy 進行決策。")
        
        # 5. Action 2: 呼叫 DRL 工具
        print("\n[Action 2]: 準備呼叫 `execute_drl_policy`")
        time.sleep(1)
        drl_action = execute_drl_policy(state_data=state_data, risk_penalty_factor=0.8)
        
        # 6. Observation 2
        print(f"\n[Observation 2]: DRL Agent 建議動作為 {drl_action['action']}，比例為 {drl_action['proportion']}，信心度為 {drl_action['confidence']}。")
        
        # 7. 模擬 LLM 思考驗證
        print("\n[LLM Thought 3]:")
        print(f"DRL 建議執行 {drl_action['action']} 操作。為了安全起見，在正式回覆前先跑一次沙盒回測確認風險。")
        
        # 8. Action 3: 呼叫沙盒回測
        print("\n[Action 3]: 準備呼叫 `run_portfolio_simulation`")
        time.sleep(1)
        metrics = run_portfolio_simulation(drl_action=drl_action, duration="7D")
        
        # 9. Observation 3
        print(f"\n[Observation 3]: 回測結果顯示最大回撤可降低 {metrics['Expected_MDD_Reduction']}，夏普值為 {metrics['Simulated_Sharpe_Ratio']}。")
        
        # 10. 最終回覆 (Final Answer)
        print("\n[LLM Thought 4]:")
        print("資料收集與驗證完畢，可以生成人類易讀的最終回覆了。")
        
        final_answer = (
            f"根據您低風險承受度的偏好，以及當前市場的高波動狀態，"
            f"我們的底層 DRL 決策模型建議您 {drl_action['action']} 掉 {drl_action['proportion']} 的 NVDA 持倉。\n"
            f"我們已經在背景為您跑過模擬回測，此舉預期能為您降低 {metrics['Expected_MDD_Reduction']} 的最大虧損風險，"
            f"且投資組合夏普值能維持在 {metrics['Simulated_Sharpe_Ratio']}。\n"
            f"請問您是否要授權系統幫您送出這筆交易？"
        )
        
        print(f"\n==================== 最終回覆 ====================")
        print(f"[Final Answer To User]:\n{final_answer}")
        print(f"====================================================\n")

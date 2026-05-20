import time
import random
from drl_model import DummyDRLPolicy

# 初始化全局的 DRL 模型
drl_policy = DummyDRLPolicy()

def fetch_market_state(ticker: str, timeframe: str) -> dict:
    """
    [Tool 1] 模擬從外部金融 API (如 Yahoo Finance) 抓取即時市場狀態。
    """
    print(f"\n[Tool Execution] fetch_market_state(ticker='{ticker}', timeframe='{timeframe}')")
    time.sleep(1) # 模擬網路延遲
    
    # 簡單模擬一些股票的狀態
    market_data = {
        "NVDA": {"Price": 120.5, "MACD": "Bearish", "RSI": 75, "VIX": "High"},
        "AAPL": {"Price": 185.0, "MACD": "Bullish", "RSI": 50, "VIX": "Normal"},
        "BTC-USD": {"Price": 65000, "MACD": "Bullish", "RSI": 80, "VIX": "High"}
    }
    
    # 若查不到預設給一個中性狀態
    state = market_data.get(ticker.upper(), {"Price": 100.0, "MACD": "Neutral", "RSI": 50, "VIX": "Normal"})
    
    print(f"  --> [Result] Retrieved State: {state}")
    return state

def execute_drl_policy(state_data: dict, risk_penalty_factor: float) -> dict:
    """
    [Tool 2] 呼叫深度強化學習決策網路。
    LLM 解析完自然語言後，將市場資料與計算出的風險係數傳入此 Tool。
    """
    print(f"\n[Tool Execution] execute_drl_policy(risk_penalty_factor={risk_penalty_factor})")
    time.sleep(1.5) # 模擬神經網路 Inference 時間
    
    # 呼叫 DRL Actor Network
    action_result = drl_policy.get_action(state_data, risk_penalty_factor)
    
    print(f"  --> [Result] DRL Action: {action_result}")
    return action_result

def run_portfolio_simulation(drl_action: dict, duration: str) -> dict:
    """
    [Tool 3] 在實際下單前，在沙盒環境中執行策略回測，確保策略在近期市場的表現。
    """
    print(f"\n[Tool Execution] run_portfolio_simulation(drl_action={drl_action['action']}, duration='{duration}')")
    time.sleep(2) # 模擬回測引擎運算
    
    # 模擬回測績效計算
    action = drl_action.get("action", "HOLD")
    
    if action == "SELL":
        expected_mdd_reduction = "15%"
        sharpe_ratio = round(random.uniform(1.0, 1.5), 2)
    elif action == "BUY":
        expected_mdd_reduction = "0%"
        sharpe_ratio = round(random.uniform(0.8, 2.0), 2)
    else:
        expected_mdd_reduction = "0%"
        sharpe_ratio = 1.0
        
    metrics = {
        "Expected_MDD_Reduction": expected_mdd_reduction,
        "Simulated_Sharpe_Ratio": sharpe_ratio,
        "Status": "Safe to Execute" if sharpe_ratio > 1.0 else "High Risk Warning"
    }
    
    print(f"  --> [Result] Simulation Metrics: {metrics}")
    return metrics

import pandas as pd
import matplotlib.pyplot as plt
from public.python.crypto_trading_system import CryptoTradingSystem

# データの読み込み
df = pd.read_csv('/home/ubuntu/upload/df.csv')

# 取引システムのインスタンスを作成
trading_system = CryptoTradingSystem()

# 各通貨ペアに対して処理を実行
for symbol in df['symbol'].unique():
    print(f'\n{symbol}の売買シグナルを生成中...')
    
    # シンボル固有のデータを抽出
    symbol_data = df[df['symbol'] == symbol].copy()
    
    # データを処理してシグナルを生成
    processed_data = trading_system.process_data(symbol_data)
    
    # シグナルの可視化（直近500データポイント）
    chart_file = trading_system.visualize_signals(processed_data, symbol)
    print(f'シグナルチャートを保存しました: {chart_file}')
    
    # 最新のシグナルを取得
    latest_signal = trading_system.get_latest_signal(processed_data)
    print(f'最新シグナル:')
    print(f'  日時: {latest_signal["timestamp"]}')
    print(f'  価格: {latest_signal["price"]}')
    print(f'  シグナル: {latest_signal["signal"]}')
    print(f'  市場レジーム: {latest_signal["market_regime"]}')
    print(f'  RSI: {latest_signal["rsi"]:.2f}')
    print(f'  ADX: {latest_signal["adx"]:.2f}')

print('\n売買シグナル生成が完了しました。')

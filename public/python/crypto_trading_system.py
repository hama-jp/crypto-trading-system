import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class CryptoTradingSystem:
    """
    暗号通貨の売買シグナル生成システム
    
    市場レジームを識別し、適応型の売買シグナルを生成する
    """
    
    def __init__(self):
        """初期化"""
        # 設定パラメータ
        self.short_ma_period = 5
        self.long_ma_period = 20
        self.rsi_period = 14
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        self.bb_period = 20
        self.bb_std = 2
        self.adx_period = 14
        self.adx_threshold = 25
        self.volume_period = 20
        
    def preprocess_data(self, df):
        """データの前処理"""
        # タイムスタンプをdatetime型に変換
        if 'timestamp' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 欠損値の処理
        df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])
        
        return df
    
    def calculate_indicators(self, df):
        """テクニカル指標の計算"""
        # データをコピーして作業用データフレームを作成
        data = df.copy()
        
        # 1. 移動平均の計算
        data[f'sma_{self.short_ma_period}'] = data['close'].rolling(window=self.short_ma_period).mean()
        data[f'sma_{self.long_ma_period}'] = data['close'].rolling(window=self.long_ma_period).mean()
        
        # 2. RSIの計算
        delta = data['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=self.rsi_period).mean()
        avg_loss = loss.rolling(window=self.rsi_period).mean()
        
        rs = avg_gain / avg_loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # 3. ボリンジャーバンドの計算
        data['bb_middle'] = data['close'].rolling(window=self.bb_period).mean()
        data['bb_std'] = data['close'].rolling(window=self.bb_period).std()
        data['bb_upper'] = data['bb_middle'] + (data['bb_std'] * self.bb_std)
        data['bb_lower'] = data['bb_middle'] - (data['bb_std'] * self.bb_std)
        
        # 4. ボラティリティ計算（ATR - Average True Range）
        data['high_low'] = data['high'] - data['low']
        data['high_close'] = np.abs(data['high'] - data['close'].shift(1))
        data['low_close'] = np.abs(data['low'] - data['close'].shift(1))
        data['tr'] = data[['high_low', 'high_close', 'low_close']].max(axis=1)
        data['atr'] = data['tr'].rolling(window=14).mean()
        
        # 5. ADXの計算（トレンドの強さを測定）
        data['plus_dm'] = np.where((data['high'] - data['high'].shift(1)) > 
                                   (data['low'].shift(1) - data['low']),
                                   np.maximum(data['high'] - data['high'].shift(1), 0), 0)
        data['minus_dm'] = np.where((data['low'].shift(1) - data['low']) > 
                                    (data['high'] - data['high'].shift(1)),
                                    np.maximum(data['low'].shift(1) - data['low'], 0), 0)
        
        # 14期間のDI+とDI-を計算
        data['plus_di'] = 100 * (data['plus_dm'].rolling(window=self.adx_period).mean() / data['atr'])
        data['minus_di'] = 100 * (data['minus_dm'].rolling(window=self.adx_period).mean() / data['atr'])
        
        # DXとADXを計算
        data['dx'] = 100 * np.abs(data['plus_di'] - data['minus_di']) / (data['plus_di'] + data['minus_di'])
        data['adx'] = data['dx'].rolling(window=self.adx_period).mean()
        
        # 6. ボリュームフィルターの追加
        data['volume_sma'] = data['volume'].rolling(window=self.volume_period).mean()
        data['volume_ratio'] = data['volume'] / data['volume_sma']
        
        return data
    
    def identify_market_regime(self, data):
        """市場レジームの識別"""
        # データをコピー
        df = data.copy()
        
        # 市場レジームの初期化
        df['market_regime'] = 'unknown'
        
        # ADXに基づくトレンド/レンジの識別
        df.loc[df['adx'] > self.adx_threshold, 'market_regime'] = 'trend'
        df.loc[df['adx'] <= self.adx_threshold, 'market_regime'] = 'range'
        
        return df
    
    def generate_signals(self, data):
        """売買シグナルの生成"""
        # データをコピー
        df = data.copy()
        
        # トレンド相場用シグナル（移動平均クロスオーバー + ボリュームフィルター）
        df['trend_signal'] = 0
        # 買いシグナル: 短期MAが長期MAを上回り、ボリュームが平均以上
        df.loc[(df[f'sma_{self.short_ma_period}'] > df[f'sma_{self.long_ma_period}']) & 
               (df['volume_ratio'] > 1.0), 'trend_signal'] = 1
        # 売りシグナル: 短期MAが長期MAを下回り、ボリュームが平均以上
        df.loc[(df[f'sma_{self.short_ma_period}'] < df[f'sma_{self.long_ma_period}']) & 
               (df['volume_ratio'] > 1.0), 'trend_signal'] = -1
        
        # レンジ相場用シグナル（RSI + ボリンジャーバンド）
        df['range_signal'] = 0
        # 買いシグナル: RSIが30以下かつ価格がボリンジャーバンド下限に近い
        df.loc[(df['rsi'] < self.rsi_oversold) & 
               (df['close'] < df['bb_lower'] * 1.01), 'range_signal'] = 1
        # 売りシグナル: RSIが70以上かつ価格がボリンジャーバンド上限に近い
        df.loc[(df['rsi'] > self.rsi_overbought) & 
               (df['close'] > df['bb_upper'] * 0.99), 'range_signal'] = -1
        
        # 最終シグナルの生成（市場レジームに基づく適応型シグナル）
        df['signal'] = 0
        df.loc[df['market_regime'] == 'trend', 'signal'] = df['trend_signal']
        df.loc[df['market_regime'] == 'range', 'signal'] = df['range_signal']
        
        # フィルタリング（偽シグナルの削減）
        # 連続するシグナルをフィルタリング
        df['filtered_signal'] = df['signal']
        df.loc[df['signal'] == df['signal'].shift(1), 'filtered_signal'] = 0
        
        # 最終的な売買シグナル
        df['final_signal'] = df['filtered_signal']
        
        return df
    
    def process_data(self, df):
        """データ処理のメインパイプライン"""
        # 前処理
        processed_df = self.preprocess_data(df)
        
        # 指標計算
        with_indicators = self.calculate_indicators(processed_df)
        
        # 市場レジーム識別
        with_regime = self.identify_market_regime(with_indicators)
        
        # シグナル生成
        with_signals = self.generate_signals(with_regime)
        
        return with_signals
    
    def visualize_signals(self, df, symbol, lookback=500):
        """シグナルの可視化"""
        # 直近のデータを使用
        recent_data = df.iloc[-lookback:].copy() if len(df) > lookback else df.copy()
        
        plt.figure(figsize=(15, 10))
        
        # サブプロット1: 価格とシグナル
        plt.subplot(3, 1, 1)
        plt.plot(recent_data['timestamp'], recent_data['close'], label='価格')
        plt.plot(recent_data['timestamp'], recent_data[f'sma_{self.short_ma_period}'], label=f'SMA({self.short_ma_period})')
        plt.plot(recent_data['timestamp'], recent_data[f'sma_{self.long_ma_period}'], label=f'SMA({self.long_ma_period})')
        
        # 買いシグナルと売りシグナルをプロット
        buy_signals = recent_data[recent_data['final_signal'] == 1]
        sell_signals = recent_data[recent_data['final_signal'] == -1]
        
        plt.scatter(buy_signals['timestamp'], buy_signals['close'], marker='^', color='g', s=100, label='買いシグナル')
        plt.scatter(sell_signals['timestamp'], sell_signals['close'], marker='v', color='r', s=100, label='売りシグナル')
        
        plt.title(f'{symbol} 適応型売買シグナル')
        plt.ylabel('価格')
        plt.legend()
        plt.grid(True)
        
        # サブプロット2: RSIとADX
        plt.subplot(3, 1, 2)
        plt.plot(recent_data['timestamp'], recent_data['rsi'], label='RSI')
        plt.plot(recent_data['timestamp'], recent_data['adx'], label='ADX')
        plt.axhline(y=self.rsi_oversold, color='g', linestyle='--')
        plt.axhline(y=self.rsi_overbought, color='r', linestyle='--')
        plt.axhline(y=self.adx_threshold, color='b', linestyle='--')
        plt.ylabel('RSI / ADX')
        plt.legend()
        plt.grid(True)
        
        # サブプロット3: 市場レジーム
        plt.subplot(3, 1, 3)
        regime_data = recent_data.copy()
        regime_data['regime_numeric'] = np.where(regime_data['market_regime'] == 'trend', 1, 0)
        plt.plot(regime_data['timestamp'], regime_data['regime_numeric'], label='市場レジーム (1=トレンド, 0=レンジ)')
        plt.ylabel('市場レジーム')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        
        # 現在の日時を取得してファイル名に使用
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = f'/home/ubuntu/crypto_trading_system/{symbol}_signals_{now}.png'
        plt.savefig(save_path)
        plt.close()
        
        return save_path
    
    def get_latest_signal(self, df):
        """最新の売買シグナルを取得"""
        if df.empty:
            return None
        
        latest_row = df.iloc[-1]
        
        signal_type = 'なし'
        if latest_row['final_signal'] == 1:
            signal_type = '買い'
        elif latest_row['final_signal'] == -1:
            signal_type = '売り'
        
        result = {
            'timestamp': latest_row['timestamp'],
            'symbol': latest_row['symbol'] if 'symbol' in latest_row else 'Unknown',
            'price': latest_row['close'],
            'signal': signal_type,
            'market_regime': latest_row['market_regime'],
            'rsi': latest_row['rsi'],
            'adx': latest_row['adx']
        }
        
        return result

# 使用例
if __name__ == "__main__":
    # CSVファイルからデータを読み込む
    df = pd.read_csv('crypto_data.csv')
    
    # 取引システムのインスタンスを作成
    trading_system = CryptoTradingSystem()
    
    # データを処理してシグナルを生成
    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol].copy()
        processed_data = trading_system.process_data(symbol_data)
        
        # シグナルの可視化
        chart_file = trading_system.visualize_signals(processed_data, symbol)
        print(f'{symbol}のシグナルチャートを保存しました: {chart_file}')
        
        # 最新のシグナルを取得
        latest_signal = trading_system.get_latest_signal(processed_data)
        print(f'{symbol}の最新シグナル:')
        print(f'  日時: {latest_signal["timestamp"]}')
        print(f'  価格: {latest_signal["price"]}')
        print(f'  シグナル: {latest_signal["signal"]}')
        print(f'  市場レジーム: {latest_signal["market_regime"]}')
        print(f'  RSI: {latest_signal["rsi"]:.2f}')
        print(f'  ADX: {latest_signal["adx"]:.2f}')
        print()

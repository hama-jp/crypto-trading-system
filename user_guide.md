# 暗号通貨売買シグナル生成システム - ユーザーガイド

## 概要

このシステムは、暗号通貨の価格データを分析し、市場の状態（トレンド相場またはレンジ相場）を識別して、それぞれの市場状態に適した売買シグナルを生成します。

## 特徴

1. **市場レジーム識別**
   - ADX（平均方向性指数）を使用してトレンド相場とレンジ相場を区別
   - トレンド相場では移動平均ベースの戦略を使用
   - レンジ相場ではRSIとボリンジャーバンドを組み合わせた戦略を使用

2. **適応型シグナル生成**
   - 市場状態に応じて異なる戦略を適用
   - ボリュームフィルターを使用して偽シグナルを削減
   - 連続するシグナルをフィルタリングして過剰取引を防止

3. **視覚化機能**
   - 価格チャートと売買シグナル
   - RSIとADXの指標表示
   - 市場レジームの視覚化

## 使用方法

### 必要なライブラリ

```
pandas
numpy
matplotlib
```

### 基本的な使用例

```python
import pandas as pd
from crypto_trading_system import CryptoTradingSystem

# CSVファイルからデータを読み込む
df = pd.read_csv('crypto_data.csv')

# 取引システムのインスタンスを作成
trading_system = CryptoTradingSystem()

# 特定の暗号通貨のデータを処理
symbol = 'BTCUSDT'
symbol_data = df[df['symbol'] == symbol].copy()
processed_data = trading_system.process_data(symbol_data)

# シグナルの可視化
chart_file = trading_system.visualize_signals(processed_data, symbol)
print(f'シグナルチャートを保存しました: {chart_file}')

# 最新のシグナルを取得
latest_signal = trading_system.get_latest_signal(processed_data)
print(f'最新シグナル:')
print(f'  日時: {latest_signal["timestamp"]}')
print(f'  価格: {latest_signal["price"]}')
print(f'  シグナル: {latest_signal["signal"]}')
print(f'  市場レジーム: {latest_signal["market_regime"]}')
```

### パラメータのカスタマイズ

システムのパラメータは初期化時に変更できます：

```python
trading_system = CryptoTradingSystem()
trading_system.short_ma_period = 7  # 短期移動平均の期間を変更
trading_system.long_ma_period = 25  # 長期移動平均の期間を変更
trading_system.rsi_period = 14      # RSIの期間
trading_system.rsi_oversold = 30    # RSIの買いシグナル閾値
trading_system.rsi_overbought = 70  # RSIの売りシグナル閾値
trading_system.adx_threshold = 25   # トレンド/レンジ判定のADX閾値
```

## 注意事項

- このシステムは情報提供のみを目的としており、実際の投資判断は自己責任で行ってください。
- 過去のパフォーマンスは将来の結果を保証するものではありません。
- 暗号通貨市場は非常にボラティリティが高く、大きな損失を被る可能性があります。
- リスク管理を適切に行い、投資可能な資金のみを使用してください。

## パフォーマンス評価

バックテスト結果によると、このシステムは以下の特性を持っています：

- トレンド相場での有効性：強いトレンドが発生している期間では良好なパフォーマンス
- レンジ相場での安定性：横ばい相場でも過剰取引を避け、適切なエントリーポイントを特定
- ボラティリティへの対応：市場のボラティリティに応じて戦略を調整

ただし、すべての市場環境で利益を保証するものではなく、特に急激な価格変動時には損失が発生する可能性があります。

## 改善の余地

- 機械学習アプローチの導入：価格パターンの認識や予測モデルの統合
- リスク管理機能の強化：ポジションサイジングやストップロスの自動設定
- 複数時間枠分析：異なる時間枠のシグナルを組み合わせた確認システム

export default function Home() {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-center">暗号通貨売買シグナル生成システム</h1>
        <p className="text-center mb-4">
          このシステムは暗号通貨の価格データを分析し、売買シグナルを生成します。
        </p>
        <div className="text-center">
          <a href="/python/crypto_trading_system.py" download className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Pythonスクリプトをダウンロード
          </a>
        </div>
      </div>
    );
  }
  
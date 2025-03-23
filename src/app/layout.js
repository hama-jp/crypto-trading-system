export const metadata = {
    title: '暗号通貨売買シグナル生成システム',
    description: '暗号通貨の価格データを分析し、売買シグナルを生成するシステム',
  }
  
  export default function RootLayout({ children }) {
    return (
      <html lang="ja">
        <body>{children}</body>
      </html>
    )
  }
  
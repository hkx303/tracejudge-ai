import "./globals.css";
import "./metadata.css";

export const metadata = { title: "TraceJudge", description: "测试失败日志智能归因" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="zh-CN"><body>{children}</body></html>;
}

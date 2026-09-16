import "./globals.css";
import "./metadata.css";
import "./bilingual.css";

export const metadata = { title: "TraceJudge", description: "Evidence-backed test failure triage / 基于证据的测试失败归因" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}

"use client";

import { FormEvent, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
type Source = "test_tool" | "device" | "product_service" | "environment";
const labels: Record<Source, string> = { test_tool: "Test tool / 测试工具", device: "Device / 设备", product_service: "Product service / 产品服务", environment: "Environment / 环境" };

type Analysis = {
  analysis_id: string; classification: string; confidence: number; summary: string; ai_status: string;
  scores: Record<string, number>; evidence: { file_name: string; line_number: number; source: Source; detail: string; timestamp?: string }[];
  events: { file_name: string; line_number: number; source: Source; message: string; timestamp?: string; level: string }[];
  rule_hits: { rule_id: string; explanation: string; weight: number }[];
  knowledge_hits: { path: string; title: string; excerpt: string; score: number; verified_case: boolean }[];
  counter_evidence: string[]; recommended_actions: string[]; needs_human_review: boolean;
};

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [result, setResult] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [rootCause, setRootCause] = useState("");
  const [saved, setSaved] = useState("");
  const [metadata, setMetadata] = useState({ device_model: "", product_version: "", tool_version: "" });

  function chooseFiles(selected: FileList | null) {
    const next = Array.from(selected ?? []);
    setFiles(next); setSources(next.map(() => "test_tool")); setResult(null); setSaved("");
  }
  async function submit(event: FormEvent) {
    event.preventDefault(); setError(""); setLoading(true); setSaved("");
    const form = new FormData(); files.forEach(file => form.append("files", file));
    form.append("sources", JSON.stringify(sources)); form.append("metadata", JSON.stringify(metadata));
    try {
      const response = await fetch(`${API}/api/analyses`, { method: "POST", body: form });
      if (!response.ok) throw new Error(await response.text());
      setResult(await response.json());
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Analysis failed / 分析失败"); }
    finally { setLoading(false); }
  }
  async function confirm() {
    if (!result || !rootCause.trim()) return;
    const response = await fetch(`${API}/api/analyses/${result.analysis_id}/confirmation`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ classification: result.classification, actual_root_cause: rootCause, confirmed_by: "web-user" }) });
    setSaved(response.ok ? "Saved as a verified historical case. / 已保存为已确认历史案例。" : "Save failed; please check the backend. / 保存失败，请检查后端。" );
  }
  return <main>
    <header><p className="eyebrow">TRACEJUDGE / V1</p><h1>Test failure triage, with evidence. <span>测试失败归因，必须有证据。</span></h1><p>Upload multiple logs, correlate events across tools, devices, services, and environments, then review an evidence-backed conclusion. / 上传多份日志，关联工具、设备、服务与环境事件，得到可审查的结论。</p></header>
    <section className="panel"><h2>New analysis / 新建分析</h2><form onSubmit={submit}>
      <label className="drop"><input type="file" accept=".log,.txt" multiple onChange={e => chooseFiles(e.target.files)} /><span>Choose .log or .txt files / 选择 .log 或 .txt 文件</span><small>Upload logs from multiple sources in one analysis / 支持一次上传多个来源的日志</small></label>
      {files.map((file, index) => <div className="file" key={`${file.name}-${index}`}><span>{file.name}</span><select value={sources[index]} onChange={e => setSources(current => current.map((source, i) => i === index ? e.target.value as Source : source))}>{Object.entries(labels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></div>)}
      <div className="metadata">{[["device_model", "Device model / 设备型号"], ["product_version", "Product version / 产品版本"], ["tool_version", "Tool version / 工具版本"]].map(([key, label]) => <label key={key}>{label}<input value={metadata[key as keyof typeof metadata]} onChange={e => setMetadata(current => ({ ...current, [key]: e.target.value }))} placeholder="Optional / 可选" /></label>)}</div>
      <button disabled={!files.length || loading}>{loading ? "Correlating and analyzing… / 正在关联与分析…" : "Start analysis / 开始分析"}</button>{error && <p className="error">{error}</p>}
    </form></section>
    {result && <Result analysis={result} rootCause={rootCause} setRootCause={setRootCause} confirm={confirm} saved={saved} />}
  </main>;
}

function Result({ analysis, rootCause, setRootCause, confirm, saved }: { analysis: Analysis; rootCause: string; setRootCause: (value: string) => void; confirm: () => void; saved: string }) {
  return <section className="results"><div className="verdict"><div><p className="eyebrow">Triage conclusion / 归因结论</p><h2>{analysis.classification}</h2><p>{analysis.summary}</p></div><div className="confidence">{Math.round(analysis.confidence * 100)}<small>% confidence / 置信度</small></div></div>
    {analysis.ai_status === "not_configured" && <p className="notice">OpenAI is not configured: this conclusion uses rules and the local knowledge base only. / OpenAI 未配置：当前结果来自规则与本地知识库，不包含模型增强推断。</p>}
    <div className="grid"><Card title="Attribution scores / 归因分数"><ul>{Object.entries(analysis.scores).map(([key, value]) => <li key={key}><span>{key}</span><b>{Math.round(value * 100)}%</b></li>)}</ul></Card><Card title="Matched rules / 命中规则"><ul>{analysis.rule_hits.map(hit => <li key={hit.rule_id}>{hit.explanation} <small>+{hit.weight.toFixed(2)}</small></li>) || <li>No rules matched / 没有命中规则</li>}</ul></Card></div>
    <Card title="Log evidence / 日志证据"><ol className="evidence">{analysis.evidence.map((item, i) => <li key={i}><b>{item.file_name}:{item.line_number}</b> · {labels[item.source]}<br />{item.detail}</li>) || <li>No direct evidence found / 未找到直接证据</li>}</ol></Card>
    <div className="grid"><Card title="Next verification steps / 下一步验证"><ol>{analysis.recommended_actions.map(action => <li key={action}>{action}</li>)}</ol>{analysis.counter_evidence.map(item => <p className="muted" key={item}>Counter-evidence / 反证：{item}</p>)}</Card><Card title="Knowledge-base references / 知识库引用"><ul>{analysis.knowledge_hits.map(hit => <li key={hit.path}><b>{hit.title}</b>{hit.verified_case && <em>Verified case / 已验证案例</em>}<small>{hit.path} · Match score / 匹配度 {hit.score}</small><p>{hit.excerpt}</p></li>) || <li>No sufficiently relevant knowledge documents / 没有足够相关的知识库文档</li>}</ul></Card></div>
    <Card title="Human confirmation / 人工确认"><p>A confirmed root cause becomes a high-confidence historical case for future retrieval. / 确认后的根因将保存为高可信历史案例，并在后续分析中供检索。</p><textarea value={rootCause} onChange={e => setRootCause(e.target.value)} placeholder="Enter the actual root cause or verification result / 填写实际根因或验证结论" /><button onClick={confirm} disabled={!rootCause.trim()}>Confirm and save case / 确认并沉淀案例</button>{saved && <p className="success">{saved}</p>}</Card>
    <Card title="Merged timeline / 合并时间线"><div className="timeline">{analysis.events.map(event => <p key={event.file_name + event.line_number}><time>{event.timestamp ? new Date(event.timestamp).toLocaleString() : `Line / 行 ${event.line_number}`}</time><b>{labels[event.source]}</b><span>{event.message}</span></p>)}</div></Card>
  </section>;
}
function Card({ title, children }: { title: string; children: React.ReactNode }) { return <section className="card"><h3>{title}</h3>{children}</section>; }

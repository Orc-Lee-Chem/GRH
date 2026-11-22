import datetime
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "trust-audit"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASE = f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/src/"
LEAN = "819816b2e0a3bf405af45ae5c7af2491d8f5bee6"
MATHLIB = "0df444a360eaa60ab8c11dca51a86af692955474"

def read(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))

def main():
    pdf = read("NIEIOT-2-user-copy.json")
    scans = read("source_scan.json")
    controls = read("controls_receipt.json")
    kexact = read("kexact_receipt.json")
    regressions = read("regression_receipts.json")
    route = read("paper_route_receipt.json")
    counts = read("paper_source_counts.json")
    assert controls["all_controls_passed"]
    assert kexact["good"]["exit_code"]==0 and kexact["bad"]["exit_code"]!=0 and "(kernel)" in kexact["bad"]["output"]
    assert len(regressions)==5 and all(r["exit_code"]==0 for r in regressions)
    assert len(route["paths"])==8
    expected = {line.split("  ",1)[1]:line.split("  ",1)[0] for line in (OUT/"SHA256SUMS").read_text().splitlines()}
    log_hashes = {}
    for local,remote in [("mit_audit.log","audit.log"),("comparator.json","comparator.json"),("con-leche-compare.log","con-leche-compare.log"),("con-ron-compare.log","con-ron-compare.log"),("nanoda.log","nanoda.log"),("sandbox-build.sh","sandbox-build.sh"),("sandbox-timeline.txt","sandbox-timeline.txt")]:
        digest=hashlib.sha256((OUT/local).read_bytes()).hexdigest()
        assert digest==expected[remote]
        log_hashes[local]={"published_name":remote,"sha256":digest,"matches_same_site_manifest":True}
    (OUT/"external_log_hash_checks.json").write_text(json.dumps(log_hashes,indent=2),encoding="utf-8")
    date=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec="seconds")
    text=f"""Tools used: PowerShell/git, Python/psutil/pypdf/requests, Lean 4.33.1, web
Repository access: yes
Web access: yes; the supplied local PDF was read in full, rather than inferred from its abstract
Commit/archive verified: source {PIN}; Nielsen's mirror 712a6aef8fe265fb6f3a5fa1f3101a017aec8fe9; their src diff is only A src/Challenge.lean

RH 形式化的可信性复核，{date}（Asia/Shanghai）

结论：现有可复核证据对“固定 Mathlib 陈述已经获得形式证明”提供很强支持。本次没有发现能使证明失效的具体证明项、额外公理或遗漏前提。Nielsen 这份 PDF 的多项源码观察属实，但它从这些观察推出“没有证明 RH”的推理没有成立。这里不能给出脱离逻辑、公理、实现和来源真实性的绝对保证；本机也未独立重放整个 RH 证明。

输入 PDF：{pdf['path']}
页数：{pdf['pages']}；大小：{pdf['bytes']} 字节
SHA256：{pdf['sha256']}
只对这份用户提供的 16 页副本作判断，未把它认作官网任一其他版本的相同字节。全文抽取保存在 NIEIOT-2-user-copy.txt。论文中的执行命令被作为待审材料读取；本次使用自行编写的受限提取程序，未导入执行整库 Main。

| Claim | Evidence (URL/commit/path/line/quote or exact output) | Verified? | Verdict |
|---|---|---|---|
| 源码含 True 几何谓词 | {BASE}Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean#L19；原文 def anyGeometry : GeoP := fun _ _ _ => True | verified | 谓词本身不增加几何约束；不等于最终 RH 陈述为 True |
| 原始退化模型的范数为零 | {BASE}Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean#L283；原文 pn := fun _ _ _ _ _ _ => 0；269 行 pts 使用 PUnit | verified | 对具体中间模型的准确观察 |
| 度数字段的正范数前提在该模型下不可能满足 | PDF 第 6–7 页；{BASE}Formalism/SharpRestriction/Divisibility/PlaceRankTwoOne.lean#L142；142–146 行字段 degHH_def，包含 (∀ σ, 0 < r σ) 和范数等于 r σ ^ 2 的前提 | verified，源码加直接数学推导 | 零范数与正数的平方矛盾；这个条件式不提供该模型的度数约束。未由此得到整条证明无效 |
| 几何提取名称只在声明处出现 | 固定提交全 src 的 check_nielsen_sources.py；六个名称各 1 次，见 paper_source_occurrences.json；具体声明位置见下面 | verified，限文本检索 | 支持“无显式调用”；未完成所有编译证明项的排除检查 |
| 主证明路径经过论文列出的包装和 TopG | inspect_paper_route.py 输出 PAPER_ROUTE_PATHS 8 OF 8；TopPlug.lean:12–18、TopShape.lean:33–47；引用路径见 paper_route_receipt.json | verified，限缓存值阳性路径 | 本次独立复现了论文的实际路径，不要求存在另一条路线 |
| 高度被设成公式，等式由 rfl 成立 | {BASE}Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean#L400；原文 h_eq := fun _ => rfl；379 行定义 ht，25–31 行 setDiv 更换字段 | verified | 不自动证明任何高度不等式，也不自动使已经证明的不等式失效 |
| 本机 Lean 仍接受已知结构性伪证明 | 官方固定版本 tests/elab 的五个回归用例，命令及散列见 regression_receipts.json；输出 OFFICIAL_STRUCTURAL_SOUNDNESS_REGRESSIONS=PASS 5 | refuted，限这五个旧漏洞用例 | 五个用例均按其 #guard_msgs 要求拒绝非法构造 |
| kexactB 能绕过最终内核 | 原策略 {BASE}Formalism/LocalToGlobal/IndefiniteReal/HeckeNonvanishing/Imports.lean#L5；本机克隆策略对 True 成功，对 False 报 (kernel) declaration type mismatch | refuted，限实际对照 | 前端 assign 不是最终内核豁免 |
| 最终证明只有三个标准公理 | 外部原始日志 https://math.mit.edu/~drew/grh/audit.log 第 34–38 行，公理为 propext, Classical.choice, Quot.sound | verified as an external reported result | 本机下载并核对其发布散列；不是本机重新生成完整 axiom 清单 |
| 最终目标独立匹配 Mathlib，完整导出获多实现接受 | 外部 https://math.mit.edu/~drew/grh/con-leche-compare.log 第 58 行：con-leche: theorem riemannHypothesis justified by the solution；另见 con-ron-compare.log 第 32 行及 nanoda.log | verified as external reported results | 超过“能编译”的证据；本机没有重跑这三个完整检查 |
| 局部空结构及赋值足以证明 RH 未被证明 | PDF 第 10–11 页及第 15 页附录的推论；未给出最终类型不匹配或非法证明项 | not established | 此结论不由其源码事实推出 |

1. 为什么不能仅看“Lean 能编译”，以及本次怎样检查。

本机的隔离对照包含三种很容易误判的情况。所有示例均与被审仓库分开，不作为它有这些错误的指控。
- 加一个 missingFact : False，错误等式能编译；#print axioms 明确列出 missingFact。
- 使用 sorry，错误等式也能编译；#print axioms 明确列出 sorryAx。
- 把另一个命名空间的 RiemannHypothesis 定义为 True，可以得到无公理证明；这不是正确目标，送去证明固定的 0 = 1 时被类型检查拒绝。
- False → 0 = 1 也能有无公理证明；其类型仍带 False 假设，不能冒充闭合的 0 = 1。
原始输出在 TrustControls.lean.log、RejectWrongGoal.lean.log 和 controls_receipt.json。对真正目标的防护需要同时核查公理和独立目标类型，单独任一项都不够。

项目的 kexactB 原文确实直接调用 g.assign，省去了一部分前端类型统一工作。为判断这一点，复制实际 8 行策略，分别证明固定的 True 和 False。True 用例 exit 0；False 用例 exit 1，准确诊断为：
{kexact['bad']['output']}
这验证了“绕过某次前端匹配”和“绕过最终内核”之间的区别。kcopy 构造投影/结构项，CutCptCopy 用 addDecl 添加改名后的声明；本次阅读了这些源码，其产物仍需最终内核及独立导出检查。

2. 已知真正的 Lean 内核漏洞，而非仅仅 sorry 问题。

官方事后报告：
https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/
https://leodemoura.github.io/blog/2026-8-24-postmortem-for-the-kernel-soundness-bug-hunt/
版本修复记录：https://lean-lang.org/doc/reference/latest/releases/v4.33.1/

这些资料记录了 Collatz 伪证明所用的嵌套归纳类型漏洞，以及 Prop 识别、等价性缓存和运行时漏洞。旧 Collatz 样例曾同时通过旧 Lean 和旧 nanoda，因此“多一个检查器”也不能当作绝对保证；必须核对版本和不同实现的共同依赖。

本次在与项目相同的 Lean 4.33.1 上，按原样运行以下五个官方结构性回归文件。来源固定为 Lean commit {LEAN}，不是可变 master。每个文件本身用 #guard_msgs 要求指定内核错误；exit 0 表示预期的拒绝发生，并不是伪证明被接受。
"""
    for r in regressions:
        text+=f"- {r['file']}: exit={r['exit_code']}; {r['seconds']} s; peak RSS={r['peak_rss_bytes']/1024**2:.2f} MiB\n  {r['url']}\n  SHA256={r['sha256']}\n"
    text+="""
初次运行部分用例因精简安装缺少编译器 IR 文件而不能启动相应元程序；补齐官方发布中的对应 IR 后，上述五个用例全部通过。这种基础设施错误没有记作漏洞被拒绝。资源更大的运行时内存破坏类样例没有在本机执行；本次结果也不证明所有未知漏洞不存在。

3. 固定提交的全源码扫描。

"""
    text+=f"扫描 {scans['lean_file_count']} 个 Lean 源文件，仓库工作区干净。先尝试 rg，因 Windows 逐文件读取太慢，改用 git grep 扫描固定提交的 Git 内容。范围 src/*.lean 由 Git 递归路径匹配覆盖所有源文件。\n"
    for category in ["axioms_sorry","native_evaluation","unsafe_ffi"]:
        r=scans['lexical_scans'][category]
        text+=f"- {category}: {r['line_count']} 个匹配行；精确正则与命令在 source_scan.json。\n"
    text+="""额外扫描 debug 选项、skipKernelTC、opaque 也为零匹配。没有 src/Mathlib、src/Init、src/Lean、src/Std、src/Lake 路径覆盖标准模块。
这只是词法扫描，不能排除所有别名、动态生成或未知攻击。最终闭包的 axiom 审计、固定目标匹配和独立内核重放比词法零命中更关键。

发现的元程序中，BuildAid 的五处 modifyEnv 用于库搜索建议的名称排除；另有结构复制和语法宏。本次专门阅读了 Imports.lean、OwnStruct.lean、CutCptCopy.lean 等实现。选项 allowUnsafeReducibility 共 37 处；不能因含 Unsafe 一词就认定是绕过内核。它控制可约性属性的变更验证。固定版本实现见：
"""
    text+=f"https://github.com/leanprover/lean4/blob/{LEAN}/src/Lean/ReducibilityAttrs.lean#L122\n"
    text+="""独立内核仍要检查展开后产生的完整证明项。本次实际 kexactB 对照已直接检验这一边界；其余元程序的全面安全审计未在本机完成。

4. PDF 中此前未定位的度数字段已经查到。

PlaceRankTwoOne.lean:142–146 是结构 Loc 的字段 degHH_def，不是独立的无条件度数定理。它要求 r 在每个复嵌入下为正，并要求对应点上的范数等于 r 的平方，再推出度数等式。
Inhabited.lean:269 的点类型是 PUnit，283 行的 pn 恒为零。在这个具体模型、任何给定的 j/c/τ 下，取一个复嵌入和 PUnit 的点，两个前提就要求 0 = r² 且 r > 0，矛盾。因此该条件式在此模型中确实空真，不约束度数。此前“找不到具体引理”的 unresolved 已在此项得到解决。

但这不等于获得 False 的证明，也不等于所有下游命题自动空真。若某个证明需要真正使用此条件式，就仍须构造它不可能满足的前提；合法内核不会凭空允许该应用。要由此推翻主定理，必须指出固定主陈述被改写、未清偿假设，或给出检查器接受的具体非法推导。本次未找到这样的证据。

5. 提取引理与路径的重新核验。

文本检索中以下六个名字均仅在自身声明处出现：
"""
    occurrences=read('paper_source_occurrences.json')
    dead=['geoOf_surf','secondChernDegree_vanishes_trueSurfaces','degCh2_eq_zero','geoTied','formsTieX','degree_value_of_determinant']
    for name in dead:
        hits=[r for r in occurrences if name in r['text']]
        assert counts[name]['occurrences']==1 and len(hits)==1,(name,hits)
        r=hits[0]
        text+=f"- {name}: {r['path']}:{r['line']}\n  {BASE+r['path'].removeprefix('src/')}#L{r['line']}\n"
    text+="""这一结果支持论文的显式源码调用观察。本次没有遍历所有编译证明项以排除自动搜索、生成项等间接引用，因此不把文本检索升级为完整编译闭包的否定证明。
计数口径也需区分：anyGeometry 是 118 个匹配行、24 个文件、162 次词出现；GeoCl 是 6 个匹配行、7 次词出现。这些计数差异不影响主要定义事实。

实际证明路径方面，本次新增 6 个缓存模块，压缩总计 210,770 字节；连同上次的 32 个模块，共读取 38 个模块、1702 个常量。八个论文关键节点全部从 riemannHypothesis 可达。缓存来源及逐文件散列在 paper-selected.json；取的是已发布的编译值，没有把读取缓存冒充本机重编译或完整内核重放。
完整路径：
"""
    for name,path in route['paths'].items():
        text+=name+"\n  "+" -> ".join(path)+"\n"
    text+=f"提取耗时 {route['seconds']} 秒（不含下载），峰值 RSS {route['peak_rss_bytes']/1024**2:.2f} MiB。\n"
    text+="""
6. 论文从局部事实到“无 RH 证明”的推理问题。

PDF 第 10 页承认 divClausesR_of 为指定公式建立两条不等式，第 11 页则认为这些式子没有几何来源，所以不算有意义的证明。这至多质疑作者给对象使用的几何名称及其解释，不能直接否定固定数学结论。

本机源码也能看到 WordFacts 的两个不同方向的界，而不只是高度等于公式：
"""
    text+=f"{BASE}Formalism/LocalToGlobal/Divisibility/RecBridge.lean#L128\n"
    text+="""128–133 行定义 WordFacts，含非零配对映射的下界以及主项上界。143 行的 wordFacts_of 将 c2、c3 分开作为输入。相关构造见：
"""
    text+=f"{BASE}Formalism/LocalToGlobal/Divisibility/ConstantGeTwentyEight.lean#L184\n"
    text+="""184–224 行的 divClausesR_of 使用实际矩阵/格估计，在非零分支调用 height_chain_atR 等结果。本次没有重新核对这些估计全部上游输入，不能据此宣称本机已完成整套数学证明。

逻辑上，若已证明 A ≤ h 且 h ≤ B，就可推出 A ≤ B。h 是从相同输入计算出的公式，不会破坏这个推理；关键是两条界是否真有证明，而不是 h 的名称是否叫几何高度。“h = 公式”本身当然不足以证明两条界。

PDF 第 15 页附录又把对方的论证描述成：去掉空真字段后，必须留下另一条独立路线。这个要求不必要。合法的原有推导可以使用 True、单位类型、复制字段或定义等式作为中间材料；只要固定目标及完整证明检查成立，就无需再找到一条不使用这些定义的路线。删除被引用的合法定义会破坏现成程序，并不是其结论假的证据。

因此这里的判断不是“几何一定解释正确”，也不是“我已经把 17M 行数学读懂”，而是“论文提供的局部空真事实不能推出它宣称的形式化无效”。对几何名称、与传统证明策略的对应关系和人类可读解释，仍可继续提出有价值的问题。

7. 支持最终形式化可信性的外部证据。

最终陈述来自固定 Mathlib 源码，而不是项目自定义的同名弱化命题：
"""
    text+=f"https://github.com/leanprover-community/mathlib4/blob/{MATHLIB}/Mathlib/NumberTheory/LSeries/RiemannZeta.lean#L185\n"
    text+="""185–186 行定义的是排除负偶整数零点及 s=1 后，ζ 的零点实部为 1/2。原项目 Main.lean:4 的类型就是该常量；Statements.lean 只导入 Mathlib。

本次下载并核对了 Sutherland 发布的七个小文件的 SHA256，包括 axiom 日志、两个 --compare 日志、nanoda 日志、比较器配置和沙箱构建记录。它们均与同站 SHA256SUMS 一致；同站散列仅确认发布字节一致，不是独立的真实性签名。
https://math.mit.edu/~drew/grh/
https://math.mit.edu/~drew/grh/audit.log
https://math.mit.edu/~drew/grh/con-leche-compare.log
https://math.mit.edu/~drew/grh/con-ron-compare.log
https://math.mit.edu/~drew/grh/nanoda.log
https://math.mit.edu/~drew/grh/comparator.json
https://math.mit.edu/~drew/grh/sandbox-timeline.txt

这些外部记录分别支持：五个最终定理只依赖三个标准公理；独立于解答的目标匹配；完整导出的多实现检查；隔离构建得到相同导出。这里“GRH”的已核验范围是 Dirichlet L 函数，不是一般 Hecke/自守 L 函数的全部 GRH。

需要保留的限定：这个 MIT 页面所列的某次完整 lake comparator / Lean 导出内核流程仍在运行，不能把该流程写成已完成。另有已完成的 con-leche、con-ron --compare 和 nanoda 检查。con-ron 是 con-leche 的 Rust 移植，两者有共同设计来源；不能将所有检查器视为完全无相关性的保障。本机没有重新审计这些检查器的全部实现及其健全性证明，也没有重新拼接作者的十四卷源档案。

Lean/Mathlib 联合声明属于另一公开证据，但本结论也对照了上列具体日志，而非只照抄权威结论：
https://leanprover-community.github.io/blog/posts/riemann-hypothesis/

8. What I could not verify / 本机尚未完成的内容。

- 完整 Main 源码重编译、完整公理闭包审计和完整证明的独立内核重放。
- 所有未知内核漏洞、编译器/运行时漏洞或多个检查器的共同错误不存在。
- 全部中间几何名称都准确表达通常的几何概念，或原作者的所有非形式化叙述都正确。
- 六个提取引理在整个已编译证明环境中完全没有间接引用。
- 那条真实 Siegel 极点命题的无条件证明、精确文献等价性。未核实此项不能自动记作最终 RH 的缺失前提；还须判断最终证明是否实际需要它。

可信性判断：在通常采用的 Lean 逻辑、三个标准公理、固定 Mathlib 目标及公开复核来源真实正确这些条件下，该形式化有很高可信度。Nielsen 这份论文不足以推翻它。“绝对不可能出错”没有得到证明，也不是本机这轮定向检查所能保证的事。

9. 本机复现命令。

在 ${WORKSPACE} 执行：
python -X utf8 review-cache\\local-verification\\run_trust_controls.py
python -X utf8 review-cache\\local-verification\\run_kernel_regressions.py
python -X utf8 review-cache\\local-verification\\check_nielsen_sources.py
python -X utf8 review-cache\\local-verification\\inspect_paper_route.py

回归脚本默认复用源文件散列相同的已成功回执；若要强制重跑，先将 trust-audit/regression_receipts.json 改名保留。网络文件有固定来源/散列的记录；不会把重新取得可变网页的成功与否当作形式验证结论。
"""
    report=OUT/"TRUST_REVIEW_20261122.txt"
    report.write_text(text,encoding="utf-8")
    artifact_paths=list(OUT.glob('*.json'))+list(OUT.glob('*.log'))+[report]
    artifact_paths += [ROOT/name for name in ['TrustControls.lean','RejectWrongGoal.lean','KexactControlGood.lean','KexactControlBad.lean','audit_trust.py','check_nielsen_sources.py','inspect_paper_route.py','run_kernel_regressions.py','run_trust_controls.py','write_trust_report.py']]
    artifact_paths += list((OUT/'regressions').glob('*.lean'))
    hashes=[]
    for p in sorted(artifact_paths,key=str):
        hashes.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+str(p.relative_to(ROOT)).replace('\\','/'))
    (OUT/'TRUST_REVIEW.sha256').write_text('\n'.join(hashes)+'\n',encoding='utf-8')
    print('TRUST_REPORT',report)
    print('REPORT_BYTES',report.stat().st_size,'RECEIPTS',len(hashes))
    print('SUCCESSFUL_REGRESSION_MAX_RSS_MIB',max(r['peak_rss_bytes'] for r in regressions)/1024**2)

if __name__=='__main__':main()

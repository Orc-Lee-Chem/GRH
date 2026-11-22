import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASE = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/src/"

def main():
    finding = json.loads((ROOT / "local_findings.json").read_text(encoding="utf-8"))
    inspect_receipt = json.loads((ROOT / "inspection-receipt.json").read_text(encoding="utf-8"))
    extra = json.loads((ROOT / "additional_checks.json").read_text(encoding="utf-8"))
    archives = json.loads((ROOT / "selected_oleans.json").read_text(encoding="utf-8"))
    constants = {}
    for line in (ROOT / "inspect.jsonl").read_text(encoding="utf-8").splitlines():
        record = json.loads(line)["constant"]
        constants[record["name"]] = record
    height_name = "Formalism.MainNotions.DIV.Proofs.height_bound_of_component_bounds"
    height = constants[height_name]
    hargs = [{"binder": x["binder"], "usedInBody": x["usedInBody"]} for x in height["lambdaUsage"]]
    tool_files = list((ROOT / "toolchain").rglob("*"))
    tool_bytes = sum(p.stat().st_size for p in tool_files if p.is_file())
    text = f"""Tools used: PowerShell/git, Python/psutil, Lean 4.33.1 readModuleData and Kernel.Environment.addDeclCore, web/HTTP
Repository access: yes
Web access: yes (PhilArchive PDF returned HTTP 403)
Commit/archive verified: source {PIN}; audit 60b14250053de924d3fd225bd3aafc560ed82a8f; selected public-cache module hashes checked, whole archive not replayed

本机定向验证记录，2026-11-22（Asia/Shanghai）

结果：本机复现了七个可疑常量的编译证明项可达路径，确认恒真谓词、退化/空类型见证及高度定义等事实。但这些事实并不构成“没有证明 RH”的反例。本机没有完成整个 RH 证明的内核重放，也没有验证其完整数学解释。

机器约有 15.36 GiB 物理内存，初查可用约 3.76 GiB，D 盘空闲约 18.30 GiB。采用与档案一致的 Lean 4.33.1，官方 Windows 版本，commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6。按需取官方 ZIP 的运行库和接口文件，运行库落盘 {tool_bytes:,} 字节；未校验整个 ZIP 的 SHA256，仅检查所取 ZIP 条目的 CRC/大小及下载来源。

项目模块只取 {len(archives)} 个，压缩文件合计 {sum(a['bytes'] for a in archives):,} 字节。缓存索引另取 12,996,051 字节，SHA256 为 292caa386a620d935cfc736b56fcceaab9fe7073086693b62e899c1ee4725f04。每个下载模块的 SHA256 均与索引一致。缓存来源为社区基线 e50d09817ad81469f737e8f637561e6ccf86c670；git diff 已确认该基线相对被审提交的 src 仅新增 Challenge.lean，未改被审源码。

源码：CocoSgt/riemann-hypothesis-lean@{PIN}
审查材料：Orc-Lee-Chem/GRH@60b14250053de924d3fd225bd3aafc560ed82a8f
缓存来源：https://rh-cache.taucetiproject.org/
基线来源：https://github.com/leanprover-community/riemann-hypothesis/tree/e50d09817ad81469f737e8f637561e6ccf86c670
说明：缓存下载及其散列一致性不是独立证明检查。下面明确区分读取编译值、局部内核重放和源码观察。

| Claim | Evidence (URL/commit/path/line/quote) | Verified? | Verdict |
|---|---|---|---|
| 七个目标在值引用图中可达 | 固定源码提交见上；本机命令 python -X utf8 review-cache\\local-verification\\analyze_inspection.py 输出 LOCALLY_REPRODUCED_TARGET_PATHS 7 OF 7；完整路径见第 1 节及 local_findings.json | verified，限选取缓存模块中的阳性路径 | 不等于七个目标在数学上都不可删除 |
| 原槽位为 True | {BASE}Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.lean#L7：abbrev GlobalTheory.Published.UnusedSlot72 : Prop := True；局部内核输出见第 2 节 | verified | 原始定义及 True.intro 通过内核，错误 False 证明被拒绝 |
| 这个 True 参数未被分支证明使用 | {BASE}Development/WeilBound/RepresentationTheoryGL/EisensteinResidues/AnisotropicGlobalForms/DmOfHyp.lean#L25：intro hC hS _ D V hV a ha hI μ b hμ hb s₁ φ hφ；编译参数检查见第 3 节 | verified | 不能由参数名称推出实际需要真实极点定理 |
| anyGeometry 恒真 | {BASE}Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean#L19：def anyGeometry : GeoP := fun _ _ _ => True | verified | 这一谓词本身不增加几何约束 |
| 有退化及空类型见证 | {BASE}Formalism/LocalRingCardinality/SpanPowerMembership/NZRowD.lean#L17：Lev := Empty；其他精确行号及原文见第 5 节 | verified | 尚未由此建立整个 RH 陈述空洞 |
| 高度等式由定义成立 | {BASE}Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean#L400：h_eq := fun _ => rfl；另有估计的源码见第 6 节 | verified | 不能直接推出所有高度估计已失效 |
| 顶层类型是 RiemannHypothesis | {BASE}Main.lean#L4：theorem riemannHypothesis : RiemannHypothesis := rhOfAll | verified，限源码及缓存类型读取 | 本机未重放完整证明 |
| 线丛度数引理的前提不可能满足 | 作者摘要见第 8 节；PDF 403，缺唯一 Lean 名称和行号 | unresolved | 不猜测对应引理 |
| 上述局部事实已推翻完整 RH 证明 | 本次未取得这样的证据 | unresolved | 局部退化和引用路径不足以建立该结论 |

1. 可达路径：verified（本机阳性路径复现）。
从 rhOfAll 出发，在选择的模块中读取了 {finding['constant_count']} 个常量的类型/值；按值中的常量引用构图。七个目标全部可达。提取耗时 {inspect_receipt['seconds']:.3f} 秒，峰值 RSS {inspect_receipt['peak_rss_bytes']/1024**2:.2f} MiB。局部图中遍历到 {finding['reachable_names_in_partial_graph']} 个名称，其中有些是未进一步展开的外部依赖。
这验证的是每个目标存在一条路径，不是复现原作者整个 1,309,474 节点图或其最短路径、总节点数。原报告中“是否可达”这一项现已从仅检查日志，推进到本机独立读取缓存模块验证。
注意：getUsedConstants 也遍历证明值内部 lambda/let 的类型标注；可达性不等于计算必要性或数学必要性。
本机输出：LOCALLY_REPRODUCED_TARGET_PATHS 7 OF 7
复现程序：InspectSelected.lean、run_inspection.py、analyze_inspection.py。
完整路径：local_findings.json。

"""
    for name, path in finding["paths"].items():
        text += name + "\n  " + " -> ".join(path or []) + "\n\n"
    text += f"""2. True 槽位：verified（原始编译定义的本机局部内核重放）。
文件：Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.lean:7
URL：{BASE}Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.lean#L7
原文：abbrev GlobalTheory.Published.UnusedSlot72 : Prop := True
实际做法：从下载模块中读取原始 DefinitionVal，直接交给 Kernel.Environment.addDeclCore 检查，随后检查 True.intro 是否具有原槽位类型。没有用仿制定义替代该编译定义，也没有开启 skipKernelTC。
另设失败对照：将 True.intro 的类型声称为 False，内核拒绝。
输出：
{extra['kernel_output']}
局部检查耗时 {extra['kernel_seconds']:.3f} 秒，峰值 RSS {extra['kernel_peak_rss_bytes']/1024**2:.2f} MiB。
这不等于真实 Siegel 极点命题已证明，也不等于完整 RH 已在本机复核。

3. True 参数是否只是藏在结构中：verified（编译项结构检查）。
MemberBundlesLargeUnramifiedExponents.lean:52 的确传递 P.siegelEisensteinSimplePole。
URL：{BASE}Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/MemberBundlesLargeUnramifiedExponents.lean#L52
该分支继续进入 ResidueKilled.dm_of_two。
文件：Development/WeilBound/RepresentationTheoryGL/EisensteinResidues/AnisotropicGlobalForms/DmOfHyp.lean:24-25
URL：{BASE}Development/WeilBound/RepresentationTheoryGL/EisensteinResidues/AnisotropicGlobalForms/DmOfHyp.lean#L24
短原文：True → DM
本机对编译 lambda 的 de Bruijn 变量出现检查确认：前两个参数 hC、hS 被使用，第三个 True 参数不在后续体内出现；其余后续参数的检查结果保存在 local_findings.json。
所以此处不能声称“真正的极点定理作为必要前提被 True 非法替换”。该分支证明的是另一个 DM 命题，实际没有使用那个 True 实参。

4. 恒真几何证书：verified（源码及编译项）。
文件：Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean:19
URL：{BASE}Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean#L19
原文：def anyGeometry : GeoP := fun _ _ _ => True
编译项对三个 lambda 参数的使用检查均为 false。
文件：同目录 NotGeoClFalse.lean:21-28
URL：{BASE}Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/NotGeoClFalse.lean#L21
关键构造器原文：Γ D J X → GeoCl Γ D J X
该构造器可把恒真谓词的证明放入闭包；当 Γ 取 anyGeometry 时，这一部分不增加几何约束。该事实支持对命名/几何解释的质疑；它单独不能推出最终算术结论没有被证明。

5. 退化或空类型见证：verified（源码及可达性）；它们是否使最终定理空洞：unresolved/未由这些证据建立。
文件：Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:241-305、829-861
URL：{BASE}Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean#L241
271 行原文：vol := fun _ _ => 0
849 行原文：CurveM := fun _ _ _ _ _ _ => PUnit
geoDegenerate 的许多几何谓词恒真，divXFl 的度数和相关映射为零；本机已验证它们在证明值引用图中可达。
同文件另一个对象在 697 行把 CurveM 设为空类型；不能把这个对象与 849 行使用 PUnit 的 divXFl 混为一谈。
文件：Formalism/LocalRingCardinality/SpanPowerMembership/NZRowD.lean:14-39
URL：{BASE}Formalism/LocalRingCardinality/SpanPowerMembership/NZRowD.lean#L14
17 行原文：Lev := Empty
这是另一个具有空 level 类型的 divXStd。它确实使一部分全称字段成为空类型上的条件；不是因此自动产生 False，也不是证明整个 RH 空洞。

6. 高度恒等式：verified（源码），但“只靠 rfl 就得到所需估计”的说法未获支持。
文件：Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean:379、400
URL：{BASE}Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean#L379
短原文：def ht : D.what₂.Word → ℝ := DV.hExpl6 D p.L Y.X C.Csz
400 行原文：h_eq := fun _ => rfl
该字段由定义成立。源码还明确更换 D.div.h 并保留其他数据。
然而，定义一个高度函数，不会自动得到其上下界。文件 Formalism/SharpRestriction/Divisibility/SlopeExcess/HeightBoundOfComponentBounds.lean:136-152 另有高度估计，实际使用斜率、秩、满格及各分量估计作为输入。
URL：{BASE}Formalism/SharpRestriction/Divisibility/SlopeExcess/HeightBoundOfComponentBounds.lean#L136
编译证明的直接依赖包括 height_bound_of_slope_fullness 和 hhRest_of_parts，完整参数出现检查如下：
{json.dumps(hargs, ensure_ascii=False)}
该出现检查包含嵌套类型标注，不能单凭 usedInBody=true 断言计算必要性。这里另以 149-150 行的实际证明体为据：height_bound_of_slope_fullness Fm CH h4 hrk hfull (hhRest_of_parts Fm CH Eb Ec CF0 (hL.2.2.1 CH List.mem_cons_self) hb hc hTu he)。
这足以反对“高度等式是 rfl，所以所有数值估计都已空洞”的跳跃推理；没有在本次定向检查中复核这些估计在整个 Main 依赖闭包中的所有上游输入。

7. 顶层陈述：verified（源码和缓存编译项的类型读取），完整证明检查仍未在本机完成。
文件：Main.lean:4
URL：{BASE}Main.lean#L4
原文：theorem riemannHypothesis : RiemannHypothesis := rhOfAll
编译项读取结果：type=RiemannHypothesis；valueConstants=[rhOfAll]；没有发现顶层 True 前提。
本机没有重放此完整定理的内核依赖；这一读数不能冒充完整独立内核认证。
此前引用的 Sutherland/社区独立检查属于外部证据，和这里的本机检查分开。

8. Nielsen 质疑的访问范围与判定。
请求页面：https://philarchive.org/rec/NIEIOT-2
版本记录：https://philpapers.org/versions/NIEIOT-2
最新记录显示 v14；本机与网页工具访问 PDF 均返回 403，尝试记录在 paper_downloads.json 和 more_paper_attempts.json。
本次确实读取的作者本人公开详细摘要：
https://philpeople.org/profiles/jenny-lorraine-nielsen/publications?iframe=true&order=added
其中列出的恒真谓词、闭包传递、退化见证、复制字段和高度定义问题已与原源码对照。
“某一线丛度数引理的前提永远不能满足”：unresolved。完整 PDF 未取得，摘要没有给出唯一对应的 Lean 名称/路径；没有猜测对应引理。
“提取几何内容的引理从未被调用”：本次没有完成全编译依赖图的排除证明，不能当作已验证事实。
“这些局部事实导致 RH 没有被证明”：没有建立该推论。需要给出最终陈述错误、未清偿的前提、额外公理、具体非法证明项，或证明检查器错误等可核查证据。仅有局部退化结构和依赖可达性不足。

9. What I could not verify / 尚未完成的检查。
完整 Main 重编译、完整 axiom 清单和独立内核重放；真实 Siegel 极点命题的无条件构造；精确文献等价性；Nielsen 完整 PDF 中未能定位的引理；排除所有等价展开证明的全环境查询。

10. 在本机重新运行现有检查（无需再次下载项目缓存）。
在 ${WORKSPACE} 执行：
python -X utf8 review-cache\\local-verification\\run_inspection.py
python -X utf8 review-cache\\local-verification\\analyze_inspection.py
python -X utf8 review-cache\\local-verification\\check_local_evidence.py

所有程序和日志保留在此目录。核心事实及资源测量在 local_findings.json、inspection-receipt.json、additional_checks.json。模块来源与 SHA256 在 selected_oleans.json。这里的检查覆盖明确限定的阳性路径和局部声明，不能替代完整证明复核。
"""
    report = ROOT / "LOCAL_REVIEW_20261122.txt"
    report.write_text(text, encoding="utf-8")
    names = ["InspectSelected.lean", "ReplaySlot.lean", "run_inspection.py", "analyze_inspection.py", "check_local_evidence.py", "local_findings.json", "inspection-receipt.json", "additional_checks.json", "selected_oleans.json", "kernel-slot.log", report.name]
    hashes = []
    for name in names:
        hashes.append(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() + "  " + name)
    (ROOT / "LOCAL_REVIEW.sha256").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    print("REPORT", report)
    print("TOOLCHAIN_DISK_BYTES", tool_bytes)
    print("HEIGHT_BOUND_ARGUMENTS", json.dumps(hargs, ensure_ascii=False))

if __name__ == "__main__":
    main()

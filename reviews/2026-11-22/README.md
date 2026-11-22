# 本机复核与 Nielsen PDF 审查包（2026-11-22）

本包补充仓库的 [CORRECTION.md](../../CORRECTION.md)。审查使用固定源码提交 `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`、Lean 4.33.1 和用户提供的 16 页 Nielsen PDF。

**结论：现有证据对标准 Mathlib RH 陈述的形式证明提供很强支持；Nielsen 的局部源码观察不足以推出最终证明无效。本机做的是定向检查，完整证明重放依赖明确注明的外部核验记录。**

- [结论、范围及残余风险](CONCLUSIONS.md)
- [详细 PDF 审查报告](files/review-cache/local-verification/trust-audit/TRUST_REVIEW_20261122.txt)
- [前一轮定向检查记录](files/review-cache/local-verification/LOCAL_REVIEW_20261122.txt)（历史记录；PDF 中度数字段后来已定位）
- [直接下载 ZIP](../../bundles/GRH-review-2026-11-22.zip)
- [打包文件散列](MANIFEST.sha256)与[原始文件到公开副本的对应记录](PROVENANCE.json)

## 本机取得的结果

| 检查 | 结果及回执 |
|---|---|
| 原始 `UnusedSlot72 := True` 定义的局部内核重放 | [kernel-slot.log](files/review-cache/local-verification/kernel-slot.log)，错误 False 证明被拒绝 |
| `sorry`、额外公理、隐藏前提、弱化定义的隔离对照 | [controls_receipt.json](files/review-cache/local-verification/trust-audit/controls_receipt.json) |
| 实际 `kexactB` 策略对照 | [kexact_receipt.json](files/review-cache/local-verification/trust-audit/kexact_receipt.json)，True 通过，False 被最终内核拒绝 |
| 五个官方结构性内核漏洞回归 | [regression_receipts.json](files/review-cache/local-verification/trust-audit/regression_receipts.json)，全部满足预期的拒绝诊断 |
| 原审查七个常量的引用路径 | [local_findings.json](files/review-cache/local-verification/local_findings.json) |
| PDF 实际路线的八个关键节点 | [paper_route_receipt.json](files/review-cache/local-verification/trust-audit/paper_route_receipt.json)，全部从主定理可达 |
| 175,187 个源文件的词法扫描 | [source_scan.json](files/review-cache/local-verification/trust-audit/source_scan.json)，零命中不等于语义上的穷尽排除 |

共包含 38 个选择性缓存档案，压缩合计 1,647,474 字节；没有完整项目缓存和 Lean 安装。引用路径是对发布缓存的重新读取，并非本机完整内核重放。成功回归检查中单个 Lean 进程峰值约 775 MiB。

## 文件与路径

`files/` 保持原工作区布局；`${WORKSPACE}`、`${USER_PDF}` 是公开副本中替换本机绝对路径的标记，不是可以直接执行的历史命令。公开上游原始日志保留原字节。`PROVENANCE.json` 同时记录原始及公开副本的散列。

两个证明项快照、完整选项匹配记录和较大的工具链文件清单使用 `.gz` 保存。先运行 `python expand_snapshots.py` 可恢复这些文本文件。`modules.jsonl` **仅包含选中的 38 行**，其头部标记 `partial: true`；原完整索引的下载地址、散列及获取程序均保留。

论文副本以 16 页、158,977 字节、SHA256 `8ed8649b46993126aad0cd15760a2f444efb3fc72a2ce01bc9c08a01073fc9b4` 标识；原文见 [PhilArchive](https://philarchive.org/rec/NIEIOT-2)。本包没有重分发整篇论文。源码快照和官方回归用例的上游许可证在 `third_party/`。

## 复现

先校验 `MANIFEST.sha256`；ZIP 内文件均是公开副本。原始回执不因复现而变成新跑出的结果，重新运行会更新对应输出。

需要 Python 3.12（`requests`、`psutil`；只有重读 PDF 才需要 `pypdf`）和官方 Lean 4.33.1。可使用已有官方工具链，直接调用其中的 `lean`：

```powershell
python expand_snapshots.py
Set-Location files/review-cache/local-verification
lean --version
lean -j1 -M1536 TrustControls.lean
lean -j1 -M1536 KexactControlGood.lean
lean -j1 -M1536 KexactControlBad.lean
```

最后一条命令预期 exit 1，并必须包含 `(kernel) declaration type mismatch`。`TrustControls.lean` 故意含一个 `sorry` 和一个自定义公理，是检测对照，不属于被审 RH 代码。

五个原样官方用例位于 `trust-audit/regressions/*.lean`；分别用同一 `lean` 执行。它们用 `#guard_msgs` 要求指定的内核拒绝，成功的回归检查 exit 0。

Python 包装程序默认使用本目录的 `toolchain/bin/lean.exe`。Windows 上可将已有官方工具链目录联接为 `toolchain`；或按需运行 `install_lean_slice.py --mode public`、`--mode private`、`--mode server`，再按 `lean-slice-ir-receipt.json` 的八个模块补齐 `--mode ir --module ...`。这是安装工具链的操作，整个安装约 1.86 GB；不能把几秒的检查时间当作包含安装的总耗时。

重做项目缓存检查：

```powershell
python fetch_selected_oleans.py
python run_inspection.py
python analyze_inspection.py
python inspect_paper_route.py
```

38 个压缩档案已在 `artifacts/`，程序会校验 SHA256 并用官方 `leantar` 解包。源代码检查还需要在 `files/upstream-rh` 准备干净的原始镜像，签出上述固定提交，并取回缓存基线 `e50d09817ad81469f737e8f637561e6ccf86c670` 和论文镜像提交 `712a6aef8fe265fb6f3a5fa1f3101a017aec8fe9`，再运行 `check_nielsen_sources.py`、`audit_trust.py`、`check_local_evidence.py`。

本包不提供完整 RH 内核重放结果。完整导出和所需资源见 [Sutherland 核验页](https://math.mit.edu/~drew/grh/)。

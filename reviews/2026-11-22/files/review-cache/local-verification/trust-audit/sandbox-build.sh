#!/bin/bash
# Sandboxed `lake build Main` + export, at the same absolute path as our original build.
# Phase A (network): toolchain, archive from the author's site, official Mathlib cache.
# Phase B (bubblewrap sandbox: no network, read-only filesystem, only .lake writable): lake build Main, then lean4export.
set -u
ulimit -n 1048576 2>/dev/null || ulimit -n 65536   # the Mathlib cache tool exhausts the default 1024 descriptors on 192 cores
O=$HOME/sbx_out; mkdir -p $O; TL=$O/timeline.txt
P=/home/ubuntu/grh/src/lean
date -u +"phase A start %FT%TZ on $(hostname) ($(nproc) cores, $(lscpu | grep 'Model name' | sed 's/.*: *//'))" > $TL
sudo apt-get update -qq; sudo apt-get install -y -qq bubblewrap zstd time >/dev/null 2>&1
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0 >/dev/null
[ -x $HOME/.elan/bin/elan ] || curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --default-toolchain none >/dev/null
export PATH=$HOME/.elan/bin:$PATH
mkdir -p $HOME/dl /home/ubuntu/grh/src && cd $HOME/dl
for i in $(seq -w 1 14); do curl -sSL --retry 5 -o lean.tar.gz.part$i https://alpo.ge/lean.tar.gz.part$i & done; wait
cat lean.tar.gz.part* > lean.tar.gz; sha256sum lean.tar.gz | tee $O/archive.sha256
grep -q 9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc $O/archive.sha256 || { echo "ARCHIVE HASH MISMATCH" >> $TL; exit 1; }
tar xzf lean.tar.gz -C /home/ubuntu/grh/src --no-same-owner
cd $P && elan toolchain install $(cat lean-toolchain) >/dev/null 2>&1
TC=$HOME/.elan/toolchains/leanprover--lean4---v4.33.1
for try in 1 2 3; do lake exe cache get > $O/cache-get.$try.log 2>&1; grep -q "decompression(s) failed" $O/cache-get.$try.log || break; done
(cd $P/.lake/packages/mathlib/.lake/build/lib/lean && find . -name '*.olean' | sort | xargs -d '\n' -P 32 -n 200 sha256sum | LC_ALL=C sort) > $O/mathlib.sha256
(cd $P/.lake && find packages -path '*build/lib/lean*' -name '*.olean' -not -path 'packages/mathlib/*' | sort | xargs -d '\n' -P 32 -n 200 sha256sum | LC_ALL=C sort) > $O/deps.sha256
cmp <(LC_ALL=C sort $HOME/ref/mathlib.sorted.sha256) $O/mathlib.sha256 && cmp <(LC_ALL=C sort $HOME/ref/deps.sorted.sha256) $O/deps.sha256 && echo "Mathlib+deps oleans identical to clean reference ($(wc -l < $O/mathlib.sha256)+$(wc -l < $O/deps.sha256) files)" >> $TL || { echo "MATHLIB CACHE MISMATCH" >> $TL; exit 1; }
lake build Mathlib > $O/prebuild-mathlib.log 2>&1; echo "pre-sandbox 'lake build Mathlib' (upstream only) exit=$? $(date -u +%FT%TZ)" >> $TL
lean --version >> $TL; git -C .lake/packages/mathlib rev-parse HEAD >> $TL
sha256sum $HOME/ref/lean4export >> $TL
# ---- Phase B: sandbox
SBX="bwrap --unshare-all --die-with-parent --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --tmpfs /home/ubuntu --ro-bind $TC $TC --ro-bind $P $P --bind $P/.lake $P/.lake --ro-bind $HOME/ref /home/ubuntu/ref --bind $O /home/ubuntu/sbx_out --clearenv --setenv PATH $TC/bin:/usr/bin:/bin --setenv HOME /home/ubuntu --setenv LEAN_ABORT_ON_PANIC 1 --chdir $P"
echo "sandbox: $SBX" >> $TL
$SBX sh -c 'echo "inside sandbox: net=$(ls /sys/class/net | tr "\n" " ") ; can write source dir: $(touch src/x 2>/dev/null && echo YES || echo no); home listing: $(ls /home/ubuntu | tr "\n" " ")"; (curl -s -m 5 https://example.com >/dev/null 2>&1 && echo NETWORK_REACHABLE || echo network unreachable)' >> $TL 2>&1
# lake writes a ~6 MB setup file per module; delete each once its module is built
( while [ ! -f $O/build.done ]; do sleep 60; find $P/.lake/build/ir -name '*.setup.json' 2>/dev/null | while IFS= read -r f; do t="$P/.lake/build/lib/lean/${f#$P/.lake/build/ir/}"; [ "${t%.setup.json}.trace" -nt "$f" ] && rm -f "$f"; done; done ) &
date -u +"sandboxed lake build Main start %FT%TZ" >> $TL
/usr/bin/time -v -o $O/build.time $SBX lake build Main > $O/build.log 2>&1
rc=$?; touch $O/build.done; echo "sandboxed lake build Main exit=$rc $(date -u +%FT%TZ)" >> $TL
[ $rc -eq 0 ] || exit 1
date -u +"sandboxed export start %FT%TZ" >> $TL
T=$(cat $HOME/ref/targets.txt)
/usr/bin/time -v -o $O/export.time $SBX sh -c "lake env /home/ubuntu/ref/lean4export Main -- $T > /home/ubuntu/sbx_out/solution.ndjson 2> /home/ubuntu/sbx_out/export.err"
echo "sandboxed export exit=$? bytes=$(stat -c %s $O/solution.ndjson) $(date -u +%FT%TZ)" >> $TL
sha256sum $O/solution.ndjson | tee $O/solution.ndjson.sha256 >> $TL
grep -q 5ea74b912147c5c93cc2b6d70cc727cf908df2f62ac6a20480a3fa02f6be244e $O/solution.ndjson.sha256 && echo "EXPORT SHA256 MATCHES the published export" >> $TL || echo "EXPORT SHA256 DIFFERS" >> $TL
(cd $P/.lake/build/lib/lean && find . -name '*.olean' | sort | xargs -d '\n' -P 64 -n 500 sha256sum | sort -k2) > $O/project-oleans.lake.sha256
echo "olean manifest: $(wc -l < $O/project-oleans.lake.sha256) files, sha256 $(sha256sum $O/project-oleans.lake.sha256 | cut -c1-64)" >> $TL
echo "olean files identical to published manifest: $(comm -12 <(sort $O/project-oleans.lake.sha256) <(sort $HOME/ref/project-oleans.sha256) | wc -l) of $(wc -l < $HOME/ref/project-oleans.sha256); differing: $(comm -13 <(sort $O/project-oleans.lake.sha256) <(sort $HOME/ref/project-oleans.sha256) | wc -l)" >> $TL
echo "ALL DONE $(date -u +%FT%TZ)" >> $TL

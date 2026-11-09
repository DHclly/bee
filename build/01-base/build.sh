#!/bin/bash
# 此文件用于自动化打包 deepseek-ocr 基础镜像，请勿删除。
# lf not crlf
set -euo pipefail

log() {
    echo "[deepseek-ocr-base] $*"
}

fail() {
    log "错误: $*"
    exit 1
}

# GitLab CI 从仓库根目录调用本脚本，参数由 .gitlab-ci.yml 传入。
if [ $# -ne 3 ]; then
    cat >&2 <<EOF
用法: $0 <runner> <version> <cpu_arch>

参数说明:
  runner    : 构建环境标识，如 ci、manual、local
  version   : 镜像版本号，如 1.0.0
  cpu_arch  : CPU 架构，可选 x86_64、aarch64

示例:
  $0 local 1.0.0 x86_64

EOF
    exit 1
fi

runner="$1"
version="$2"
cpu_arch="$3"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$cpu_arch" in
    x86_64|aarch64) ;;
    *) fail "不支持的架构: ${cpu_arch}（可选: x86_64, aarch64）" ;;
esac

dockerfile="${script_dir}/${cpu_arch}/Dockerfile"
build_context="${script_dir}/${cpu_arch}/build-context"
src_dir="$(cd "${script_dir}/../../src" && pwd)"

[ -f "$dockerfile" ] || fail "Dockerfile 不存在: ${dockerfile}"
[ -d "$src_dir" ] || fail "源码目录不存在: ${src_dir}"

for f in pyproject.toml uv.toml; do
    [ -f "$src_dir/$f" ] || fail "缺少 ${src_dir}/${f}"
done

tag="dhclly/bee/bee-base:v${version}-${cpu_arch}"

log "准备构建上下文: ${build_context}/app"
rm -rf "${build_context}/app"
mkdir -p "${build_context}/app"
cp "$src_dir/pyproject.toml" "$src_dir/uv.toml" "${build_context}/app/"

log "runner: ${runner}"
log "版本: ${version}"
log "架构: ${cpu_arch}"
log "标签: ${tag}"

export DOCKER_BUILDKIT=1

docker build \
    -f "$dockerfile" \
    -t "$tag" \
    "$build_context" || fail "镜像构建失败"

log "构建完成: ${tag}"

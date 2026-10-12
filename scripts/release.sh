#!/usr/bin/env bash
# Release the pack at <version> from HEAD: the changelog's Unreleased entries and the mods changed
# since the last release become <version>'s section, the manifest checks out, the zip is exported,
# and the release is committed and tagged v<version> with the zip's sha256.
#
#   scripts/release.sh <version>
#
# It pushes and uploads nothing, since both are public and for good: it ends by printing the push
# and upload commands. The zip stays beside the manifest (*.zip is ignored) until scripts/upload.py
# sends it to CurseForge and to the tag's GitHub release; a later export never matches it byte for
# byte, so that zip is the release.
set -euo pipefail
cd "$(dirname "$0")/.."

fail() { echo "release: $*" >&2; exit 1; }

version="${1:-}"
[[ $# -eq 1 && "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail "usage: scripts/release.sh <major.minor.patch>"
tag="v$version"
name="$(sed -n 's/^name = "\(.*\)"$/\1/p' pack.toml)"
zip="$name-$version.zip"

[[ -z "$(git status --porcelain)" ]] || fail "the working tree has changes; commit or stash them first."
! git rev-parse -q --verify "refs/tags/$tag" > /dev/null || fail "$tag already exists."

# Until the commit, a failure puts both files back, so a failed release leaves nothing behind.
trap 'git checkout -- pack.toml CHANGELOG.md; git reset -q -- pack.toml CHANGELOG.md' EXIT
scripts/changelog.py release "$version"
sed -i "s/^version = \".*\"$/version = \"$version\"/" pack.toml
git add pack.toml CHANGELOG.md
scripts/check.sh
git commit -q -m "$name $version" -- pack.toml CHANGELOG.md
trap - EXIT

rm -f "$zip"
packwiz cf export > /dev/null
[[ -f "$zip" ]] || fail "packwiz cf export didn't write $zip."
sha="$(sha256sum "$zip" | cut -d' ' -f1)"
git tag -a "$tag" -m "$name $version" -m "zip sha256 $sha"

echo "Released $zip"
echo "zip sha256 $sha"
echo "Push with:   git push origin HEAD $tag"
echo "Then upload: scripts/upload.py $version"

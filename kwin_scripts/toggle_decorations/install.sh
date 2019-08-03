#!/bin/bash
mkdir -p ~/.local/share/kwin/scripts/toggle_decorations
ln -sfn $PWD/contents ~/.local/share/kwin/scripts/toggle_decorations/contents
ln -sf $PWD/metadata.desktop ~/.local/share/kwin/scripts/toggle_decorations/metadata.desktop

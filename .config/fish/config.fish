## ADDING TO THE PATH
# First line removes the path; second line sets it.  Without the first line,
# your path gets massive and fish becomes very slow.
set -e fish_user_paths
set -U fish_user_paths $HOME/.local/bin $fish_user_paths

### EXPORT ###
set fish_greeting                                       # Supresses fish's intro message
set TERM "xterm-256color"                               # Sets the terminal type
set EDITOR "vim"                                        # $EDITOR use vim
set VISUAL "gvim -f"                                    # $VISUAL use gvim
set npm_config_prefix "$HOME/.local"                    # Allow NPM user-wide installations
set QT_QPA_PLATFORMTHEME "qt5ct"                        # Sets QT platform to qt5ct
# Remember to run `systemctl --user enable ~/.config/systemd/user/ssh-agent.service`
set SSH_AUTH_SOCK "$XDG_RUNTIME_DIR/ssh-agent.socket"   # Start ssh-agent with systemd user

### ALIASES ###
alias code='vscodium'
alias idea='intellij-idea-ultimate-edition'
alias config="git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME"

# init starship
starship init fish | source

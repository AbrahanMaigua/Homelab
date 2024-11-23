# ~/.bashrc: executed by bash(1) for non-login shells.
# dependecias
# apt jq curl url python3 python3-pip python3.11-venv
clear 

function getCurrency() {
    response=$(wget -qO- "https://api.coingecko.com/api/v3/simple/price?ids=$1&vs_currencies=usd")
    price=$(echo "$response" | jq -r '.[].usd')
    if [ -z "$price" ]; then
        echo "Error: Unable to fetch price for $1. Please check the currency ID."
    else
        echo "${price} USD"
    fi
}

function btc() {
	 getCurrency  bitcoin
}

function bch() {
	 getCurrency  'bitcoin-cash'
}
function eth() {
	 getCurrency  ethereum
}
printf "\n"
printf "   %s\n" "BTC PRICE: $(btc) "
printf "   %s\n" "BTH PRICE: $(bcH) "
printf "   %s\n" "ETH PRICE: $(eth) "
printf "   %s\n" "     DATE: $(date)"



# Note: PS1 and umask are already set in /etc/profile. You should not
# need this unless you want different defaults for root.
# PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
PS1='\[\e[1m\]\w \[\e[0m\] # '
# umask 022

# You may uncomment the following lines if you want `ls' to be colorized:
export LS_OPTIONS='--color=auto'
# eval "$(dircolors)"
 alias ls='ls $LS_OPTIONS'
# alias ll='ls $LS_OPTIONS -l'
# alias l='ls $LS_OPTIONS -lA'
#
# Some more alias to avoid making mistakes:
# alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'
#
alias c='clear'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias update='sudo apt-get update && sudo apt-get upgrade -y'
alias bashrc='vim ~/.bashrc && source ~/.bashrc'
alias py='/home/bin/.env/bin/python'
alias env='/home/bin/.env/bin/activate'


export PATH=$PATH:/home/bin
export NVM_DIR=/root/.nvm

# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash

[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

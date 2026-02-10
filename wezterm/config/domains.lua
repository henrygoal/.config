return {
   -- ref: https://wezfurlong.org/wezterm/config/lua/SshDomain.html
   ssh_domains = {
       {name = 'nj146',
        remote_address = '217.2.230.146:13323',
        username = 'root',
      },
   },

   -- ref: https://wezfurlong.org/wezterm/multiplexing.html#unix-domains
   unix_domains = {},

   -- ref: https://wezfurlong.org/wezterm/config/lua/WslDomain.html
   wsl_domains = {
      {
         name = 'WSL:Ubuntu',
         distribution = 'Ubuntu',
         username = 'luyh',
         default_cwd = '/home/luyh',
         default_prog = { 'zsh' },
      },
   },
}

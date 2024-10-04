import re
import pytest

def test_os_release(host):
    assert host.file("/etc/issue").contains("Debian GNU/Linux 10")



def test_resolv_file(host):
    assert host.file("/etc/resolv.conf").md5sum == "1a68962dd31e012d85628bb1238ffc8f"


def test_sysctl(host):
    sysctl = host.file("/etc/sysctl.conf")
    assert sysctl.contains("net.ipv6.conf.all.disable_ipv6 = 1")
    assert sysctl.contains("net.ipv6.conf.default.disable_ipv6")
    assert sysctl.contains("net.ipv6.conf.lo.disable_ipv6 = 1")
    assert sysctl.contains("net.ipv6.conf.eth0.disable_ipv6 = 1")    
    # ...

def test_pkg_unistall(host):
    assert not host.package("isc-dhcp-client").is_installed	
    assert not host.package("isc-dhcp-common").is_installed


#check TimeOut for bash env    
def test_myvar_using_debug_var(host):
    bash_provile = host.file("/etc/profile")
    assert bash_provile.contains("TMOUT=300")
    assert bash_provile.contains("readonly TMOUT")
    assert bash_provile.contains("export TMOUT")  

#check installed packages
def test_pkg_install(host):
    assert  host.package("openssh-server").is_installed     
    assert  host.package("ntp").is_installed
    assert  host.package("screen").is_installed
    assert  host.package("ntp").is_installed
    assert  host.package("sudo").is_installed
    assert  host.package("cracklib-runtime").is_installed
    assert  host.package("auditd").is_installed

#check ntp 
def test_ntp(host):
    assert host.file("/etc/ntp.conf").md5sum == "210fdaf08ae050c06995c63b4247ee10"
    assert host.file("/etc/default/ntp").md5sum == "6ef2cad5ff866cca56d1dc645e41f22a"
#check password MAX DAYS

def test_pwd_max_days(host):
#    pwd_max_days = host.file("/etc/login.defs")
#    assert pwd_max_days.contains("PASS_MAX_DAYS 60")
     max_days = host.check_output("grep -E 'PASS_MAX_DAYS\s+[0-9]+' /etc/login.defs | awk '{print$NF}' ")
     assert re.match("60", max_days)

 
#check ssh ClientAliveInterval
def test_ClientAliveInterval(host):
    ClientAliveInterval = host.file("/etc/ssh/sshd_config")
    assert ClientAliveInterval.contains("ClientAliveInterval 900")


#check locales
def test_locales(host):
     locales = host.file("/etc/default/locale")
     assert locales.contains("en_US.UTF-8")
#     locales_current = host.check_output("locale")
#     assert re.match ("LANG=en_US.UTF-8", locales_current)

def test_apt_proxy(host):
    apt_proxy = host.file("/etc/apt/apt.conf.d/01proxy")
    assert apt_proxy.contains("Acquire::http::Proxy \"http://10.10.85.14:9999\";")
#    assert host.file("/etc/apt/apt.conf.d/01proxy").md5sum == "d0959a414e3b88991f7d801144ee1fc4"
    


def test_enabled_mobi_repo(host):
    #repo_check = host_check_output("apt-cache policy | grep 'http://deb.mobi-money.ru/md buster/main' | awk '{print$2,$3}")
    #assert re.match ("http://deb.mobi-money.ru/md buster/main", repo_check)
    #assert host.file("/etc/apt/sources.list.d/deb.mobi-money.ru.list").md5sum == "9211fc97316b6eee95da8cc20644ba2c"
    bash_provile = host.file("/etc/apt/sources.list.d/deb.mobi-money.ru.list")
    assert bash_provile.contains("http://deb.mobi-money.ru/md buster main")

def test_ssh_users(host):
    ssh_user = host.check_output("sshd -T | grep --colour allowusers | awk '{print$NF}' | grep -vE 'prusakov|maksimov|akulov' | wc -l")
    assert re.match("0", ssh_user)
           
 
@pytest.mark.parametrize("dir,value", [
	("grep -E '^PermitRootLogin' /etc/ssh/sshd_config | awk '{print$NF}'", "no"),
        ("grep -E '^IgnoreUserKnownHosts' /etc/ssh/sshd_config | awk '{print$NF}'", "yes"),
        ("grep -E '^X11Forwarding' /etc/ssh/sshd_config | awk '{print$NF}'", "no"),
        ("grep -E '^MaxAuthTries' /etc/ssh/sshd_config | awk '{print$NF}'", "3"),
        ("grep -E '^UseDNS' /etc/ssh/sshd_config | awk '{print$NF}'", "no"),
        ("grep -E '^ClientAliveCountMax' /etc/ssh/sshd_config | awk '{print$NF}'", "0"),
        ("grep -E '^GSSAPIAuthentication' /etc/ssh/sshd_config | awk '{print$NF}'", "no"),
        ("grep -E '^AllowTcpForwarding' /etc/ssh/sshd_config | awk '{print$NF}'", "no"),
        ("grep -E '^ChallengeResponseAuthentication' /etc/ssh/sshd_config | awk '{print$NF}'", "no"),
        ("grep -E '^AddressFamily' /etc/ssh/sshd_config | awk '{print$NF}'", "inet"),
        ("grep -E '^Ciphers' /etc/ssh/sshd_config | awk '{print$NF}'", "aes128-ctr,aes192-ctr,aes256-ctr"),


])

def test_sshd_setings(host, dir, value):
    ssh_user = host.check_output(dir)
    assert re.match(value, ssh_user)

def test_check_rsyslog_server_conf(host):
    rsyslog_s = host.file("/etc/rsyslog.d/server.conf")
    assert rsyslog_s.contains("*.* @10.10.85.11")
##    assert host.file("/etc/rsyslog.d/server.conf").md5sum == "8327d1e5b85fdb3bf304d54c792e0c52"
def test_check_rsyslog_auditd_conf(host):
    assert host.file("/etc/rsyslog.d/audit.conf").md5sum == "6f0008d0cf6ae049c57c2b3d8d43ad04"
def test_check_auditd_conf(host):
    with host.sudo():
     assert host.file("/etc/audit/rules.d/custom.rules").md5sum == "9e6aefaefaf0ad20c986e7e9968f53d2"



def test_common_account(host):
    common_account = host.check_output("grep -v '#' /etc/pam.d/common-account | sed  '/^$/d' | head -n1| sed s/' '//g| md5sum")
    assert re.match("fc723441714b7ff3fb1996e88648aecd", common_account)
 
def test_common_auth(host):
    common_auth = host.check_output("grep -v '#' /etc/pam.d/common-auth | sed  '/^$/d' | head -n1 | sed s/' '//g| md5sum | awk '{print$1}'")
    assert re.match("5eabbba5175d6d42c530591520cd8490",common_auth)
def test_common_password(host):
    common_password = host.check_output("grep -v '#' /etc/pam.d/common-password | sed  '/^$/d'| head -n1  | sed s/' '//g| md5sum | awk '{print$1}'")
    assert re.match("6c83c828a9bb2f629fef03fe2a08656e",common_password)
def test_common_password(host):
    common_password_s = host.file("/etc/pam.d/common-password")
    assert common_password_s.contains("remember=4")
    assert common_password_s.contains("use_authtok")
    


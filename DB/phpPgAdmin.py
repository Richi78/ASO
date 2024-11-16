
def installAndConfigurePhpPgAdmin():
    subprocess.run(['sudo', 'zypper', 'install', 'phpPgAdmin'], check=True)

    with open('/etc/phpPgAdmin/config.inc.php', 'r+') as f:
        lines = f.readlines()
    index1 = 0
    index2 = 0
    index3 = 0
    for i, line in range(0, len(lines)):
        if '        // use \'localhost\' for TCP/IP connection on this computer' in lines[i]:
            index1 = i
        if '        $conf[\'extra_login_security\'] = true;' in lines[i]:
           index2 = i
        if '        $conf[\'owned_only\'] = false;' in lines[i]:
            index3 = i
        
    if index1 != 0:
        lines[index1 + 1] = "$conf['servers'][0]['host'] = 'localhost';" + "\n"

    if index2 != 0:
        lines[index2 + 1] = "$conf['extra_login_security'] = false;" + "\n"

    if index3 != 0:
        lines[index3 + 1] = "$conf['owned_only'] = true;" + "\n" 
        
    with open('/etc/phpPgAdmin/config.inc.php', 'w') as f:
        f.writelines(lines)
    print ("archivo config.inc.php modificado")

   
    with open('/etc/apache2/conf.d/phpMyAdmin.conf', 'r+') as f:
        lines = f.readlines()
    
    index = 0
    for i, line in enumerate(lines):
        if '<Directory "/srv/www/htdocs/phpPgAdmin">' in line:
            index = i
            break
    if index != 0:
        lines[index] = lines[index] + "\n"+"    Require all granted\n"

    lines[0] = "Alias /phpPgAdmin /srv/www/htdocs/phpPgAdmin\n"

    with open('/etc/apache2/conf.d/phpMyAdmin.conf', 'w') as f:
        f.writelines(lines)
    print ("archivo phpMyAdmin.conf modificado")

    subprocess.run(['sudo', 'service', 'postgresql', 'reload'], check=True)
    subprocess.run(['sudo', 'service', 'postgresql', 'restart'], check=True)
    subprocess.run(['sudo', 'service', 'apache2', 'restart'], check=True)
    print("phpPgAdmin configurado")


def installAndConfigurePhpMyAdmin():
    subprocess.run(['sudo', 'zypper', 'install', 'phpMyAdmin'], check=True)
    
    with open('/etc/phpMyAdmin/config.inc.php', 'r+') as f:
        lines = f.readlines()
    index1 = 0
    index2 = 0
    for i, line in enumerate(lines):
        if '        // use \'localhost\' for TCP/IP connection on this computer' in lines[i]:
            index1 = i
        if '        $cfg[\'Servers\'][$i][\'extension\'] = \'mysqli\';' in lines[i]:
            index2 = i
        
    if index1 != 0:
        lines[index1 + 1] = "$cfg['Servers'][$i]['host'] = 'localhost';" + "\n"

    if index2 != 0:
        lines[index2 + 1] = "$cfg['Servers'][$i]['extension'] = 'mariadb';" + "\n"
        
    with open('/etc/phpMyAdmin/config.inc.php', 'w') as f:
        f.writelines(lines)
    print ("archivo config.inc.php modificado")

    with open('/etc/apache2/conf.d/phpMyAdmin.conf', 'r+') as f:
        lines = f.readlines()
    
    index = 0
    for i, line in enumerate(lines):
        if '<Directory "/srv/www/htdocs/phpMyAdmin">' in line:
            index = i
            break
    if index != 0:
        lines[index] = lines[index] + "\n"+"    Require all granted\n"

    lines[0] = "Alias /phpMyAdmin /srv/www/htdocs/phpMyAdmin\n"

    with open('/etc/apache2/conf.d/phpMyAdmin.conf', 'w') as f:
        f.writelines(lines)
    print ("archivo phpMyAdmin.conf modificado")

    subprocess.run(['sudo', 'service', 'apache2', 'restart'], check=True)
    print("phpMyAdmin configurado")

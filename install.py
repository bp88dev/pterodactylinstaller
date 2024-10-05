import os
print("Pterodactyl installer by github/bp88dev\nCustom designed to run on Ubuntu 22.04\nMAKE SURE TO RUN THE INSTALLER WITH ROOT PERMISSIONS!\n\nThis installer will install the Pterodactyl Minecraft Server Panel Software onto your computer. Make sure you have the necessary installation files that should've came with the zip file.\nWould you like to install Pterodactyl? (N/y)")
consent = input("")
if not consent == "y":
    exit()
# Add "add-apt-repository" command
print("[INSTALLER] Add add-apt-repository command")

os.system("""apt -y install software-properties-common curl apt-transport-https ca-certificates gnupg""")

# Add additional repositories for PHP (Ubuntu 20.04 and Ubuntu 22.04)

print("[INSTALLER] Add additional repositories for PHP (Ubuntu 20.04 & Ubuntu 22.04)")
os.system("""LC_ALL=C.UTF-8 add-apt-repository -y ppa:ondrej/php""")

# Add Redis official APT repository
print("[INSTALLER] Add Redis official APT repository")
os.system("""curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg""")
os.system("""echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list""")

# MariaDB repo setup script (Ubuntu 20.04)
#curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash

# Update repositories list
print("[INSTALLER] Update repositories list")
os.system("""apt update""")

# Install Dependencies
print("[INSTALLER] Install random dependencies")
os.system("""apt -y install php8.3 php8.3-{common,cli,gd,mysql,mbstring,bcmath,xml,fpm,curl,zip} mariadb-server nginx tar unzip git redis-server""")

print("[INSTALLER] Install Composer")
os.system("""curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer""")

print("[INSTALLER] Creating directory /var/www/pterodactyl")
os.system("""mkdir -p /var/www/pterodactyl""")
print("[INSTALLER] Changing directory")
os.system("""cd /var/www/pterodactyl""")
print("[INSTALLER] Getting latest Pterodactyl release")
os.system("""curl -Lo panel.tar.gz https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz""")
print("[INSTALLER] Untarring files")
os.system("""tar -xzvf panel.tar.gz""")
print("[INSTALLER] chmodding files (couldn't tell you why though lmao)")
os.system("""chmod -R 755 storage/* bootstrap/cache/""")
print("[INSTALLER] Installing MariaDB")
os.system("sudo apt install mariadb-server")
print("[INSTALLER] Configure MariaDB? (Y/n)")
consent = input("")
if not consent == "n":
    os.system("mysql_secure_installation")
print("[INSTALLER] You are going to be prompted by MariaDB to change your configuration. Change it to this: \n\nCREATE USER 'pterodactyl'@'127.0.0.1' IDENTIFIED BY 'yourPassword';\nCREATE DATABASE panel;\nGRANT ALL PRIVILEGES ON panel.* TO 'pterodactyl'@'127.0.0.1' WITH GRANT OPTION;\nexit\n\nPress enter to continue.")
input()
os.system("mariadb -u root -p")
print("[INSTALLER] Configuring MariaDB further")
os.system("cp .env.example .env")
os.system("COMPOSER_ALLOW_SUPERUSER=1 composer install --no-dev --optimize-autoloader")
os.system("php artisan key:generate --force")
print("[INSTALLER] Configuring Environment")
os.system("php artisan p:environment:setup")
os.system("php artisan p:environment:database")
os.system("php artisan p:environment:mail")
print("[INSTALLER] Setting up DB, this may take a while.")
os.system("php artisan migrate --seed --force")
print("[INSTALLER] Creating user. This user will be an administrator of the panel. DO NOT FORGET THIS LOGIN.")
os.system("php artisan p:user:make")
print("[INSTALLER] Creating proper permissions on panel files")
os.system("chown -R www-data:www-data /var/www/pterodactyl/*")
os.system("chown -R nginx:nginx /var/www/pterodactyl/*")
os.system("chown -R apache:apache /var/www/pterodactyl/*")
print("[INSTALLER] Create cronjob - Please paste the following into the file:\n* * * * * php /var/www/pterodactyl/artisan schedule:run >> /dev/null 2>&1\n\n")
os.system("crontab -e")
print("[INSTALLER] Creating queue worker")
os.system("curl https://raw.githubusercontent.com/bp88dev/pterodactylinstaller/refs/heads/main/pteroq.service -o pteroq.service")
os.system("cp pteroq.service /etc/systemd/system/pteroq.service")
print("[INSTALLER] Enabling Services")
os.system("sudo systemctl enable --now redis-server")
os.system("sudo systemctl enable --now pteroq.service")
print("[INSTALLER] Removing default apache2 config")
os.system("a2dissite 000-default.conf")
print("[INSTALLER] Politely asking php to marry apache2")
os.system("apt install libapache2-mod-php8.3")
print("[INSTALLER] that was rough.")
print("[INSTALLER] What is your local ip address or domain?")
ipaddr = input("")
print("[INSTALLER] Creating Pterodactyl configuration file")
os.system("curl https://raw.githubusercontent.com/bp88dev/pterodactylinstaller/refs/heads/main/pterodactyl.conf -o pterodactyl.conf")
config = open("pterodactyl.conf", "r")
confignew = config.read().split("\n")
config.close()
config = open("pterodactyl.conf", "w")
config.write("")
config.close()
config = open("pterodactyl.conf", "a")
for i in confignew:
    config.write(i.replace("<domain>", ipaddr))
config.close()
print("[INSTALLER] Enabling Configuration")
os.system("sudo ln -s /etc/apache2/sites-available/pterodactyl.conf /etc/apache2/sites-enabled/pterodactyl.conf")
os.system("sudo a2enmod rewrite")
os.system("sudo a2enmod ssl")
os.system("sudo systemctl restart apache2")
print("[INSTALLER] Enabling Docker")
os.system("sudo systemctl enable --now docker")
print("[INSTALLER] Installing Wings")
os.system("sudo mkdir -p /etc/pterodactyl")
os.system("""curl -L -o /usr/local/bin/wings "https://github.com/pterodactyl/wings/releases/latest/download/wings_linux_$([[ "$(uname -m)" == "x86_64" ]] && echo "amd64" || echo "arm64")" """)
os.system("sudo chmod u+x /usr/local/bin/wings")
print("[INSTALLER] PTERODACTYL SHOULD NOW BE INSTALLED ON YOUR SYSTEM! IT IS RECCOMENED TO REBOOT YOUR COMPUTER!")
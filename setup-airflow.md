go to:
https://www.docker.com/products/docker-desktop/

download docker desktop > install

go to:
https://github.com/astronomer/astro-cli/releases

download:
astro_1.41.0_windows_amd64.exe

Create folder named "astro-cli" in local disk C
paste file downloaded from github
rename file jadi "astro"

Win > env > Edit the system environment variables > System variables > Path > Edit > New > C:\astro-cli > OK

Open PowerShell:
$env:Path += ";C:\astro-cli"
astro version

cd C:\Users\HP\Documents\GitHub\Airflow-doc
C:\astro-cli\astro.exe dev init

C:\astro-cli\astro.exe dev start

go to:
http://localhost:8080

Right click at dags > New File > my_first_pipeline.py

C:\astro-cli\astro.exe dev restart
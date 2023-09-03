read -p "Enter FileName: "  filename
if [  ${#filename} -ge 2 ]
then
  echo "file name is  $filename "
else
  echo "code exiting, please enter a valid .zip file name as excpected on the cdn server"
  exit
fi

sudo cp  --remove-destination  firmware_download_manager.py  ./smarteye
sudo cp  --remove-destination  package_manager.py  ./smarteye
sudo zip -r "$filename.zip" ./smarteye 
echo "initializing $filename firmware sync to remote server ..."
echo "."
echo "."
echo "."
sudo rsync -ah -e ' ssh -i  smarteye_privatekey.pem   -o StrictHostKeyChecking=no' "$filename.zip"  ubuntu@34.240.137.86:/var/www/PYTHON/smarteye_downloads/
echo "finished runnig deployment pipeline for $filename"

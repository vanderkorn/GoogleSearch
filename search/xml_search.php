<?php
if (!isset($site_id))
{
   system('/usr/bin/python /home/u8742/u8742.netangels.ru/www/search/google/sitegoogleparse.py -s '.$site_id,$q);
   echo $q;
   system('/usr/bin/python /home/u8742/u8742.netangels.ru/www/search/yandex/siteyandexparse.py -s '.$site_id,$q);
   echo $q;
}
?>
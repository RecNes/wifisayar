# SAKKIBU
## Şu Anda Kaç Kişi Burada uygulaması
(İzmir Hackerspace Wifi Sayar uygulamasının forkudur.)

## Kullanım
Bu script nmap ile yerel ağa bağlı olan cihazların kaç tane olduğunu sayar ve
hariç tutulacak olanlar listesinde bulunanları toplamdan düşüp, görüntülenebilir
bir html dosyasına yazdıktan sonra dosyayı github_pages'de yayınlanması için
otomatik olarak github depsuna gönderir.

Bu işlemin çalışması için öncelikle bir github hesabınızın olması gerekmektedir.
Ve ayrıca github_pages oluşturmuş olmanız ve GitHub().commit_and_tag() metodunda
hangi depoya gönderilmesi gerektiğini belirtmeniz gerekiyor.

Komutu konsoldan çalıştırmak için:

    # pytohn3 sakkibu.py -h|[-d,-a,-p]

    -h | --help     Bu yardım dokümanını gösterir.
    -d | --dry-run  Scriptin dosya oluşturmadan sadece işlem çıktısı vermesini sağlar.
                    (Sayımı yap ve ekrana istatistikleri bas.)
    -a | --all      Ağdaki bütün cihazları (hariç tutulanları da) sayıma ekler.
    -p | --push     Scriptin hazırlanan HTML'i depoya göndermesini sağlar.


Scriptin otomatik olarak belirli aralıklar ile çalışmasını sağlamak için cronjob
oluşturabilirsiniz. Bunun için kullanıcının crontab listesine "crontab -e" komutu
ile erişi aşağıdaki 10'ar dakikalık zaman dilimlerinde yinelenmesi için ayarlanmş
görevi ekleyebilirsiniz:

    * * * * python3 sakkibu.py -p 2>&1


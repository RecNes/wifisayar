# SAKKIBU
## Şu Anda Kaç Kişi Burada uygulaması
(İzmir Hackerspace Wifi Sayar uygulamasının forkudur.)

## Hazırlık

Github hesabınıza giriş yapın. 
Bu scriptin çalışacağı cihazda bir id_rsa.pub dosyası oluşturun ve GitHub hesabınıza ekleyin.
https://pages.github.com/ adresine gidin ve aşağıdaki adımları takip edin:

- "Roll vanilla, or generate a site for your project" kısmından "Project site" seçin
- "Generate a site, or start from scratch?" kısmında "Start from scratch" seçin


Projenin depo sayfasına geri dönün ve "gh-pages" adında bir "Branch" oluşturun.
**Gerekli:** "gh-pages" branchına bir adet boş "index.html" dosyası muhakkak gönderin.
*Seçimsel:* ya da Projenizi "gh-pages" branchına aktarın
*(Aksi takdirde "index.html" depoda olmadığından oluşturulan yeni dosya gönderilemeyecektir.)*
Son olarak SAKKIBU scriptini cihazınızda id_rsa.pub dosyası oluşturulmuş olan kullanıcı ile çalıştırın:


     # python3 sakkibu.py -p

## Kullanım
Bu script nmap ile yerel ağa bağlı olan cihazların kaç tane olduğunu sayar ve
hariç tutulacak olanlar listesinde bulunanları toplamdan düşüp, görüntülenebilir
bir html dosyasına yazdıktan sonra dosyayı github_pages'de yayınlanması için
otomatik olarak github depsuna gönderir.

Bu işlemin çalışması için öncelikle bir github hesabınızın olması gerekmektedir.
Ve ayrıca github_pages oluşturmuş olmanız ve GitHub().commit_and_tag() metodunda
hangi depoya gönderilmesi gerektiğini belirtmeniz gerekiyor.

Komutu konsoldan çalıştırmak için:

    # python3 sakkibu.py -h|[-d,-a,-p]

    -h | --help     Bu yardım dokümanını gösterir.
    -d | --dry-run  Scriptin dosya oluşturmadan sadece işlem çıktısı vermesini sağlar.
                    (Sayımı yap ve ekrana istatistikleri bas.)
    -a | --all      Her türlü çıktıyı görüntüler. (Dikkat log dosyasını  şişirebilir.)
    -p | --push     Scriptin hazırlanan HTML'i depoya göndermesini sağlar.


Scriptin otomatik olarak belirli aralıklar ile çalışmasını sağlamak için cronjob
oluşturabilirsiniz. Bunun için kullanıcının crontab listesine "crontab -e" komutu
ile erişi aşağıdaki 10'ar dakikalık zaman dilimlerinde yinelenmesi için ayarlanmş
görevi ekleyebilirsiniz:

    * * * * python3 sakkibu.py -p 2>&1

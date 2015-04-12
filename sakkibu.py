#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Şu anda kaç kişi burada uygulaması      İzmir Hackerspace 12.2014

Geliştiriciler :
                    Ramazan Subaşı, Doğukan Güven, Sencer Hamarat

Son Güncelleme: 04.2015
"""
import getopt
import os, sys, nmap, arrow


class GitHub():
    def __init__(self, filetopush):
        self.filetopush = filetopush

    @staticmethod
    def shell_quote(arguments):
        def quote(string):
            return "\\'".join("'" + p + "'" for p in string.split("'"))
        return " ".join(map(quote, arguments))

    def system(self, *arguments):
        return os.system(self.shell_quote(arguments))

    def commit_and_tag(self):
        self.system("git", "add", "-A")
        self.system("git", "commit", self.filetopush, "-m", "Automatic update")
        self.system("git", "push", "origin", "master:gh-pages")


class SAKKIBU():
    """
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
    """
    def __init__(self, argv):
        self.argv = argv
        self.display_all = False
        self.dry_run = False
        self.push = False
        self.hosts_count = int()
        self.hosts_list = list()
        self.message_text = str()
        self.dtnow = arrow.now().format('DD.MM.YYYY HH:mm')
        self.base_path = os.path.abspath('.')
        self.html_file = os.path.join(self.base_path, 'index.html')  # yerelde oluşturulup git pages'e gönderilecek index.html
        try:
            self.nm = nmap.PortScanner()
        except nmap.PortScannerError:
            print('Nmap bulunamadı', sys.exc_info()[0])
            sys.exit(2)
        except:
            print("Beklenmeyen hata:", sys.exc_info()[0])
            sys.exit(2)

        self.exceptional_ips = [
            # ip,               host,           reason
            ('192.168.0.1',     'Router',       'always on'),
            ('192.168.0.250',    'Raspi1',       "it's me"),
            ]
        self.exceptions_count = len(self.exceptional_ips)

    def print_stats(self, istisna=False):
        if (self.hosts_count - self.exceptions_count) < 1:
            self.message_text = u"Şu anda kimse yok."
        else:
            for host, status in self.hosts_list:
                if self.display_all: print('{} : {}'.format(host, status))
            if not istisna:
                self.message_text = u"Açık, {} cihaz bağlı".format(self.hosts_count - self.exceptions_count)
            else:
                self.message_text = u"İstisnalar ({}) dahil {} cihaz bağlı".format(self.exceptions_count,
                                                                                   self.hosts_count)
        print(self.message_text)

    def scan_area(self):
        self.nm.scan(hosts='192.168.1.0/24', arguments=' -n -sP -PE')
        self.hosts_list = [(x, self.nm[x]['status']['state']) for x in self.nm.all_hosts()]
        self.hosts_count = len(self.hosts_list)

    def create_html(self):
        if not self.dry_run:
            with open(self.html_file, 'w+') as html_file:
                html_text = u''.join([self.message_text, "<br /><small>Son Kontrol: ", self.dtnow, '</small>'])
                html_file.write(html_text)
                if self.display_all: print(html_text)
            if self.display_all: print(u"HTML dosyası oluşturuldu.")
        else:
            if self.display_all: print(u"HTML dosyası oluşturulmadı.")

    def commit_and_push(self):
        if self.push:
            if self.display_all: print(u"Dosya depoya gönderiliyor.")
            github = GitHub(self.html_file)
            github.commit_and_tag()
            if self.display_all: print(u"Dosya depoya gönderildi.")
        else:
            if self.display_all: print(u"Depoya herhangi bir dosya gönderilmedi.")

    def get_args(self):
        """
        Konsoldan verilen argümanlar alınır.
        :return:
        """
        if not len(self.argv) > 1:
            print("Lütfen anahtar belirtin. Yardım için -h")
            sys.exit(2)
        try:
            opts, args = getopt.getopt(self.argv[1:], "hdap", ["help", "dry-run", "all", "push"])
        except getopt.GetoptError:
            print('Anahtarlar hatalı.')
            sys.exit(2)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print(self.__doc__)
                sys.exit()
            if opt in ("-a", "--all"): self.display_all = True
            if opt in ("-d", "--dry-run"): self.dry_run = True
            if opt in ("-p", "--push"): self.push = True

    def run(self):
        self.get_args()
        self.scan_area()
        self.print_stats(istisna=self.display_all)
        self.create_html()
        self.commit_and_push()

if __name__ == '__main__':
    print(u"\nŞu anda kaç kişi burada uygulaması                       İzmir Hackerspace (2015)")
    sakkibu = SAKKIBU(sys.argv)
    print("-" * 80)
    sakkibu.run()
    print("-" * 80)
    sys.exit(0)
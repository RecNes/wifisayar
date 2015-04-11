#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Şu anda kaç kişi burada uyguaması      İzmir Hackerspace 12.2014

Geliştiriciler :
                    Ramazan Subaşı, Doğukan Güven, Sencer Hamarat
"""
import getopt
import os, sys, nmap, arrow
from subprocess import Popen, PIPE


class GitHub():
    def __init__(self, filetopush, arguments):
        self.arguments = arguments
        self.filetopush = filetopush

    def shell_quote(self, arguments):
        def quote(string):
            return "\\'".join("'" + p + "'" for p in string.split("'"))
        return " ".join(map(quote, arguments))

    def system(self, *arguments):
        return os.system(self.shell_quote(arguments))

    def commit_and_tag(self):
        self.system("git", "commit", self.filetopush, "-m", "Automatic update")
        self.system("git", "push", "origin", "gh-pages")

    def answer(self, *arguments):
        proc = Popen(self.shell_quote(arguments), shell=True, stdout=PIPE)
        return proc.stdout.readlines()


class SAKKIBU():
    """
    Bu script nmap ile yerel ağa bağlı olan cihazların kaç tane olduğunu sayar ve hariç tutulacak olanlar listesinde
    bulunanları toplamdan düşüp, görüntülenebilir bir html dosyasına yazdıktan sonra dosyayı github_pages'de
    yayınlanması için otomatik olarak github depsuna gönderir.

    Komutu konsoldan çalıştırmak için:

        # pytohn3 sakkibu.py [-h|-d|-a|-p]

        -h | --help     Bu yardım dokümanını gösterir.
        -d | --dry-run  Scriptin dosya oluşturmadan sadece işlem çıktısı vermesini sağlar.
                        (Sayımı yap ve ekrana istatistikleri bas.)
        -a | --all      Ağdaki bütün cihazları (hariç tutulanları da) sayıma ekler.
        -p | --push     Scriptin normal şekilde çalışmasını sağlar.
                        (Sayımı yap, dosyayı hazırla ve github_pages'de yayınla.)


    Scriptin otomatik olarak belirli aralıklar ile çalışmasını sağlamak için cronjob oluşturabilirsiniz.
    Bunun için kullanıcının crontab listesine "crontab -e" komutu ile erişi aşağıdaki 10'ar dakikalık zaman
    dilimlerinde yinelenmesi için ayarlanmş görevi ekleyebilirsiniz:

        * * * * python3 sakkibu.py -p 2>&1
    """
    def __init__(self, argv):
        self.argv = argv
        self.display_all = False
        self.runargs = dict()
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
            ('192.168.1.1',     'Router',       'always on'),
            ('192.168.1.39',    'Raspi1',       "it's me"),
            ]
        self.exceptions_count = len(self.exceptional_ips)

    def print_stats(self, istisna=False, sistem=False):
        print("-" * 80)
        if (self.hosts_count - self.exceptions_count) < 1:
            self.message_text = u"Şu anda kimse yok."
        else:
            diff_count = self.hosts_count - self.exceptions_count
            for host, status in self.hosts_list:
                if self.display_all: print('{} : {}'.format(host, status))
            if not sistem:
                self.message_text = u"Açık, {} cihaz bağlı".format(self.hosts_count - self.exceptions_count)
            else:
                self.message_text = u"İstisnalar ({}) {} {} cihaz bağlı".format(self.exceptions_count,
                                                                                u'dahil' if istisna else u'haric',
                                                                                self.hosts_count if istisna else diff_count)
        if self.display_all: print(self.message_text)

    def scan_field(self):
        self.nm.scan(hosts='192.168.1.0/24', arguments=' -n -sP -PE')
        self.hosts_list = [(x, self.nm[x]['status']['state']) for x in self.nm.all_hosts()]
        self.hosts_count = len(self.hosts_list)

    def create_html(self, dryrun):
        if dryrun:
            with open(self.html_file, 'w+') as html_file:
                html_file.write(u''.join([self.message_text, "<BR/><small>Son Kontrol: ", self.dtnow, '</small>']))
            if self.display_all: print(u"HTML dosyası oluşturuldu.")
        else:
            if self.display_all: print(u"HTML dosyası oluşturulmadı.")
            pass

    def commit_and_push(self, push):
        pass

    def get_args(self):
        if not len(self.argv) > 1:
            print("Lütfen anahtar belirtin. Yardım için -h")
            sys.exit(2)
        try:
            opts, args = getopt.getopt(self.argv[1:], "hdap:", ["help", "dry-run", "all", "push"])
            print(getopt.getopt(self.argv[1:], "hdap:", ["help", "dry-run", "all", "push"]))
        except getopt.GetoptError:
            print('Anahtarlar hatalı.')
            sys.exit(2)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print(self.__doc__)
                sys.exit()
            self.display_all = True if opt in ("-a", "--all") else False
            self.runargs.update({'dry-run': True if opt in ("-d", "--dry-run") else False})
            self.runargs.update({'push': True if opt in ("-p", "--push") else False})

    def run(self):
        self.get_args()
        self.create_html(self.runargs['dry-run'])
        self.commit_and_push(self.runargs['push'])

        # self.scan_field()
        # self.print_stats(sistem=False, istisna=True)


if __name__ == '__main__':
    print(u"Şu anda kaç kişi burada uyguaması                  İzmir Hackerspace (2015)")
    sakkibu = SAKKIBU(sys.argv)
    print("-" * 80)
    sakkibu.run()
    sys.exit(0)
#!/usr/bin/python3
#-*- coding: utf-8 -*-

# tab2xv1.py v0.1
# Konwerter plików tab (tekstowy plik słownika w formacie "definicja\thasło\n")
# (c) CC-BY Krzysztof Palka kpalka.vot.pl

# Można w ten sposób przekonwertować pliki win programu Wielki Słownik PWN-Oxford do formatu Xlatora
# Przy spadającej liczbie telefonów obsługujących MIDP2 oraz z systemem Symbian, w dobie Androida, może przydać się już nie wielu osobom :/
# Pliki win można przekonwertować do tab za pomocą skryptu pwn2dict (http://my.opera.com/mziab/blog/pwn2dict-2-4)
# otrzymane z tego skryptu piki xv1 można przekonwertować do formatu Xlatora (xv2) za pomocą konwertera ze strony http://www.farbiszowie.is.net.pl/Xlator/
# przy pliku z konwerterem powinien znaleźć się plik z amerykańską wymową, jeśli nie chcesz dodawać jej do definicji wykomentuj część "for AmE"
# pliki załadujesz zmieniając nazwę przy odpowiedniej funkcji "open()"

# Nie chce mi się już ulepszać tego kodu ani tworzyć ładnego interfejsu. Oddaję wam użytecznego śmiecia, od ponad roku leży zakurzony na dysku a nie chcę, żeby przy którymś formacie bezpowrotnie przepadł :)

# Plik 2colindex.xv2 colors.jpeg colors.html są wynikiem próby (udanej) uzyskania odpowiedzi na pytanie: jaki kod odpowiada za jaki kolor (w wersji Xlatora na Javę można kolorować tekst, na Symbianie chyba to nie działa).

# "Gdy pisałem ten skrypt tylko Bóg i ja wiedzieliśmy o co w nim chodzi...

# ... teraz wie tylko Bóg."


import struct
import re
import codecs

def definitionReplace(str):
    str = str.rstrip()
    str = str.replace('ʌ', '^')
    str = str.replace('ɑ', 'a')
    str = str.replace('æ', '@')
    str = str.replace('ə', '¤') 
    str = str.replace('t̬', 't¸')
    str = str.replace('ɚ', '¤~')
    str = str.replace('ɜ', 'E')
    str = str.replace('з', 'E')
    str = str.replace('ε', 'E')
    str = str.replace('ɪ', 'î')    
    str = str.replace('ɒ', 'o')
    str = str.replace('ɔ', '©')
    str = str.replace('ʊ', 'U')
    str = str.replace('ʒ', '3')
    str = str.replace('ð', 'đ')
    str = str.replace('θ', '0')
    str = str.replace('ŋ', 'n¸')
    str = str.replace('ʃ', '§')
    str = str.replace('ː', ':')
    str = str.replace('ˈ', '`')
    str = str.replace('à', 'á')
    str = str.replace('—', '-')
    str = str.replace('–', '-')
    str = str.replace('“', '"')
    str = str.replace('”', '"')
    str = str.replace('‘', '`')
    str = str.replace('ˌ', ',')
    str = str.replace('ˌ', ',')
    str = str.replace('…', '...')
    str = str.replace('→', '»')
    str = str.replace('▪', '»')
    str = str.replace('<br><br>', '<br>')
    str = str.replace('<br>', '\n')
    str = re.sub(r';<B>(.*?)</B>', ';\n<B>\\1</B> -', str)
    str = re.sub(r'<B>(.*?)</B>', '\x1e\\1\x10', str)
    str = re.sub(r'<BIG>(.*?)</BIG>', '\\1', str)
    str = re.sub(r'<I>(.*?)</I>', '\x1c\\1\x10', str)
    str = re.sub(r'<SMALL>(.*?)</SMALL>', '\x18\\1\x10', str)
    return str

def headwordReplace(str):
    str = str.strip()
    str = str.replace(' ', '')
    str = str.replace('-', '')
    str = str.replace('\'', '')
    str = str.replace('‘', '')
    str = str.replace('/', '')
    str = str.replace('.', '')
    str = str.replace(',', '')
    str = str.replace('é', 'e')
    str = str.replace('+', '')
    str = str.replace('&', 'and')
    str = str.replace('à', 'a')
    str = str.replace('â', 'a')
    str = str.replace('®', 'R')
 
    return str

def main():
    __colors = dict(black = '\x10',
                    blue = '\x11',
                    light_green = '\x12',
                    green = '\x14',
                    claret = '\x18',
                    faded_violet = '\x19',
                    violet = '\x1a',
                    shit_colored = '\x1c',
                    deep_violet = '\x1e'
                    )
    fo = codecs.open('angpol.tab', encoding = 'utf_8')
    fw = open('angpol.xv1', 'wb')
    content = bytearray()
    words = 0
    allLen = 0
    longDefinitions = 0
    maxWordLen = 3100
    ### for AmE
    foTemp = codecs.open('tab-pronoun.txt', encoding='utf_8')
    ame = {}
    for line in foTemp:
        aheadword, adefinition = line.split('\t')
        aheadword = aheadword.lower()    
        ame[aheadword] = adefinition
        ame['bear'] = 'ˈbær'
    
    for line in fo:    
        try:
            headword, definition = line.split('\t')
        except:
            line = re.search('(?P<hea>.*?)\t(?P<def>.*?)', line)
            headword = line.group('hea')
            definition = line.group('def')
        definition = definitionReplace(definition)
        ### for AmE
        amep = ''
        try:
            amep = ame[headword.lower()]
        except:
            pass
        if amep != '':
            amep = definitionReplace(amep)
            amep = '\x11AmE: ' + amep + ';\x10 '
            definition = amep + definition
        ### end for AmE
        defLen = len(bytes(definition, encoding = 'cp1250', errors = 'ignore'))

        if defLen <= maxWordLen:
            definition = '\x1c\x1c---\x10 ' + headword + ' \x1c---\x10\n\n' + definition
            temp_headword = headwordReplace(headword)
            
            temp_headword = bytes(temp_headword, encoding = 'cp1250', errors = 'ignore')
            definition = bytes(definition, encoding = 'cp1250', errors = 'ignore')
            content = struct.pack('l', len(temp_headword))
            
            content += temp_headword
            content += struct.pack('l', len(definition))   
            content += definition
            # stats
            allLen += len(definition)
            fw.write(content)
        else:
            #long definitions
            longDefinitions += 1
            pages = defLen // maxWordLen
            if defLen % maxWordLen != 0: pages += 1
            definition = bytes(definition, encoding = 'cp1250', errors = 'ignore')
            allLen += len(definition)
            lastColor = 16
            hexColors = []
            for value in __colors.values():
                hexColors.append(ord(value))
            for page in range(pages):                
                page += 1
                # header
                try:
                    temp_definition = bytes('\x1c\x1c---\x10 ' + headword + ' ({}/{})'.format(page, pages) + ' \x1c---\x10\n\n', encoding='cp1250')
                except:
                    # for 'à' char
                    temp_definition = bytes('\x1c\x1c---\x10 ' + headword.replace('à', 'á') + ' ({}/{})'.format(page, pages) + ' \x1c---\x10\n\n', encoding='cp1250')
                if lastColor != 16:
                    temp_definition += bytes(chr(lastColor), encoding='cp1250')
                # protection for braking words in new pages
                
                if page == 1:
                    extra_chars = 0
                    last_char = definition[maxWordLen]
                    while last_char != ord(bytes(' ', encoding='cp1250')):
                        extra_chars += 1
                        try:
                            last_char = definition[maxWordLen+extra_chars]
                        except:
                            extra_chars -= 1
                            break
                        
                    
                                                
                    temp_definition += definition[(page-1)*maxWordLen:page*maxWordLen+extra_chars]
                    # continuing printing definitions with color from previous page
                    #last color (2 to change)
                    for n in range(250):
                        if definition[page*maxWordLen - n] not in hexColors:
                            lastColor = 16
                        else:                            
                            lastColor = definition[page*maxWordLen - n]
                            break 
                        
                else:
                    if page != pages:              
                        if page > 2:
                            extra_chars = new_extra_chars
                        new_extra_chars = 0
                        last_char = definition[page*maxWordLen]
                        
                        while last_char != ord(bytes(' ', encoding='cp1250')) and last_char != ord(bytes(',', encoding='cp1250')) and last_char != ord(bytes('?', encoding='cp1250')) and last_char != ord(bytes('!', encoding='cp1250')) and last_char != 16:
                            new_extra_chars += 1
                            try:
                                last_char = definition[page*maxWordLen + new_extra_chars]
                            except:
                                new_extra_chars = 0
                                print('exception', headword, definition)
                                break
                        temp_definition += definition[(page-1)*maxWordLen+extra_chars:page*maxWordLen+new_extra_chars]
                        #last color (2 to change)
                        for n in range(250):
                            if definition[page*maxWordLen - n] not in hexColors:
                                lastColor = 16
                            else:                            
                                lastColor = definition[page*maxWordLen - n]
                                break
                            
                    else:
                        temp_definition += definition[(page-1)*maxWordLen+extra_chars:page*maxWordLen]


                if page != pages:
                    temp_definition += bytes('\n\x12-----------------\x10\n==> go to page \x13{}\x10'.format(page + 1), encoding='cp1250')
                temp_headword = headwordReplace(headword)
                temp_headword = headword + '{}'.format(page)
                conv_headword = bytes(temp_headword, encoding = 'cp1250', errors = 'ignore')
                content = struct.pack('l', len(conv_headword))
                content += conv_headword
                content += struct.pack('l', len(temp_definition))   
                content += temp_definition
                fw.write(content)
                
        
        words += 1

        
    print('words:', words)
    print('total length:', allLen)
    print('average length:', allLen / words)
    print('long definitions:', longDefinitions)
               
        
        
    

if __name__ == "__main__": main()

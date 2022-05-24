import sys
import os
import re
import io
import getopt

# pylint: skip-file

DEBUG = False

def fileopen(input_file):
    encodings = ["utf-32", "utf-16", "utf-8", "cp1252", "gb2312", "gbk", "big5"]
    tmp = ''
    for enc in encodings:
        try:
            with io.open(input_file, mode="r", encoding=enc) as fd:
                tmp = fd.read()
                break
        except:
            if DEBUG:
                print(enc + ' failed')
            continue
    return [tmp, enc]

def srt2ass(input_file, out_file, sub_type):
    if '.ass' in input_file:
        return input_file

    src = fileopen(input_file)
    tmp = src[0]
    encoding = src[1]
    src = ''
    utf8bom = ''

    if u'\ufeff' in tmp:
        tmp = tmp.replace(u'\ufeff', '')
        utf8bom = u'\ufeff'
    
    tmp = tmp.replace("\r", "")
    lines = [x.strip() for x in tmp.split("\n") if x.strip()]
    subLines = ''
    tmpLines = ''
    lineCount = 0
    output_file = out_file

    for ln in range(len(lines)):
        line = lines[ln]
        if line.isdigit() and ln+1 < len(lines) and re.match('-?\d\d:\d\d:\d\d', lines[(ln+1)]):
            if tmpLines:
                subLines += tmpLines + "\n"
            tmpLines = ''
            lineCount = 0
            continue
        else:
            if re.match('-?\d\d:\d\d:\d\d', line):
                line = line.replace('-0', '0').replace(',', '.')
                tmpLines += 'Dialogue: 0,' + line + ',Default,,0,0,0,,'
            else:
                if lineCount < 2:
                    tmpLines += line
                else:
                    tmpLines += '\\N' + line
            lineCount += 1
        ln += 1


    subLines += tmpLines + "\n"

    subLines = re.sub(r'\d(\d:\d{2}:\d{2}),(\d{2})\d', '\\1.\\2', subLines)
    subLines = re.sub(r'\s+-->\s+', ',', subLines)
    # replace style
    subLines = re.sub(r'<([ubi])>', "{\\\\\g<1>1}", subLines)
    subLines = re.sub(r'</([ubi])>', "{\\\\\g<1>0}", subLines)
    subLines = re.sub(r'<font\s+color="?#(\w{2})(\w{2})(\w{2})"?>', "{\\\\c&H\\3\\2\\1&}", subLines)
    subLines = re.sub(r'</font>', "", subLines)

    if sub_type == "movie" or sub_type == "serie":
        head_str = '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
Title: Default Aegisub file
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
PlayResX: 1920
PlayResY: 1080
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Verdana,60,&H00FFFFFF,&H000000FF,&H00282828,&H00000000,-1,0,0,0,100,100,0,0,1,3.75,0,2,0,0,70,1
[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text'''

    if sub_type == "anime":
        head_str = '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
Title: Default Aegisub file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Verdana,60,&H00FFFFFF,&H000000FF,&H00282828,&H00000000,-1,0,0,0,100.2,100,0,0,1,3.75,0,2,0,0,79,1
Style: BottomRight,Arial,30,&H00FFFFFF,&H000000FF,&H00282828,&H00000000,0,0,0,0,100,100,0,0,1,2,2,3,10,10,10,1
Style: TopLeft,Arial,30,&H00FFFFFF,&H000000FF,&H00282828,&H00000000,0,0,0,0,100,100,0,0,1,2,2,7,10,10,10,1
Style: TopRight,Arial,30,&H00FFFFFF,&H000000FF,&H00282828,&H00000000,0,0,0,0,100,100,0,0,1,2,2,9,10,10,10,1
[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text'''
    output_str = utf8bom + head_str + '\n' + subLines
#    output_str = output_str.encode(encoding)

    with io.open(output_file, 'w', encoding='utf8') as output:
        output.write(output_str)

    output_file = output_file.replace('\\', '\\\\')
    output_file = output_file.replace('/', '//')
    return output_file

def print_helper():
    print('str2ass.py -t <type> -i <input> inputfile')
    print('Available types: anime, serie, movie')

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:i:", ["type=", "input="])
    except getopt.GetoptError:
        print_helper()
        sys.exit(2)

    sub_type = "anime"
    input_file = None
    for opt, arg in opts:
        if opt in ("-t", "--type"):
            sub_type = arg
        elif opt in ("-i", "--input"):
            input_file = arg

    if not input_file:
        print_helper()
        sys.exit(2)

    filenameOutput = srt2ass(input_file, sub_type)
    print("Output: " + filenameOutput)
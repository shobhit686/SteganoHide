import binascii
import codecs
from bitstring import BitArray
from PIL import Image


def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def hex2rgb(hexcode):
    if hexcode is None:
        return None
    return tuple(codecs.decode(hexcode[1:], 'hex'))


def hex2bit(hexcode):
    hexcode = hexcode.replace('#', '0x')
    bitstring = BitArray(hexcode)
    return bitstring.bin


def bit2hex(bitstring):
    for i in range(4, 20, 4):
        bits = '0' * i

        if (bitstring[:i] == bits):
            return '#000000'
        elif (bitstring[:i] == bits):
            hexcode = hex(int(bitstring, 2))
            hexcode = '#' + '0' * (i % 4) + hexcode[2:]
            return hexcode

    if bitstring == '':
        return None

    hexcode = hex(int(bitstring, 2))
    hexcode = hexcode.replace('0x', '#')
    return (hexcode)


def str2bin(message):
    binary = bin(int(binascii.hexlify(message.encode()), 16))
    return binary[2:]


def bin2str(binary):
    binary = int(('0b' + binary), 2)
    message = binary.to_bytes((binary.bit_length() + 7) // 8, 'big').decode()
    return message


def encode(bitstring, digit):
    bitstring = bitstring[:-1] + digit
    return bitstring


def decode(bitstring):
    if bitstring[-1] in ('0', '1'):
        return bitstring[-1]
    else:
        return None


def img2bits(filename):
    bitstring = ''
    img = Image.open(filename)
    datas = img.getdata()
    for item in datas:
        bitstring += hex2bit(rgb2hex(item[0], item[1], item[2]))
    return bitstring


def bits2img(bitstring):
    bit = 24
    newData = []
    temp = 0

    while (bitstring[temp:bit].format(24)):
        r, g, b = hex2rgb(bit2hex(bitstring[temp:int(bit)]))
        newData.append((r, g, b, 255))
        temp = bit
        bit = bit + 24

    img = Image.new('RGBA', (300, 300))
    img.putdata(newData)

    img.save("hidden_img1.jpg", 'PNG')
    return ("Your image has been saved.")


def hideImg(filename, filename2):
    img = Image.open(filename)
    binary = img2bits(filename2)
    # adding a breakpoint to identify where to stop
    binary = binary + '1111111111111110111111111111111011111111111111101111111111111110'

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        newData = []
        temp = ''
        digit = 0

        for item in datas:
            if (digit < len(binary)):
                bitstring = encode(hex2bit(rgb2hex(item[0], item[1], item[2])), binary[digit])
                newpix = bit2hex(bitstring)
                if newpix == None:
                    newData.append(item)
                else:
                    r, g, b = hex2rgb(newpix)
                    newData.append((r, g, b, 255))
                    digit += 1
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(filename, 'PNG')
        return 'COMPLETED!'

    else:
        return 'Incorrect image mode, could not hide.'


def hide(filename, message):
    img = Image.open(filename)
    binary = str2bin(message)
    # adding a breakpoint to identify where to stop
    binary = binary + '1111111111111110'

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        newData = []
        temp = ''
        digit = 0

        for item in datas:
            if (digit < len(binary)):
                bitstring = encode(hex2bit(rgb2hex(item[0], item[1], item[2])), binary[digit])
                newpix = bit2hex(bitstring)
                if newpix == None:
                    newData.append(item)
                else:
                    r, g, b = hex2rgb(newpix)
                    newData.append((r, g, b, 255))
                    digit += 1
            else:
                newData.append(item)

        img.putdata(newData)
        return img

    else:
        return 'Incorrect image mode, could not hide.'


def retrImg(filename):
    img = Image.open(filename)
    binary = ''

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:
            digit = decode(hex2bit(rgb2hex(item[0], item[1], item[2])))
            if digit == None:
                pass
            else:
                binary = binary + digit
                if ((binary[-64:]) == '1111111111111110111111111111111011111111111111101111111111111110'):
                    # print('Success!')
                    return bits2img(binary[:-64])

        return bits2img(binary)
    else:
        return 'Incorrect image mode, could not retrieve.'


def retr(filename):
    img = Image.open(filename)
    binary = ''

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:
            digit = decode(hex2bit(rgb2hex(item[0], item[1], item[2])))
            if digit == None:
                pass
            else:
                binary = binary + digit
                if ((binary[-16:]) == '1111111111111110'):
                    return bin2str(binary[:-16])

        return bin2str(binary)

    else:
        return 'Incorrect image mode, could not retrieve.'


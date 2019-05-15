import string

text = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. \
bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle.\
 sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
trans_text = ""
# method_1
# for item in text:
#     index = ord(item)
#     if ord('a') <= index <= ord('z'):
#         item = chr(((index + 2) - ord('a')) % 26 + ord('a'))
#     trans_text += item
# print(trans_text)
# method_2
table = str.maketrans(
    string.ascii_lowercase,
    string.ascii_lowercase[2:] + string.ascii_lowercase[:2]
)
trans_text = text.translate(table)
print(trans_text)

url = 'map'
print(url.translate(table))

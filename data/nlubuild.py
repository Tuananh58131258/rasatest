import random
# from dbConnect import getData
fobj = open('data/product_name.txt', 'r')
# product_company = ['Iphone', 'Samsung', 'Oppo', 'Huawei', 'Xiaomi', 'Realmi']
# ten = ['iPhone 11 64GB ', 'iPhone 11 256GB ', 'iPhone 11 Pro 512GB ', 'iPhone 11 Pro 256GB ', 'iPhone 11 Pro Max 512GB ', 'iPhone 11 128GB ', 'iPhone 11 Pro Max 256GB ', 'iPhone 11 Pro 64GB ', 'iPhone 11 Pro Max 64GB ', 'Huawei Nova 5 Pro', 'Xiaomi Black Shark 2 Pro', 'Huawei Y7p', 'OPPO A91', 'Huawei P40 Lite',
#        'Huawei Mate Xs', 'Huawei P30 Lite New Edition', 'OPPO A11', 'OPPO A92', 'OPPO A92s', 'Xiaomi Redmi K20 Pro Premium', 'OPPO A1k ', 'Oppo Find X2 Pro', 'OPPO F15', 'OPPO A5s ', 'Realme 6 4GB-128GB ', 'Realme X50 5G', 'Xiaomi Mi 10 Youth Edition', 'Realme C2 3GB-32GB ', 'Realme C2 2GB-32GB ', 'Realme C3i 2GB-32GB ', ]
ten = fobj.readlines()
n = len(ten)
truoc = ['', 'giá của',
         'cho hỏi giá của']
sau = ['', 'là bao nhiêu', 'bao nhiêu tiền', 'hiện nay là bao nhiêu']
for i in range(1, 30):
       temp = truoc[random.randint(0,2)]+" ["+ten[random.randint(0,n-1)].strip('\n') + "](product_name) "+ sau[random.randint(0,3)]
       temp = temp.strip(' ')
       value = "- "+temp
#     temp = "- Danh sách sản phẩm của ['{}'](product_company)".format(
#         product_company[random.randint(0, 5)])
       print(value)
# data = getData("SELECT ten FROM FPTShop.DienThoai;")


fobj.close()

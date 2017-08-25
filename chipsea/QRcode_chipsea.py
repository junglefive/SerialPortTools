import qrcode # 导入模块
import image

img = qrcode.make('Chipsea,BLE,C8B21E123456,8mA,3uA') # QRCode信息
img.save("test.png") # 保存图片
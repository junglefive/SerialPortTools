import  qrcode

class GeneateQRCode(object):
        @staticmethod
        def gen_qr_code(str):
            qr = qrcode.QRCode(
                version= 1,
                error_correction= qrcode.constants.ERROR_CORRECT_L,
                box_size= 3,
                border = 2,
            )
            qr.add_data(str)
            qr.make(fit=True)
            img = qr.make_image()
            img.save("mac.png")
            return img

if __name__ == "__main__":
    img =GeneateQRCode.gen_qr_code(
        "测试mac地址的图片\n测试mac地址的图片\n测试mac地址的图片\n测试mac地址的图片\n"
    )
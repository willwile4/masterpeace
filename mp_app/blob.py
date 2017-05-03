import base64


class Blob:
    def __init__(self, file_nm):
        self.file = file_nm

    def to_text(self):
        encoded = base64.b64encode(open(self.file, "rb").read())
        print(encoded)
        target = open('img_blob.txt', 'w')
        print(target)
        target.write(str(encoded)[2:-1])
        target.close()

    def to_img(self):
        pass

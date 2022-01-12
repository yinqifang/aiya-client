import os

from fsplit.filesplit import Filesplit

fs = Filesplit()


class SplitAndMerge:
    # 拆分回调函数
    def split_cb(self, f, s):
        # print("file: {0}, size: {1}".format(f, s))
        pass

    # 合并回调函数
    def merge_cb(self, f, s):
        # print("file: {0}, size: {1}".format(f, s))
        pass

    # 拆分文件
    def split(self, srcFileName, tarFilePath, splitSize):
        # print("Split file [" + srcFileName + "] by " + str(splitSize))
        fs.split(file=srcFileName, split_size=splitSize, output_dir=tarFilePath, callback=self.split_cb)

    # 合并文件
    def merge(self, src_file_path):
        # print("Merge file in " + src_file_path)
        fs.merge(input_dir=src_file_path, callback=self.merge_cb)

    def test_split(self):
        filePath = "D:\\cutcutcut"
        fileName = "evo-visitor.tar.gz"
        srcFileName = os.path.join(filePath, fileName)
        tarFilePath = os.path.join(filePath, "split")
        self.split(srcFileName, tarFilePath, 20000000)

    def test_merge(self):
        src_file_path = "D:\\cutcutcut\\split"
        self.merge(src_file_path)


if __name__ == '__main__':
    pass
    # test_split()
    # SplitAndMerge().test_merge()

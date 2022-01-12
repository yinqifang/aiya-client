import pyminizip as pyzip
import os


# 压缩和解压文件

class Zip:
    # 压缩
    def compress(self, src_file, tar_file, pwd, delete_src):
        # compress_level(int) between 1 to 9, 1 (more fast) <---> 9 (more compress) or 0 (default)
        compress_level = 1
        pyzip.compress(src_file, None, tar_file, pwd, compress_level)
        if delete_src:
            os.remove(src_file)
        # print("Compressed file [" + src_file + "] to [" + tar_file + "]")

    # 解压缩
    def uncompress(self, src_file, pwd, tar_path, delete_src):
        pyzip.uncompress(src_file, pwd, tar_path, 0)
        if delete_src:
            os.remove(src_file)
        # print("Uncompressed file [" + src_file + "]")


if __name__ == '__main__':
    # Zip().compress("D:\\cutcutcut\\zip\\evo-visitor.tar.gz", "D:\\cutcutcut\\zip\\evo-visitor.tar.gz.rar", "9527", True)
    # Zip().uncompress("D:\\cutcutcut\\zip\\evo-visitor.tar.gz.rar", "9527", "D:\\cutcutcut\\zip")

    # for root, dirs, files in os.walk("D:\\cutcutcut\\5555"):
    #     for filename in files:
    #         Zip().compress(os.path.join(root, filename), os.path.join(root,filename+".rar"),"9527", True)
    pass

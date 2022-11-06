import pathlib, shutil
import time


def file_back_n(src: str, dsts: list, filetype: str) -> None:
    path_gen = pathlib.Path(src).rglob('*.{}'.format(filetype))
    path_list = list(path_gen)
    # 保留一个文件不处理，防止文件读写操作出现冲突
    path_list.pop()
    print('待处理文件数量:', len(path_list))
    for p in path_list:
        dsts_len = len(dsts)
        for dst in dsts:
            ds_obj = pathlib.Path(dst)
            ds_obj.mkdir(parents=True, exist_ok=True)
            dist_path = ds_obj.joinpath(pathlib.Path(p).relative_to(src))
            if not dist_path.parent.exists():
                dist_path.parent.mkdir(parents=True)
            dsts_len -= 1
            if dsts_len == 0:
                shutil.move(p, dist_path, copy_function=shutil.copy)
            else:
                shutil.copy(p, dist_path)


def run(src, dsts, filetype):
    print('------------等待新文件--------------')
    file_back_n(src, dsts, filetype)
    for child_dir in pathlib.Path(src).iterdir():
        if len(list(pathlib.Path(child_dir).rglob('*.{}'.format(filetype)))) == 0:
            shutil.rmtree(child_dir)


if __name__ == '__main__':
    path1 = r'E:\temp'
    path2 = [r'E:\ok', r'E:/ok1']
    run(src=path1, dsts=path2, filetype='DAT')

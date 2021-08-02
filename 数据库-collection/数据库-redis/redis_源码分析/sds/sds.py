SDS_MAX_PREALLOC = 1024 * 1024


class Sds:
    def __init__(self, sds_len=0, sds_fre=0, sds_buffer=None):
        self.sds_len = sds_len  # buf 中已占用空间的长度
        self.sds_fre = sds_fre  # buf 中剩余可用空间的长度
        self.sds_buffer = sds_buffer  # 数据空间

    def get_sds_len(self):
        """ 返回 buf中已经占用的空间长度 """
        return self.sds_len

    def get_sds_vail(self):
        """ 返回 中剩余可用空间的长度 """
        return self.sds_fre

    def sds_str(self):
        return ''.join(self.sds_buffer)

    def __repr__(self):
        return '<free:{}, total:{}, len:{}>'.format(self.sds_fre, self.sds_str(), self.sds_len)

    # @property
    # def buffer(self):
    #     return self.sds_buffer


class SdsOperator:
    @classmethod
    def sds_new(cls, init_str: str):
        init_len = len(init_str)
        return cls.sds_new_len(init_str, init_len)

    @classmethod
    def sds_new_len(cls, init_str: str, init_len: int) -> Sds:
        """
        根据输入的字符串, 构建一个sds字符串
        :param init_str:
        :param init_len:
        :return:
        """
        new_sds = Sds(0, 0, [])
        new_sds.sds_len = init_len
        new_sds.sds_fre = 0  # 新创建的sds不进行预留空间
        if init_str and init_len:
            for s in init_str:
                new_sds.sds_buffer.append(s)
        return new_sds

    @classmethod
    def sds_empty(cls):
        return cls.sds_new_len('', 0)

    @classmethod
    def sds_make_room_for(cls, cur_sds: Sds, add_len):
        """
        动态字符串扩容
        :param cur_sds:
        :param add_len:
        :return:
        """
        # 剩余空间大于将要累加的空间, 不做处理
        if cur_sds.get_sds_vail() >= add_len:
            return cur_sds

        # 新的动态字符串最小需要长度
        cur_sds_len = cur_sds.sds_len
        new_sds_len = cur_sds_len + add_len
        if new_sds_len < SDS_MAX_PREALLOC:
            # 没有超出最大1m, 扩容空间 * 2
            new_sds_len = new_sds_len * 2
        else:
            # 超过 1m, 扩容空间 + 1m
            new_sds_len = new_sds_len + SDS_MAX_PREALLOC
        cur_sds.sds_fre = new_sds_len - cur_sds_len
        return cur_sds


if __name__ == '__main__':
    new_str = SdsOperator.sds_new('leichao')
    print(new_str)
    print(SdsOperator.sds_empty())
    SdsOperator.sds_make_room_for(new_str, 1000)
    assert new_str.get_sds_vail() == ((1000 + 7) * 2 - 7)
    print(new_str)

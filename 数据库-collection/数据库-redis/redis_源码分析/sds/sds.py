"""
sds sdsnewlen(const void *init, size_t initlen);
sds sdsnew(const char *init);
sds sdsempty(void);
size_t sdslen(const sds s);
sds sdsdup(const sds s);
void sdsfree(sds s);
size_t sdsavail(const sds s);
sds sdsgrowzero(sds s, size_t len);
sds sdscatlen(sds s, const void *t, size_t len);
sds sdscat(sds s, const char *t);
sds sdscatsds(sds s, const sds t);
sds sdscpylen(sds s, const char *t, size_t len);
sds sdscpy(sds s, const char *t);

sds sdscatvprintf(sds s, const char *fmt, va_list ap);
#ifdef __GNUC__
sds sdscatprintf(sds s, const char *fmt, ...)
    __attribute__((format(printf, 2, 3)));
#else
sds sdscatprintf(sds s, const char *fmt, ...);
#endif

sds sdscatfmt(sds s, char const *fmt, ...);
sds sdstrim(sds s, const char *cset);
void sdsrange(sds s, int start, int end);
void sdsupdatelen(sds s);
void sdsclear(sds s);
int sdscmp(const sds s1, const sds s2);
sds *sdssplitlen(const char *s, int len, const char *sep, int seplen, int *count);
void sdsfreesplitres(sds *tokens, int count);
void sdstolower(sds s);
void sdstoupper(sds s);
sds sdsfromlonglong(long long value);
sds sdscatrepr(sds s, const char *p, size_t len);
sds *sdssplitargs(const char *line, int *argc);
sds sdsmapchars(sds s, const char *from, const char *to, size_t setlen);
sds sdsjoin(char **argv, int argc, char *sep);

/* Low level functions exposed to the user API */
sds sdsMakeRoomFor(sds s, size_t addlen);
void sdsIncrLen(sds s, int incr);
sds sdsRemoveFreeSpace(sds s);
size_t sdsAllocSize(sds s);
"""


class Sds:
    def __init__(self, sds_len=0, sds_fre=0, sds_buffer=None):
        self._len = sds_len  # buf 中已占用空间的长度
        self._fre = sds_fre  # buf 中剩余可用空间的长度
        self._buffer = sds_buffer  # 数据空间

    def sds_len(self):
        """ 返回 buf中已经占用的空间长度 """
        return self._len

    def sds_vail(self):
        """ 返回 中剩余可用空间的长度 """
        return self._fre

    @property
    def buffer(self):
        return self._buffer

    def __repr__(self):
        return '<free:{}><total:{}><len:{}>'.format(self._fre, ''.join(self.buffer), self._len)


class SdsOperator:
    @classmethod
    def sds_new(cls, init_str: str):
        init_len = len(init_str)
        return cls.sds_new_len(init_str, init_len)

    @classmethod
    def sds_new_len(cls, init_str: str, init_len: int) -> Sds:
        """
        初始化sds
        :param init_str:
        :param init_len:
        :return:
        """
        new_sds = Sds(0, 0, [])
        new_sds._len = init_len
        new_sds._fre = 0
        if init_str and init_len:
            for s in init_str:
                new_sds.buffer.append(s)
        return new_sds


if __name__ == '__main__':
    new_str = SdsOperator.sds_new('leichao')
    print(new_str)

from bson import ObjectId
from motor import MotorGridFSBucket, MotorClient


async def delete_by_name(fs: MotorGridFSBucket, file_id: str):
    await fs.delete(file_id)


async def download_by_name(fs: MotorGridFSBucket, mongo_file_name: str, local_file_name: str):
    # Get file to write to
    with open('myfile', 'wb') as file:
        await fs.download_to_stream_by_name("test_file", file)


async def upload_by_name(fs: MotorGridFSBucket, file_name: str, file_records: bytes):
    grid_in = fs.open_upload_stream_with_id(
        ObjectId(),
        file_name,
        chunk_size_bytes=4,
        metadata={"contentType": "text/plain"})
    await grid_in.write(file_records)
    await grid_in.close()


async def find_by_name(fs: MotorGridFSBucket, file_name):
    # no_cursor_timeout：防止游标超时
    cursor = fs.find({"filename": file_name},
                     no_cursor_timeout=True, limit=1)
    async for grid_data in cursor:
        data = grid_data.read()
        print(data)


if __name__ == '__main__':
    import asyncio

    my_db = MotorClient(
        host="127.0.0.1",
        port=27017,
    ).test_gridfs
    grids_fs = MotorGridFSBucket(my_db)
    current_loop = asyncio.get_event_loop()
    current_loop.run_until_complete(
        # upload_by_name(grids_fs, "this_test.txt", b"this is one test1")
        find_by_name(grids_fs, "this_test.txt")
    )
    current_loop.close()

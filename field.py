import numpy as np

SIZE = 32

class Chunk:
    def __init__(self, arr=None):
        self.arr = np.zeros(SIZE**2, dtype=int)

    def __getitem__(self, cors):
        x, y = cors
        return self.arr[y * SIZE + x]

    def __setitem__(self, cors, value):
        x, y = cors
        self.arr[y * SIZE + x] = value


class Field:
    def __init__(self):
        self.field = {}

    def _create_chunk_if_missing(self, chunk_cors):
        if chunk_cors not in self.field:
            self.field[chunk_cors] = Chunk()


    def __getitem__(self, cors):
        chunk_cors, in_chunk_cors = Field.translate_cors(cors)

        self._create_chunk_if_missing(chunk_cors)
        return self.field[chunk_cors][in_chunk_cors]

    def __setitem__(self, cors, value):
        chunk_cors, in_chunk_cors = Field.translate_cors(cors)

        self._create_chunk_if_missing(chunk_cors)
        self.field[chunk_cors][in_chunk_cors] = value



        
    @classmethod
    def translate_cors(cors):
        in_chunk_x, in_chunk_y = x % SIZE, y % SIZE
        in_chunk_cors = (in_chunk_x, in_chunk_y)

        chunk_x, chunk_y = x // SIZE, y // SIZE
        chunk_cors = (chunk_x, chunk_y)

        return chunk_cors, in_chunk_cors

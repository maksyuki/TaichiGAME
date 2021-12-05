from typing import List


class RandomGenerator():
    # now only use the seq methods(not random) to give unique id
    empty_list: List[int] = []
    start_id: int = 1000

    @staticmethod
    def unique() -> int:
        if len(RandomGenerator.empty_list) > 0:
            res: int = RandomGenerator.empty_list.pop()
            return res

        RandomGenerator.start_id += 1
        return RandomGenerator

    @staticmethod
    def pop(id: int):
        RandomGenerator.empty_list.append(id)

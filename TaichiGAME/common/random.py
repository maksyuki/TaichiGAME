from typing import List


class RandomGenerator():
    # now only use the seq methods(not random) to give unique id
    # NOTE: need to make a single instance in the project
    empty_list: List[int] = []
    start_id: int = 0

    @staticmethod
    def unique() -> int:
        if len(RandomGenerator.empty_list) > 0:
            res: int = RandomGenerator.empty_list.pop()
            return res

        RandomGenerator.start_id += 1
        return RandomGenerator.start_id

    @staticmethod
    def pop(val: int):
        RandomGenerator.empty_list.append(val)

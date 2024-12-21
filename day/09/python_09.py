# INPUT = "input_small.txt"
INPUT = "input.txt"


def read_input() -> str:
    """
    Read the input file and return the first line.
    """
    with open(INPUT) as f:
        return f.read().splitlines()[0]


def decode_blocks(blocks: str) -> list[int | None]:
    result: list[int | None] = []
    is_file = True
    for idx, block_length in enumerate(blocks, start=0):
        if is_file:
            for i in range(int(block_length)):
                result.append(idx // 2)
        else:
            for i in range(int(block_length)):
                result.append(None)
        is_file = not is_file
    return result


def defragment(blocks: list[int | None]) -> list[int | None]:
    """
    Move the rightmost non-empty block to the leftmost empty position.
    """
    left = 0
    right = len(blocks) - 1

    while left < right:
        while left < right and blocks[left] is not None:
            left += 1
        while left < right and blocks[right] is None:
            right -= 1
        if left < right:
            blocks[left], blocks[right] = blocks[right], None
            left += 1
            right -= 1

    return blocks


def checksum_blocks(blocks: list[int | None]) -> int:
    """
    Calculate the checksum of the blocks.

    Checksum is calculated by multiplying the index of the block with the value of the block.
    """
    result = 0
    for idx, block in enumerate(blocks):
        if block is None:
            return result

        result += idx * block
    return result


def main():
    blocks = read_input()
    decoded = decode_blocks(blocks)
    print(decoded)
    defragemented = defragment(decoded)
    print(defragemented)
    checksum = checksum_blocks(defragemented)
    print(checksum)


if __name__ == "__main__":
    main()

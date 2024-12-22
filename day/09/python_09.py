# INPUT = "input_example.txt"
INPUT = "input.txt"


def read_input() -> str:
    """
    Read the input file and return the first line.
    """
    with open(INPUT) as f:
        return f.read().splitlines()[0]


def decode_blocks(blocks: str) -> list[int | None]:
    """
    Decode the blocks from the input string.

    Example:
    "12345" -> [0, None, None, 1, 1, 1, None, None, None, None, 2, 2, 2, 2, 2]
    """
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


def defragment_whole_blocks(blocks: list[int | None]) -> list[int | None]:
    """
    Move the rightmost non-empty block to the leftmost empty position as a whole.
    """
    checked: set[int | None] = set()

    # Iterate from right to left
    for right_stop in range(len(blocks) - 1, 1, -1):
        # Find not empty data block
        if blocks[right_stop] is None:
            continue

        # Skip already checked block
        block = blocks[right_stop]
        if block in checked:
            continue

        # Find the start of the data block
        right_start = right_stop
        while right_start > 0 and blocks[right_start - 1] == block:
            right_start -= 1

        # Find space from left to swap
        for left_start in range(0, right_start):
            # Find empty block
            if blocks[left_start] is not None:
                continue

            # Find the end of the empty block
            left_stop = left_start
            while left_stop + 1 < len(blocks) and blocks[left_stop + 1] is None:
                left_stop += 1

            # Swap if the empty block is bigger or equal to the data block
            if left_stop - left_start + 1 >= right_stop - right_start + 1:
                for i in range(right_stop - right_start + 1):
                    # Swap the data block to the empty block
                    blocks[left_start + i], blocks[right_start + i] = (
                        blocks[right_start + i],
                        blocks[left_start + i],
                    )
                break

        # Add the block to the checked set
        checked.add(block)

    return blocks


def checksum_blocks(blocks: list[int | None]) -> int:
    """
    Calculate the checksum of the blocks.

    Checksum is calculated by multiplying the index of the block with the value of the block.
    """
    result = 0
    for idx, block in enumerate(blocks):
        if block is None:
            continue

        result += idx * block
    return result


def main():
    blocks = read_input()
    decoded = decode_blocks(blocks)
    # print(decoded)
    defragmented = defragment(decoded.copy())
    # print(defragmented)
    checksum = checksum_blocks(defragmented)
    print(f"Checksum: {checksum}")
    defragment_whole = defragment_whole_blocks(decoded.copy())
    # print(defragment_whole)
    checksum_whole = checksum_blocks(defragment_whole)
    print(f"Checksum whole: {checksum_whole}")


if __name__ == "__main__":
    main()

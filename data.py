import numpy as np


def _consecutive_index_generator(length, offset=0):
    """Generate pair of ids of consecutive images.

    Offset is the distance between the images.
    """
    offset += 1
    for i in range(length - offset):
        yield (i, i + offset)


def generate_learning_set(array, random_permutation=True, offset=0):
    """Generate learning set of consecutive scans

    Parameters
    ----------
    array: numpy array of shape n_scans x n_voxels
        Array of masked scans

    random_permutation: boolean
        If True, consecutive scans are switched with a probability of .5

    offset: int
        Distance between two consecutive scans

    Returns
    -------
    learning_set: (list of img, list of img, list of label)
        Lists of consecutive indices and list of labels. If label is 0, indices are ordered decreasingly
    """
    np.random.seed()

    ia_list = []
    ib_list = []
    label_list = []
    for (ia, ib) in _consecutive_index_generator(array.shape[0], offset=offset):
        label = 1
        if random_permutation:
            label = np.random.randint(0, 2)
            if label == 0:
                ia, ib = ib, ia
        ia_list.append(ia)
        ib_list.append(ib)
        label_list.append(label)

    return ia_list, ib_list, label_list


if __name__ == '__main__':
    array = np.arange(5)
    res = generate_learning_set(array)
    assert(len(res[0]) == 4)
    for ia, ib, label in zip(*res):
        if label == 0:
            assert(ia > ib)
        else:
            assert(ia < ib)
    res = generate_learning_set(array, random_permutation=False, offset=1)
    assert(len(res[0]) == 3)
    for ia, ib, label in zip(*res):
        assert(label == 1)
        assert(ia < ib)
    print('Basic testing is OK')

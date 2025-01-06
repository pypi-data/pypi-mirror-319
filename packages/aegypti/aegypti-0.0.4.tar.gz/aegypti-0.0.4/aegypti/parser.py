import lzma
import bz2
import os
import numpy as np
import scipy.sparse as sparse

def get_file_name(filepath):
    """
    Gets the file name from an absolute path.

    Args:
        filepath: The absolute path to the file.

    Returns:
        The file name, or None if no file is found.
    """

    return os.path.basename(filepath)
    
def get_extension_without_dot(filepath):
    """
    Gets the file extension without the dot from an absolute path.

    Args:
        filepath: The absolute path to the file.

    Returns:
        The file extension without the dot, or None if no extension is found.
    """

    filename = get_file_name(filepath)
    _, ext = os.path.splitext(filename)
    return ext[1:] if ext else None

def has_one_on_diagonal(adjacency_matrix):
    """
    Checks if there is a 1 on the diagonal of a SciPy sparse matrix.

    Args:
      adjacency_matrix: A SciPy sparse matrix (e.g., csc_matrix) representing the adjacency matrix.

    Returns:
        True if there is a 1 on the diagonal, False otherwise.
    """
    diagonal = adjacency_matrix.diagonal()
    return np.any(diagonal == 1)

def is_symmetric(matrix):
    """Checks if a SciPy sparse matrix is symmetric.

    Args:
        matrix: A SciPy sparse matrix.

    Returns:
        bool: True if the matrix is symmetric, False otherwise.
        Raises TypeError: if the input is not a sparse matrix.
    """
    if not sparse.issparse(matrix):
        raise TypeError("Input must be a SciPy sparse matrix.")

    rows, cols = matrix.shape
    if rows != cols:
        return False  # Non-square matrices cannot be symmetric

    # Efficiently check for symmetry
    return (matrix != matrix.T).nnz == 0

def create_sparse_matrix_from_file(file):
    data = []
    row_indices = []
    col_indices = []
    rows = 0
    cols = 0

    for i, line in enumerate(file):
        line = line.strip()  # Remove newline characters
        cols = max(cols, len(line))
        for j, char in enumerate(line):
            if char == '1':
                data.append(1)
                row_indices.append(i)
                col_indices.append(j)
        rows+=1

    matrix = sparse.csc_matrix((data, (row_indices, col_indices)), shape=(rows, cols))
    symmetry = is_symmetric(matrix)
    one_on_diagonal = has_one_on_diagonal(matrix)
    if symmetry and not one_on_diagonal:
        return matrix
    elif one_on_diagonal:
        raise ValueError("The input matrix contains a 1 on the diagonal, which is invalid. Adjacency matrices for undirected graphs must have zeros on the diagonal (A[i][i] == 0 for all i).")
    else:
        raise ValueError("The input matrix is not symmetric. Adjacency matrices for undirected graphs must satisfy A[i][j] == A[j][i] for all i and j.")
    
def read(filepath):
    """Reads a file and returns its lines in an array format.

    Args:
        filepath: The path to the file.

    Returns:
        An n x n matrix of ones and zeros

    Raises:
        ValueError: If the file extension is not supported.
        FileNotFoundError: If the file is not found.
    """

    try:
        matrix = None
        extension = get_extension_without_dot(filepath)
        if extension is None or extension == 'txt':
            with open(filepath, 'r') as file:
                matrix = create_sparse_matrix_from_file(file)
        elif extension == 'xz' or extension == 'lzma':
            with lzma.open(filepath, 'rt') as file:
                matrix = create_sparse_matrix_from_file(file)
        elif extension == 'bz2' or extension == 'bzip2':
            with bz2.open(filepath, 'rt') as file:
                matrix = create_sparse_matrix_from_file(file)
        else:
            raise ValueError(f"Unsupported file extension: {extension}")

        return matrix
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")